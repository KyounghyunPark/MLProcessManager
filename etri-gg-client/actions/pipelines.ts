"use server"

import { PipelineComponent } from "@/hooks/use-pipeline-store";
import { ANALYSIS_ITEMS } from "@/data/pipeline-components-list";
import axios from "axios";
import { db } from "@/lib/db";
import { currentUser } from "@/lib/auth";
import { AnalysisStatus } from "@prisma/client";

export const pipelinesExecution = async (pipelines: PipelineComponent[]) => {
  const analysisComponent = pipelines.filter((item) => ANALYSIS_ITEMS.includes(item.name));

  const successInfo: string[] = []
  const errorInfo: string[] = []

  const BASE_API_URL = process.env.NEXT_PUBLIC_AI_SERVER

  console.log(analysisComponent)

  for (const analysis of analysisComponent){
    console.log({ analysis });
    let apiUrl = BASE_API_URL!;
    let sendData = { ...analysis, value: "" }
    switch (analysis.name) {
      case "Map Matching":
        apiUrl = `${BASE_API_URL}/api/mm/mapmatching`;
        break;
      case "SVDD":
        apiUrl = `${BASE_API_URL}/api/svdd/exec`;
        break;
      case "OOSP":
        apiUrl = `${BASE_API_URL}/api/oosp/exec`;
        break;
      case "LSTM Train":
        apiUrl = `${BASE_API_URL}/api/lstm/train`;
        break;
      case "LSTM Predict":
        apiUrl = `${BASE_API_URL}/api/lstm/predict`;
        break;
    }

    console.log({ apiUrl, sendData });

    const user = await currentUser()
    if (user) {
      const saveData = {
        ...sendData,
        userId: user.id!,
        params: JSON.stringify(analysis.params),
        input: analysis.params?.input || "",
        output: analysis.params?.output || "",
      }
      console.log({ saveData });

      // check if pipeline is created already
      const existingPipeline = await db.analysisResult.findFirst({
        where: {
          id: saveData.id
        }
      })
      if (existingPipeline) {
        await db.analysisResult.update({
          where: {
            id: saveData.id
          },
          data: saveData
        })
      } else {
        await db.analysisResult.create({
          data: saveData
        })
      }
    }

    const response = await axios.post(apiUrl, sendData)

    if (response.status === 200) {
      // console.log({ response })
      successInfo.push(response.data)
      await db.analysisResult.update({
        where: {
          id: analysis.id
        },
        data: {
          output: response.data as string,
          status: AnalysisStatus.SUCCESS,
        }
      })
    } else {
      console.log(response.statusText);
      errorInfo.push(response.statusText)
      await db.analysisResult.update({
        where: {
          id: analysis.id
        },
        data: {
          output: "",
          status: AnalysisStatus.FAILED,
        }
      })
    }


  }

  if (errorInfo.length > 0) {

    return { error: "Pipelines execution failed!", errorInfo: errorInfo };
  }

  return { success: "Pipelines execution successfully!", successInfo: successInfo };
}
