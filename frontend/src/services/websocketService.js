class WebSocketService {

    constructor() {

        this.socket = null;

        this.listeners = [];

    }

    connect() {

        if (
            this.socket &&
            this.socket.readyState === WebSocket.OPEN
        ) {
            return;
        }

        this.socket = new WebSocket(
            "ws://127.0.0.1:8000/ws/alerts"
        );

        this.socket.onopen = () => {

            console.log(
                "WebSocket Connected"
            );

        };

        this.socket.onmessage = (event) => {

            const data = JSON.parse(
                event.data
            );

            this.listeners.forEach(
                callback => callback(data)
            );

        };

        this.socket.onclose = () => {

            console.log(
                "WebSocket Closed"
            );

        };

        this.socket.onerror = (error) => {

            console.error(
                error
            );

        };

    }

    disconnect() {

        if (this.socket) {

            this.socket.close();

        }

    }

    subscribe(callback) {

        this.listeners.push(
            callback
        );

    }

}

export default new WebSocketService();