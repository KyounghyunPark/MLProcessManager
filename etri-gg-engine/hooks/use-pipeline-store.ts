import { create } from 'zustand'
import { createJSONStorage, persist } from "zustand/middleware";

export type PipelineComponent = {
  id: string
  name: string
  value?: string
  params?: ComponentParameter
}

export type ComponentParameter = {
  input?: string
  output?: string

  hour?: number
  cValue?:number

  modelFile?: string;
  ratio?: number;
  optimizerType?: string;
  learningRate?: number;
  weightDecay?: number;
  epochNum?: number;
  timeSteps?: number;
  batchSize?: number;
  cnnHiddenLayer?: number;
  lstmHiddenLayer?: number;
}

type PipelineStoreState = {
  pipelines: PipelineComponent[]
}

type PipelineStoreActions = {
  setPipelines: (pipelines: PipelineComponent[]) => void
  onDelete: (id: string) => void
  updateValue: (id: string, value: string) => void
  updateParams: (id: string, params: ComponentParameter) => void
  getValue: (id: string) => string | undefined
  getParams: (id: string) => ComponentParameter | undefined
}

type PipelineStore = PipelineStoreState & PipelineStoreActions


const usePipelineStore = create<PipelineStore, [["zustand/persist", unknown]]>(
  persist(
    (set, get) => ({
      pipelines: [], // initial pipeline state

      setPipelines: (pipelines: PipelineComponent[]) => {
        set({ pipelines })
      },

      onDelete: (id) => set((state) => ({
        pipelines: state.pipelines.filter((pipeline) => pipeline.id !== id)
      })), // Action to delete a pipeline by id,

      getValue: (id: string) => {
        const pipeline = get().pipelines.find((pipeline) => pipeline.id === id)
        return pipeline?.value
      },

      getParams: (id: string) => {
        const pipeline = get().pipelines.find((pipeline) => pipeline.id === id)
        return pipeline?.params
      },

      updateValue: (id, value) => set((state) => ({
        pipelines: state.pipelines.map((pipeline) =>
          pipeline.id === id ? { ...pipeline, value } : pipeline
        )
      })), // Action to update params of a specific pipeline by id

      updateParams: (id, params) => set((state) => ({
        pipelines: state.pipelines.map((pipeline) =>
          pipeline.id === id ? { ...pipeline, params } : pipeline
        )
      })) // Action to update params of a specific pipeline by id

    }),
    {
      name: 'pipeline',
      storage: createJSONStorage(() => sessionStorage),
    }
  ),
)


export default usePipelineStore
