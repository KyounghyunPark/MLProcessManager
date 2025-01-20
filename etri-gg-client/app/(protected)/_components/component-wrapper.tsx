import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { FaArrowRight } from "react-icons/fa";
import { IoCloseCircleOutline } from "react-icons/io5";
import usePipelineStore from "@/hooks/use-pipeline-store";
import React from "react";

export interface ComponentWrapperProps {
  children?: React.ReactNode;
  header?: string;
  footer?: React.ReactNode;
  className?: string;
  id: string;
}

export const ComponentWrapper = ({ children, header, footer, className, id }: ComponentWrapperProps) => {
  const { onDelete } = usePipelineStore((state) => state);
  return (
    <Card key={id} className={`grid w-60 h-96 ${className}`}>
      <CardHeader>
        <div className="flex items-center justify-between gap-1">
          {header}
          <FaArrowRight className="w-5 h-5"/>
          <IoCloseCircleOutline
            className="w-10 h-10 text-gray-400 hover:text-black"
            onMouseDown={() => onDelete(id)}/>
        </div>
      </CardHeader>
      <CardContent>
        {children}
      </CardContent>
      <CardFooter className="align-bottom">
        <div className="grid w-full justify-center">
          {footer}
        </div>
      </CardFooter>
    </Card>
  )
}
