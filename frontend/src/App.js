import './App.css'
import React, {Component} from 'react'
import Main from './Components/Main/Main'
import { Route, Routes } from 'react-router'
import Course from './Components/Course/Course'
import './App.css'
import Knowledges from './Components/Knowledges/Knowledges'
import Loader from './Loader/Loader'

class App extends Component {
  state = {
    courses: [],
    themes: [],
    knowledges: [],
    quantums: [],
    competences: [],
    error: null,
    loading: true
  }

  componentDidMount() {
    fetch('http://164.92.253.119/course/all')
      .then(res => res.json())
      .then(
        (res) => {
          this.setState({
            courses: res.courses,
            themes: res.themes,
            knowledges: res.knowledges,
            quantums: res.quantums,
            competences: res.competences,
            loading: false
          })
        },
        (error) => {
          this.setState({
            error
          })
        }
      )
  }

  render () {
    return (
      <div className='app'>
        <Routes>
          <Route path='/course/:id/:id' element={
            <Knowledges
              themes={this.state.themes}
              knowledges={this.state.knowledges}
              quantums={this.state.quantums}
            />} 
          />
          <Route path='/course/:id' element={
            <Course
              courses={this.state.courses}
              themes={this.state.themes}
              knowledges={this.state.knowledges}
            />} 
          />
          <Route path='/' element={
            this.state.loading 
            ? <Loader />
            :<Main 
              courses={this.state.courses}
            />}
          />
        </Routes>
        
      </div>
    )
  }
}

export default App
