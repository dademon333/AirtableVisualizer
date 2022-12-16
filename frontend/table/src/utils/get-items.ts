import { EntityConnection, AllData } from '../types/types';
import { wrapSecondColElement } from './wrap';

export const getChilds = (connections: EntityConnection[], id: number): number[] => {
  return connections
    .filter((connection: EntityConnection) => connection.parent_id === id)
    .map((connection: EntityConnection) => connection.child_id);
};

export const getItems = (items: JSX.Element[], childs: number[], data: AllData): JSX.Element[] => {
  childs.forEach((child, index) => {
    const item = data.entities.filter((entity) => entity.id === child);
    items.push(
      wrapSecondColElement(item[0].name, index)
    );
  });
  return items;
};
