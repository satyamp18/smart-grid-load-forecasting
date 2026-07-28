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

        const apiUrl = import.meta.env.VITE_API_URL || (window.location.protocol === "https:" ? `https://${window.location.host}/api/v1` : `http://${window.location.host}/api/v1`);
        const WS_URL = apiUrl
          .replace(/\/api\/v1\/?$/, "")
          .replace(/^https:\/\//, "wss://")
          .replace(/^http:\/\//, "ws://");

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