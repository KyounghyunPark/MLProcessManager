import { ComponentWrapper, ComponentWrapperProps } from "@/app/(protected)/_components/component-wrapper";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import usePipelineStore from "@/hooks/use-pipeline-store";
import { Badge } from "@/components/ui/badge";
import { extractFilename } from "@/lib/file-io-utils";

interface SvddProps extends ComponentWrapperProps {
  id: string;
}

export const SvddCard = ({ id }: SvddProps) => {
  const { pipelines, updateParams, getParams } = usePipelineStore((state) => state);

  const [cValue, setCValue] = useState<number>(0.1);
  const [hour, setHour] = useState(0);
  const [fileInput, setFileInput] = useState<string>("");
  const [fileOutput, setFileOutput] = useState<string>("");

  function updateComponent() {
    const currentParams = pipelines.find((p) => p.id === id)?.params;
    console.log({ current: currentParams });
    if (currentParams) {
      updateParams(id, { ...currentParams, cValue: cValue, hour: hour });
    } else {
      updateParams(id, { cValue: cValue, hour: hour });
    }
  }

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
    <ComponentWrapper header={"SVDD"} id={id}>
      <div className="grid w-full max-w-sm items-center gap-1.5 min-h-24">
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

        <div>
          <Label>Hour</Label>
          <Input
            type={"number"}
            min={0}
            max={23}
            value={hour}
            onChange={(event) => {
              return setHour(Number(event.target.value));
            }}
            onPointerDown={(e) => e.stopPropagation()}
          />
        </div>
        <div>
          <Label>C value</Label>
          <Input
            type={"number"}
            min={0}
            max={23}
            value={cValue}
            onChange={(event) => {
              return setCValue(Number(event.target.value));
            }}
            onPointerDown={(e) => e.stopPropagation()}
          />
        </div>

        <Button
          variant={"outline"}
          onMouseDown={() => updateComponent()}
        >
          Update
        </Button>

      </div>
    </ComponentWrapper>
  )
}