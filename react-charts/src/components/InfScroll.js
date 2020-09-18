import React from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import './scrollbar.css';
import axios from 'axios';

const style = {
  height: 30,
  border: "1px solid green",
  margin: 6,
  padding: 8
};

class InfScroll extends React.Component {
    state = {
      trips: [],
      hasMore: true
    };

    componentWillMount() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:5000/trips',
        params: {number: 0}
      }).then(
        (res) => res.data
      ).then(
        (data) => this.setState({
          trips: data
        })
      )
    }

    fetchMoreData = () => {
        axios({
          method: 'get',
          url: 'http://127.0.0.1:5000/trips',
          params: {number: this.state.trips.length}
        })
        .then(
          (res) => res.data
        )
        .then(
          (data) => this.setState({
            ...this.state, trips: data
          })
        )
        .catch( 
          (err) => console.log(err)
        )
      };

      
    componentDidUpdate() {
      console.log(this.state)
    }

    componentDidMount() {
      console.log(this.state)
    }

  render() {
    const myScrollbar = {
      width: 400,
      height: 400,
    };

    return (
      <div>
        <hr />
        <div id="scrollableDiv" style={{ height: 300, overflow: "auto" }}>
          <InfiniteScroll
            dataLength={this.state.trips.length}
            next={this.fetchMoreData}
            hasMore={this.state.hasMore}
            loader={<h4>Loading...</h4>}
            scrollableTarget="scrollableDiv"
          >
            {this.state.trips.map((i, index) => (
              <div style={style} key={index}>
                {i.name}
              </div>
            ))}
          </InfiniteScroll>
        </div>
      </div>
    );
  }
}

export default InfScroll;