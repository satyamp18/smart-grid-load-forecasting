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

        const WS_URL =
        import.meta.env.VITE_API_URL
        .replace("/api/v1", "")
        .replace("https://", "wss://")
        .replace("http://", "ws://");

        this.socket = new WebSocket(
        `${WS_URL}/ws/alerts`
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