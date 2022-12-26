import { useEffect, useState } from 'react';
import './App.css';
import NetworkGraph from '../NetworkGraph/NetworkGraph';
import Filters from '../filters/filters';
import { useDispatch } from 'react-redux';
import { getEntitiesAndConnectionsAsync } from '../../services/entities-connections.service';
import { setConnectionsAndEntities, setEntities } from '../../redux/slices/entity-connection.slice';
// import data from '../../mocks/data.json';
import newMock from '../../mocks/newMock.json'
import { getAllEntities } from '../../requests/entitiesRequest';
import { getAllConnections } from '../../requests/connectionsRequest';
import EntityType from '../../enums/entity-type.enum';

function App() {
  
  const [isLoaded, setIsLoaded] = useState(false);
  const dispatch = useDispatch();

  const getData = () => {
    let newEntities = []
    for (let item in EntityType)
    {
      if (Object.keys(newMock).includes(EntityType[item])) {
        newEntities.push(...newMock[EntityType[item]])
        // console.log(EntityType[item])
        // console.log(Object.keys(newMock))
      }

    }
    return ({entities: newEntities, connections: newMock.connections.entity_connections})
  }



  useEffect(() => {
    const getCourses = async () => {
      const result = getData()

      // getAllEntities(console.log)
      // getAllConnections()

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
        <NetworkGraph data={getData()}/>
        </div>
        </div>
      </div>
  );
}

export default App;
