import { EntitiesConnectionsEndpoint } from "../endpoints";
import IEntitiesAndConnectionsResponse from "../interfaces/response/entities-connections-response.interface";
import { getCachedAsync } from "./request.service";

export async function getEntitiesAndConnectionsAsync(): Promise<IEntitiesAndConnectionsResponse> {
    return getCachedAsync(EntitiesConnectionsEndpoint, 'entitiesConnections');
}