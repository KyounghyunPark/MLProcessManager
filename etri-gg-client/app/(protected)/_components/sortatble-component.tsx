import { SortableContext, useSortable, verticalListSortingStrategy } from "@dnd-kit/sortable";
import { FileInput } from "@/app/(protected)/_components/file-input";
import { FileOutput } from "@/app/(protected)/_components/file-output";
import React, { useCallback, useEffect } from "react";
import { CSS } from "@dnd-kit/utilities";
import { LstmPredictCard } from "@/app/(protected)/_components/lstm-predict-card";
import { OospCard } from "@/app/(protected)/_components/oosp-card";
import { SvddCard } from "@/app/(protected)/_components/svdd-card";
import { MapMatchingCard } from "@/app/(protected)/_components/map-matching-card";
import usePipelineStore from "@/hooks/use-pipeline-store";
import { LstmTrainCard } from "@/app/(protected)/_components/lstm-train-card";
import { cn } from "@/lib/utils";

interface SortableComponentProps {
  description?: string
}

interface SortableComponentItemProps {
  id: string;
  children: React.ReactNode;
}

const SortableComponentItem = ({ id, children }: SortableComponentItemProps) => {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id });

  const style: React.CSSProperties = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div ref={setNodeRef} {...attributes} {...listeners} style={style}>
      {children}
    </div>
  )
}

export const SortableComponent = ({ }: SortableComponentProps) => {
  const { pipelines } = usePipelineStore((state) => state);
  useEffect(() => {
    console.log(pipelines);
  }, [pipelines]);

  const calcGridSize = useCallback(() => {
    if (pipelines.length > 2 && pipelines.length < 6) {
      switch (pipelines.length % 3) {
        case 0:
          return "grid-cols-3"
        case 1:
          return "grid-cols-4"
        case 2:
          return "grid-cols-5"
        default:
          return "grid-cols-1"
      }
    } else {
      return "grid-cols-6";
    }

  }, [pipelines]);

  return (
    <SortableContext items={pipelines} strategy={verticalListSortingStrategy}>
      <div className={cn("grid items-center gap-4", calcGridSize() )}>
        {pipelines.map(({ id, name }) => {
            switch (name) {
              case 'File Upload':
                return (
                  <SortableComponentItem id={id} key={id}>
                    <FileInput id={id} />
                  </SortableComponentItem>

                )
              case 'File Download':
                return (
                  <SortableComponentItem id={id} key={id}>
                    <FileOutput id={id} />
                  </SortableComponentItem>
                )
              case 'Map Matching':
                return (
                  <SortableComponentItem id={id} key={id}>
                    <MapMatchingCard id={id} />
                  </SortableComponentItem>
                )
              case "SVDD":
                return (
                  <SortableComponentItem id={id} key={id}>
                    <SvddCard id={id} />
                  </SortableComponentItem>
                )
              case "OOSP":
                return (
                  <SortableComponentItem id={id} key={id}>
                    <OospCard id={id} />
                  </SortableComponentItem>
                )
              case "LSTM Train":
                return (
                  <SortableComponentItem id={id} key={id}>
                    <LstmTrainCard id={id} />
                  </SortableComponentItem>
                )

              case "LSTM Predict":
                return (
                  <SortableComponentItem id={id} key={id}>
                    <LstmPredictCard id={id} />
                  </SortableComponentItem>
                )
              default:
                return (
                  <SortableComponentItem id={id} key={id}>
                    {id}
                  </SortableComponentItem>
                )
            }
          }
        )}
      </div>

    </SortableContext>
  );
};
