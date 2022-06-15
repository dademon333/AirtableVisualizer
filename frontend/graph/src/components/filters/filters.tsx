import Components from './children/components/components';
import Nodes from './children/nodes/nodes';
import ShortestPath from './children/shortest-path/shortest-path';
import './style.css';

export default function Filters() {
    return (<div className="filters">
        <Components />
        <Nodes />
        
    </div>)
}

//<ShortestPath />