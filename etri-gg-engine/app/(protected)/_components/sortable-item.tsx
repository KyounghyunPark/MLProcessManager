import React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

type SortableItemProps = {
  id: string;
};

export const SortableItem: React.FC<SortableItemProps> = ({ id }) => {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id });

  const style: React.CSSProperties = {
    transform: CSS.Transform.toString(transform),
    transition,
    padding: '10px',
    margin: '5px',
    background: 'lightgray',
    border: '1px solid gray',
    cursor: 'grab',
    minWidth: '150px',
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}
         className={'text-center rounded-md'}
    >
      {id}
    </div>
  );
};
