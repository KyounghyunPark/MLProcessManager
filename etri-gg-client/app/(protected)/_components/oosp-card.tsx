import { ComponentWrapper, ComponentWrapperProps } from "@/app/(protected)/_components/component-wrapper";
import usePipelineStore from "@/hooks/use-pipeline-store";
import { useCallback, useEffect, useState } from "react";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { extractFilename } from "@/lib/file-io-utils";

interface OospProps extends ComponentWrapperProps {
  id: string;
}

export const OospCard = ({ id }: OospProps) => {
  const { pipelines } = usePipelineStore((state) => state);

  const [fileInput, setFileInput] = useState<string>("");
  const [fileOutput, setFileOutput] = useState<string>("");

  const updateIOValue = useCallback(() => {
    const temp = pipelines.find((item) => item.id === id);
    if (temp && temp !== undefined && temp.params) {
      if (temp.params.input) {
        setFileInput(temp.params?.input);
      }
      if (temp.params.output) {
        setFileOutput(temp.params.output);
      }
    }
  }, [id, pipelines])

  useEffect(() => {
    updateIOValue();
  }, [pipelines, updateIOValue]);

  return (
    <ComponentWrapper header={"OOSP"} id={id}>
      <div className="flex flex-col w-full max-w-sm gap-4 min-h-24">
        <div className={"flex flex-col gap-2"}>
          <Label className="mt-1 text-sm font-medium text-gray-500">
            Input file
          </Label>
          <Badge variant={"outline"}>
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
      </div>
    </ComponentWrapper>
  )
}