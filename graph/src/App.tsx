import { useEffect, useState } from 'react';
import './App.css';
import { getCourseListAsync } from './libs/services/courses.service';
import Graph from './graph';
import { getEntitiesAndConnectionsAsync } from './libs/services/entities-connections.service';

function App() {
  const [courses, setCourses] = useState([]);
  
  useEffect(() => {
    const getCourses = async () => {
    };

    getCourses();
  }, []);

  return (
    <div className="App">
      <Graph />
    </div>
  );
}

export default App;
