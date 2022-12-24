import { useEffect, useState } from 'react';
import './App.css';
import NetworkGraph from '../NetworkGraph/NetworkGraph';
import Filters from '../filters/filters';
import { useDispatch } from 'react-redux';
import { getEntitiesAndConnectionsAsync } from '../../services/entities-connections.service';
import { setConnectionsAndEntities } from '../../redux/slices/entity-connection.slice';
import data from '../../mocks/data.json';

function App() {
  
  const [isLoaded, setIsLoaded] = useState(false);
  const dispatch = useDispatch();

  const formatData = (rawData) => {
    return{
    nodes: Object.keys(rawData.entities).map(key => ({id: rawData.entities[key].name, type: rawData.entities[key].type})),
    links: rawData.connections
    .map(connection => connection.entities_connections)
    .flat(1)
    .map(link => ({source: rawData.entities[link.parent_id].name, target: rawData.entities[link.child_id].name}))
  }}

  useEffect(() => {
    const getCourses = async () => {
      const result = data;
      dispatch(setConnectionsAndEntities(result));
      setIsLoaded(true);
    };
  
    getCourses();
  }, []);

  return (
      <div className="App">
        <div className="container">
        {isLoaded && <Filters/>}
        <div className="column">
        <NetworkGraph data={data}/>
        </div>
        </div>
      </div>
  );
}

export default App;
