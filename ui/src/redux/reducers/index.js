import { combineReducers } from "redux";
import MarketActions from "./market_action";
import MarketStatus from "./market_status";
import MarketFacts from "./market_facts";

export default combineReducers({ marketAction: MarketActions, marketStatus: MarketStatus, makretFacts: MarketFacts })