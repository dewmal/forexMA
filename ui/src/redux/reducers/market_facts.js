import {
    ADD_MARKET_FACT_QUANTITATIVE, ADD_MARKET_FACT_QUALITATIVE } from "../actionTypes";

const initState = {
	maxHistoryLength: 5,
	qualitativeFacts: [],
	qunatitativeFacts: []
}

const MarketFacts = (state = initState, action) => {
	switch (action.type) {
		case ADD_MARKET_FACT_QUANTITATIVE: {
			if (state.qunatitativeFacts.length >= state.maxHistoryLength)
				state.qunatitativeFacts.shift()
			return {
				...state,
				qunatitativeFacts: [
					...state.qunatitativeFacts,
					...action.payload
				]
			}
		}
		case ADD_MARKET_FACT_QUALITATIVE: {
			if (state.qualitativeFacts.length >= state.maxHistoryLength)
				state.qualitativeFacts.shift()
			return {
				...state,
				qualitativeFacts: [
					...state.qualitativeFacts,
					...action.payload
				]
			}
		}
		default:
			return state
	}
}

export default MarketFacts;