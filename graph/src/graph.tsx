import { useEffect } from 'react';
import GraphModel from './libs/classes/graph.model';
import IEntitiesAndConnectionsResponse from './libs/interfaces/response/entities-connections-response.interface';

export default function Graph(data: IEntitiesAndConnectionsResponse): JSX.Element {

    useEffect(() => {
        const graph = new GraphModel("svg", data);
        graph.addSimulation();
    }, []);


    return <svg width="5000" height="5000"></svg>;
}

export {};