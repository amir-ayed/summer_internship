import React, {Component} from 'react';
import LineChart from './LineChart';

class Speed extends Component {
    state = {
        loading : true,
        dataset : {
            time : [],
            speed : []
        }
    }

    async componentDidMount () {
        const url = "http://127.0.0.1:5000/speed";
        fetch(url)
        .then( (res) => res.json())
        .then( (data) => {
            this.setState( {
                loading : false, dataset : {time : data['time'], speed : data['speed']}
            })
        })
    }

    render() {
        return(
            <div>
                {this.state.loading ? <div>loading...</div> : <div>Api responded</div>}
                <LineChart data = {this.state}/>
            </div>
        );
    }
}

export default Speed;