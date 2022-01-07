import React, { Component } from "react"
import { NavLink } from 'react-router-dom'
import BackDrop from "../../BackDrop/BackDrop"
import './Main.css'

class Main extends Component {
    state = {
        isBackDropOpen: false
    }

    onOpen = () => {
        this.setState({
            isBackDropOpen: !this.state.isBackDropOpen
        })
    }

    onBackDrop = () => {
        this.setState({
            isBackDropOpen: false
        })
    }

    render() {
        const classes = []

        if (!this.state.isBackDropOpen) {
            classes.push('closed')
        } else {
            classes.push('opened')
        }

        return (
            <React.Fragment>
                <h1>Все курсы</h1>
                <ul className="courses">
                    {this.props.courses.map(course => {
                        return (
                            <li key={course.id}>
                                <NavLink to={'/course/' + course.id}>
                                    {course.name}
                                </NavLink>
                            </li>
                        )
                    })}
                </ul>
                <div className={'pages ' + classes.join(' ')} onClick={this.onOpen}>⮝</div>
                <ul className={'themesAndKnowledges ' + classes.join(' ')}>
                    <li><NavLink to='/themes'>Все темы</NavLink></li>
                    <li><NavLink to='/knowledges'>Все знания</NavLink></li>
                </ul>
                { this.state.isBackDropOpen
                ? <BackDrop onClick={this.onBackDrop} />
                : null }
        </React.Fragment>
        )    
    }
}

export default Main