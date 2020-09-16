import React, { Component } from 'react';
import {Bar} from 'react-chartjs-2';

const styles = {
    graphContainer: {
      border: '1px solid black',
      padding: '1px'
    }
}


class VbarChart extends Component{
    constructor(props){
        super(props);

        this.state = {
            chartData : {
                labels: ['Expressway', 'Suburban', 'City', 'Urban', 'Traffic'],
                datasets:[
                    {
                        label: 'Percentage',
                        data: [],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(255, 206, 86, 0.7)',
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(153, 102, 255, 0.7)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)'
                        ]
                    }
                ]
            }
        }
    }


    componentDidUpdate(prevProps, prevState) {
        if(prevProps.data.loading !== this.props.data.loading) {
            //console.log(this.props.data.context)
            let newstate = this.state;
            newstate['chartData']['datasets'][0]['data'] = this.props.data.context
            this.setState({
                state : newstate
            })
        }
    }
    

    render() {
        return(
            <div>
                <Bar 
                    data = {this.state.chartData}
                    //height = {100}
                    options= {{
                        maintainAspectRatio: true,
                        title:{
                            display: true,
                            text: 'Percentage of the trip per context',
                            fontSize: 25
                        },
                        legend:{
                            display: false,
                            position: "right",
                            labels:{
                                fontColor: '#000'
                            }
                        },
                        layout:{
                            padding:{
                                left:50,
                                right:0,
                                bottom:0,
                                top:0
                            }
                        },
                        tooltips:{
                            enabled:true
                        }
                    }}
                />
            </div>
        )
    }
}

export default VbarChart;