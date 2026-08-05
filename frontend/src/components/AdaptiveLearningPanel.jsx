import React, { useState, useEffect, useRef } from "react";

/**
 * LOT AI Adaptive Learning Panel v1.0
 * ======================================
 * Real-time learning progress dashboard showing:
 *   • User expertise level & Bloom's Taxonomy tier
 *   • Domain mastery scores across all knowledge areas
 *   • Forgetting curve spaced repetition schedule
 *   • Skill progression ring animation
 *
 * Design: Glassmorphic dark panel with micro-animations
 * Inspired by: open-design (78 UI systems) + impeccable (41 UI rules)
 */

// ─────────────────── Bloom's Level Metadata ──────────────────────────────

const BLOOM_LEVELS = {
  1: { name: "Remember",    color: "#10b981", icon: "💡", desc: "Recall & recognition" },
  2: { name: "Understand",  color: "#3b82f6", icon: "🔵", desc: "Explain & paraphrase" },
  3: { name: "Apply",       color: "#f59e0b", icon: "🟡", desc: "Implement & execute" },
  4: { name: "Analyse",     color: "#f97316", icon: "🟠", desc: "Compare & differentiate" },
  5: { name: "Evaluate",    color: "#ef4444", icon: "🔴", desc: "Critique & justify" },
  6: { name: "Create",      color: "#8b5cf6", icon: "🟣", desc: "Design & build novel solutions" },
};

// ─────────────────── Sub-Components ──────────────────────────────────────

function BloomRing({ level = 3, size = 80 }) {
  const meta = BLOOM_LEVELS[level] || BLOOM_LEVELS[3];
  const radius = (size - 12) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (level / 6) * circumference;

  return (
    <div style={{ position: "relative", width: size, height: size, flexShrink: 0 }}>
      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
        {/* Track */}
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
          stroke="rgba(255,255,255,0.07)" strokeWidth={8} />
        {/* Progress */}
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
          stroke={meta.color} strokeWidth={8}
          strokeDasharray={`${progress} ${circumference}`}
          strokeLinecap="round"
          style={{ transition: "stroke-dasharray 1.2s cubic-bezier(0.34, 1.56, 0.64, 1)", filter: `drop-shadow(0 0 6px ${meta.color}88)` }}
        />
      </svg>
      <div style={{
        position: "absolute", inset: 0, display: "flex",
        flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 1
      }}>
        <span style={{ fontSize: 18 }}>{meta.icon}</span>
        <span style={{ fontSize: 9, color: meta.color, fontWeight: 700, letterSpacing: "0.04em" }}>
          L{level}
        </span>
      </div>
    </div>
  );
}

