import { useEffect, useState, useRef } from 'react';

const WS_URL = "ws://127.0.0.1:8000/ws";

export const useWebSocket = (token: string | null, onUpdate: (data: any) => void) => {
    const ws = useRef<WebSocket | null>(null);
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        if (!token) return;

        const connect = () => {
            // Connect with token in query param (mock secure handshake)
            ws.current = new WebSocket(`${WS_URL}?token=${token}`);

            ws.current.onopen = () => {
                console.log("WS Connected");
                setIsConnected(true);
            };

            ws.current.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    if (message.type === "UPDATE") {
                        onUpdate(message.data);
                    }
                } catch (e) {
                    console.error("WS Parse Error", e);
                }
            };

            ws.current.onclose = () => {
                console.log("WS Disconnected");
                setIsConnected(false);
                // Reconnect logic could go here
            };
        };

        connect();

        return () => {
            ws.current?.close();
        };
    }, [token]);

    return { isConnected };
};
