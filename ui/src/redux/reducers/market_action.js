import { ADD_MARKET_ACTION } from "../actionTypes";

const initState = {
    pastActions: 5,
    allActions: []
}

const MarketActions = (state = initState, action) => {
    switch (action.type) {
        case ADD_MARKET_ACTION: {
            if (state.allActions.length >= state.pastActions)
                state.allActions.shift()
            return {
                ...state,
                allActions: [
                    ...state.allActions,
                    ...action.payload
                ]
            }
        }
        default:
            return state
    }
}

export default MarketActions;