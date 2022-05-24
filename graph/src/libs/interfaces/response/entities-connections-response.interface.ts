import { EntitySize } from "../core/entity-size.enum";
import { EntityType } from "../core/entity-type.enum";

interface IEntitiesAndConnectionsResponse {
    connections: IConnection[],
    entities: { [id: string]: IEntity }
}

interface IConnection {
    parent_type: EntityType,
    child_type: EntityType,
    id: number,
    entities_connections: IEntityConnection[]
}

interface IEntityConnection {
    parent_id: number,
    child_id: number
}

interface IEntity {
    name: string,
    type: EntityType,
    size: EntitySize,
    description?: string,
    study_time?: number;
}

export default IEntitiesAndConnectionsResponse;