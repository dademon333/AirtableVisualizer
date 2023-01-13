import { Entity, TypeConnections, AllData, Row } from '../types/types';
import { EntityType } from '../const';
import { getChilds, getParents, getItems } from './get-items';
import { WrapperFirstColElement, wrapSecondColElements } from './wrap';
import { getAllConnections } from './get-all-connections';

type MakeRowsProps = {
  items: Entity[];
  types: TypeConnections[];
  connectionNumber: number;
  entityType: EntityType;
  data: AllData;
}

export const makeRows = ({ items, types, connectionNumber, entityType, data }: MakeRowsProps): Row[] => {
  const allConnections = getAllConnections({ types, entityType, entity_connections: data.entity_connections });

  return items.map((item) => {
    const row = makeEmptyRow();
    const childs: number[][] = [];
    const parents: number[][] = [];
    let items: JSX.Element[][] = [];
    const column_names: string[] = [];

    allConnections.forEach((element, index) => {
      childs.push(getChilds(element.connections, item.id!));
      parents.push(getParents(element.connections, item.id!));
      items.push(getItems([], childs[index].concat(parents[index]), data));
      column_names.push(element.column_name);
    });

    row.id = item.id!;
    row.name = <WrapperFirstColElement entity={item} items={items} column_names={column_names} />;
    row.body = wrapSecondColElements(items[connectionNumber]);
    return row;
  });
};

const makeEmptyRow = (): Row => ({
  id: 0,
  name: <></>,
  body: <></>
});
