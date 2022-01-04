import React, {Component} from "react"
import { NavLink } from "react-router-dom"
import Back from "../../Back/Back"
import './Knowledges.css'

class Knowledges extends Component {
    state = {
        themes: this.props.themes,
        knowledges: this.props.knowledges,
        quantums: this.props.quantums,
        themeID: window.location.pathname.split('/')[3],
        courseID: window.location.pathname.split('/')[2]
    }

    renderKnowledges = () => {
        return(
            this.state.knowledges
            .filter(knowledge => knowledge.themes.includes(this.state.themeID))
            .map((knowledge, index) => {
                const quantumID = knowledge.quantums[0]
                const quantum = this.state.quantums.filter(quantum => quantum.id === quantumID)[0]
                return (
                    <li key={index} className="knowledge">
                        <div className="name">{knowledge.name}</div>
                        <div className="quantum">
                            <p className="type">Тип</p>
                            {quantum.name}
                        </div>
                    </li>
                )
            })
        )
    }
    
    render() {
        const themeName = this.state.themes.filter(theme => theme.id == this.state.themeID)[0].name
        const knowledges = this.renderKnowledges(); 
        return (
            <React.Fragment>
                <NavLink to={'/course/' + this.state.courseID}><Back /></NavLink>
                <h1 className="themeName">{themeName}</h1>
                { knowledges.length === 0
                ? <h1 className="empty">Знаний здесь пока нет</h1>
                : <ul className="knowledges">{ knowledges }</ul>
                }
            </React.Fragment>
            
        )
    }
}

export default Knowledges
