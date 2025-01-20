import { getAnalysisResults } from "@/actions/analysis-results";
import { useEffect, useState, useTransition } from "react";

export const useAnalysisResult = () => {
  const [isPending, startTransition] = useTransition();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any[] | null>(null);

  const getData = () => {
    setError(null);
    setSuccessMessage(null);

    startTransition(async () => {
      try {
        const response = await getAnalysisResults();
        if (response.success) {
          setSuccessMessage(response.success);
          setData(response.data)
        }
      } catch (err: any) {
        setError(err.message || 'An unexpected error occurred');
      }
    });
  };

  useEffect(() => {
    getData();
  }, []);

  return {
    data,
    isPending,
    successMessage,
    error,
    refetch: getData
  };
}