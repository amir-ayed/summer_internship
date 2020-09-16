import React, { Component } from 'react';
import VbarChat from './VbarChart'

class Context extends Component {
    state = {
        loading: true,
        context: []
    };
    
    async componentDidMount() {
        const url = "http://127.0.0.1:5000/context";
        fetch(url)
        .then((res) => res.json())
        .then(data => {
            this.setState({loading : false , context : [data['Expressways'], data['Suburban'], data['City'], data['Heavy urban traffic'], data['Traffic Jam']]});
        });
    }
    
    render() {
        return (
            <div>
                {this.state.loading ? <div>loading...</div> : <div>Api responded</div>}
                <VbarChat data = {this.state}/>
            </div>
        )
    }
}

export default Context;
