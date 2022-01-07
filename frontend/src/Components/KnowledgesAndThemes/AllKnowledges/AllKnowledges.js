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
        error: [],
        duplicates: []
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

    /* updateDuplicate = (knowledge) => {
        const count = this.state.knowledges.reduce((total, e) => (
            e.name == knowledge.name ? total + 1 : total
        ), 0)
        const dup = this.state.duplicates
        if (count > 1) {
            dup.push(knowledge)
        }
    } */
    
    getKnowledges = () => {
        return (
            this.state.knowledges.map((knowledge, index) => {
                const quantumID = knowledge.quantums[0]
                const quantum = this.state.quantums.filter(quantum => quantum.id === quantumID)[0]
                console.log(quantum)
                return (
                    <li key={index}>
                        <NavLink to='/'>
                            <div className="name">{knowledge.name}</div>
                            <div className="quantum">
                                {quantum == undefined ? null : 
                                <React.Fragment>
                                    <p className="type">Тип</p>
                                    {quantum.name}
                                </React.Fragment>}
                            </div>
                        </NavLink>
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
