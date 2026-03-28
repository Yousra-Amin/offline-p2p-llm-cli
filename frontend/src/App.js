import React, { useState } from "react";

function App() {
	const [input, setInput] = useState("");
	const [logs, setLogs] = useState([]);

	const runTask = async () => {
		if (!input) return;

		setLogs((prev) => [...prev, `> ${input}`]);

		// const res = await fetch("http://127.0.0.1:8000/run", {
		// 	method: "POST",
		// 	headers: {
		// 		"Content-Type": "application/json",
		// 	},
		// 	body: JSON.stringify({ task: input }),
		// });

		// const data = await res.json();


		const data = { // mock backend
			"steps": [
				{
					"step": "step 1",
					"result": "result 1",
					"review": "review 1"
				},
				{
					"step": "step 2",
					"result": "result 2",
					"review": "review 2"
				},
				{
					"step": "step 3",
					"result": "result 3",
					"review": "review 3"
				},
				{
					"step": "step 4",
					"result": "result 4",
					"review": "review 4"
				},
				{
					"step": "step 5",
					"result": "result 5",
					"review": "review 5"
				},
			]
		}

		data.steps.forEach((s, i) => {
			setLogs((prev) => [
				...prev,
				`Step ${i + 1}: ${s.step}`,
				`Result: ${s.result}`,
				`Review: ${s.review}`,
			]);
		});

		setInput("");
	};

	return (
		<div style={{ color: "black", padding: "20px" }}>
			<h2>Agentic CLI</h2>

			<div style={{ marginBottom: "20px" }}>
				{logs.map((log, i) => (
					<div key={i}>{log}</div>
				))}
			</div>

			<input
				style={{
					width: "80%",
					padding: "10px",
					color: "black",
					border: "1px solid black",
				}}
				value={input}
				onChange={(e) => setInput(e.target.value)}
				onKeyDown={(e) => e.key === "Enter" && runTask()}
				placeholder="Enter task..."
			/>
		</div>
	);
}

export default App;