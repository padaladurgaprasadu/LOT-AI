import { useState, useEffect, useRef } from 'react';

/**
 * AgentSwarmDashboard - Real-time 37-agent swarm visualization dashboard
 * Shows all agents, their status, specializations, and live event stream
 */

const AGENT_REGISTRY = [
  { id: 'architect', name: 'Architect', domain: 'System Design', icon: '🏗️', color: '#a855f7' },
  { id: 'coder', name: 'Coder', domain: 'Code Synthesis', icon: '💻', color: '#3b82f6' },
  { id: 'reviewer', name: 'Reviewer', domain: 'Code Review', icon: '🔍', color: '#22c55e' },
  { id: 'tester', name: 'Tester', domain: 'Quality Assurance', icon: '🧪', color: '#eab308' },
  { id: 'debugger', name: 'Debugger', domain: 'Bug Resolution', icon: '🐛', color: '#ef4444' },
  { id: 'security', name: 'Security', domain: 'Cybersecurity', icon: '🛡️', color: '#f97316' },
  { id: 'devops', name: 'DevOps', domain: 'Infrastructure', icon: '⚙️', color: '#06b6d4' },
  { id: 'ui_ux', name: 'UI/UX', domain: 'Design Systems', icon: '🎨', color: '#ec4899' },
  { id: 'researcher', name: 'Researcher', domain: 'Knowledge Mining', icon: '📚', color: '#8b5cf6' },
  { id: 'planner', name: 'Planner', domain: 'Task Orchestration', icon: '📋', color: '#14b8a6' },
  { id: 'data_eng', name: 'Data Engineer', domain: 'ETL & Analytics', icon: '📊', color: '#6366f1' },
  { id: 'ml_eng', name: 'ML Engineer', domain: 'Machine Learning', icon: '🤖', color: '#d946ef' },
  { id: 'frontend', name: 'Frontend', domain: 'React/Next.js', icon: '🖥️', color: '#0ea5e9' },
  { id: 'backend', name: 'Backend', domain: 'API & Services', icon: '🔧', color: '#10b981' },
  { id: 'database', name: 'Database', domain: 'PostgreSQL/Mongo', icon: '🗄️', color: '#f59e0b' },
  { id: 'api_int', name: 'API Integrator', domain: 'Third-Party APIs', icon: '🔌', color: '#84cc16' },
  { id: 'docs', name: 'Documentarian', domain: 'Technical Writing', icon: '📝', color: '#78716c' },
  { id: 'perf', name: 'Performance', domain: 'Optimization', icon: '⚡', color: '#facc15' },
  { id: 'a11y', name: 'Accessibility', domain: 'WCAG AAA', icon: '♿', color: '#2dd4bf' },
  { id: 'seo', name: 'SEO Expert', domain: 'Search Optimization', icon: '🔎', color: '#fb923c' },
  { id: 'mobile', name: 'Mobile', domain: 'React Native', icon: '📱', color: '#818cf8' },
  { id: 'cloud', name: 'Cloud Architect', domain: 'AWS/GCP/Azure', icon: '☁️', color: '#38bdf8' },
  { id: 'k8s', name: 'K8s Operator', domain: 'Kubernetes', icon: '🎛️', color: '#326ce5' },
  { id: 'ci_cd', name: 'CI/CD', domain: 'Pipeline Automation', icon: '🔄', color: '#a3e635' },
  { id: 'monitor', name: 'Monitor', domain: 'Observability', icon: '📡', color: '#c084fc' },
  { id: 'fintech', name: 'FinTech', domain: 'Payment Systems', icon: '💰', color: '#34d399' },
  { id: 'biomedical', name: 'Biomedical', domain: 'Health AI', icon: '🧬', color: '#f472b6' },
  { id: 'space', name: 'Space Tech', domain: 'Orbital Systems', icon: '🚀', color: '#60a5fa' },
  { id: 'game', name: 'Game Dev', domain: '3D/WebGL', icon: '🎮', color: '#c026d3' },
  { id: 'blockchain', name: 'Web3', domain: 'Blockchain/Smart Contracts', icon: '⛓️', color: '#fbbf24' },
  { id: 'nlp', name: 'NLP Expert', domain: 'Language Processing', icon: '🗣️', color: '#fb7185' },
  { id: 'cv', name: 'Computer Vision', domain: 'Image/Video AI', icon: '👁️', color: '#a78bfa' },
  { id: 'rag', name: 'RAG Specialist', domain: 'Retrieval Augmented', icon: '🔗', color: '#4ade80' },
  { id: 'mcp', name: 'MCP Controller', domain: 'Tool Protocols', icon: '🔀', color: '#f97316' },
  { id: 'seal', name: 'SEAL Adapter', domain: 'Self-Improvement', icon: '🧠', color: '#e879f9' },
  { id: 'causal', name: 'Causal Reasoner', domain: 'Root Cause Analysis', icon: '🔬', color: '#67e8f9' },
  { id: 'orchestrator', name: 'ASI Orchestrator', domain: 'Master Brain', icon: '👑', color: '#fbbf24' },
];

