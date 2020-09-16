import React, {Component} from 'react'
import DoughnutChart from './DoughnutChart'

class TimeSpent extends Component {
    state = {
        loading : true,
        runTime : 0.0,
        stopTime : 0.0
    }

    componentDidMount() {
        const url = "http://127.0.0.1:5000/time";
        fetch(url)
        .then( (res) => res.json() )
        .then( (data) => this.setState({
            loading : false, runTime : data[0], stopTime : data[1]
        }))
    }

    render() {
        return(
            <div>
                {this.state.loading ? <div>loading...</div> : <div>Api responded</div>}
                <DoughnutChart data = {this.state}/>
            </div>
        )
    }
}

export default TimeSpent;