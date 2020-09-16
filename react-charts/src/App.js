import React from 'react';
import logo from './logo.svg';
import './App.css';
import Header from './components/Header';
import Context from './components/Context';
import Speed from './components/Speed';
import TimeSpent from './components/TimeSpent';
import SimpleMap from './components/Map';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col} from 'react-bootstrap';
import './scrollbar.css';
import InfScroll from './components/InfinteScroll';



function App() {
  return (
  <div className = 'App'>
        <Container fluid className = 'Col'>
          <Row  fluid className = 'Col'>
            <Col>
              <Header />
            </Col>
          </Row>
          <Row >
            <Col lg={2} className = "Col">
              <div className = 'scrollhost'>
                <InfScroll/>
              </div>
            </Col>
            <Col lg={10}>
              <Container fluid>
                <Row>
                  <Col md>
                    <Context />
                  </Col>
                  <Col md>
                    <Speed />
                  </Col>
                </Row>
                <Row>
                  <Col md>
                  <TimeSpent/>
                  </Col>
                  <Col md>
                    <SimpleMap />
                  </Col>
                </Row>
              </Container>
            </Col>
          </Row>
          <Row className = 'Col'>
         <Col>
            <div className="App"> 
              <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
              </header>
            </div>
          </Col>
        </Row>
        </Container>
      </div>
  );
}

export default App;