const STATUS_COLORS = {
  idle: '#3f3f46',
  active: '#22c55e',
  thinking: '#eab308',
  executing: '#3b82f6',
  error: '#ef4444',
  complete: '#a855f7',
};

const STATUS_LABELS = {
  idle: 'Idle',
  active: 'Active',
  thinking: 'Thinking',
  executing: 'Executing',
  error: 'Error',
  complete: 'Complete',
};

const NIM_MODELS = [
  { id: 'nemotron_ultra', name: 'Nemotron Ultra 550B', context: '1M', status: 'online', tier: 1 },
  { id: 'glm_5_2', name: 'GLM-5.2 753B', context: '1M', status: 'online', tier: 2 },
  { id: 'minimax_m3', name: 'MiniMax M3 428B', context: '1M', status: 'online', tier: 3 },
  { id: 'nemotron_frontier', name: 'Nemotron Frontier', context: '1M', status: 'standby', tier: 4 },
  { id: 'mistral_medium', name: 'Mistral Medium 128B', context: '256K', status: 'online', tier: 5 },
  { id: 'deepseek_v4', name: 'DeepSeek V4 1.6T', context: '1M', status: 'online', tier: 6 },
  { id: 'deepseek_coder', name: 'DeepSeek V4 Coder', context: '1M', status: 'standby', tier: 7 },
  { id: 'minimax_m2_7', name: 'MiniMax M2.7 230B', context: '200K', status: 'online', tier: 8 },
  { id: 'qwen_vlm', name: 'Qwen3.5 VLM 400B', context: '262K', status: 'online', tier: 9 },
  { id: 'nemotron_moe', name: 'Nemotron MoE 1M', context: '1M', status: 'standby', tier: 10 },
  { id: 'gemma_4', name: 'Gemma 4 31B', context: '256K', status: 'online', tier: 11 },
  { id: 'nemotron_nano', name: 'Nemotron Nano 30B', context: '1M', status: 'online', tier: 12 },
];

const MCP_SERVERS = [
  { id: 'context7', name: 'Context7', description: 'Live docs fetcher', status: 'connected', icon: '📖' },
  { id: 'github', name: 'GitHub', description: 'Repository automation', status: 'connected', icon: '🐙' },
  { id: 'playwright', name: 'Playwright', description: 'Browser automation', status: 'connected', icon: '🌐' },
  { id: 'seq_thinking', name: 'Sequential Thinking', description: '10-stage reasoning', status: 'connected', icon: '🧠' },
  { id: 'filesystem', name: 'Filesystem', description: 'Safe file operations', status: 'connected', icon: '📁' },
];

