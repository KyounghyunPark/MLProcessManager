import { ComponentWrapper, ComponentWrapperProps } from "@/app/(protected)/_components/component-wrapper";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import usePipelineStore from "@/hooks/use-pipeline-store";
import { useState } from "react";
import { Button } from "@/components/ui/button";

interface FileOutputProps extends ComponentWrapperProps {
  id: string;
}

export const FileOutput = ({ id }: FileOutputProps) => {
  const [fileName, setFileName] = useState<string>("");
  const { updateValue, getValue } = usePipelineStore((state) => state);

  const [status, setStatus] = useState<string | undefined>("Not Setup");

  function ensureCsvExtension(filename: string) {
    if (!filename.includes('.') || filename.lastIndexOf('.') === 0) {
      return filename + '.csv'; // Add the default extension
    }
    return filename; // Return as is if it already has an extension
  }

  const updateOutputFilename = (id: string, fileName: string) => {
    updateValue(id, ensureCsvExtension(fileName))
    setStatus("Updated " + getValue(id)?.replace(/^.*(\\|\/|\:)/, ''));
  }

  const Footer = () => (
    <>
      <div className="text-center">Status:</div>
      <div className="text-center">{status}</div>
    </>
  )

  return (
    <ComponentWrapper header={"File Output"} id={id} footer={<Footer/>}>
      <div className="grid w-full max-w-sm items-center gap-1.5 min-h-24">
        <Label className="text-sm font-medium text-gray-700">
          Output file name:
        </Label>

        <Input
          value={fileName}
          onChange={(e) => setFileName(e.target.value)}
          onPointerDown={(e) => e.stopPropagation()}
        />
        <Button
          variant={"outline"}
          onMouseDown={() => updateOutputFilename(id, ensureCsvExtension(fileName))}
        >
          Update
        </Button>

      </div>
    </ComponentWrapper>
  )
}
