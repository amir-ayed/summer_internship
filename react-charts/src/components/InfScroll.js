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
        items: []
    };

    fetchMoreData = () => {

      };

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
            dataLength={this.state.items.length}
            next={this.fetchMoreData}
            hasMore={true}
            loader={<h4>Loading...</h4>}
            scrollableTarget="scrollableDiv"
          >
            {this.state.items.map((i, index) => (
              <div style={style} key={index}>
                div - #{index}
              </div>
            ))}
          </InfiniteScroll>
        </div>
      </div>
    );
  }
}

export default InfScroll;