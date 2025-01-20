import { Input } from "@/components/ui/input";
import { ComponentWrapper, ComponentWrapperProps } from "@/app/(protected)/_components/component-wrapper";
import usePipelineStore from "@/hooks/use-pipeline-store";
import { Button } from "@/components/ui/button";
import React, { useState } from "react";
import axios from "axios";
import { extractFilename } from "@/lib/file-io-utils";
import { Label } from "@/components/ui/label";

interface FileInputProps extends ComponentWrapperProps {
  id: string;
}

export const FileInput = ({ id }: FileInputProps) => {
  const { updateValue, getValue } = usePipelineStore((state) => state);

  const [uploadedFile, setUploadedFile] = useState<File[]>([])
  const [status, setStatus] = useState<string>("Not Uploaded")

  const uploadFile = () => {

    let data: any = new FormData()
    Array.from(uploadedFile).forEach((file, index) => {
      data.append('file', file, `${id}@${file.name}`)
    })

    axios.post(`${process.env.NEXT_PUBLIC_AI_SERVER}/api/gg/upload-file`, data, {
      headers: {
        accept: 'application/json',
        'Accept-Language': 'en-US,en;q=0.8',
        'Content-Type': `multipart/form-data; boundary=${data.boundary}`,
      },
    }).then((response) => {
      console.log(response.data);
      updateValue(id, response.data.content)
      setStatus("Uploaded " + extractFilename(response.data.content))
    }).catch(error => {
      console.log(error)
    }).finally(() => {

    })
  }

  const Footer = () => (
    <>
      <div className="text-center">Status:</div>
      <div className="text-center">{status}</div>
    </>
  )

  return (
    <ComponentWrapper header={"File Input"} id={id} footer={<Footer/>}>
      <div className="grid w-full max-w-sm items-center gap-1.5 min-h-24">
        <Label className="text-sm font-medium text-gray-700">Upload file:</Label>
        <Input type="file" accept=".csv" onChange={(e: any) => setUploadedFile(e.target.files)}
        />
        <Button variant={"outline"} onMouseDown={() => uploadFile()}>Upload</Button>
      </div>
    </ComponentWrapper>
  )
}
