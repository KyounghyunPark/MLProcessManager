import { closestCenter, DndContext, DragEndEvent, useDroppable } from '@dnd-kit/core';
import { arrayMove } from "@dnd-kit/sortable";
import { SortableComponent } from "@/app/(protected)/_components/sortatble-component";
import usePipelineStore from "@/hooks/use-pipeline-store";

const DroppableArea = () => {
  const { pipelines, setPipelines } = usePipelineStore((state) => state);

  const { setNodeRef, isOver } = useDroppable({
    id: 'droppable-area',
  });

  const style: React.CSSProperties = {
    padding: '10px',
    width: '100%',
    minHeight: '300px',
    backgroundColor: isOver ? 'lightblue' : 'lightyellow',
    border: '2px dashed gray',
    marginTop: '20px',
  };

  const handleDragEndOnDroppableArea = (event: DragEndEvent) => {
    const { active, over } = event;
    console.log(event);

    if (!over) return;

    if (active.id !== over.id) {
      // Item reordered within SortableList
      const activeId = active.id as string
      const overId = over.id as string
      const oldIndex = pipelines.findIndex( (element) => element.id === activeId);
      const newIndex = pipelines.findIndex( (element) => element.id === overId);
      const newPipeline = arrayMove(pipelines, oldIndex, newIndex);

      setPipelines(newPipeline);
    }
  }

  return (
    <div
      ref={setNodeRef} style={style}
      className={'flex items-center justify-center rounded-md'}
    >
      {pipelines.length > 0 ? (
        <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEndOnDroppableArea}>
          <SortableComponent />
        </DndContext>
      ) : (
        <p>Drag items here</p>
      )}
    </div>
  );
};

export default DroppableArea;
