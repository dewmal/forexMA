import React, { Component } from 'react'
import logo from './logo.svg';
import './App.css';
import { startSocketIO } from "./service/socket";
import store from './redux/store'
import ActionViewComponent from './components/action_view_component';
import MarketPriceViewCompoennt from "./components/market_status_price_view_component";
import MarketNewsViewCompoennt from "./components/market_status_news_view_component";

class App extends Component {
  componentWillMount() {
    startSocketIO(store);
  }

  render() {
    return (
      <div className="App">
        <ActionViewComponent />
        <MarketPriceViewCompoennt />
        <MarketNewsViewCompoennt />
      </div>

    );
  }
}

export default App;
