# 📘 Agentic ERP System – Architecture Notes (Day 1–7)

A running collection of principles, laws, and lessons learned during this learning journey.

---

## 1️⃣ Core Philosophy

**AI is Not Authority**

- LLM = probabilistic reasoning engine
- Domain layer = deterministic authority
- **AI suggests, domain decides**
- AI must be removable without breaking system

> If removing AI breaks accounting logic, architecture is wrong.

---

## 2️⃣ Agent Architecture Fundamentals

**Basic Agent Loop**

```
User Input
    ↓
LLM → Propose JSON Command
    ↓
Schema Validation
    ↓
Authorization Check
    ↓
Business Invariant Validation
    ↓
Execution
```

---

## 3️⃣ Schema > Prompt

| Concept | Role |
|--------|------|
| **Prompt** | Guidance |
| **Schema** | Enforcement |

**Never trust:**

- “Return only JSON” instructions
- LLM formatting discipline
- Type assumptions

**Always implement:**

- Strict schema validation
- Required field enforcement
- Type enforcement
- Unknown field rejection

---

## 4️⃣ Validation Layering

**Correct order:**

1. JSON parsing
2. Schema validation (structure + type)
3. Authorization validation
4. Business invariant validation
5. Execution

Each layer has one responsibility.

---

## 5️⃣ Type Safety in Financial Systems

**Never Use Float for Money**

- **Float:** Binary approximation, rounding drift, aggregation instability
- **Use:** `Decimal`, `condecimal(...)`, strict types

**Finance rules:**

- Enforce precision per currency
- Reject invalid precision
- Never silently round user-entered values
- Rounding must be deterministic and documented

---

## 6️⃣ Business Invariants

Business invariants must:

- Be deterministic
- Be domain-owned
- Be AI-independent
- Remain unchanged even if AI is removed

**Examples:**

- Invoice amount > 0
- Currency precision enforcement
- Only draft invoices can be approved
- No posting in closed accounting period

---

## 7️⃣ Separation of Duties

**AI should:**

- Draft documents
- Suggest risk
- Recommend review

**AI must NOT:**

- Approve invoices
- Post to ledger
- Modify policy thresholds
- Change domain rules

| Layer | Responsibility |
|-------|----------------|
| Domain | Economic truth |
| Application | Orchestration |
| Database | Storage |
| AI | Advisory intelligence |

---

## 8️⃣ Threshold Abuse & Structuring

**Risk pattern:**

- Splitting invoices below approval threshold
- Multi-vendor threshold evasion
- Rapid-fire micro transactions

**Deterministic safeguards:**

```
If sum(actor invoices in 1 hour) > threshold:
    escalate
If N invoices < threshold within X minutes:
    require review
```

AI can detect patterns, but domain must enforce limits.

---

## 9️⃣ Event-Driven AI Integration

**Instead of:** User → AI → Execute

**Safer pattern:** Domain Event → AI → Advisory

AI acts as:

- Observer
- Analyst
- Risk signal generator

**AI does NOT mutate state.**

---

## 🔟 Safe RAG in ERP

**Never send raw documents to LLM.**

**Do NOT:**

- Send vendor notes
- Send free-text comments
- Send policy documents raw
- Send entire history

**Instead – Structured RAG:**

```
Repository → Domain → Structured Summary DTO → LLM
```

**Example context:**

```json
{
  "vendor_status": "approved",
  "invoice_amount": 4999,
  "recent_24h_spend": 15000,
  "threshold_limit": 5000
}
```

LLM reasons on facts, not raw text.

---

## 1️⃣1️⃣ Context Poisoning Risks

When using RAG:

- Retrieval-based prompt injection
- Vector database poisoning
- Semantic manipulation
- Policy rewriting via stored text
- De-anonymization through context aggregation

**Mitigation:**

- Sanitize inputs
- Use structured summaries
- Restrict raw text exposure
- Keep domain as context gatekeeper

---

## 1️⃣2️⃣ Calibration Layer

- **LLM output** = raw signal  
- **Humans** = limited review capacity  

**Between them must exist: Risk Calibration Layer**

**Responsibilities:**

- Assign risk score
- Track precision/recall
- Filter noise
- Enforce escalation thresholds
- Prevent alert fatigue

**Flow:**

```
LLM Advisory
    ↓
Risk Scoring Layer
    ↓
Escalation Decision
    ↓
Compliance Workflow
```

---

## 1️⃣3️⃣ Alert Fatigue & Governance

If false positives are high:

- Human trust collapses
- Alerts ignored
- Real fraud missed
- AI disabled

**AI systems must:**

- Prioritize precision
- Expand gradually
- Be feedback-calibrated

---

## 1️⃣4️⃣ Hybrid Intelligence Model

| Approach | Traits |
|----------|--------|
| **Deterministic rules** | High precision, stable, auditable |
| **LLM reasoning** | Adaptive, pattern-based, exploratory |

**Correct hybrid:**

- **Firewall** (deterministic rules)  
- **+**  
- **Analyst** (LLM advisory)

Never replace deterministic logic with LLM reasoning.

---

## 1️⃣5️⃣ Model Drift Resilience

**If model precision drops, system should:**

- Continue operating
- Reduce escalation rate
- Adjust calibration thresholds
- Log performance degradation

**System must NOT:**

- Break invariants
- Lose financial correctness
- Depend on model stability

**AI must be:** Removable · Replaceable · Degradable

---

## 1️⃣6️⃣ Graduated Risk Response Model

**When AI flags risk:**

1. Add risk metadata
2. Escalate to compliance workflow
3. Human review
4. Deterministic action (if required)

**Never:**

- Auto-freeze vendor based on AI alone
- Auto-block without deterministic trigger

---

## 1️⃣7️⃣ Enterprise AI Principles

1. AI informs, domain decides  
2. Prompts guide, schemas enforce  
3. LLM reasoning must be bounded  
4. Business invariants must be AI-independent  
5. Observability must increase with automation  
6. Calibration prevents system decay  
7. Context must be curated, not raw  
8. **Governance > intelligence**

---

## 1️⃣8️⃣ Architectural Boundary Summary

**Command path:**

```
LLM
  ↓
Orchestration Layer
  ↓
Schema Validation
  ↓
Domain Invariants
  ↓
Execution
```

**Advisory path (parallel):**

```
Domain Event
  ↓
Structured Summary
  ↓
LLM Advisory
  ↓
Calibration Layer
  ↓
Compliance Workflow
```

---

## 1️⃣9️⃣ What We Have Built So Far

You now understand:

- Controlled agent execution
- Tool safety
- Strict schema enforcement
- Decimal precision handling
- Invariant-driven design
- Event-driven AI observer pattern
- Structured RAG architecture
- Risk scoring calibration
- Drift-resilient AI systems
- Hybrid deterministic + probabilistic systems

**This is enterprise-grade AI system design.**

---

*Updated: February 2026*
