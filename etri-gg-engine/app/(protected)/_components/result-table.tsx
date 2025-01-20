"use client"

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { downloadCSV, downloadCSVFromFolder, extractFilename } from "@/lib/file-io-utils";
import { Button } from "@/components/ui/button";
import { ConfirmDialog } from "@/app/(protected)/_components/confirm-dialog";
import { deleteAnalysisResult } from "@/actions/analysis-results";
import { toast } from "sonner";
import { useAnalysisResult } from "@/hooks/use-analysis-result";
import { Skeleton } from "@/components/ui/skeleton";
import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";


export const ResultTable = () => {
  const { data, refetch, isPending, error } = useAnalysisResult()

  const handleDelete = (id: string) => {
    deleteAnalysisResult(id)
      .then((data) => {
        if (data.error) {
          toast.error(data.error)
        }
        if (data.success) {
          refetch()
          toast.success(data.success)
        }
      });
  }

  const [currentPage, setCurrentPage] = useState<number>(1);
  const ITEMS_PER_PAGE = Number(process.env.NEXT_PUBLIC_ITEMS_PER_PAGE) || 2;

  const handlePrev = () => {
    if (currentPage > 1) setCurrentPage((prev) => prev - 1);
  };

  const handleNext = () => {
    if (currentPage < totalPages) setCurrentPage((prev) => prev + 1);
  };

  const dataLength = data?.length || 0

  const totalPages = Math.ceil(dataLength / ITEMS_PER_PAGE);

  const paginatedData = data?.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  );

  const TableRowsData = () => {
    return (
      paginatedData?.map((res) => (
        <TableRow key={res.id}>
          <TableCell className="">{res.id}</TableCell>
          <TableCell>{res.status}</TableCell>
          <TableCell>{res.name}</TableCell>
          <TableCell
            className="cursor-pointer hover:underline"
            onClick={() => downloadCSVFromFolder(res.input, "input")}
          >
            {extractFilename(res.input)}
          </TableCell>
          <TableCell
            className="cursor-pointer hover:underline"
            onClick={() => downloadCSV(res.output)}
          >
            {extractFilename(res.output)}
          </TableCell>
          <TableCell className="">{res.createdAt.toLocaleString()}</TableCell>
          <TableCell className="">{res.updatedAt.toLocaleString()}</TableCell>
          <TableCell className="w-[10px]">
            <ConfirmDialog
              title="Are you sure you want to delete this result?"
              description={"This action cannot be undone."}
              onProceed={() => handleDelete(res.id)}
            >
              <Button
                className="p-1"
                size={"sm"}
                variant={"destructive"}
              >
                Delete
              </Button>
            </ConfirmDialog>
          </TableCell>
        </TableRow>
      ))
    )
  }


  return (
    <div>
      <h1 className={'text-2xl font-semibold text-center mb-4'}>
        Pipeline Results
      </h1>

      <Table>
        {/*<TableCaption>A list of your recent analysis results.</TableCaption>*/}
        <TableHeader>
          <TableRow>
            <TableHead className="">Pipeline Id</TableHead>
            <TableHead className="">Status</TableHead>
            <TableHead>Function</TableHead>
            <TableHead>Input</TableHead>
            <TableHead className="">Output</TableHead>
            <TableHead className="">Created at</TableHead>
            <TableHead className="">Updated at</TableHead>
            <TableHead className="">Action</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isPending ?
            <TableDataSkeleton/> :
            <TableRowsData/>
          }
        </TableBody>
        <TableFooter>
        </TableFooter>
      </Table>

      <div className="mt-4 flex justify-between items-center">
        <Button
          className="px-4 py-2 rounded disabled:opacity-50"
          onClick={handlePrev}
          disabled={currentPage === 1}
          variant="outline"
          size={"sm"}
        >
          Previous
        </Button>
        <span className={"text-sm"}>
            Page {currentPage} of {totalPages}
          </span>
        <Button
          className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
          onClick={handleNext}
          disabled={currentPage === totalPages}
          variant="outline"
          size="sm"
        >
          Next
        </Button>
      </div>
    </div>
  )
}


const TableDataSkeleton = () => {
  return (
    <>
      <TableRow>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
      </TableRow>
      <TableRow>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
      </TableRow>
      <TableRow>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
        <TableCell className="text-center"><SkeletonCell/></TableCell>
      </TableRow>
    </>
  )
}

const SkeletonCell = () => {
  return (
    <Skeleton className="h-4 w-10 rounded-md"/>
  )
}