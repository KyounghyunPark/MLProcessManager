import { ComponentWrapper, ComponentWrapperProps } from "@/app/(protected)/_components/component-wrapper";
import usePipelineStore from "@/hooks/use-pipeline-store";
import React, { useCallback, useEffect, useState } from "react";


import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";


interface LstmProps extends ComponentWrapperProps {
  id: string;
}

interface LstmTrainParam {
  modelFile: string;
  ratio: number;
  optimizerType: string;
  learningRate: number;
  weightDecay: number;
  epochNum: number;
  timeSteps: number;
  batchSize: number;
  cnnHiddenLayer: number;
  lstmHiddenLayer: number;

}

export const LstmTrainCard = ({ id }: LstmProps) => {
  const { pipelines, updateParams } = usePipelineStore((state) => state);

  const [status, setStatus] = useState("Not Submit");

  const [paramStatus, setParamStatus] = useState(false);

  const [localParams, setLocalParams] = useState<LstmTrainParam>({
    modelFile: `lstm_${new Date().valueOf()}.pt`,
    ratio: 0.2,
    optimizerType: "Adam",
    learningRate: 0.001,
    weightDecay: 0.0001,
    epochNum: 20,
    timeSteps: 5,
    batchSize: 128,
    cnnHiddenLayer: 256,
    lstmHiddenLayer: 256,
  });


  const updateState = (name: string, value: any) => {
    setStatus("Modified");
    setLocalParams({ ...localParams, [name]: value });
  }

  const submitParam = () => {
    setParamStatus(false)
    setStatus("Submitted")
    updateParams(id, {
      ...localParams,
    })
  }


  const Footer = () => (
    <>
      <div className="text-center">Status:</div>
      <div className="text-center">{status}</div>
    </>
  )

  return (
    <ComponentWrapper header={"LSTM Train"} id={id} footer={<Footer/>}>
      <div className="grid w-full gap-1.5 min-h-24  ">
        <Label className="text-sm font-medium text-gray-700">Model file name:</Label>
        <Input value={localParams.modelFile} onChange={(e) => updateState("modelFile", e.target.value)}/>
        <Popover open={paramStatus} onOpenChange={setParamStatus}>
          <PopoverTrigger asChild>
            <Button variant="outline" onPointerDown={(e) => e.stopPropagation()}>Edit Parameter</Button>
          </PopoverTrigger>
          <PopoverContent className="w-[500px]">
            <div className="grid grid-cols-3 w-full items-center gap-1.5 min-h-24 ">
              <div>
                <Label className="text-sm font-medium text-gray-700">Test Ratio:</Label>
                <Input value={localParams.ratio} onChange={(e) => updateState("ratio", e.target.value)}/>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">Optimizer Type:</Label>
                <Select onValueChange={(value) => updateState("optimizerType", value)}>
                  <SelectTrigger className="">
                    <SelectValue placeholder="Adam"/>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Adam">Adam</SelectItem>
                    <SelectItem value="SGD">SGD</SelectItem>
                    <SelectItem value="RMSprop">RMSprop</SelectItem>
                    <SelectItem value="Adagrad">Adagrad</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">Learning Rate:</Label>
                <Input value={localParams.learningRate} onChange={(e) => updateState("learningRate", e.target.value)}/>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">Epoch Number:</Label>
                <Input value={localParams.epochNum} onChange={(e) => updateState("epochNum", e.target.value)}/>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">Time Steps:</Label>
                <Input value={localParams.timeSteps} onChange={(e) => updateState("timeSteps", e.target.value)}/>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">Batch Size:</Label>
                <Input value={localParams.batchSize} onChange={(e) => updateState("batchSize", e.target.value)}/>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">CNN Hidden Layer:</Label>
                <Input value={localParams.cnnHiddenLayer}
                       onChange={(e) => updateState("cnnHiddenLayer", e.target.value)}/>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">LSTM Hidden Layer:</Label>
                <Input value={localParams.lstmHiddenLayer}
                       onChange={(e) => updateState("lstmHiddenLayer", e.target.value)}/>
              </div>


            </div>

            <div className="mt-3 w-full text-center">
              <Button variant={"default"} onMouseDown={() => submitParam()}>Submit params</Button>
            </div>
          </PopoverContent>
        </Popover>
      </div>

    </ComponentWrapper>
  )
}
