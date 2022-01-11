import React, { Component } from "react"
import { NavLink } from "react-router-dom"
import './KnowledgesAndThemes.css'
import Loader from "../../../Loader/Loader"
import Back from '../../../Back/Back'
import '../../Knowledges/Knowledges.css'

class AllKnowledges extends Component {
    state = {
        courses: [],
        knowledges: [],
        themes: [],
        quantums: [],
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
                        knowledges: res.knowledges,
                        themes: res.themes,
                        quantums: res.quantums,
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
    
    getKnowledges = () => {
        return (
            this.state.knowledges.map((knowledge, index) => {
                const quantumID = knowledge.quantums[0]
                const quantum = this.state.quantums.filter(quantum => quantum.id === quantumID)[0]
                const themesID = knowledge.themes
                const themes = themesID.map(id => this.state.themes.filter(theme => theme.id === id))
                const themesName = themes.map(theme => theme[0].name)
                const coursesID = themes.map(theme => theme[0].courses[0])
                return (
                    <li key={index}>
                        <React.Fragment>
                            <div className="wrapper">
                                <div className="name">{knowledge.name}</div>
                                <div className="quantum">
                                    {quantum == undefined ? null : 
                                    <React.Fragment>
                                        <p className="type">Тип</p>
                                        {quantum.name}
                                    </React.Fragment>}
                                </div>
                            </div>
                            {themesName.length === 0 ? null
                            : themesName.length === 1 ?
                            <fieldset className="themesName">
                                <legend>Тема</legend>
                                <NavLink to={coursesID.length === 0 ? null 
                                : '/course/' + coursesID[0] + '/' + themesID[0]}>
                                    {themesName}
                                    <i>➜</i>
                                </NavLink>
                            </fieldset>
                            : <fieldset className="themesName">
                                <legend>Темы</legend>
                                {themesName.map((name, index) => 
                                    <NavLink key={index} to={coursesID.length === 0 ? null 
                                    : '/course/' + coursesID[index] + '/' + themesID[index]}>
                                        {name}
                                        <i>➜</i>
                                    </NavLink>
                                )}
                                </fieldset>}
                        </React.Fragment>
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
                <h1>Все знания</h1>
                <ul className="allKnowledges">
                    { this.getKnowledges() }
                </ul>
            </React.Fragment>
        )
    }
}

export default AllKnowledges
