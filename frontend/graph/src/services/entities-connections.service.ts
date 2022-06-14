import { EntitiesConnectionsEndpoint } from "../constants/endpoints";
import EntityType from "../enums/entity-type.enum";
import ISelect from "../interfaces/control/select.interface";
import IEntitiesAndConnectionsResponse from "../interfaces/response/entities-connections-response.interface";
import { getCachedAsync } from "./request.service";

export async function getEntitiesAndConnectionsAsync(): Promise<IEntitiesAndConnectionsResponse> {
    return getCachedAsync(EntitiesConnectionsEndpoint, 'entitiesConnections');
}