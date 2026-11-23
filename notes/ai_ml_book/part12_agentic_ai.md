# PART XII — Agentic AI

[📖 Table of contents](README.md) · [← previous part](part11_llm_customization.md) · [next part →](part13_software_engineering_mlops.md) · [Appendices](appendix.md)


> **Days 99–111 · Category: LLM agents that plan, use tools and act · Levels: 1 → 3 in every chapter**
> **You will be able to:** write an agent loop with no framework, add planning and memory, rebuild it in LangGraph, expose tools through MCP, coordinate several agents, evaluate and secure an agent, and ship the HRM payslip agent.
> **Math you meet here (just-in-time):** expected cost = steps × cost per step (Day 99) · token budget (101) · success-rate metrics (104).
> **More depth:** Advanced shelf Days 177–180 (Reflexion, Tree-of-Thoughts, code / computer-use agents, A2A, durable workflows, OWASP LLM Top-10).

---

## Chapter 49 — Agent fundamentals: tool calling, planning, memory

> ⚠️ **Common mistakes:** no `max_steps` · vague tool descriptions · unbounded context · letting the agent write to production data.

### Level 1: tool calling and the loop
<a id="day-99"></a>
#### ☐ Day 99 — Tool calling & the agent loop (no framework)
- 🧮 **New math today (just-in-time):** expected cost = steps × cost per step.
- 🧠 **Idea · L1:** an agent = an LLM in a **loop**: think → call a tool → read the result → repeat until done.
- ➗ **Equation · L1:** success rate `= tasks solved/total` · expected cost `= steps × cost per step` · `max_steps` guards against infinite loops
- ⌨️ **Build · L2:** define 3 tools with JSON schemas (calculator, search, DB lookup); write the loop by hand with the Claude API; handle tool errors.
- 📊 **Measure · L2:** steps, tokens and success on 10 tasks.
- 📈 **Improve · L3:** one-shot answer → tool loop → better tool descriptions → better error messages.
- 🎤 **Interview · L3:** How does tool calling work? · Agent vs workflow? · How do you stop loops?
- ✅ **Done when:** your loop solves a 3-step task without a framework.


### Level 2: ReAct and planning
<a id="day-100"></a>
#### ☐ Day 100 — ReAct, planning & task decomposition
- 🧠 **Idea · L1:** reason → act → observe. Plan first for long tasks. Reflect and retry on failure.
- ➗ **Equation · L1:** none — measure plan quality: steps wasted, success rate.
- ⌨️ **Build · L2:** ReAct prompt; plan-and-execute; a self-check step ("is the answer supported by the tool output?").
- 📊 **Measure · L2:** success vs the plain loop on 15 multi-step tasks.
- 📈 **Improve · L3:** loop → ReAct → plan-and-execute → + reflection.
- 🎤 **Interview · L3:** What is ReAct? · When is a single call better than an agent? · How does reflection help?
- ✅ **Done when:** measured gain from planning (or an honest "no gain").


### Level 3: memory and context engineering
<a id="day-101"></a>
#### ☐ Day 101 — Memory & context engineering
- 🧠 **Idea · L1:** the context window is a budget. Decide what goes in: recent messages, summaries, retrieved facts, tool results.
- ➗ **Equation · L1:** token budget `system + history + retrieved + tools + answer ≤ window`
- ⌨️ **Build · L2:** short-term memory (message trimming), summarization, long-term memory in a vector store; context compaction.
- 📊 **Measure · L2:** answer quality vs context size; cost.
- 📈 **Improve · L3:** full history → trimmed → summarized → retrieved memory.
- 🎤 **Interview · L3:** Short- vs long-term memory? · What is context compaction? · Why does more context sometimes hurt?
- ✅ **Done when:** the agent remembers a fact from 50 turns ago using < 20 % of the tokens.


## Chapter 50 — Frameworks and protocols: LangChain, LangGraph, MCP

### Level 2: graphs, state and human-in-the-loop
<a id="day-102"></a>
#### ☐ Day 102 — LangChain & LangGraph
- 🧠 **Idea · L1:** frameworks give structure: chains, tools, retrievers (**LangChain**; **LlamaIndex** for data / RAG); **LangGraph** = a state machine (nodes, edges, conditions, checkpoints, human-in-the-loop).
- ➗ **Equation · L1:** none — graph `G = (nodes, edges)`, state is passed along.
- ⌨️ **Build · L2:** rebuild the Day-99 agent in LangGraph; add a conditional edge, a retry node, a human-approval step.
- 📊 **Measure · L2:** lines of code, success, debuggability vs the hand-written loop.
- 📈 **Improve · L3:** write when to use a framework and when not to.
- 🎤 **Interview · L3:** LangChain vs LangGraph? · Why a graph for agents? · What is a checkpoint?
- ✅ **Done when:** the same agent works in both styles.


