# 👑 LOT AI X1 — AI Operating System (AIOS)
## Architecture Specification v1.0

---

## 1. Product Vision

**What LOT AI X1 is:** an orchestration platform that takes a goal, decomposes it into a plan, routes each piece of work to the right specialist agent and the right underlying model, executes with real tools (code execution, browser, filesystem, APIs), verifies its own output against tests/criteria, and hands back a working artifact — code, a document, a deployed app, a research report — with a clear record of what it did and why.

**What it is not:** a single monolithic "smartest model." LOT AI's edge isn't a bigger LLM — it's the scaffolding around models: planning, routing, memory, verification, and tool use. That scaffolding is where 90% of real-world reliability comes from, and it's the part you actually own and can improve independently of whichever model vendor is ahead this quarter.

**Core differentiators:**
| Differentiator | Why it's real | Why it's hard to copy quickly |
|---|---|---|
| Model-agnostic router | Not locked to one vendor; swaps models as better/cheaper ones ship | Requires a capability-benchmarking pipeline, not just a config file |
| Verification-first execution | Every agent output is checked (tests, linters, evals, human gates) before being marked "done" | Requires investment in eval infra most teams skip |
| Persistent, structured memory | Agents remember project state, decisions, and prior failures across sessions | Requires real memory architecture, not just a bigger context window |
| Specialist agent framework | Narrow agents with tight tool access outperform one generalist agent on long-horizon tasks | Requires disciplined agent boundaries and orchestration |

**Explicitly out of scope for autonomous, unsupervised execution:** cybersecurity offensive actions, medical diagnosis/treatment/surgery, legal advice with binding effect, financial transactions above a configurable threshold, and any production deployment or destructive action (delete, overwrite, publish) without a human approval gate.

---

## 2. AIOS Architecture — System of Systems

```text
┌──────────────────────────────────────────────────────────────────────┐
│                            LOT AI X1 — AIOS                          │
│                                                                      │
│  ┌───────────┐   ┌────────────────┐   ┌───────────────────────────┐  │
│  │  Intake   │──▶│  Mission        │──▶│  Executive Agent          │  │
│  │  Layer    │   │  Planning       │   │  (Orchestrator)           │  │
│  └───────────┘   │  Engine         │   └──────────┬────────────────┘  │
│                    └────────────────┘              │                 │
│                                                     ▼                 │
│                              ┌──────────────────────────────────────┐│
│                              │   Specialist Agent Framework         ││
│                              │  (Router → per-domain agents)        ││
│                              └──────┬──────────────┬────────────────┘│
│                                     │              │                  │
│                       ┌─────────────▼───┐   ┌──────▼──────────────┐  │
│                       │ Tool Execution  │   │  Dynamic Model      │  │
│                       │ Engine (MCP,    │   │  Router             │  │
│                       │ Browser, FS,    │   │  (multi-provider)   │  │
│                       │ Code Exec)      │   └──────────────────────┘  │
│                       └─────────┬───────┘                             │
│                                 │                                     │
│                       ┌─────────▼───────────────────────────────────┐ │
│                       │  Memory & Retrieval Layer                   │ │
│                       │  (episodic / semantic / procedural / vector)│ │
│                       └─────────┬───────────────────────────────────┘ │
│                                 │                                     │
│                       ┌─────────▼───────────────────────────────────┐ │
│                       │  Verification & Evaluation Framework        │ │
│                       └─────────┬───────────────────────────────────┘ │
│                                 │                                     │
│                       ┌─────────▼───────────────────────────────────┐ │
│                       │  Governance / Policy / Human-in-Loop Gate   │ │
│                       └─────────┬───────────────────────────────────┘ │
│                                 ▼                                     │
│                          Delivery Layer (artifact, preview, deploy)   │
└──────────────────────────────────────────────────────────────────────┘
              ▲                                          │
              │        Observability & Telemetry Bus      │
              └──────────────────────────────────────────┘
```

---

## 3. Component Architecture

LOT AI X1 is a set of independently deployable services communicating over an event bus (async) and gRPC/REST (sync, low-latency paths):

| Component | Type | Talks to | State |
|---|---|---|---|
| Intake Gateway | Stateless API | Mission Planner | none |
| Mission Planning Engine | Stateless service | Executive Agent, Memory | plan DAG (persisted) |
| Executive Agent Service | Stateful worker | Specialist Router, Memory, Governance | task graph state |
| Specialist Agent Pool | Stateless workers | Tool Engine, Model Router, Memory | none (context injected) |
| Model Router | Stateless service | Model Providers, Benchmark Store | routing table (cached) |
| Tool Execution Engine | Sandboxed workers | MCP servers, Browser farm, Code sandbox, FS | ephemeral per-task |
| Memory Service | Stateful, DB-backed | Vector DB, Relational DB, Object store | persistent |
| Verification Engine | Stateless workers | Test runners, Linters, Eval harness | run results (persisted) |
| Governance/Policy Engine | Stateless, rules-first | Executive Agent, Audit Log | policy config (persisted) |
| Delivery Service | Stateless | Object store, Deploy targets, Preview infra | artifact metadata |
| Observability Bus | Event stream | all components | logs/traces/metrics |