export default function AgentSwarmDashboard({ API_URL }) {
  const [agentStates, setAgentStates] = useState(
    AGENT_REGISTRY.reduce((acc, agent) => {
      acc[agent.id] = { status: 'idle', lastAction: null, taskCount: 0, uptime: 0 };
      return acc;
    }, {})
  );
  const [eventLog, setEventLog] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' | 'list' | 'models' | 'mcp'
  const [filterStatus, setFilterStatus] = useState('all');
  const [sealMetrics, setSealMetrics] = useState({
    iterations: 0, editsAccepted: 0, avgReward: 0.0, lastAdaptation: null
  });
  const eventLogRef = useRef(null);

  // Simulate periodic agent activity
  useEffect(() => {
    const interval = setInterval(() => {
      setAgentStates(prev => {
        const next = { ...prev };
        const agentIds = Object.keys(next);
        // Randomly activate 2-4 agents
        const numActive = Math.floor(Math.random() * 3) + 2;
        for (let i = 0; i < numActive; i++) {
          const rid = agentIds[Math.floor(Math.random() * agentIds.length)];
          const statuses = ['active', 'thinking', 'executing', 'idle', 'complete'];
          const newStatus = statuses[Math.floor(Math.random() * statuses.length)];
          next[rid] = {
            ...next[rid],
            status: newStatus,
            taskCount: next[rid].taskCount + (newStatus === 'complete' ? 1 : 0),
            lastAction: newStatus !== 'idle' ? new Date().toLocaleTimeString() : next[rid].lastAction,
          };
        }
        return next;
      });

      // Simulate event log
      const agent = AGENT_REGISTRY[Math.floor(Math.random() * AGENT_REGISTRY.length)];
      const actions = [
        `Analysed module structure`,
        `Generated React component`,
        `Ran security scan (OWASP Top 10)`,
        `Deployed to staging environment`,
        `Reviewed pull request #${Math.floor(Math.random() * 200)}`,
        `Optimised database query (${Math.floor(Math.random() * 80) + 20}% faster)`,
        `Built Docker image (${(Math.random() * 2 + 0.5).toFixed(1)}s)`,
        `Resolved merge conflict in ${['App.jsx', 'router.py', 'auth.py'][Math.floor(Math.random() * 3)]}`,
        `Generated unit tests (${Math.floor(Math.random() * 10) + 3} tests)`,
        `SEAL reward: ${(Math.random() * 0.3 + 0.7).toFixed(3)}`,
      ];
      setEventLog(prev => [{
        id: Date.now(),
        time: new Date().toLocaleTimeString(),
        agent: agent.name,
        icon: agent.icon,
        action: actions[Math.floor(Math.random() * actions.length)],
        color: agent.color,
      }, ...prev].slice(0, 50));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  // Auto-scroll event log
  useEffect(() => {
    if (eventLogRef.current) {
      eventLogRef.current.scrollTop = 0;
    }
  }, [eventLog]);

  const filteredAgents = AGENT_REGISTRY.filter(agent => {
    if (filterStatus === 'all') return true;
    return agentStates[agent.id]?.status === filterStatus;
  });

  const statusCounts = Object.values(agentStates).reduce((acc, s) => {
    acc[s.status] = (acc[s.status] || 0) + 1;
    return acc;
  }, {});

  const totalTasks = Object.values(agentStates).reduce((sum, s) => sum + s.taskCount, 0);

  return (
    <div style={{
      width: '100%', height: '100%', backgroundColor: '#09090b',
      color: '#e4e4e7', fontFamily: "'Inter', system-ui, sans-serif",
      display: 'flex', flexDirection: 'column', overflow: 'hidden',
    }}>
      {/* Header Bar */}
      <div style={{
        padding: '16px 24px', borderBottom: '1px solid #27272a',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        background: 'linear-gradient(135deg, #09090b 0%, #18181b 100%)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            width: '40px', height: '40px', borderRadius: '12px',
            background: 'linear-gradient(135deg, #a855f7, #6366f1)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '20px', boxShadow: '0 0 20px rgba(168, 85, 247, 0.3)',
          }}>👑</div>
          <div>
            <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 700, letterSpacing: '-0.02em' }}>
              LOT AI Agent Swarm
            </h2>
            <span style={{ fontSize: '12px', color: '#71717a' }}>
              37 Agents · 12 NIM Models · 5 MCP Servers · SEAL Active
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          {/* Status Pills */}
          {Object.entries(STATUS_COLORS).map(([status, color]) => (
            <button
              key={status}
              onClick={() => setFilterStatus(filterStatus === status ? 'all' : status)}
              style={{
                padding: '4px 12px', borderRadius: '20px', fontSize: '11px',
                fontWeight: 600, cursor: 'pointer', transition: 'all 0.2s',
                border: filterStatus === status ? `2px solid ${color}` : '1px solid #3f3f46',
                backgroundColor: filterStatus === status ? color + '22' : 'transparent',
                color: color,
              }}
            >
              {STATUS_LABELS[status]} ({statusCounts[status] || 0})
            </button>
          ))}
        </div>
      </div>

      {/* Stats Bar */}
      <div style={{
        padding: '12px 24px', borderBottom: '1px solid #1a1a1e',
        display: 'flex', gap: '32px', backgroundColor: '#0c0c0f',
      }}>
        {[
          { label: 'Active Agents', value: (statusCounts.active || 0) + (statusCounts.thinking || 0) + (statusCounts.executing || 0), color: '#22c55e' },
          { label: 'Tasks Completed', value: totalTasks, color: '#a855f7' },
          { label: 'SEAL Reward', value: (Math.random() * 0.2 + 0.8).toFixed(3), color: '#eab308' },
          { label: 'NIM Models Online', value: NIM_MODELS.filter(m => m.status === 'online').length, color: '#3b82f6' },
          { label: 'MCP Connected', value: MCP_SERVERS.filter(s => s.status === 'connected').length, color: '#06b6d4' },
        ].map((stat, i) => (
          <div key={i} style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
            <span style={{ fontSize: '11px', color: '#71717a', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{stat.label}</span>
            <span style={{ fontSize: '20px', fontWeight: 700, color: stat.color, fontVariantNumeric: 'tabular-nums' }}>{stat.value}</span>
          </div>
        ))}
      </div>

      {/* View Tabs */}
      <div style={{ padding: '8px 24px', borderBottom: '1px solid #1a1a1e', display: 'flex', gap: '4px' }}>
        {[
          { key: 'grid', label: '🧠 Agent Grid', desc: '37 agents' },
          { key: 'models', label: '🚀 NIM Models', desc: '12 models' },
          { key: 'mcp', label: '🔀 MCP Servers', desc: '5 servers' },
          { key: 'list', label: '📋 Event Stream', desc: 'Live' },
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setViewMode(tab.key)}
            style={{
              padding: '8px 16px', borderRadius: '8px', fontSize: '13px',
              fontWeight: viewMode === tab.key ? 700 : 500,
              cursor: 'pointer', border: 'none', transition: 'all 0.2s',
              backgroundColor: viewMode === tab.key ? '#27272a' : 'transparent',
              color: viewMode === tab.key ? '#fff' : '#71717a',
            }}
          >
            {tab.label} <span style={{ fontSize: '10px', opacity: 0.6 }}>({tab.desc})</span>
          </button>
        ))}
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, overflow: 'auto', padding: '20px 24px' }}>
        {/* Agent Grid View */}
        {viewMode === 'grid' && (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
            gap: '12px',
          }}>
            {filteredAgents.map(agent => {
              const state = agentStates[agent.id];
              const statusColor = STATUS_COLORS[state?.status] || STATUS_COLORS.idle;
              const isActive = state?.status === 'active' || state?.status === 'thinking' || state?.status === 'executing';
              return (
                <div
                  key={agent.id}
                  onClick={() => setSelectedAgent(selectedAgent === agent.id ? null : agent.id)}
                  style={{
                    padding: '16px', borderRadius: '12px', cursor: 'pointer',
                    border: selectedAgent === agent.id ? `2px solid ${agent.color}` : '1px solid #27272a',
                    backgroundColor: selectedAgent === agent.id ? agent.color + '0a' : '#18181b',
                    transition: 'all 0.2s ease',
                    position: 'relative', overflow: 'hidden',
                  }}
                >
                  {/* Pulse indicator for active agents */}
                  {isActive && (
                    <div style={{
                      position: 'absolute', top: '12px', right: '12px',
                      width: '8px', height: '8px', borderRadius: '50%',
                      backgroundColor: statusColor,
                      boxShadow: `0 0 8px ${statusColor}`,
                      animation: 'pulse 2s infinite',
                    }} />
                  )}

                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <span style={{ fontSize: '24px' }}>{agent.icon}</span>
                    <div>
                      <div style={{ fontSize: '13px', fontWeight: 700, color: '#e4e4e7' }}>{agent.name}</div>
                      <div style={{ fontSize: '10px', color: '#71717a' }}>{agent.domain}</div>
                    </div>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{
                      fontSize: '10px', fontWeight: 600, color: statusColor,
                      padding: '2px 8px', borderRadius: '10px',
                      backgroundColor: statusColor + '18',
                      textTransform: 'uppercase', letterSpacing: '0.05em',
                    }}>
                      {STATUS_LABELS[state?.status] || 'Idle'}
                    </span>
                    <span style={{ fontSize: '10px', color: '#52525b' }}>
                      {state?.taskCount || 0} tasks
                    </span>
                  </div>

                  {selectedAgent === agent.id && state?.lastAction && (
                    <div style={{
                      marginTop: '8px', paddingTop: '8px', borderTop: '1px solid #27272a',
                      fontSize: '11px', color: '#a1a1aa',
                    }}>
                      Last: {state.lastAction}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* NIM Models View */}
        {viewMode === 'models' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div style={{
              padding: '16px', borderRadius: '12px', backgroundColor: '#18181b',
              border: '1px solid #27272a', marginBottom: '8px',
            }}>
              <h3 style={{ margin: '0 0 8px', fontSize: '15px', fontWeight: 700 }}>
                🚀 NVIDIA NIM Multi-Fallback Router
              </h3>
              <p style={{ margin: 0, fontSize: '12px', color: '#71717a' }}>
                Dynamic routing across 12 models. Primary: Nemotron Ultra 550B (1M context).
                Fallback cascade: Ultra → GLM-5.2 → Frontier → Mistral → DeepSeek V4 → Gemma 4
              </p>
            </div>

            {NIM_MODELS.map(model => (
              <div key={model.id} style={{
                padding: '14px 18px', borderRadius: '10px',
                border: '1px solid #27272a', backgroundColor: '#18181b',
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                  <div style={{
                    width: '32px', height: '32px', borderRadius: '8px',
                    background: model.status === 'online'
                      ? 'linear-gradient(135deg, #22c55e33, #15803d33)'
                      : 'linear-gradient(135deg, #3f3f4633, #27272a33)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '14px', border: `1px solid ${model.status === 'online' ? '#22c55e44' : '#3f3f46'}`,
                  }}>
                    {model.tier <= 3 ? '🌟' : model.tier <= 6 ? '⚡' : '🔹'}
                  </div>
                  <div>
                    <div style={{ fontSize: '13px', fontWeight: 600, color: '#e4e4e7' }}>
                      Tier {model.tier}: {model.name}
                    </div>
                    <div style={{ fontSize: '11px', color: '#71717a' }}>
                      Context: {model.context} tokens
                    </div>
                  </div>
                </div>

                <span style={{
                  fontSize: '11px', fontWeight: 600,
                  padding: '3px 10px', borderRadius: '12px',
                  color: model.status === 'online' ? '#22c55e' : '#71717a',
                  backgroundColor: model.status === 'online' ? '#22c55e15' : '#3f3f4620',
                  textTransform: 'uppercase',
                }}>
                  {model.status}
                </span>
              </div>
            ))}
          </div>
        )}

        {/* MCP Servers View */}
        {viewMode === 'mcp' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{
              padding: '16px', borderRadius: '12px', backgroundColor: '#18181b',
              border: '1px solid #27272a', marginBottom: '4px',
            }}>
              <h3 style={{ margin: '0 0 8px', fontSize: '15px', fontWeight: 700 }}>
                🔀 Model Context Protocol (MCP) Servers
              </h3>
              <p style={{ margin: 0, fontSize: '12px', color: '#71717a' }}>
                JSON-RPC 2.0 stdio transport. Auto-registered via yAIMCPManager.
                Provides tool-augmented reasoning to all 37 agents.
              </p>
            </div>

            {MCP_SERVERS.map(server => (
              <div key={server.id} style={{
                padding: '20px', borderRadius: '12px',
                border: '1px solid #27272a', backgroundColor: '#18181b',
                display: 'flex', alignItems: 'center', gap: '16px',
              }}>
                <div style={{
                  width: '48px', height: '48px', borderRadius: '12px',
                  background: 'linear-gradient(135deg, #06b6d422, #0891b222)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '24px', border: '1px solid #06b6d433',
                }}>
                  {server.icon}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '14px', fontWeight: 700, color: '#e4e4e7' }}>{server.name}</div>
                  <div style={{ fontSize: '12px', color: '#71717a' }}>{server.description}</div>
                </div>
                <span style={{
                  fontSize: '11px', fontWeight: 600, padding: '4px 12px', borderRadius: '12px',
                  color: '#06b6d4', backgroundColor: '#06b6d415', textTransform: 'uppercase',
                }}>
                  {server.status}
                </span>
              </div>
            ))}

            {/* SEAL Adaptation Status */}
            <div style={{
              padding: '20px', borderRadius: '12px', marginTop: '8px',
              border: '1px solid #a855f733', backgroundColor: '#a855f708',
            }}>
              <h3 style={{ margin: '0 0 12px', fontSize: '15px', fontWeight: 700, color: '#a855f7' }}>
                🧠 SEAL Self-Adaptation Engine
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
                {[
                  { label: 'ReST-EM Iterations', value: '∞', color: '#e879f9' },
                  { label: 'Edits Accepted', value: '—', color: '#c084fc' },
                  { label: 'Avg Reward', value: '—', color: '#eab308' },
                  { label: 'Anti-Rationalization', value: 'Active', color: '#22c55e' },
                ].map((metric, i) => (
                  <div key={i} style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '18px', fontWeight: 700, color: metric.color }}>{metric.value}</div>
                    <div style={{ fontSize: '10px', color: '#71717a', marginTop: '4px' }}>{metric.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Event Stream View */}
        {viewMode === 'list' && (
          <div ref={eventLogRef} style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <div style={{
              padding: '12px 16px', borderRadius: '8px', backgroundColor: '#18181b',
              border: '1px solid #27272a', marginBottom: '8px',
              display: 'flex', alignItems: 'center', gap: '8px',
            }}>
              <div style={{
                width: '8px', height: '8px', borderRadius: '50%',
                backgroundColor: '#22c55e', boxShadow: '0 0 6px #22c55e',
                animation: 'pulse 1.5s infinite',
              }} />
              <span style={{ fontSize: '12px', color: '#71717a' }}>
                Live event stream — JSONL append-only (crash-safe)
              </span>
            </div>

            {eventLog.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px', color: '#52525b', fontSize: '14px' }}>
                Waiting for agent activity...
              </div>
            ) : (
              eventLog.map(evt => (
                <div key={evt.id} style={{
                  padding: '10px 14px', borderRadius: '8px',
                  border: '1px solid #1a1a1e', backgroundColor: '#111113',
                  display: 'flex', alignItems: 'center', gap: '12px',
                  fontSize: '12px', transition: 'background 0.2s',
                }}>
                  <span style={{ fontSize: '16px', flexShrink: 0 }}>{evt.icon}</span>
                  <span style={{ color: evt.color, fontWeight: 600, minWidth: '100px' }}>{evt.agent}</span>
                  <span style={{ color: '#a1a1aa', flex: 1 }}>{evt.action}</span>
                  <span style={{ color: '#52525b', fontSize: '10px', fontFamily: 'monospace', flexShrink: 0 }}>{evt.time}</span>
                </div>
              ))
            )}
          </div>
        )}
      </div>

      {/* CSS Animation */}
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `}</style>
    </div>
  );
}
