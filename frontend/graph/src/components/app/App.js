import { useEffect, useState } from 'react';
import './App.css';
import NetworkGraph from '../NetworkGraph/NetworkGraph';
import Filters from '../filters/filters';
import { useDispatch, useSelector } from 'react-redux';
import { getEntitiesAndConnectionsAsync } from '../../services/entities-connections.service';
import { setConnectionsAndEntities, setEntities } from '../../redux/slices/entity-connection.slice';
// import data from '../../mocks/data.json';
import newMock from '../../mocks/newMock.json'
import { getAllEntities } from '../../requests/entitiesRequest';
import { getAllConnections } from '../../requests/connectionsRequest';
import EntityType from '../../enums/entity-type.enum';
import { setVisibleEntites } from '../../redux/slices/entity-connection.slice';

function App() {
  
  const [isLoaded, setIsLoaded] = useState(false);
  const dispatch = useDispatch();

  const getData = () => {
    let newEntities = []
    for (let item in EntityType)
    {
      if (Object.keys(newMock).includes(EntityType[item])) {
        newEntities.push(...newMock[EntityType[item]])
      }
    }
    return ({entities: newEntities, connections: newMock.connections.entity_connections})
  }

  const selectFilters = useSelector(state => ({components: {types: state.filters.components.types}}))

  // const setVisibleData = (rawData) => {
  //   console.log(rawData)
  //   return {
  //     nodes: rawData.entities
  //     .filter(entity => selectFilters.components.types.length ? selectFilters.components.types.includes(entity.type) : entity)
  //     .map(entity => ({id: entity.id, name: entity.name, type: entity.type})),
  //     links: rawData.connections
  //     .filter(link => selectFilters.components.types.length ? selectFilters.components.types.includes(rawData.entities.find(entity => entity.id == link.parent_id).type) && selectFilters.components.types.includes(rawData.entities.find(entity => entity.id == link.child_id).type) : link)
  //     .map(link => ({source: link.parent_id, target: link.child_id}))
  //   }
  // }

  // useEffect(() => {
  //   dispatch(setVisibleEntites(setVisibleData(getData())))
  // }, [selectFilters])



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
