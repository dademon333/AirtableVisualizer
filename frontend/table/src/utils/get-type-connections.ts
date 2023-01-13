import { TypeConnections } from '../types/types';
import { EntityType } from '../const';

type GetTypeConnectionsProps = {
  typeConnections: TypeConnections[];
  entityType: EntityType | string;
}

export const filterTypeConnections = ({ typeConnections, entityType }: GetTypeConnectionsProps): TypeConnections[] => {
  return typeConnections
    .filter(e => (e.parent_type === entityType || e.child_type === entityType) && e.child_column_name !== null);
};
