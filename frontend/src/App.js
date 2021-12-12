import './App.css'
import React, {Component} from 'react'
import Main from './Components/Main/Main'
import DataJSON from './ALL Courses.json'
import { Route, Routes } from 'react-router'
import Course from './Components/Course/Course'
import './App.css'
import Knowledges from './Components/Knowledges/Knowledges'
class App extends Component {

  render () {
    return (
      <div className='app'>
        <Routes>
          <Route path='/course/:id/:id' element={<Knowledges />} />
          <Route path='/course/:id' element={<Course />} />
          <Route path='/' element={<Main data={DataJSON.courses}/>} />
        </Routes>
        

        
      </div>
    )
  }
}

export default App
