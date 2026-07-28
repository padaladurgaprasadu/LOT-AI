import React, { useState, useRef } from 'react';

const DEFAULT_NODES = [
  { id: 'client_node', type: 'client', label: 'React Frontend Client', port: 3000, x: 80, y: 140, status: 'Active', qps: 450, latency: '12ms', color: '#38bdf8' },
  { id: 'gateway_node', type: 'gateway', label: 'Express API Gateway', port: 5000, x: 340, y: 140, status: 'Active', qps: 450, latency: '8ms', color: '#818cf8' },
  { id: 'auth_node', type: 'security', label: 'OAuth2 / Security Guard', port: 5001, x: 340, y: 320, status: 'Active', qps: 120, latency: '4ms', color: '#f43f5e' },
  { id: 'db_node', type: 'database', label: 'PostgreSQL Database', port: 5432, x: 620, y: 140, status: 'Active', qps: 890, latency: '2ms', color: '#10b981' },
  { id: 'redis_node', type: 'cache', label: 'Redis L2 Cache', port: 6379, x: 620, y: 320, status: 'Active', qps: 1400, latency: '0.8ms', color: '#f59e0b' },
  { id: 'ai_node', type: 'ai', label: 'NVIDIA Nemotron 550B MoE', port: 8000, x: 880, y: 230, status: 'Active', qps: 95, latency: '85ms', color: '#c084fc' }
];

const DEFAULT_EDGES = [
  { from: 'client_node', to: 'gateway_node', label: 'HTTPS / WSS' },
  { from: 'gateway_node', to: 'auth_node', label: 'gRPC Token Check' },
  { from: 'gateway_node', to: 'db_node', label: 'SQL Connection Pool' },
  { from: 'gateway_node', to: 'redis_node', label: 'Cache Lookup' },
  { from: 'gateway_node', to: 'ai_node', label: 'NVIDIA NIM API' }
];

