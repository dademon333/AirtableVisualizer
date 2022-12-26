import EntitySize from "../../enums/entity-size.enum";
import EntityType from "../../enums/entity-type.enum";

export interface IEntitiesAndConnectionsResponse {
    connections: IConnection[],
    entities: { [id: string]: IEntity }
    visibleEntities: {}
}

export interface IConnection {
    parent_type: EntityType,
    child_type: EntityType,
    id: number,
    entities_connections: IEntityConnection[]
}

export interface IEntityConnection {
    parent_id: number,
    child_id: number
}

export interface IEntity {
    name: string,
    type: EntityType,
    size: EntitySize,
    description?: string,
    study_time?: number;
}

export default IEntitiesAndConnectionsResponse;