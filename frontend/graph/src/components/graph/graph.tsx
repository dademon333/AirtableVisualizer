import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import GraphModel from '../../models/graph/graph.model';
import { setConnectionsAndEntities } from '../../redux/slices/entity-connection.slice';
import { getEntitiesAndConnectionsAsync } from '../../services/entities-connections.service';
import NetworkGraph from '../NetworkGraph/NetworkGraph';

export default function Graph(): JSX.Element {

    const dispatch = useDispatch();

    useEffect(() => {
        const getCourses = async () => {
            const data = await getEntitiesAndConnectionsAsync();
            dispatch(setConnectionsAndEntities(data));
            const graph = new GraphModel("svg", data);
            graph.addSimulation();
        };
    
        getCourses();
    }, []);

    const width = window.innerWidth - 1;
    const height = window.innerHeight - 4;

    return <div></div>;
}

export {};