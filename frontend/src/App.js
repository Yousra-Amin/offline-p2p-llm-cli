import { useEffect, useState } from "react";
import axios from "axios";

const NODES = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
];

export default function App() {
    const [task, setTask] = useState("");
    const [result, setResult] = useState([]);

    useEffect(() => {
        console.log(result)
    }, [result])

    const sendTask = async () => {
        for (let node of NODES) {
            try {
                const res = await axios.post(`${node}/task`, {
                    task: task,
                });
                setResult(res.data.result);
                return;
            } catch (err) {
                continue; // try next node
            }
        }
    };

    return (
        <div style={{ padding: 20 }}>
            <h1>P2P Task System</h1>

            <input
                value={task}
                onChange={(e) => setTask(e.target.value)}
                placeholder="Enter task"
            />

            <button onClick={sendTask}>Send</button>

            <h3>Result:</h3>
            <p>{result.map(r => r + "\n\n")}</p>
        </div>
    );
}
