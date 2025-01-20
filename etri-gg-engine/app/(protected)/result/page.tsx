import { ResultTable } from "@/app/(protected)/_components/result-table";

const ResultPage = async () => {

  return (
    <div className={'w-[90%] bg-secondary rounded-lg shadow-sm p-5 mt-2 md:mt-10'}>
      <ResultTable />
    </div>
  )
}

export default ResultPage