import React, {Component} from "react"
import { NavLink } from "react-router-dom"
import Loader from "../../Loader/Loader"
import './Course.css'
import Back from "../../Back/Back"

class Course extends Component {
    state = {
        id: window.location.pathname.split('/')[2],
        courses: [],
        themes: [],
        knowledges: [],
        loading: true,
        error: []
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
    
    renderKnowledges = (id) => {
        const knowledges = this.getKnowledges(id)
        return (
            <fieldset className="knowledgesInTheme">
                <legend>Знания</legend>
                { knowledges.length === 0
                ? <p>Пусто</p> 
                : <ol>{ knowledges }</ol>
                }
            </fieldset>
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
                            { <h3>{theme.name}</h3> }
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
            this.state.loading
            ? <Loader /> :
            <div className='course'>
                <NavLink to='/'><Back /></NavLink>
                <h1>{currentCourse.name}</h1>
                <ul className="themes">
                    { this.renderThemes() }
                </ul>
            </div>
        )
    }
}

export default Course