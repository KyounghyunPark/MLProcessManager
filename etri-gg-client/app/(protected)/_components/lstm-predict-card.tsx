import { ComponentWrapper, ComponentWrapperProps } from "@/app/(protected)/_components/component-wrapper";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import usePipelineStore from "@/hooks/use-pipeline-store";
import { useCallback, useEffect, useState } from "react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import axios from "axios";
import { extractFilename } from "@/lib/file-io-utils";


interface LstmProps extends ComponentWrapperProps {
  id: string;
}

export const LstmPredictCard = ({ id }: LstmProps) => {
  const { pipelines } = usePipelineStore((state) => state);

  const [modelList, setModelList] = useState([]);

  const [fileInput, setFileInput] = useState<string>("");
  const [fileOutput, setFileOutput] = useState<string>("");

  const updateIOValue = useCallback(() => {
    const temp = pipelines.find((item) => item.id === id);
    if (temp && temp.params) {
      if (temp.params.input) {
        setFileInput(temp.params.input);
      }
      if (temp.params.output) {
        setFileOutput(temp.params.output);
      }
    }
  }, [id, pipelines])

  useEffect(() => {
    updateIOValue();
  }, [pipelines, updateIOValue]);


  useEffect(() => {
    axios.get(`${process.env.NEXT_PUBLIC_AI_SERVER}/api/lstm/list-model`).then((response) => {
      console.log(response.data);
      setModelList(response.data.content)
    }).catch(error => {
      console.log(error)
    }).finally(() => {

    })
  }, []);


  const selectModel = (value: string) => {
    // TODO: update pipeline
    console.log("selectModel", value);
  }

  return (
    <ComponentWrapper header={"LSTM Predict"} id={id}>
      <div className="grid w-full max-w-sm items-center gap-1.5 min-h-24">
        <div className={"flex flex-col gap-2"}>
          <Label className="mt-1 text-sm font-medium text-gray-500">
            Input file
          </Label>
          <Badge variant={"outline"} className={'truncate'}>
            {fileInput ? extractFilename(fileInput.replace(/^.*(\\|\/|\:)/, '')) : ""}
          </Badge>
        </div>
        <div className={"flex flex-col gap-2"}>
          <Label className="mt-1 text-sm font-medium text-gray-500">
            Output file
          </Label>
          <Badge variant={"outline"}>
            {fileOutput ? fileOutput.replace(/^.*(\\|\/|\:)/, '') : ""}
          </Badge>
        </div>

        <div className={"flex flex-col gap-2 truncate"}>
          <Label className="mt-1 text-sm font-medium text-gray-500">
            Select Model
          </Label>
          <Select onValueChange={(value) => selectModel(value)}>
            <SelectTrigger className="">
              <SelectValue placeholder="Select model..." />
            </SelectTrigger>
            <SelectContent>
              {
                modelList.map((item, id) => (
                  <SelectItem key={id} value={item}>{item}</SelectItem>
                ))
              }
            </SelectContent>
          </Select>
        </div>
      </div>
    </ComponentWrapper>
  )
}