### Level 3: MCP servers
<a id="day-103"></a>
#### ☐ Day 103 — MCP: Model Context Protocol
- 🧠 **Idea · L1:** a standard way to give models **tools and data**. A server exposes tools / resources; any compatible client can use them.
- ➗ **Equation · L1:** none — client ↔ server messages (JSON-RPC).
- ⌨️ **Build · L2:** an MCP server with **read-only HRM tools** (search payslips, get policy); connect a client; test the tool schemas.
- 📊 **Measure · L2:** does the model pick the right tool? tool-call accuracy on 20 prompts.
- 📈 **Improve · L3:** vague tool names → clear names + descriptions + examples.
- 🎤 **Interview · L3:** What is MCP and why? · MCP tool vs function calling? · Security risks of tools?
- ✅ **Done when:** a client lists and calls your server's tools.


## Chapter 51 — Agent evaluation, guardrails and safety

### Levels 1 → 3 (inside the day)
<a id="day-104"></a>
#### ☐ Day 104 — Agent evaluation, guardrails & safety
- 🧠 **Idea · L1:** agents act in the real world, so **permissions and tests** come first. Read-only by default; confirm before writes; treat tool output as untrusted (injection).
- ➗ **Equation · L1:** task success rate · tool-call accuracy · steps per task · cost per task · p95 latency
- ⌨️ **Build · L2:** a test set of 30 tasks with expected outcomes; trajectory logs; allow-list of tools; read-only DB user; human approval for risky actions; Langfuse (or similar) tracing.
- 📊 **Measure · L2:** success rate and failure categories.
- 📈 **Improve · L3:** fix the top 3 failure causes; re-run.
- 🎤 **Interview · L3:** How do you evaluate an agent? · Prompt injection through tool output? · How do you limit blast radius?
- ✅ **Done when:** a repeatable eval run produces a report.


## Chapter 52 — Multi-agent systems

> **You will learn:** when several agents beat one, the 7 architectures, how agents communicate and share state, the main frameworks side by side, how to keep the system reliable, cheap and safe, and a complete project.
> ⚠️ **Common mistakes:** more agents "because it is cool" · free-text handoffs · one giant shared context · no loop or budget guard · giving every agent every tool.

### Level 1 — Beginner: when to use it, and which architecture
<a id="day-105"></a>
#### ☐ Day 105 — Multi-agent I: when to use it, and which architecture
- 🧮 **New math today (just-in-time):** total cost = Σ over agents · end-to-end reliability = product of step reliabilities · fan-out speed-up.
- 🧠 **Idea · L1:** several LLM agents, each with a role and its own tools, working together. It helps when the work is **parallel**, needs **different tools or permissions**, or benefits from an **independent reviewer**. It hurts when one agent could do the job (more tokens, more failures). Architectures: **supervisor–worker**, **hierarchical** (managers of managers), **sequential pipeline**, **parallel fan-out / fan-in** (map-reduce), **router + handoff / swarm**, **debate / critic–reviewer**, **blackboard** (shared board). Failure modes: endless delegation loops, role confusion, errors that compound, cost explosions.
- ➗ **Equation · L1:** `cost = Σᵢ nᵢ·(tokens_inᵢ·p_in + tokens_outᵢ·p_out)` · end-to-end success `≈ Πᵢ pᵢ` (five steps at 0.9 → 0.59) · fan-out speed-up `≈ T_serial / (T_slowest_worker + T_merge)`.
- ⌨️ **Build (no framework) · L2:** a single-agent **baseline** for HR questions; then a supervisor that routes a request to 2 workers (policy-RAG worker from Part X, payroll read-only SQL worker) and merges their answers; a `delegate(worker, task)` tool with a JSON schema; `max_steps` and a budget guard; then parallel fan-out with `asyncio.gather`.
- 📊 **Measure · L2:** on 20 mixed questions compare single agent vs supervisor: accuracy, tokens, latency, cost.
- 📈 **Improve · L3:** single agent → supervisor + workers → parallel fan-out → + reviewer (critic).
- 🎤 **Interview · L3:** When is multi-agent better than one agent? · Name 4 architectures and when to use each. · Why does reliability drop as you add agents?
- ✅ **Done when:** a table "single vs multi: quality / cost / latency" with a clear recommendation.


