# PART X — Agentic AI

[📖 Table of contents](README.md) · [← previous part](part9_generative_ai.md) · [next part →](part11_software_engineering_mlops.md) · [Appendices](appendix.md)

> **Days 91–99 · Category: LLM agents that plan, use tools and act · Levels: 1 → 3 in every chapter**
> **You will be able to:** write an agent loop with no framework, add planning and memory, rebuild it in LangGraph, expose tools through MCP, coordinate several agents, evaluate and secure an agent, and ship the HRM payslip agent.
> **Math you meet here (just-in-time):** expected cost = steps × cost per step (Day 91) · token budget (93) · success-rate metrics (97).
> **More depth:** Advanced shelf Days 163–166 (Reflexion, Tree-of-Thoughts, code / computer-use agents, A2A, durable workflows, OWASP LLM Top-10).

---

## Chapter 46 — Agent fundamentals: tool calling, planning, memory

> ⚠️ **Common mistakes:** no `max_steps` · vague tool descriptions · unbounded context · letting the agent write to production data.

### Level 1: tool calling and the loop
<a id="day-91"></a>
#### ☐ Day 91 — Tool calling & the agent loop (no framework)
- 🧮 **New math today (just-in-time):** expected cost = steps × cost per step.
- 🧠 **Idea · L1:** an agent = an LLM in a **loop**: think → call a tool → read the result → repeat until done.
- ➗ **Equation · L1:** success rate `= tasks solved/total` · expected cost `= steps × cost per step` · `max_steps` guards against infinite loops
- ⌨️ **Build · L2:** define 3 tools with JSON schemas (calculator, search, DB lookup); write the loop by hand with the Claude API; handle tool errors.
- 📊 **Measure · L2:** steps, tokens and success on 10 tasks.
- 📈 **Improve · L3:** one-shot answer → tool loop → better tool descriptions → better error messages.
- 🎤 **Interview · L3:** How does tool calling work? · Agent vs workflow? · How do you stop loops?
- ✅ **Done when:** your loop solves a 3-step task without a framework.


### Level 2: ReAct and planning
<a id="day-92"></a>
#### ☐ Day 92 — ReAct, planning & task decomposition
- 🧠 **Idea · L1:** reason → act → observe. Plan first for long tasks. Reflect and retry on failure.
- ➗ **Equation · L1:** none — measure plan quality: steps wasted, success rate.
- ⌨️ **Build · L2:** ReAct prompt; plan-and-execute; a self-check step ("is the answer supported by the tool output?").
- 📊 **Measure · L2:** success vs the plain loop on 15 multi-step tasks.
- 📈 **Improve · L3:** loop → ReAct → plan-and-execute → + reflection.
- 🎤 **Interview · L3:** What is ReAct? · When is a single call better than an agent? · How does reflection help?
- ✅ **Done when:** measured gain from planning (or an honest "no gain").


### Level 3: memory and context engineering
<a id="day-93"></a>
#### ☐ Day 93 — Memory & context engineering
- 🧠 **Idea · L1:** the context window is a budget. Decide what goes in: recent messages, summaries, retrieved facts, tool results.
- ➗ **Equation · L1:** token budget `system + history + retrieved + tools + answer ≤ window`
- ⌨️ **Build · L2:** short-term memory (message trimming), summarization, long-term memory in a vector store; context compaction.
- 📊 **Measure · L2:** answer quality vs context size; cost.
- 📈 **Improve · L3:** full history → trimmed → summarized → retrieved memory.
- 🎤 **Interview · L3:** Short- vs long-term memory? · What is context compaction? · Why does more context sometimes hurt?
- ✅ **Done when:** the agent remembers a fact from 50 turns ago using < 20 % of the tokens.


## Chapter 47 — Frameworks and protocols: LangChain, LangGraph, MCP

### Level 2: graphs, state and human-in-the-loop
<a id="day-94"></a>
#### ☐ Day 94 — LangChain & LangGraph
- 🧠 **Idea · L1:** frameworks give structure: chains, tools, retrievers (**LangChain**; **LlamaIndex** for data / RAG); **LangGraph** = a state machine (nodes, edges, conditions, checkpoints, human-in-the-loop).
- ➗ **Equation · L1:** none — graph `G = (nodes, edges)`, state is passed along.
- ⌨️ **Build · L2:** rebuild the Day-91 agent in LangGraph; add a conditional edge, a retry node, a human-approval step.
- 📊 **Measure · L2:** lines of code, success, debuggability vs the hand-written loop.
- 📈 **Improve · L3:** write when to use a framework and when not to.
- 🎤 **Interview · L3:** LangChain vs LangGraph? · Why a graph for agents? · What is a checkpoint?
- ✅ **Done when:** the same agent works in both styles.


