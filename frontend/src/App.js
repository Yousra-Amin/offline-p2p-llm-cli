import { useState, useRef, useEffect } from "react";

const NODES = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
];

export default function App() {
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const fetchFromNodes = async (prompt) => {
        for (let node of NODES) {
            try {
                const res = await fetch(`${node}/task`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ task: prompt }),
                });

                if (res.status === 404) continue;
                if (!res.ok) continue;

                const data = await res.json();
                return data.result;
            } catch (err) {
                continue;
            }
        }
        throw new Error("All nodes failed");
    };

    const streamText = async (text, index) => {
        const words = text.split(" ");
        let current = "";

        for (let i = 0; i < words.length; i++) {
            current += (i === 0 ? "" : " ") + words[i];

            await new Promise((r) => setTimeout(r, 40));

            setMessages((prev) => {
                const updated = [...prev];
                updated[index].content = current;
                return updated;
            });
        }
    };

    const handleSubmit = async () => {
        if (!input.trim()) return;

        const userMessage = { role: "user", content: input };
        const botMessage = { role: "bot", content: "" };

        setMessages((prev) => [...prev, userMessage, botMessage]);
        setInput("");
        setLoading(true);

        const botIndex = messages.length + 1;

        try {
            const response = await fetchFromNodes(input);
            await streamText(response, botIndex);
        } catch (err) {
            await streamText("Error: Unable to reach any node.", botIndex);
        }

        setLoading(false);
    };

    return (
        <div style={styles.container}>
            <div style={styles.chatContainer}>
                {messages.map((msg, i) => (
                    <div
                        key={i}
                        style={{
                            ...styles.message,
                            ...(msg.role === "user" ? styles.user : styles.bot),
                        }}
                    >
                        {msg.content}
                    </div>
                ))}
                <div ref={bottomRef} />
            </div>

            <div style={styles.inputContainer}>
                <input
                    style={styles.input}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Send a message..."
                    onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
                    disabled={loading}
                />
                <button style={styles.button} onClick={handleSubmit} disabled={loading}>
                    Send
                </button>
            </div>
        </div>
    );
}

const styles = {
    container: {
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "#343541",
        color: "white",
        fontFamily: "Arial, sans-serif",
    },
    chatContainer: {
        flex: 1,
        overflowY: "auto",
        padding: "20px",
    },
    message: {
        maxWidth: "70%",
        padding: "12px 16px",
        borderRadius: "10px",
        marginBottom: "12px",
        lineHeight: "1.5",
        whiteSpace: "pre-wrap",
    },
    user: {
        backgroundColor: "#10a37f",
        alignSelf: "flex-end",
    },
    bot: {
        backgroundColor: "#444654",
        alignSelf: "flex-start",
    },
    inputContainer: {
        display: "flex",
        padding: "15px",
        borderTop: "1px solid #555",
        backgroundColor: "#40414f",
    },
    input: {
        flex: 1,
        padding: "12px",
        borderRadius: "8px",
        border: "none",
        outline: "none",
        marginRight: "10px",
        fontSize: "16px",
    },
    button: {
        padding: "12px 18px",
        borderRadius: "8px",
        border: "none",
        backgroundColor: "#10a37f",
        color: "white",
        cursor: "pointer",
        fontWeight: "bold",
    },
};