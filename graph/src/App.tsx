import { useEffect, useState } from 'react';
import './App.css';
import Graph from './graph';
import { getEntitiesAndConnectionsAsync } from './libs/services/entities-connections.service';
import IEntitiesAndConnectionsResponse from './libs/interfaces/response/entities-connections-response.interface';

function App() {
  const [entitiesConnections, setEntitiesConnections] = useState<IEntitiesAndConnectionsResponse | null>(null);
  
  useEffect(() => {
    const getCourses = async () => {
      const result = await getEntitiesAndConnectionsAsync();
      console.log(result);
      setEntitiesConnections(result);
    };

    getCourses();
  }, []);

  return (
    <div className="App">
      {entitiesConnections && <Graph {...entitiesConnections}/> }
    </div>
  );
}

export default App;
