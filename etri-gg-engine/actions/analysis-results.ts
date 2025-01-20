"use server"

import { db } from "@/lib/db";
import { currentUser } from "@/lib/auth";

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export const getAnalysisResults = async () => {
  const user = await currentUser()

  if (user) {
    const result = await db.analysisResult.findMany({
      where: {
        userId: user.id
      }
    })

    return { data: result, success: "Successfully retrieved analysis result!" };
  }

  return { error: "Unauthorized!" }
}

export const deleteAnalysisResult = async (id: string) => {
  const user = await currentUser()

  if (user) {
    const deletedResult = await db.analysisResult.delete({
      where: {
        id: id,
        userId: user.id
      }
    })

    if (deletedResult) {
      return { success: "Deleted successfully." };
    } else {
      return { error: "Failed to delete analysis result." };
    }
  }

  return { error: "Unauthorized!" };

}