### Level 2 — Intermediate: communication, state and frameworks
<a id="day-106"></a>
#### ☐ Day 106 — Multi-agent II: communication, shared state and contracts
- 🧮 **New math today (just-in-time):** context saved by isolation · state reducers.
- 🧠 **Idea · L1:** agents must exchange *just enough*. **Message passing** (agents send messages) vs **shared state** (all read and write one state object — LangGraph state with *reducers*). Use **structured contracts** (pydantic / JSON schema) so one agent's output is valid input for the next. Give each sub-agent its **own context window** (context isolation) and let it return a short **summary**, not its whole transcript. Share long-term memory through a store and tools through **MCP**; **A2A** is a standard for agents from different systems to talk.
- ➗ **Equation · L1:** context saved `= Σ (sub-agent transcript tokens) − Σ (summary tokens)` · valid handoff `∈ {0,1}` by schema check · reducer `state′ = reduce(state, update)`.
- ⌨️ **Build · L2:** pydantic contracts (`Task`, `Finding`, `Report`); a shared-state graph where workers append findings with a reducer; a sub-agent that returns a ≤ 150-token summary; a per-agent tool allow-list; one MCP tool server shared by two agents; an A2A-style message exchange between two small services.
- 📊 **Measure · L2:** tokens per run with and without isolation; invalid-handoff rate (schema failures) and retries; whether any worker saw information it should not see.
- 📈 **Improve · L3:** free-text handoffs → schema-validated → + summaries → + per-agent permissions.
- 🎤 **Interview · L3:** Message passing vs shared state? · Why isolate each sub-agent's context? · How do you stop one agent's mistake from poisoning the others?
- ✅ **Done when:** handoff failures are below 2 % over 50 runs and the context cost drops measurably.

<a id="day-107"></a>
#### ☐ Day 107 — Multi-agent III: frameworks side by side (LangGraph, CrewAI, AutoGen, agent SDKs)
- 🧠 **Idea · L1:** the same task in three frameworks. **LangGraph:** an explicit graph (nodes, edges, state, checkpoints, human-in-the-loop; supervisor / swarm / hierarchical sub-graphs) — most control. **CrewAI:** roles, goals, tasks and crews (sequential / hierarchical) — fastest to prototype. **AutoGen / AG2:** conversational agents in group chats — flexible, harder to bound. **Agent SDKs** (Claude Agent SDK, OpenAI Agents SDK): sub-agents, tools and handoffs as first-class features. Also read how **AutoGPT** and **BabyAGI** loop (goal → task list → execute → re-prioritize) and why they were unreliable.
- ➗ **Equation · L1:** none — compare on lines of code, success rate, tokens, p95 latency, debuggability (1–5) and control (1–5).
- ⌨️ **Build · L2:** the **same task** — "check employee X's March payslip, explain any anomaly with the policy, draft a note" — in LangGraph, CrewAI and one of AutoGen / an agent SDK, with the same tools (payroll SQL tool, policy RAG, anomaly model from Day 39).
- 📊 **Measure · L2:** success on 20 tasks, tokens, latency, lines of code, and how hard it was to debug one failure; fill the comparison table.
- 📈 **Improve · L3:** choose one framework for the project and justify it with numbers; note what you would do without a framework.
- 🎤 **Interview · L3:** LangGraph vs CrewAI vs AutoGen? · When would you not use a framework? · How do you debug a conversation between agents?
- ✅ **Done when:** three working versions and a comparison table with your recommendation.


### Level 3 — Advanced: reliability, security and the project
<a id="day-108"></a>
#### ☐ Day 108 — Multi-agent IV: reliability, cost control and security
- 🧮 **New math today (just-in-time):** per-agent vs end-to-end success · budget guard · expected retries.
- 🧠 **Idea · L1:** multi-agent systems fail in new ways: loops, deadlocks, role drift, silent errors, cost explosions, and security — one agent reading a poisoned document can pass an injection to the others. Build in **tracing across agents** (one run id), **per-agent cost accounting**, **timeouts / retries / circuit breakers**, **loop guards**, **human approval** for risky actions, **durable workflows** that resume after a crash, and **least privilege** per agent. (General agent evaluation was Day 104.)
- ➗ **Equation · L1:** end-to-end success `= Π pᵢ` (improve the weakest link first) · expected attempts `= 1/p` · budget guard `Σ cost ≤ B` · blast radius = what an agent's credentials can touch.
- ⌨️ **Build · L2:** trace every agent call with Langfuse (or similar) under one run id; unit-test each agent with mocked neighbours; an end-to-end set of 30 tasks; **inject failures** (tool timeout, invalid JSON, a document with a prompt-injection) and check that the system degrades gracefully; add a loop guard, timeouts, a budget cap and human approval for any write action.
- 📊 **Measure · L2:** per-agent and end-to-end success; cost per run; failures by category; injection success rate.
- 📈 **Improve · L3:** fix the weakest agent first → add guards → re-run.
- 🎤 **Interview · L3:** How do you test a multi-agent system? · What is your plan when two agents loop? · How do you contain prompt injection across agents?
- ✅ **Done when:** a repeatable eval report with per-agent and end-to-end numbers.

