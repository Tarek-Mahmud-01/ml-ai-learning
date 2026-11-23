# PART VIII — Reinforcement Learning

[📖 Table of contents](README.md) · [← previous part](part7_nlp.md) · [next part →](part9_generative_ai.md) · [Appendices](appendix.md)


> **Days 74–76 · Category: reinforcement learning (learn by reward) · Levels: 1 → 3 in every chapter**
> **You will be able to:** model a problem as an MDP, write the Bellman equation, build Q-learning and a DQN, explain PPO, and describe how RLHF / DPO / GRPO turn a text predictor into an assistant.
> **Math you meet here (just-in-time):** return, discount factor, Bellman equation (Day 74) · policy-gradient theorem, PPO clip (75) · reward model, KL penalty (76).
> **More RL (bandits deep dive, SAC / TD3, offline, multi-agent):** Advanced shelf, Days 174–176.

---

## Chapter 37 — RL basics: MDP, Bellman, Q-learning

> ⚠️ **Common mistakes:** reward hacking · no exploration decay · judging by one seed.

### Levels 1 → 3 (inside the day)
<a id="day-74"></a>
#### ☐ Day 74 — MDP, Bellman equation & Q-learning
- 🧮 **New math today (just-in-time):** return, discount factor γ, the Bellman equation, the temporal-difference update.
- 🧠 **Idea · L1:** an agent acts, gets rewards, and learns a policy. Start with **bandits** (one state), then states.
- ➗ **Equation · L1:** return `Gₜ = Σ γᵏ rₜ₊ₖ₊₁` · Bellman `V(s) = maxₐ Σ P(s′|s,a)[R + γV(s′)]` · **Q-learning** `Q(s,a) ← Q(s,a) + α[r + γ·maxₐ′ Q(s′,a′) − Q(s,a)]` · ε-greedy
- ⌨️ **Build · L2:** multi-armed bandit; Q-learning on FrozenLake / GridWorld from scratch; SARSA for comparison.
- 📊 **Measure · L2:** average reward per episode; success rate.
- 📈 **Improve · L3:** random → greedy → ε-greedy → decaying ε → tuned α, γ.
- 🎤 **Interview · L3:** Explore vs exploit? · On-policy vs off-policy? · What is γ?
- ✅ **Done when:** the agent solves FrozenLake > 70 %.


## Chapter 38 — Deep RL: DQN, policy gradient, PPO

### Levels 1 → 3 (inside the day)
<a id="day-75"></a>
#### ☐ Day 75 — DQN, policy gradient, PPO
- 🧮 **New math today (just-in-time):** the policy-gradient theorem and the PPO clipped objective.
- 🧠 **Idea · L1:** use a neural net for Q (DQN) or directly for the policy (policy gradient). PPO = a safe, popular policy-gradient method.
- ➗ **Equation · L1:** DQN loss `(r + γ·max Q_target(s′,·) − Q(s,a))²` + replay buffer + target net · REINFORCE `∇J = E[∇log π(a|s)·G]` · PPO `min(rₜAₜ, clip(rₜ, 1−ε, 1+ε)Aₜ)`
- ⌨️ **Build · L2:** CartPole with a DQN (or Stable-Baselines3 DQN / PPO); read about actor-critic, A3C, DDPG, model-based RL.
- 📊 **Measure · L2:** reward curve; seeds matter (run 3).
- 📈 **Improve · L3:** DQN → +replay + target network → PPO.
- 🎤 **Interview · L3:** Why a replay buffer? · Value-based vs policy-based? · Why clip in PPO?
- ✅ **Done when:** CartPole is solved (≥ 195 average).


## Chapter 39 — RL for language models

### Levels 1 → 3 (inside the day) — Part checkpoint
<a id="day-76"></a>
#### ☐ Day 76 — RL for language models
- 🧮 **New math today (just-in-time):** Bradley–Terry reward model and the KL penalty.
- 🧠 **Idea · L1:** RL turns a text predictor into a helpful assistant. **RLHF**, **DPO**, **GRPO / RLVR** (verifiable rewards).
- ➗ **Equation · L1:** reward model (Bradley–Terry) `P(a ≻ b) = σ(r_a − r_b)` · RLHF objective `max E[r(x,y)] − β·KL(π‖π_ref)`
- ⌨️ **Build · L2:** a tiny **bandit that chooses among 3 prompts** by reward; write a one-page explanation of RLHF → DPO → GRPO.
- 📊 **Measure · L2:** regret of your bandit.
- 📈 **Improve · L3:** uniform → ε-greedy → UCB.
- 🎤 **Interview · L3:** answer **20 questions** (Days 74–76). What does the KL term do? RLHF vs DPO?
- ✅ **Done when:** you can explain how a chat model is trained, end to end.


---

### ✅ Part VIII cheat card — RL algorithm families
| Family | Examples | Learns | Good for | Weakness |
|---|---|---|---|---|
| Value-based | Q-learning, SARSA, DQN | `Q(s,a)` | discrete actions | unstable with function approximation |
| Policy-based | REINFORCE | `π(a|s)` | continuous actions | high variance |
| Actor-critic | A2C, PPO, SAC, TD3 | both | **most real tasks** | tuning |
| Model-based | Dyna, MuZero | the world model | sample efficiency | model errors |
| For LLMs | RLHF (PPO), DPO, GRPO | policy from preferences / verifiable rewards | alignment, reasoning | reward hacking |

[📖 Table of contents](README.md) · [← previous part](part7_nlp.md) · [next part →](part9_generative_ai.md) · [Appendices](appendix.md)
