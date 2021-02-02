import io from "socket.io-client";
import { ADD_MARKET_ACTION, 
    ADD_MARKET_STATE_PRICE, 
    ADD_MARKET_STATE_TEXT, 
    ADD_MARKET_FACT_QUANTITATIVE, ADD_MARKET_FACT_QUALITATIVE,ADD_PREDICTION_PERFORMANCE } from "../redux/actionTypes";

const connectSocket = async (store) => {
    const socket = io("ws://127.0.0.1:7878", {
        transports: ["websocket", "polling"],
        jsonp: true,
        forceNew: true,
    });
    socket.on("connect", function () {
        console.log("Working")
    })
    socket.on("connect_error", err => {
        console.log(err instanceof Error); // true
        console.log(err.message); // not authorized
        console.log(err.data); // { content: "Please retry later" }
    });
    socket.on('DecisionAgent', (message) => {
        console.log(message);
        store.dispatch({
            type: ADD_MARKET_ACTION,
            payload: [message.body.message]
        })
    });


    socket.on('CryptoReadingAgent', (message) => {
        store.dispatch({
            type: ADD_MARKET_STATE_PRICE,
            payload: [message.body.message]
        })
    });


    socket.on('NewsReadingAgent', (message) => {
        store.dispatch({
            type: ADD_MARKET_STATE_TEXT,
            payload: [message.body.message]
        })
    });



    socket.on('QuantitativeFAAgent', (message) => {
        store.dispatch({
            type: ADD_MARKET_FACT_QUANTITATIVE,
            payload: [message.body.message]
        })
    });



    socket.on('QualitativeFAAgent', (message) => {
        store.dispatch({
            type: ADD_MARKET_FACT_QUALITATIVE,
            payload: [message.body.message]
        })
    });

    

    socket.on('PerformanceAnalysingAgent', (message) => {
        store.dispatch({
            type: ADD_PREDICTION_PERFORMANCE,
            payload: [message.body.message]
        })
    });

}

export const startSocketIO = (store) => {
    connectSocket(store).then(() => console.log("Done"))
}