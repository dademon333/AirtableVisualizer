import React, { Component } from "react";
import { getCourses } from '../services/services';
import Spinner from '../components/Spinner/Spinner';

const withData = (View, getData) => {
    return class extends Component {
        state = {
            data: null,
            error: false
        }
        
        componentDidMount() {
            /* fetch('http://37.77.106.103/api/types_connections/list')
                .then(res => res.json())
                .then(res => console.log(res)); */
            getCourses()
                .then(data => {
                    this.setState({
                        data
                    });
                    console.log(data);
                }, error =>  this.setState({ error: true }))
                .catch(error => this.setState({ error: true }));
        }
        
        render() {
            const {data, error} = this.state;
            
            if (error) {
                return <div className="error">Что-то пошло не так</div>;
            }

            if (!data) {
                return <Spinner />
            }

            return (
                <View data={data} />        
            );
        }
    }
}

export default withData;