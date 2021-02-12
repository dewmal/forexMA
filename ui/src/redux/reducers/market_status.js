import { ADD_MARKET_STATE_PRICE, ADD_MARKET_STATE_TEXT,ADD_MARKET_TRENDS,ADD_MARKET_EQUILIBRIUM } from "../actionTypes";

const initState = {
	asset: '1INCHUSDT',
	maxHistoryLength: 50,
	prices: [],
	texts: [],
	trends:[],
	equilibriums :[]
}

const MarketStatus = (state = initState, action) => {	
	switch (action.type) {	
			
		case ADD_MARKET_EQUILIBRIUM: {
			return {
				...state,
				equilibriums : [
					...action.payload
				]
			}
		}	
		case ADD_MARKET_TRENDS: {
			return {
				...state,
				trends: [
					...action.payload
				]
			}
		}
		case ADD_MARKET_STATE_PRICE: {
			if (state.prices.length >= state.maxHistoryLength)
				state.prices.shift()
			return {
				...state,
				prices: [
					...state.prices,
					...action.payload
				]
			}
		}
		case ADD_MARKET_STATE_TEXT: {
			if (state.texts.length >= state.maxHistoryLength)
				state.texts.shift()
			return {
				...state,
				texts: [
					...state.texts,
					...action.payload
				]
			}
		}
		default:
			return state
	}
}

export default MarketStatus;