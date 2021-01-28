import {ADD_DEPTH_STATE} from "../actionTypes";

const initState = {
    symbol: "",
    allDepths: ["A", "B"]
}

const OrderDepths = (state = initState, action) => {
    console.log(":WS",action.payload, action.type)
    switch (action.type) {
        case ADD_DEPTH_STATE: {
            return {
                ...state,
                allDepths: [
                    ...state.allDepths,
                    ...action.payload
                ]
            }
        }
        default:
            return state
    }
}

export default OrderDepths;