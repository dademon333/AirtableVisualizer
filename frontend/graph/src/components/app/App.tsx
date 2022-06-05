import { useEffect, useState } from 'react';
import './App.css';
import Graph from '../graph/graph';
import Filters from '../filters/filters';
import { useDispatch } from 'react-redux';
import { getEntitiesAndConnectionsAsync } from '../../services/entities-connections.service';
import { setConnectionsAndEntities } from '../../redux/slices/entity-connection.slice';

function App() {
  const [isLoaded, setIsLoaded] = useState(false);
  const dispatch = useDispatch();

  useEffect(() => {
    const getCourses = async () => {
      const result = await getEntitiesAndConnectionsAsync();
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