function MasteryBar({ domain, score = 0, color = "#8b5cf6" }) {
  const pct = Math.round(score * 100);
  const label = domain.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
  return (
    <div style={{ marginBottom: 6 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
        <span style={{ fontSize: 10, color: "rgba(255,255,255,0.7)", fontFamily: "inherit" }}>{label}</span>
        <span style={{ fontSize: 10, color, fontWeight: 700 }}>{pct}%</span>
      </div>
      <div style={{ height: 4, borderRadius: 4, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
        <div style={{
          height: "100%", width: `${pct}%`, borderRadius: 4,
          background: `linear-gradient(90deg, ${color}99, ${color})`,
          transition: "width 1.2s cubic-bezier(0.34, 1.56, 0.64, 1)",
          boxShadow: `0 0 6px ${color}55`
        }} />
      </div>
    </div>
  );
}

function ConceptReviewCard({ concept, mastery, isOverdue = false }) {
  const pct = Math.round(mastery * 100);
  const label = concept.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
  return (
    <div style={{
      padding: "8px 12px", borderRadius: 8, marginBottom: 6,
      background: isOverdue ? "rgba(239,68,68,0.12)" : "rgba(255,255,255,0.05)",
      border: `1px solid ${isOverdue ? "rgba(239,68,68,0.3)" : "rgba(255,255,255,0.08)"}`,
      display: "flex", alignItems: "center", gap: 10, transition: "all 0.3s ease"
    }}>
      <span style={{ fontSize: 14 }}>{isOverdue ? "⏰" : "📚"}</span>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 11, color: "rgba(255,255,255,0.9)", fontWeight: 600 }}>{label}</div>
        <div style={{ fontSize: 9, color: "rgba(255,255,255,0.5)", marginTop: 2 }}>
          Mastery: {pct}%  {isOverdue ? "— Review now!" : ""}
        </div>
      </div>
      <div style={{
        width: 32, height: 32, borderRadius: "50%",
        background: `conic-gradient(#8b5cf6 ${pct * 3.6}deg, rgba(255,255,255,0.08) 0deg)`,
        display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0
      }}>
        <div style={{ width: 22, height: 22, borderRadius: "50%", background: "#0f1117" }} />
      </div>
    </div>
  );
}

// ─────────────────── Main Panel Component ────────────────────────────────

export default function AdaptiveLearningPanel({ isOpen, onClose }) {
  const [bloomLevel, setBloomLevel] = useState(3);
  const [overallLevel, setOverallLevel] = useState("intermediate");
  const [sessionCount, setSessionCount] = useState(1);
  const [domains, setDomains] = useState([
    { domain: "python", score: 0.72 },
    { domain: "react", score: 0.65 },
    { domain: "system_design", score: 0.58 },
    { domain: "machine_learning", score: 0.41 },
    { domain: "docker", score: 0.55 },
  ]);
  const [reviewConcepts, setReviewConcepts] = useState([
    { concept: "async_await", mastery: 0.62, isOverdue: true },
    { concept: "react_hooks", mastery: 0.48, isOverdue: false },
    { concept: "sql_joins", mastery: 0.35, isOverdue: true },
  ]);
  const [learningSummary, setLearningSummary] = useState({
    total_concepts: 24,
    mastered_count: 6,
    learning_count: 12,
    new_count: 6,
    average_mastery_pct: 58,
  });
  const [animIn, setAnimIn] = useState(false);
  const panelRef = useRef(null);

  const bloomMeta = BLOOM_LEVELS[bloomLevel] || BLOOM_LEVELS[3];

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => setAnimIn(true), 10);
    } else {
      setAnimIn(false);
    }
  }, [isOpen]);

  // Click outside to close
  useEffect(() => {
    function handleClick(e) {
      if (panelRef.current && !panelRef.current.contains(e.target)) {
        onClose?.();
      }
    }
    if (isOpen) document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const levelColors = { beginner: "#10b981", intermediate: "#3b82f6", advanced: "#f97316", expert: "#8b5cf6" };
  const levelColor = levelColors[overallLevel] || "#8b5cf6";

  return (
    <div style={{
      position: "fixed", inset: 0, zIndex: 9000,
      background: "rgba(0,0,0,0.55)", backdropFilter: "blur(6px)",
      display: "flex", alignItems: "flex-start", justifyContent: "flex-end",
      padding: "80px 16px 16px 16px",
      transition: "opacity 0.3s ease",
      opacity: animIn ? 1 : 0,
    }}>
      <div ref={panelRef} style={{
        width: 340, maxHeight: "calc(100vh - 100px)",
        background: "linear-gradient(145deg, rgba(15,17,23,0.97) 0%, rgba(20,24,36,0.97) 100%)",
        border: "1px solid rgba(139,92,246,0.25)",
        borderRadius: 16, boxShadow: "0 24px 80px rgba(0,0,0,0.7), 0 0 0 1px rgba(139,92,246,0.1)",
        overflow: "hidden", display: "flex", flexDirection: "column",
        fontFamily: "'Inter', -apple-system, sans-serif",
        transform: animIn ? "translateX(0) scale(1)" : "translateX(30px) scale(0.97)",
        transition: "transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.3s ease",
        opacity: animIn ? 1 : 0,
      }}>

        {/* Header */}
        <div style={{
          padding: "16px 20px", borderBottom: "1px solid rgba(255,255,255,0.06)",
          background: "linear-gradient(135deg, rgba(139,92,246,0.15) 0%, rgba(59,130,246,0.08) 100%)",
          display: "flex", justifyContent: "space-between", alignItems: "center"
        }}>
          <div>
            <div style={{ fontSize: 13, fontWeight: 700, color: "#fff", letterSpacing: "-0.01em" }}>
              🧠 Adaptive Learning
            </div>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.5)", marginTop: 2 }}>
              Personalised by LOT AI ASI-OS
            </div>
          </div>
          <button onClick={onClose} style={{
            background: "rgba(255,255,255,0.07)", border: "none", borderRadius: 8,
            color: "rgba(255,255,255,0.6)", cursor: "pointer", fontSize: 14,
            width: 28, height: 28, display: "flex", alignItems: "center", justifyContent: "center",
            transition: "all 0.2s ease"
          }} onMouseEnter={e => e.target.style.background = "rgba(255,255,255,0.14)"}
             onMouseLeave={e => e.target.style.background = "rgba(255,255,255,0.07)"}>
            ✕
          </button>
        </div>

        {/* Scrollable content */}
        <div style={{ overflowY: "auto", padding: "16px 20px", flex: 1,
          scrollbarWidth: "thin", scrollbarColor: "rgba(139,92,246,0.3) transparent" }}>

          {/* Bloom's Level + Overall */}
          <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 20 }}>
            <BloomRing level={bloomLevel} size={76} />
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 11, color: "rgba(255,255,255,0.45)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                Cognitive Tier
              </div>
              <div style={{ fontSize: 16, fontWeight: 800, color: bloomMeta.color, lineHeight: 1.2, marginTop: 2 }}>
                {bloomMeta.name}
              </div>
              <div style={{ fontSize: 10, color: "rgba(255,255,255,0.5)", marginTop: 3 }}>{bloomMeta.desc}</div>
              <div style={{
                display: "inline-block", marginTop: 6, padding: "2px 10px",
                background: `${levelColor}22`, border: `1px solid ${levelColor}44`,
                borderRadius: 20, fontSize: 10, color: levelColor, fontWeight: 700,
                textTransform: "uppercase", letterSpacing: "0.06em"
              }}>
                {overallLevel}
              </div>
            </div>
          </div>

          {/* Learning Summary Stats */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, marginBottom: 20 }}>
            {[
              { label: "Mastered", value: learningSummary.mastered_count, color: "#10b981" },
              { label: "Learning", value: learningSummary.learning_count, color: "#f59e0b" },
              { label: "New", value: learningSummary.new_count, color: "#3b82f6" },
            ].map(({ label, value, color }) => (
              <div key={label} style={{
                padding: "10px 8px", borderRadius: 10, textAlign: "center",
                background: `${color}11`, border: `1px solid ${color}25`
              }}>
                <div style={{ fontSize: 20, fontWeight: 800, color }}>{value}</div>
                <div style={{ fontSize: 9, color: "rgba(255,255,255,0.5)", marginTop: 2, textTransform: "uppercase", letterSpacing: "0.06em" }}>{label}</div>
              </div>
            ))}
          </div>

          {/* Overall mastery progress */}
          <div style={{ marginBottom: 20 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
              <span style={{ fontSize: 11, color: "rgba(255,255,255,0.6)", fontWeight: 600 }}>Overall Mastery</span>
              <span style={{ fontSize: 13, color: "#8b5cf6", fontWeight: 800 }}>{learningSummary.average_mastery_pct}%</span>
            </div>
            <div style={{ height: 6, borderRadius: 6, background: "rgba(255,255,255,0.08)" }}>
              <div style={{
                height: "100%", width: `${learningSummary.average_mastery_pct}%`, borderRadius: 6,
                background: "linear-gradient(90deg, #8b5cf6, #3b82f6)",
                transition: "width 1.5s cubic-bezier(0.34, 1.56, 0.64, 1)",
                boxShadow: "0 0 12px rgba(139,92,246,0.5)"
              }} />
            </div>
          </div>

          {/* Domain Mastery Bars */}
          <div style={{ marginBottom: 20 }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: "rgba(255,255,255,0.6)", textTransform: "uppercase",
              letterSpacing: "0.08em", marginBottom: 10 }}>
              Top Domains
            </div>
            {domains.map(({ domain, score }, i) => (
              <MasteryBar key={domain} domain={domain} score={score}
                color={["#8b5cf6","#3b82f6","#10b981","#f59e0b","#ef4444"][i % 5]} />
            ))}
          </div>

          {/* Spaced Repetition Review Queue */}
          {reviewConcepts.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: "rgba(255,255,255,0.6)", textTransform: "uppercase",
                letterSpacing: "0.08em", marginBottom: 10 }}>
                📅 Review Queue · {reviewConcepts.filter(c => c.isOverdue).length} due now
              </div>
              {reviewConcepts.map(({ concept, mastery, isOverdue }) => (
                <ConceptReviewCard key={concept} concept={concept} mastery={mastery} isOverdue={isOverdue} />
              ))}
            </div>
          )}

          {/* Sessions count */}
          <div style={{ padding: "10px 14px", borderRadius: 10,
            background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)",
            display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <span style={{ fontSize: 11, color: "rgba(255,255,255,0.5)" }}>LOT AI sessions</span>
            <span style={{ fontSize: 14, fontWeight: 800, color: "#8b5cf6" }}>{sessionCount}</span>
          </div>
        </div>

        {/* Footer */}
        <div style={{ padding: "12px 20px", borderTop: "1px solid rgba(255,255,255,0.06)",
          display: "flex", gap: 8 }}>
          <button style={{
            flex: 1, padding: "8px 0", borderRadius: 10, border: "1px solid rgba(139,92,246,0.3)",
            background: "rgba(139,92,246,0.12)", color: "#a78bfa", fontSize: 11, fontWeight: 700,
            cursor: "pointer", transition: "all 0.2s ease", fontFamily: "inherit"
          }}
            onMouseEnter={e => e.currentTarget.style.background = "rgba(139,92,246,0.24)"}
            onMouseLeave={e => e.currentTarget.style.background = "rgba(139,92,246,0.12)"}>
            Quick Recall
          </button>
          <button style={{
            flex: 1, padding: "8px 0", borderRadius: 10, border: "1px solid rgba(59,130,246,0.3)",
            background: "rgba(59,130,246,0.12)", color: "#60a5fa", fontSize: 11, fontWeight: 700,
            cursor: "pointer", transition: "all 0.2s ease", fontFamily: "inherit"
          }}
            onMouseEnter={e => e.currentTarget.style.background = "rgba(59,130,246,0.24)"}
            onMouseLeave={e => e.currentTarget.style.background = "rgba(59,130,246,0.12)"}>
            View All
          </button>
        </div>
      </div>
    </div>
  );
}
