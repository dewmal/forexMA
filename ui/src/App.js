import React, { Component } from 'react'
import logo from './logo.svg';
import './App.css';
import { startSocketIO } from "./service/socket";
import store from './redux/store'
import ActionViewComponent from './components/action_view_component';

class App extends Component {
  componentWillMount() {
    startSocketIO(store);
  }

  render() {
    return (
      <div className="App">
        <ActionViewComponent />
      </div>

    );
  }
}

export default App;
