import io from "socket.io-client";
import {
    ADD_MARKET_STATE_PRICE,
    ADD_MARKET_TRENDS,
    ADD_MARKET_EQUILIBRIUM
} from "../redux/actionTypes";

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
    socket.on('CryptoReadingAgent', (message) => {
        store.dispatch({
            type: ADD_MARKET_STATE_PRICE,
            payload: [message.body.message]
        })
    });

    socket.on('MarketTrendAnalysingAgent', (message) => {
        store.dispatch({
            type: ADD_MARKET_TRENDS,
            payload: message.body.message
        })
    });
    socket.on('MarketEquilibriumAnalysingAgent', (message) => {
        store.dispatch({
            type: ADD_MARKET_EQUILIBRIUM,
            payload: message.body.message
        })
    });
}

export const startSocketIO = (store) => {
    connectSocket(store).then(() => console.log("Done"))
}