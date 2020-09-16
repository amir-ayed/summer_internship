import React, {Component} from 'react';
import {Line} from 'react-chartjs-2';

const options = {
    scaleShowGridLines: true,
    scaleGridLineColor: 'rgba(153, 102, 255, 0.8)',
    scaleGridLineWidth: 1,
    scaleShowHorizontalLines: true,
    scaleShowVerticalLines: true,
    bezierCurve: true,
    bezierCurveTension: 0.4,
    pointDot: true,
    pointDotRadius: 4,
    pointDotStrokeWidth: 1,
    pointHitDetectionRadius: 20,
    datasetStroke: true,
    datasetStrokeWidth: 2,
    datasetFill: true,
    //legendTemplate: '<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>',
}

const styles = {
    graphContainer: {
      border: '1px solid black',
      padding: '1px'
    }
}

class LineChart extends Component {
    constructor(props) {
        super(props);

        this.state = {
            labels: [],
            datasets: [
                {
                    label: 'Speed in km/h',
                    data: [],
                    borderColor: ['rgba(141, 78, 87, 0.5)'],
                    backgroundColor: ['rgba(141, 78, 87, 0.4)'],
                    pointBackgroundColor : 'rgba(141, 78, 87, 0.1)',
                    pointBorderColor: 'rgba(141, 78, 87, 0.1)'
                }
            ]
        }
    }

    componentDidUpdate (prevProps, prevState) {
        if(prevProps.data.loading !== this.props.data.loading) {
            let newState = this.state;
            newState['labels'] = this.props.data.dataset.time
            newState['datasets'][0]['data'] = this.props.data.dataset.speed
            this.setState ({
                state : newState
            })
        }
    }

    render() {
        return(
            <div >
                <Line data={this.state}
                //options={options}
                />
            </div>
        );
    }
}

export default LineChart;