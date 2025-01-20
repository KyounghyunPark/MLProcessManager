import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { useState, useTransition } from "react";
import DroppableArea from "@/app/(protected)/_components/droppable-area";
import { closestCenter, DndContext, DragEndEvent } from "@dnd-kit/core";
import { arrayMove } from "@dnd-kit/sortable";
import { Button } from "@/components/ui/button";
import { SortableList } from "@/app/(protected)/_components/sortable-list";
import { BarLoader } from "react-spinners";
import { randomId } from "@/lib/random-id";
import usePipelineStore from "@/hooks/use-pipeline-store";
import { ANALYSIS_ITEMS, INPUT_ITEMS, IO_ITEMS, OUTPUT_ITEMS } from "@/data/pipeline-components-list";
import { toast } from "sonner";
import axios from "axios";
import { pipelinesExecution } from "@/actions/pipelines";
import { downloadCSV } from "@/lib/file-io-utils";
import { cn } from "@/lib/utils";

export const DrawBoard = () => {
  const [isPending, startTransition] = useTransition()

  const [ioItems, setIoItems] = useState<string[]>(IO_ITEMS);
  const [analysisItems, setAnalysisItems] = useState<string[]>(ANALYSIS_ITEMS);
  const [isValidated, setIsValidated] = useState<boolean>(false);

  const { pipelines, setPipelines, updateParams } = usePipelineStore((state) => state);

  const [outputFile, setOutputFile] = useState("")

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    console.log(event);

    if (!over) return;

    if (over.id === 'droppable-area') {
      // Item dropped into DroppableArea
      setPipelines([...pipelines, { name: active.id as string, id: randomId() }]);

    } else if (active.id !== over.id) {
      // Item reordered within SortableList
      setIoItems((prevItems) => {
        const oldIndex = prevItems.indexOf(active.id as string);
        const newIndex = prevItems.indexOf(over.id as string);
        return arrayMove(prevItems, oldIndex, newIndex);
      });

      setAnalysisItems((prevItems) => {
        const oldIndex = prevItems.indexOf(active.id as string);
        const newIndex = prevItems.indexOf(over.id as string);
        return arrayMove(prevItems, oldIndex, newIndex);
      });
    }
  };

  const handleClearDraw = () => {
    setPipelines([])
    setOutputFile("")
  }

  const handleExecution = () => {
    setOutputFile("")

    if (isValidated) {

      console.log(pipelines)


      startTransition(() => {
        pipelinesExecution(pipelines).then((data) => {
          console.log(data)
          if (data.error) {
            toast.error(data.error)
          }
          if (data.success) {
            toast.success(data.success);
            if (data && data.successInfo) {
              console.log(data.successInfo[0])
              setOutputFile(data.successInfo[0])
            }
          }
        })
      });
    } else {
      toast.error("Please validate the pipelines first!");
    }
  }


  function validatePipelines() {
    const analysisComponents = pipelines.filter((pipeline) => ANALYSIS_ITEMS.includes(pipeline.name))
    const inputComponents = pipelines.filter((pipeline) => INPUT_ITEMS.includes(pipeline.name));
    const outputComponents = pipelines.filter((pipeline) => OUTPUT_ITEMS.includes(pipeline.name));

    if (inputComponents.length < 1 || outputComponents.length < 1 || analysisComponents.length < 1) {
      return false
    }

    // TODO: handle the case with multiple Input, Output, Analysis components,
    if (inputComponents.length > 1 || outputComponents.length > 1 || analysisComponents.length > 1) {
      return false
    }

    // check if the order is correct
    const iIndex = pipelines.indexOf(inputComponents[0])
    const oIndex = pipelines.indexOf(outputComponents[0])
    for (const analysis of analysisComponents) {
      const aIndex = pipelines.indexOf(analysis)

      if (aIndex > iIndex && aIndex < oIndex) {
        continue
      } else {
        return false;
      }
    }

    // This handles basic case with 1 input, 1 output and 1 analysis components
    // check if input and output are defined
    if (inputComponents[0].value !== undefined && inputComponents[0].value !== null &&
      outputComponents[0].value !== undefined && outputComponents[0].value !== null
    ) {
      const currentParams = pipelines.find((p) => p.id === analysisComponents[0].id)?.params;
      console.log(currentParams)
      if (currentParams) {
        updateParams(analysisComponents[0].id, {
          ...currentParams,
          input: inputComponents[0].value!,
          output: outputComponents[0].value!
        });
      } else {
        updateParams(analysisComponents[0].id, {
          input: inputComponents[0].value!,
          output: outputComponents[0].value!
        });
      }
    } else {
      return false;
    }

    return true
  }

  const handleValidation = () => {
    console.log("Validation");
    if (!validatePipelines()) {
      setIsValidated(false);
      console.log("Validation failed");
      toast.error("Pipelines verification failed!");
    } else {
      setIsValidated(true);
      console.log("Validation succeeded");
      toast.success("Pipelines verification successfully!");
    }
  }

  return (
    <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
      <div className={cn("flex flex-row items-start justify-between gap-4 w-full md:px-10",
        pipelines.length > 5 ? "p-2" : "p-10"
        )}>
        <div className={"flex flex-col space-y-4"}>
          <Card className="">
            <CardHeader>
              <p className={'text-xl font-semibold text-center'}>
                I/O
              </p>
            </CardHeader>
            <CardContent>
              <div className={'flex flex-col items-center justify-between rounded-md border p-3 shadow-md gap-1'}>
                <SortableList items={ioItems}/>
              </div>

            </CardContent>
          </Card>

          <Card className="">
            <CardHeader>
              <p className={'text-xl font-semibold text-center'}>
                Analysis Functions
              </p>
            </CardHeader>
            <CardContent>
              <div className={'flex flex-col items-center justify-between rounded-md border shadow-md gap-4 p-3'}>
                <SortableList items={analysisItems}/>
              </div>
            </CardContent>
          </Card>
        </div>
        <Card className={'w-full h-full'}>
          <CardHeader>
            <p className={'text-xl font-semibold text-center'}>
              Pipeline Creator
            </p>
          </CardHeader>
          <CardContent className={'min-h-[550px]'}>
            <DroppableArea/>
          </CardContent>
          <CardFooter>
            <div className={'flex w-full items-center justify-between'}>
              <Button
                onClick={handleClearDraw}
                variant="destructive"
                disabled={isPending}
              >
                Clear
              </Button>
              {isPending && <BarLoader/>}
              <div className={'flex flex-row items-center justify-center gap-4'}>
                <Button onClick={handleValidation} variant={"secondary"} disabled={isPending}> Validate </Button>
                <Button onClick={handleExecution} variant={"success"} disabled={isPending}> Execute </Button>

                {/*<Button onClick={handleExecutionTest} variant={"success"}> Execute Test</Button>*/}
                {
                  outputFile !== "" && !isPending &&
                    <Button onClick={() => downloadCSV(outputFile)} variant={"success"}> Download CSV</Button>
                }
              </div>

            </div>
          </CardFooter>
        </Card>
      </div>
    </DndContext>
  )
}
