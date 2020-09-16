import React , {Component} from 'react';
import {Pie} from 'react-chartjs-2';

const styles = {
    graphContainer: {
      border: '1px solid black',
      padding: '1px'
    }
}


class DoughnutChart extends Component {
    constructor(props) {
        super(props);

        this.state = {
            chartData : {
                labels: ['Stop Time', 'Run Time'],
                datasets: [
                    {
                        label: 'testing',
                        data: [],
                        backgroundColor: [
                            'rgba(215, 89, 102, 0.8)',
                            'rgba(65, 255, 116, 0.8)',
                        ],
                        borderColor: [
                            'rgba(215, 89, 102, 1)',
                            'rgba(65, 255, 116, 1)',
                        ]
                    }
                ]
            }
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if(prevProps.data.loading !== this.props.data.loading) {
            let newState = this.state;
            newState['chartData']['datasets'][0]['data'] = [this.props.data.stopTime, this.props.data.runTime]
            this.setState ({
                state : newState
            })
            console.log(this.state.chartData.datasets)
        }
    }

    render() {
        return(
            <div >
                <Pie 
                    data={this.state.chartData} 
                    options={{
                        cutoutPercentage: 50,
                        animateRotate: true,
                        title: {
                            text: 'testing',
                            fontSize: 20
                        }
                    }}
                />
            </div>
        )
    }
}

export default DoughnutChart;