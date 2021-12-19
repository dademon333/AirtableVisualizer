import React, {Component} from "react"
import { NavLink } from "react-router-dom"
import './Course.css'

class Course extends Component {
    state = {
        id: window.location.pathname.split('/')[2],
        courses: this.props.courses,
        themes: this.props.themes,
        knowledges: this.props.knowledges
    }
    
    renderKnowledges = (id) => {
        const knowledges = this.getKnowledges(id)
        return (
            <div className="knowledgesInTheme">
                <h4>Знания:</h4>
                
                    { knowledges.length === 0
                    ? <p>Пусто</p> 
                    : <ol>{ knowledges }</ol>
                    }
            </div>
        )
    }

    getKnowledges = (id) => {
        return (
            this.state.knowledges
            .filter(knowledge => knowledge.themes.includes(id))
            .map((knowledge, index) => {
                return (
                    <li key={index}>{knowledge.name}</li>
              )
            })
        )
    }

    renderThemes = () => {
        return (
            this.state.themes
            .filter(theme => theme.courses.includes(this.state.id))
            .map((theme, index) => {
                return (
                    <li key={index} className="theme">
                        <NavLink to={'/course/' + this.state.id + '/' + theme.id}>
                            { <h4 className="title">{theme.name}</h4> }
                            { this.renderKnowledges(theme.id) }
                        </NavLink>
                    </li>
                )
            })
        )
    }

    render() {
        const currentCourse = this.state.courses.filter(course => course.id === this.state.id)[0]
        return (
            <div className='course'>
                <h1>{currentCourse.name}</h1>
                <ul className="themes">
                    { this.renderThemes() }
                </ul>
                <NavLink to='/'>На главную</NavLink>
            </div>
        )
    }
}

export default Course