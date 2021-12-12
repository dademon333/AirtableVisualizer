import React, {Component} from "react"
import DataJSON from '../../ALL Courses.json'

class Knowledges extends Component {
    state = {
        knowledges: DataJSON.knowledges,
        themeId: window.location.pathname.split('/')[3]
    }

    renderKnowledges = () => {
        return(
            this.state.knowledges
            .filter(knowledge => knowledge.themes.includes(this.state.themeId))
            .map((knowledge, index) => {
                return <li key={index}>{knowledge.name}</li>
            })
        )
    }
    
    render() {
        const knowledges = this.renderKnowledges(); 
        return (
            <React.Fragment>
                <h1>Знания</h1>
                { knowledges.length === 0
                ? <h1>Знаний здесь пока нет</h1>
                : <ul>{ knowledges }</ul>
                }
            </React.Fragment>
            
        )
    }
}

export default Knowledges
