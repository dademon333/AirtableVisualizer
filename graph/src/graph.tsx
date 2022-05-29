import { useEffect } from 'react';
import GraphModel from './libs/classes/graph.model';
import IEntitiesAndConnectionsResponse from './libs/interfaces/response/entities-connections-response.interface';

export default function Graph(data: IEntitiesAndConnectionsResponse): JSX.Element {

    useEffect(() => {
        const graph = new GraphModel("svg", data);
        graph.addSimulation();
    }, []);

    const width = window.innerWidth - 1;
    const height = window.innerHeight - 4;


    return <svg height={height} width={width}></svg>;
}

export {};