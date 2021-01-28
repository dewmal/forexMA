import io from "socket.io-client";

const connectSocket = async(store) => {
    const socket = io("ws://127.0.0.1:7878", {
        transports: ["websocket", "polling"],
        jsonp: true,
        forceNew: true,
    });
    socket.on("connect", function() {
        console.log("Working")
    })
    socket.on("connect_error", err => {
        console.log(err instanceof Error); // true
        console.log(err.message); // not authorized
        console.log(err.data); // { content: "Please retry later" }
    });
    console.log(socket);
    socket.on('DecisionAgent', (message) => {
        console.log(message)
    });
}

export const startSocketIO = (store) => {
    connectSocket(store).then(() => console.log("Done"))
}