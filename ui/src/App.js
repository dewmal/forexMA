import React, { Component } from 'react'
import logo from './logo.svg';
import './App.css';
import { startSocketIO } from "./service/socket";
import store from './redux/store'
import ActionViewComponent from './components/action_view_component';
import MarketPriceViewCompoennt from "./components/market_status_price_view_component";
import MarketNewsViewCompoennt from "./components/market_status_news_view_component";
import MarketQualitativeFactViewCompoennt from "./components/market_qualitative_facts_view_component";
import MarketQuantitativeFactViewCompoennt from "./components/market_quantitative_facts_view_component";
import MarketFastMoverViewComponent from "./components/market_fast_movers_view_component";

import MarketTrendViewComponent from "./components/market_trend_view_component"

class App extends Component {
  componentWillMount() {
    startSocketIO(store);
  }

  render() {
    return (
      <div className="lg h-full w-full bg-gray-900 text-gray-300 font-mono">
        <div className="grid grid-cols-3">


          <div>
            <MarketTrendViewComponent/>
          </div>

          <div className="col-span-2 gap-4">
           <MarketFastMoverViewComponent/>
          </div>
          <div>
            <ActionViewComponent />
          </div>

          <div>
            <MarketQuantitativeFactViewCompoennt />
          </div>
          <div>
            <MarketQualitativeFactViewCompoennt />
          </div>

          <div>
            <MarketQualitativeFactViewCompoennt />
          </div>

          <div className="col-span-3">
            <MarketNewsViewCompoennt />
          </div>




        </div>


      </div>

    );
  }
}

export default App;
