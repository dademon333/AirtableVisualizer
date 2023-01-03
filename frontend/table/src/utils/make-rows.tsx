import { Entity, EntityConnection, TypeConnections, AllData, Row } from '../types/types';
import { EntityType } from '../const';
import { getChilds, getParents, getItems } from './get-items';
import { WrapperFirstColElement, wrapSecondColElements } from './wrap';

type MakeRowsProps = {
  items: Entity[];
  types: TypeConnections[];
  connectionNumber: number;
  entityType: EntityType;
  data: AllData;
}

export const makeRows = ({ items, types, connectionNumber, entityType, data }: MakeRowsProps): Row[] => {
  const allConnections = types.map((type) => {
    const result: {
      column_name: string;
      connections: EntityConnection[]
    } = {
      column_name: '',
      connections: []
    };

    if (type.parent_type === entityType) {
      result.column_name = type.child_column_name;
    } else {
      result.column_name = type.parent_column_name;
    }

    data.entity_connections.forEach((connection) => {
      if (connection.type_connection_id === type.id) {
        result.connections.push(connection);
      }
    });
    return result;
  });

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
