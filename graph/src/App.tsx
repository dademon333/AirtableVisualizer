import { useEffect, useState } from 'react';
import './App.css';
import Graph from './libs/components/graph/graph';
import { getEntitiesAndConnectionsAsync } from './libs/services/entities-connections.service';
import IEntitiesAndConnectionsResponse from './libs/interfaces/response/entities-connections-response.interface';
import data from './data.json';
import Filters from './libs/components/filters/filters';
import { Provider } from 'react-redux';
import store from './libs/redux/store';

function App() {
  const [entitiesConnections, setEntitiesConnections] = useState<IEntitiesAndConnectionsResponse | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  
  useEffect(() => {
    const getCourses = async () => {
      const result = data as any;//await getEntitiesAndConnectionsAsync();
      console.log(result);
      setEntitiesConnections(result);
      setIsLoaded(true);
    };

    getCourses();
  }, []);

  return (
    <Provider store={store}>
      <div className="App">
        {isLoaded && <Filters />}
        {entitiesConnections && <Graph {...entitiesConnections}/> }
      </div>
    </Provider>
  );
}

export default App;
