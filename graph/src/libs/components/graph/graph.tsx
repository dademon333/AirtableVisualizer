import { useEffect, useState } from 'react';
import GraphModel from '../../models/graph/graph.model';
import IEntitiesAndConnectionsResponse from '../../interfaces/response/entities-connections-response.interface';
import { useSelector } from 'react-redux';

export default function Graph(): JSX.Element {

    const data = useSelector((state: { entitiesConnections: IEntitiesAndConnectionsResponse }) => {
        return state.entitiesConnections;
    });

    const [graphModel, setGraphModel] = useState<GraphModel | null>(null);

    useEffect(() => {
        console.log({data, graphModel});
        //if (graphModel) {
        //    return;
        //}

        console.log('here');
        const graph = new GraphModel("svg", data);
        graph.addSimulation();
        setGraphModel(graph);
    }, [data]);

    const width = window.innerWidth - 1;
    const height = window.innerHeight - 4;

    return <svg height={height} width={width}></svg>;
}

export {};