<a id="day-109"></a>
#### ☐ Day 109 — Multi-agent project (checkpoint): the HR assistant crew
- 🧠 **Idea · L1:** build the system. A **Manager** (supervisor) + **Policy agent** (RAG from Part X) + **Payroll agent** (read-only text-to-SQL) + **Anomaly agent** (your Day-39 detector) + **Reviewer** (checks every claim against evidence). Fan out in parallel, merge, review, answer with citations.
- ➗ **Equation · L1:** none new — use the Day-108 metrics and the Day-105 cost and speed-up formulas.
- ⌨️ **Build · L2:** your chosen framework (Day 107); pydantic contracts (Day 106); shared MCP tools; per-agent permissions; tracing; an eval set of 30 tasks; compare with the single-agent baseline from Day 105.
- 📊 **Measure · L2:** accuracy, citation accuracy, p95 latency, cost per task, unsafe actions blocked — single vs multi.
- 📈 **Improve (V1 → V4) · L3:** sequential → parallel fan-out → + reviewer → + budget and loop guards.
- 🎤 **Interview · L3:** answer **20 questions** on Days 99–109; whiteboard the architecture and defend each agent.
- ✅ **Done when:** README with an architecture diagram, a results table and an honest note on **when multi-agent was NOT worth it**.


## Chapter 53 — Build: the HRM payslip agent and an end-to-end agent

### Level 3: build and ship
<a id="day-110"></a>
#### ☐ Day 110 — Build: the HRM payslip agent
- 🧠 **Idea · L1:** an agent that answers questions about payslips using **tools**: read-only text-to-SQL, the anomaly model (Day 39), the policy RAG (Day 93). Re-use the existing tool-calling agent in `hrm_app/`.
- ➗ **Equation · L1:** none new — use the Day-104 metrics.
- ⌨️ **Build · L2:** wire the 3 tools; SQL safety (read-only user, `SELECT` only, row limit); structured answers with citations.
- 📊 **Measure · L2:** 30-question test set: correctness, safe-SQL rate, steps, cost.
- 📈 **Improve · L3:** V1 → V4 (better schema description, few-shot SQL, retry on SQL error, guardrails).
- 🎤 **Interview · L3:** Text-to-SQL risks? · How do you give the model the DB schema? · How do you make it deterministic enough?
- ✅ **Done when:** ≥ 85 % correct, 0 unsafe queries.

<a id="day-111"></a>
#### ☐ Day 111 — Agent project
- 🧠 **Idea · L1:** one more agent end to end: a **research / support agent** with memory, tools, tracing and an eval report.
- ➗ **Equation · L1:** none new.
- ⌨️ **Build · L2:** the agent + traces + eval + README. Pick one: **AI researcher agent**, **customer-support agent** (memory + DB lookup), **email & calendar assistant**, **multi-agent workflow** (manager + developer + tester) or **code-assistant agent** (GitHub repo).
- 📊 **Measure · L2:** the Day-104 metrics.
- 📈 **Improve · L3:** one ladder written up.
- 🎤 **Interview · L3:** answer **20 questions** (Days 99–111). Design an agent platform on a whiteboard.
- ✅ **Checkpoint:** demo recording + eval report.


---

### ✅ Part XII cheat card — agent patterns
| Pattern | Idea | Use when | Cost / risk |
|---|---|---|---|
| Single call | no loop | the task is one step | cheapest |
| Tool loop | call tools until done | lookups, calculations | steps × cost |
| ReAct | think → act → observe | multi-step reasoning | more tokens |
| Plan-and-execute | plan first, then run | long tasks | bad plan = wasted run |
| Reflection | critique and retry | quality matters | 2× cost |
| Multi-agent | roles / manager–workers | truly separable work | highest cost, hardest to debug |

### ✅ Part XII cheat card — multi-agent architectures
| Architecture | Idea | Use when | Cost | Main risk |
|---|---|---|---|---|
| Supervisor–worker | one manager delegates to specialists | clear sub-tasks, different tools / permissions | medium | manager becomes a bottleneck |
| Hierarchical | managers of managers | large task trees | high | latency, long failure chains |
| Sequential pipeline | A → B → C | fixed stages (draft → review → format) | low | one bad stage spoils everything |
| Parallel fan-out / fan-in | many workers, then merge | independent sub-questions, research | high tokens, low latency | merge conflicts |
| Router + handoff / swarm | route to a specialist; specialists hand off | triage, support | low–medium | wrong routing, ping-pong |
| Debate / critic–reviewer | agents challenge each other | high-stakes accuracy | 2–3× | agreement bias |
| Blackboard | a shared board everyone writes to | open-ended collaboration | medium | state sprawl |

[📖 Table of contents](README.md) · [← previous part](part11_llm_customization.md) · [next part →](part13_software_engineering_mlops.md) · [Appendices](appendix.md)