### Level 3: MCP servers
<a id="day-95"></a>
#### ☐ Day 95 — MCP: Model Context Protocol
- 🧠 **Idea · L1:** a standard way to give models **tools and data**. A server exposes tools / resources; any compatible client can use them.
- ➗ **Equation · L1:** none — client ↔ server messages (JSON-RPC).
- ⌨️ **Build · L2:** an MCP server with **read-only HRM tools** (search payslips, get policy); connect a client; test the tool schemas.
- 📊 **Measure · L2:** does the model pick the right tool? tool-call accuracy on 20 prompts.
- 📈 **Improve · L3:** vague tool names → clear names + descriptions + examples.
- 🎤 **Interview · L3:** What is MCP and why? · MCP tool vs function calling? · Security risks of tools?
- ✅ **Done when:** a client lists and calls your server's tools.


## Chapter 48 — Multi-agent systems

> ⚠️ **Common mistakes:** more agents "because cool" · no shared state discipline · cost explosions.

### Levels 1 → 3 (inside the day)
<a id="day-96"></a>
#### ☐ Day 96 — Multi-agent systems
- 🧠 **Idea · L1:** several agents with roles (researcher, writer, reviewer) or a manager with workers. More agents = more cost; use only when it helps.
- ➗ **Equation · L1:** total cost `= Σ over agents (tokens × price)`
- ⌨️ **Build · L2:** manager + 2 workers (CrewAI / AutoGen-style patterns, or plain code); read how AutoGPT and BabyAGI work (goal → task list → loop); shared state; hand-offs.
- 📊 **Measure · L2:** quality, cost and time vs one agent.
- 📈 **Improve · L3:** single agent → manager + workers → add a reviewer.
- 🎤 **Interview · L3:** When is multi-agent worth it? · How do agents hand off? · Failure modes?
- ✅ **Done when:** a table compares single vs multi-agent on cost and quality.


## Chapter 49 — Agent evaluation, guardrails and safety

### Levels 1 → 3 (inside the day)
<a id="day-97"></a>
#### ☐ Day 97 — Agent evaluation, guardrails & safety
- 🧠 **Idea · L1:** agents act in the real world, so **permissions and tests** come first. Read-only by default; confirm before writes; treat tool output as untrusted (injection).
- ➗ **Equation · L1:** task success rate · tool-call accuracy · steps per task · cost per task · p95 latency
- ⌨️ **Build · L2:** a test set of 30 tasks with expected outcomes; trajectory logs; allow-list of tools; read-only DB user; human approval for risky actions; Langfuse (or similar) tracing.
- 📊 **Measure · L2:** success rate and failure categories.
- 📈 **Improve · L3:** fix the top 3 failure causes; re-run.
- 🎤 **Interview · L3:** How do you evaluate an agent? · Prompt injection through tool output? · How do you limit blast radius?
- ✅ **Done when:** a repeatable eval run produces a report.


## Chapter 50 — Build: the HRM payslip agent and an end-to-end agent

### Level 3: build and ship
<a id="day-98"></a>
#### ☐ Day 98 — Build: the HRM payslip agent
- 🧠 **Idea · L1:** an agent that answers questions about payslips using **tools**: read-only text-to-SQL, the anomaly model (Day 39), the policy RAG (Day 90). Re-use the existing tool-calling agent in `hrm_app/`.
- ➗ **Equation · L1:** none new — use the Day-97 metrics.
- ⌨️ **Build · L2:** wire the 3 tools; SQL safety (read-only user, `SELECT` only, row limit); structured answers with citations.
- 📊 **Measure · L2:** 30-question test set: correctness, safe-SQL rate, steps, cost.
- 📈 **Improve · L3:** V1 → V4 (better schema description, few-shot SQL, retry on SQL error, guardrails).
- 🎤 **Interview · L3:** Text-to-SQL risks? · How do you give the model the DB schema? · How do you make it deterministic enough?
- ✅ **Done when:** ≥ 85 % correct, 0 unsafe queries.

<a id="day-99"></a>
#### ☐ Day 99 — Agent project
- 🧠 **Idea · L1:** one more agent end to end: a **research / support agent** with memory, tools, tracing and an eval report.
- ➗ **Equation · L1:** none new.
- ⌨️ **Build · L2:** the agent + traces + eval + README. Pick one: **AI researcher agent**, **customer-support agent** (memory + DB lookup), **email & calendar assistant**, **multi-agent workflow** (manager + developer + tester) or **code-assistant agent** (GitHub repo).
- 📊 **Measure · L2:** the Day-97 metrics.
- 📈 **Improve · L3:** one ladder written up.
- 🎤 **Interview · L3:** answer **20 questions** (Days 91–99). Design an agent platform on a whiteboard.
- ✅ **Checkpoint:** demo recording + eval report.


---

### ✅ Part X cheat card — agent patterns
| Pattern | Idea | Use when | Cost / risk |
|---|---|---|---|
| Single call | no loop | the task is one step | cheapest |
| Tool loop | call tools until done | lookups, calculations | steps × cost |
| ReAct | think → act → observe | multi-step reasoning | more tokens |
| Plan-and-execute | plan first, then run | long tasks | bad plan = wasted run |
| Reflection | critique and retry | quality matters | 2× cost |
| Multi-agent | roles / manager–workers | truly separable work | highest cost, hardest to debug |

[📖 Table of contents](README.md) · [← previous part](part9_generative_ai.md) · [next part →](part11_software_engineering_mlops.md) · [Appendices](appendix.md)