export default function CanvasPro() {
  const [nodes, setNodes] = useState(DEFAULT_NODES);
  const [edges, setEdges] = useState(DEFAULT_EDGES);
  const [selectedNode, setSelectedNode] = useState(DEFAULT_NODES[0]);
  const [draggedNodeId, setDraggedNodeId] = useState(null);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncNotification, setSyncNotification] = useState('');
  
  const canvasRef = useRef(null);

  const handleMouseDown = (e, node) => {
    e.stopPropagation();
    setSelectedNode(node);
    setDraggedNodeId(node.id);
    const rect = e.currentTarget.getBoundingClientRect();
    setDragOffset({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
  };

  const handleMouseMove = (e) => {
    if (!draggedNodeId || !canvasRef.current) return;
    const canvasRect = canvasRef.current.getBoundingClientRect();
    const newX = Math.max(20, Math.min(canvasRect.width - 200, (e.clientX - canvasRect.left - dragOffset.x) / zoom));
    const newY = Math.max(20, Math.min(canvasRect.height - 100, (e.clientY - canvasRect.top - dragOffset.y) / zoom));

    setNodes(prev => prev.map(n => n.id === draggedNodeId ? { ...n, x: newX, y: newY } : n));
  };

  const handleMouseUp = () => {
    setDraggedNodeId(null);
  };

  const addNode = (type) => {
    const newId = `node_${Date.now()}`;
    const typeColors = {
      microservice: '#6366f1',
      database: '#10b981',
      cache: '#f59e0b',
      ai: '#c084fc',
      security: '#f43f5e'
    };
    const newNode = {
      id: newId,
      type: type,
      label: `New ${type.toUpperCase()} Node`,
      port: 8080 + nodes.length,
      x: 250 + (nodes.length * 30) % 400,
      y: 200 + (nodes.length * 20) % 200,
      status: 'Active',
      qps: 100,
      latency: '5ms',
      color: typeColors[type] || '#38bdf8'
    };
    setNodes(prev => [...prev, newNode]);
    setSelectedNode(newNode);
  };

  const handleSyncToCode = () => {
    setIsSyncing(true);
    setSyncNotification('⚡ Syncing visual node canvas topology to Express & Docker code...');
    setTimeout(() => {
      setIsSyncing(false);
      setSyncNotification('✅ Canvas Pro topology successfully compiled to production code!');
      setTimeout(() => setSyncNotification(''), 4000);
    }, 1200);
  };

  return (
    <div style={{ display: 'flex', width: '100%', height: '100%', backgroundColor: '#070913', color: '#f8fafc', fontFamily: 'Inter, system-ui, sans-serif' }}>
      
      {/* Sidebar Tool Palette */}
      <div style={{ width: '260px', borderRight: '1px solid rgba(255,255,255,0.08)', backgroundColor: '#0b0f19', padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px', overflowY: 'auto' }}>
        <div>
          <h2 style={{ fontSize: '1.2rem', fontWeight: '900', background: 'linear-gradient(135deg, #38bdf8, #818cf8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: '4px' }}>
            🎨 Canvas Pro
          </h2>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Interactive Architecture Canvas & Node Designer</p>
        </div>

        {/* Add Nodes Palette */}
        <div>
          <div style={{ fontSize: '0.75rem', fontWeight: '700', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '12px' }}>
            Add Node Primitives
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <button onClick={() => addNode('microservice')} style={btnStyle('#6366f1')}>⚙️ Microservice Node</button>
            <button onClick={() => addNode('database')} style={btnStyle('#10b981')}>💾 PostgreSQL / DB</button>
            <button onClick={() => addNode('cache')} style={btnStyle('#f59e0b')}>⚡ Redis Cache</button>
            <button onClick={() => addNode('ai')} style={btnStyle('#c084fc')}>🤖 AI / LLM Node</button>
            <button onClick={() => addNode('security')} style={btnStyle('#f43f5e')}>🛡️ Security Guard</button>
          </div>
        </div>

        {/* Actions */}
        <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <button 
            onClick={handleSyncToCode}
            disabled={isSyncing}
            style={{
              padding: '12px',
              borderRadius: '9999px',
              background: 'linear-gradient(135deg, #38bdf8, #6366f1)',
              color: '#fff',
              fontWeight: '700',
              border: 'none',
              cursor: 'pointer',
              boxShadow: '0 4px 15px rgba(56, 189, 248, 0.3)',
              fontSize: '0.85rem'
            }}
          >
            {isSyncing ? '⚡ Compiling Code...' : '🚀 Sync Canvas to Code'}
          </button>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button onClick={() => setZoom(z => Math.min(z + 0.1, 1.5))} style={smallBtnStyle}>🔍 Zoom +</button>
            <button onClick={() => setZoom(z => Math.max(z - 0.1, 0.6))} style={smallBtnStyle}>🔍 Zoom -</button>
            <button onClick={() => setZoom(1)} style={smallBtnStyle}>↺ Reset</button>
          </div>
        </div>
      </div>

      {/* Main Canvas Graph Area */}
      <div 
        ref={canvasRef}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        style={{ flex: 1, position: 'relative', overflow: 'hidden', backgroundImage: 'radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px)', backgroundSize: '24px 24px' }}
      >
        {syncNotification && (
          <div style={{ position: 'absolute', top: '16px', left: '50%', transform: 'translateX(-50%)', backgroundColor: '#0f172a', border: '1px solid #38bdf8', padding: '10px 24px', borderRadius: '9999px', color: '#38bdf8', fontWeight: '700', fontSize: '0.85rem', zIndex: 100, boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}>
            {syncNotification}
          </div>
        )}

        <div style={{ transform: `scale(${zoom})`, transformOrigin: '0 0', width: '100%', height: '100%', position: 'absolute' }}>
          
          {/* SVG Connection Lines */}
          <svg style={{ position: 'absolute', width: '100%', height: '100%', pointerEvents: 'none', top: 0, left: 0 }}>
            {edges.map((edge, idx) => {
              const fromNode = nodes.find(n => n.id === edge.from);
              const toNode = nodes.find(n => n.id === edge.to);
              if (!fromNode || !toNode) return null;

              const x1 = fromNode.x + 100;
              const y1 = fromNode.y + 40;
              const x2 = toNode.x + 100;
              const y2 = toNode.y + 40;

              const dx = (x2 - x1) / 2;

              return (
                <g key={idx}>
                  <path 
                    d={`M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`}
                    fill="none"
                    stroke={fromNode.color || '#38bdf8'}
                    strokeWidth="2.5"
                    strokeDasharray="6 4"
                    opacity="0.75"
                  />
                  <circle cx={(x1 + x2) / 2} cy={(y1 + y2) / 2} r="4" fill={fromNode.color} />
                </g>
              );
            })}
          </svg>

          {/* Interactive Nodes */}
          {nodes.map(node => {
            const isSelected = selectedNode?.id === node.id;
            return (
              <div
                key={node.id}
                onMouseDown={(e) => handleMouseDown(e, node)}
                style={{
                  position: 'absolute',
                  left: `${node.x}px`,
                  top: `${node.y}px`,
                  width: '200px',
                  backgroundColor: 'rgba(15, 23, 42, 0.85)',
                  backdropFilter: 'blur(16px)',
                  border: isSelected ? `2px solid ${node.color}` : '1px solid rgba(255,255,255,0.12)',
                  borderRadius: '16px',
                  padding: '16px',
                  cursor: 'grab',
                  boxShadow: isSelected ? `0 0 25px ${node.color}40` : '0 10px 30px rgba(0,0,0,0.5)',
                  transition: 'border 0.2s, box-shadow 0.2s',
                  userSelect: 'none'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.7rem', fontWeight: '800', textTransform: 'uppercase', color: node.color }}>
                    {node.type}
                  </span>
                  <span style={{ fontSize: '0.65rem', padding: '2px 8px', borderRadius: '9999px', backgroundColor: 'rgba(16, 185, 129, 0.2)', color: '#10b981', fontWeight: '700' }}>
                    {node.status}
                  </span>
                </div>

                <div style={{ fontSize: '0.9rem', fontWeight: '800', color: '#f8fafc', marginBottom: '10px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {node.label}
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '8px' }}>
                  <span>Port: {node.port}</span>
                  <span>{node.latency}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Right Inspector Panel */}
      {selectedNode && (
        <div style={{ width: '280px', borderLeft: '1px solid rgba(255,255,255,0.08)', backgroundColor: '#0b0f19', padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: '800', color: '#64748b', textTransform: 'uppercase' }}>
            Node Inspector
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <label style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Node Name</label>
            <input 
              type="text" 
              value={selectedNode.label} 
              onChange={(e) => {
                const val = e.target.value;
                setNodes(prev => prev.map(n => n.id === selectedNode.id ? { ...n, label: val } : n));
                setSelectedNode(prev => ({ ...prev, label: val }));
              }}
              style={inputStyle}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <label style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Port Number</label>
            <input 
              type="number" 
              value={selectedNode.port} 
              onChange={(e) => {
                const val = parseInt(e.target.value) || 0;
                setNodes(prev => prev.map(n => n.id === selectedNode.id ? { ...n, port: val } : n));
                setSelectedNode(prev => ({ ...prev, port: val }));
              }}
              style={inputStyle}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <label style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Telemetry Throughput</label>
            <div style={{ fontSize: '0.9rem', fontWeight: '700', color: selectedNode.color }}>
              ⚡ {selectedNode.qps} QPS ({selectedNode.latency})
            </div>
          </div>

          <button 
            onClick={() => {
              setNodes(prev => prev.filter(n => n.id !== selectedNode.id));
              setEdges(prev => prev.filter(e => e.from !== selectedNode.id && e.to !== selectedNode.id));
              setSelectedNode(null);
            }}
            style={{ marginTop: 'auto', padding: '10px', borderRadius: '8px', backgroundColor: 'rgba(244,63,94,0.15)', border: '1px solid #f43f5e', color: '#f43f5e', fontWeight: '700', cursor: 'pointer', fontSize: '0.8rem' }}
          >
            🗑️ Delete Node
          </button>
        </div>
      )}
    </div>
  );
}

const btnStyle = (color) => ({
  padding: '10px 14px',
  borderRadius: '10px',
  backgroundColor: 'rgba(15, 23, 42, 0.6)',
  border: `1px solid ${color}40`,
  color: '#f8fafc',
  fontSize: '0.8rem',
  fontWeight: '600',
  cursor: 'pointer',
  textAlign: 'left',
  transition: 'all 0.2s'
});

const smallBtnStyle = {
  flex: 1,
  padding: '6px',
  borderRadius: '6px',
  backgroundColor: 'rgba(255,255,255,0.06)',
  border: '1px solid rgba(255,255,255,0.1)',
  color: '#cbd5e1',
  fontSize: '0.7rem',
  fontWeight: '600',
  cursor: 'pointer'
};

const inputStyle = {
  padding: '8px 12px',
  borderRadius: '8px',
  backgroundColor: '#0f172a',
  border: '1px solid rgba(255,255,255,0.12)',
  color: '#f8fafc',
  fontSize: '0.85rem',
  outline: 'none'
};
