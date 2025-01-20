import React from 'react';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { SortableItem } from "@/app/(protected)/_components/sortable-item";

type SortableListProps = {
  items: string[];
};

export const SortableList: React.FC<SortableListProps> = ({ items }) => {
  return (
    <SortableContext items={items} strategy={verticalListSortingStrategy}>
      {items.map(( id ) => (
        <SortableItem key={id} id={id} />
      ))}
    </SortableContext>
  );
};

