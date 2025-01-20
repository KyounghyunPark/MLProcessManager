export const extractFilename = (fileName: string) => {
  return fileName.split("@")[1];
}

export const downloadCSV = (outputFile: string) => {
  window.open(`${process.env.NEXT_PUBLIC_AI_SERVER}/api/gg/download-file/${outputFile}`, "_blank") //to open new page
}

export const downloadCSVFromFolder = (file: string, folder: string) => {
  window.open(`${process.env.NEXT_PUBLIC_AI_SERVER}/api/gg/download-file?filename=${file}&folder=${folder}`, "_blank") //to open new page
}