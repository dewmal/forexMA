import { combineReducers } from "redux";
import MarketActions from "./market_action";
import MarketStatus from "./market_status";

export default combineReducers({ marketAction: MarketActions, marketStatus: MarketStatus })