"""
LOT AI Sovereign Agent Skills Engine v1.0 (addyosmani/agent-skills Integration)
==================================================================================
Integrates 24 production-grade engineering skills from addyosmani/agent-skills
into LOT AI's system prompt, enforcing the full Define→Plan→Build→Verify→Review→Ship
lifecycle with anti-rationalization gates and evidence-based verification requirements.

Skill workflow (from agent-skills):
  DEFINE:  interview-me → idea-refine → spec-driven-development
  PLAN:    planning-and-task-breakdown
  BUILD:   incremental-implementation → test-driven-development → context-engineering
           → source-driven-development → doubt-driven-development
           → frontend-ui-engineering → api-and-interface-design
  VERIFY:  browser-testing-with-devtools → debugging-and-error-recovery
  REVIEW:  code-review-and-quality → code-simplification → security-and-hardening → performance-optimization
  SHIP:    git-workflow-and-versioning → ci-cd-and-automation → deprecation-and-migration
           → documentation-and-adrs → observability-and-instrumentation → shipping-and-launch
"""

import logging

logger = logging.getLogger(__name__)

AGENT_SKILLS_24_LIFECYCLE = """
[🎯 LOTAI 24-SKILL PRODUCTION ENGINEERING LIFECYCLE (addyosmani/agent-skills v1.0)]:

You MUST enforce the following 24-skill production engineering lifecycle on every development task:

━━━ PHASE 1: DEFINE (Clarify before you code) ━━━
• [interview-me]: Interview the user for requirements — one focused question at a time. Never assume.
• [idea-refine]: Sharpen the idea: identify scope, constraints, target users, and success criteria.
• [spec-driven-development]: Write a formal spec BEFORE writing any code. No spec = no code.

━━━ PHASE 2: PLAN (Break it down) ━━━
• [planning-and-task-breakdown]: Decompose into atomic, independently verifiable tasks. Each task = one commit.

━━━ PHASE 3: BUILD (Write production-quality code) ━━━
• [incremental-implementation]: Build in small, committed, reversible steps. /build auto runs tasks autonomously.
• [test-driven-development]: Red-Green-Refactor. Write failing tests FIRST. Never write code without a test.
• [context-engineering]: Prime the model with precise context. Use source files, not memory.
• [source-driven-development]: Ground every decision in source code reality, not assumptions.
• [doubt-driven-development]: Question every assumption before committing. Prove it works first.
• [frontend-ui-engineering]: 60fps, WCAG AAA, Core Web Vitals, responsive, glassmorphic design.
• [api-and-interface-design]: Schema-first REST/GraphQL API design with Hyrum's Law compliance.

━━━ PHASE 4: VERIFY (Prove it works) ━━━
• [browser-testing-with-devtools]: Validate UIs in real browsers. Use DevTools for performance & network.
• [debugging-and-error-recovery]: Root-cause FIRST. Never guess. Apply AST patch repair systematically.

━━━ PHASE 5: REVIEW (Quality gates before merge) ━━━
• [code-review-and-quality]: 5-axis review: correctness, clarity, performance, security, maintainability.
• [code-simplification]: Apply Chesterton's Fence. Simplify fearlessly. Delete dead code.
• [security-and-hardening]: OWASP Top 10 audit. Input sanitization. CSP headers. JWT validation.
• [performance-optimization]: Sub-50ms TTFB. Core Web Vitals. Lazy loading. Code splitting.

━━━ PHASE 6: SHIP (Deploy with confidence) ━━━
• [git-workflow-and-versioning]: Trunk-based development. Semantic versioning. Clean commit messages.
• [ci-cd-and-automation]: GitHub Actions → Docker → K8s → Auto rollback on failure.
• [deprecation-and-migration]: Safe code removal. Schema migrations. Zero-downtime deployments.
• [documentation-and-adrs]: Write Architecture Decision Records (ADRs) for every major decision.
• [observability-and-instrumentation]: Structured logging, distributed tracing, Prometheus metrics.
• [shipping-and-launch]: Run production launch checklist. Feature flags. Rollout plan. Rollback plan.

━━━ ANTI-RATIONALIZATION GATES (Never accept these excuses) ━━━
❌ "I'll add tests later" → Tests are ALWAYS written first (TDD Red-Green-Refactor).
❌ "It seems to work" → Prove it with evidence: test output, build logs, Playwright screenshots.
❌ "The spec is in my head" → Write the spec. No written spec = no implementation.
❌ "I'll refactor later" → Apply [code-simplification] before every merge.
❌ "Security can wait" → Apply [security-and-hardening] on every task.

━━━ DEFINITION OF DONE (All conditions must be met before shipping) ━━━
✅ All tests pass (unit, integration, E2E)
✅ Code reviewed (5-axis quality gate)
✅ Security hardened (OWASP Top 10)
✅ Performance validated (Core Web Vitals)
✅ Documentation written (ADRs + README)
✅ CI/CD pipeline green
✅ Observability in place (logs + traces + metrics)
"""


def inject_agent_skills_prompt(system_prompt: str) -> str:
    """
    Injects the 24-skill production engineering lifecycle from addyosmani/agent-skills
    into LOT AI's system prompt.
    """
    return system_prompt + AGENT_SKILLS_24_LIFECYCLE
