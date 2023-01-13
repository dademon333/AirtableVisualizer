import { TypeConnections, EntityConnection } from '../types/types';
import { EntityType } from '../const';

type AllConnectionsProps = {
  types: TypeConnections[];
  entityType: EntityType;
  entity_connections: EntityConnection[];
};

type AllConnectionsResult = {
  column_name: string;
  connections: EntityConnection[];
};

export const getAllConnections = ({ types, entityType, entity_connections }: AllConnectionsProps): AllConnectionsResult[] => {
  return types.map((type) => {
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
  
    entity_connections.forEach((connection) => {
      if (connection.type_connection_id === type.id) {
        result.connections.push(connection);
      }
    });
    return result;
  });
}