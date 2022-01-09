import React, {Component} from "react"
import { NavLink } from "react-router-dom"
import Loader from "../../../Loader/Loader"
import './KnowledgesAndThemes.css'
import Back from "../../../Back/Back"

class AllThemes extends Component {
    state = {
        courses: [],
        themes: [],
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

    getThemes = () => {
        return (
            this.state.themes.map((theme, index) => {
                const coursesID = theme.courses
                const courses = coursesID.map(id => this.state.courses.filter(course => course.id === id)[0])
                const id = courses.map(course => course.id)
                const names = courses.map(course => course.name)
                return (
                    <li key={index}>
                        <h3>{theme.name}</h3>
                        <div className="themesName">
                            {id.length === 0 ? null 
                            : id.length === 1
                            ? <fieldset>
                                <legend>Тема</legend>
                                <NavLink to={'/course/' + id} className="course">{names[0]}<i>➜</i></NavLink>
                              </fieldset>
                            : <fieldset>
                                <legend>Темы</legend>
                                {id.map((i, index) => 
                                <NavLink to={'/course/' + i} key={index} className="course">
                                    {names[index]}
                                    <i>➜</i>
                                </NavLink>)}
                              </fieldset>
                            }
                        </div>
                    </li>
                )
            })
        )
    }

    render() {
        return (
            this.state.loading
            ? <Loader /> :
            <React.Fragment>
                <NavLink to='/'><Back /></NavLink>
                <h1>Все Темы</h1>
                <ul className="allThemes">
                    { this.getThemes() }
                </ul>
            </React.Fragment>
        )
    }
}

export default AllThemes
