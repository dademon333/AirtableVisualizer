import React from "react"
import { NavLink } from 'react-router-dom'
import './Main.css'

const Main = props => {
    return (
        <React.Fragment>
            <h1>Все курсы</h1>
            <ul className='courses'>
                {props.data.map(course => {
                    return (
                        <li key={course.id}>
                            <NavLink to={'/course/' + course.id}>
                                {course.name}
                            </NavLink>
                        </li>
                    )
                })}
            </ul>
            
      </React.Fragment>
    )    
}

export default Main