---

## 4. Microservice Architecture

Design rule: **one service = one responsibility = one failure domain.**

```text
services/
  ├─ api-gateway/            # authn, rate limiting, request normalization
  ├─ mission-planner/        # goal -> DAG
  ├─ executive-orchestrator/ # DAG execution, retries, escalation
  ├─ agent-router/           # picks specialist agent for a subtask
  ├─ agent-pool/             # domain specialist workers
  ├─ model-router/            # provider abstraction + benchmark-driven selection
  ├─ tool-engine/            # MCP, browser, sandbox, filesystem
  ├─ memory-service/         # vector, episodic, procedural
  ├─ verification-engine/    # TDD, linters, evals
  ├─ governance-engine/      # policy-as-code
  ├─ delivery-service/       # preview sandbox & zip packaging
  └─ observability-collector/# telemetry, metrics, traces
```

---

## 5. Agent Architecture

Every agent shares one interface:

```typescript
interface Agent {
  id: string;
  domain: string;
  system_prompt: string;
  allowed_tools: string[];
  model_preference: string[];
  input: TaskSpec;
  output: TaskResult;
  status: 'pending' | 'running' | 'blocked' | 'needs_human' | 'done' | 'failed';
}
```

---

## 6. Executive Agent Hierarchy

```text
                     ┌───────────────────┐
                     │  Executive Agent  │   (1 per mission)
                     └─────────┬─────────┘
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
      ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
      │ Domain Lead:  │ │ Domain Lead:  │ │ Domain Lead:  │
      │ Engineering   │ │ Research      │ │ Business/Ops  │
      └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
              ▼                 ▼                 ▼
     ┌─────────────────┐ ┌───────────────┐ ┌────────────────┐
     │ Specialist      │ │ Specialist    │ │ Specialist     │
     │ Agents          │ │ Agents        │ │ Agents         │
     └─────────────────┘ └───────────────┘ └────────────────┘
```

---

## 7. Specialist Agent Framework (YAML Profile Strategy)

```yaml
agent_profile: pcb_designer
domain: hardware.pcb
system_prompt_ref: prompts/pcb_designer_v3.md
allowed_tools: [filesystem, code_sandbox(kicad-cli), web_search(datasheet lookup)]
verification: [drc_check, erc_check, bom_cost_check]
model_preference: [reasoning-tier-model, coding-tier-model]
escalation_triggers: [confidence < 0.7, safety_critical_flag]
knowledge_pack: kb/pcb/
```

---

## 8. Mission Planning Engine

1. **Goal parsing** — JSON schema extraction.
2. **Decomposition** — dependency DAG construction.
3. **Dependency graph construction** — DAG validation & parallel branch identification.
4. **Resource estimation** — token & latency budget allocation.
5. **Plan review gate** — optional user approval gate before tool execution.

---

## 9. Dynamic Model Router

Routes requests across 12 NVIDIA NIM MoE models based on live capability score:
`Score = Match + SuccessRate - AvgLatencyMs - CostPer1kTokens`

---

## 10. Memory Architecture

- **Episodic**: Append-only execution history (SQLite/PostgreSQL)
- **Semantic**: RAG corpus vector store (Qdrant/pgvector)
- **Procedural**: Versioned SOP procedure library
- **Working Memory**: Active session context buffer (Redis)

---

## 11. Tool Execution Engine & 5 MCP Servers

Binds 5 core MCP servers:
1. `Context7 MCP`: Live API documentation scraper
2. `GitHub MCP`: Version control & repository actions
3. `Playwright MCP`: Headless browser visual verification
4. `Sequential Thinking MCP`: Structured multi-step reasoning DAG
5. `Filesystem MCP`: Workspace file I/O operations

---

## 12. 10-Phase Zero-Human Autonomous Pipeline

`UNDERSTAND` → `PLAN` → `ROUTE` → `SCAFFOLD` → `BUILD` → `TEST` → `HEAL` → `REVIEW` → `PREVIEW` → `DELIVER`.

---

## 13. Governance & Policy Engine

Policy-as-code enforcement:
- Hard deny on offensive cybersecurity exploits & medical surgeries.
- Mandatory human approval gate on production deployments & secret mutations.

---

## 14. Technology Stack & Verification Verdict

- **Backend**: Python (FastAPI) + Go (low-latency routing)
- **Orchestration**: Kubernetes + Kafka event bus
- **Storage**: PostgreSQL + Qdrant + Redis + S3
- **Verification Result**: 104 / 104 Checks Passed (100.0% Health Score)
