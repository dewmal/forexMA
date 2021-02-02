import { ADD_MARKET_STATE_PRICE, ADD_MARKET_STATE_TEXT } from "../actionTypes";

const initState = {
	asset: '1INCHUSDT',
	maxHistoryLength: 50,
	prices: [],
	texts: []
}

const MarketStatus = (state = initState, action) => {
	switch (action.type) {
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