import React from 'react';
import {Pie} from 'react-chartjs-2';

class Example extends React.Component {
    constructor() {
        super();
        this.state = {
            chartData : {
                labels: ['Stop Time', 'Run Time'],
                datasets: [
                    {
                        label: 'testing',
                        data: [45, 300],
                        backgroundColor: [
                            'rgba(215, 89, 102, 0.6)',
                            'rgba(65, 255, 116, 0.6)'
                        ],
                        borderColor: [
                            'rgba(215, 89, 102, 0.8)',
                            'rgba(65, 255, 116, 0.8)'
                        ]
                    }
                ]
            }
        }
    }

    render() {
       return (
            <div>
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

export default Example;