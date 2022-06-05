import { useEffect, useState } from 'react';
import './App.css';
import Graph from './libs/components/graph/graph';
import Filters from './libs/components/filters/filters';
import {useDispatch } from 'react-redux';
import { setConnectionsAndEntities } from './libs/redux/slices/entity-connection.slice';
import { getEntitiesAndConnectionsAsync } from './libs/services/entities-connections.service';

function App() {
  const [isLoaded, setIsLoaded] = useState(false);
  const dispatch = useDispatch();

  
  useEffect(() => {
    const getCourses = async () => {
      const result = await getEntitiesAndConnectionsAsync();
      //console.log(result);
      dispatch(setConnectionsAndEntities(result));
      setIsLoaded(true);
      
    };

    getCourses();
  }, []);

  return (
      <div className="App">
        {isLoaded && <Filters />}
        <Graph />
      </div>
  );
}

export default App;
