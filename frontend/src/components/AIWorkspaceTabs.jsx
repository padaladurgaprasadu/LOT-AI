import React from 'react';
import ArtifactViewer from './ArtifactViewer';
import ArchitectureViewer from './ArchitectureViewer';
import CanvasPro from './CanvasPro';
import { WebContainerManager } from './WebContainerManager';
import ExecutionManager from './ExecutionManager';
import PlatformDashboards from './PlatformDashboards';
import MemoryView from './MemoryView';
import TasksView from './TasksView';
import DeploymentView from './DeploymentView';

const AIWorkspaceTabs = ({
  activeTab, 
  setActiveTab,
  codeFiles,
  setCodeFiles,
  blueprintJson,
  executionLogs,
  previewUrl,
  previewError,
  isBackend,
  projectId,
  isPreviewRunning,
  previewPort,
  API_URL,
  timeline
}) => {
  
  const tabs = [
    { id: 'files', label: '💻 Code', hidden: false, isPill: true },
    { id: 'preview', label: '👁️ Preview', hidden: false, isPill: true },
    { id: 'architecture', label: '📐 Architecture', hidden: false },
    { id: 'canvas_pro', label: '🎨 Canvas Pro', hidden: false },
    { id: 'logs', label: '📋 Logs', hidden: false },
    { id: 'tasks', label: '📝 Tasks', hidden: false },
    { id: 'memory', label: '🧠 Memory', hidden: false },
    { id: 'deployment', label: '🚀 Deploy', hidden: false },
    { id: 'dashboards', label: '📊 Dashboards', hidden: false }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', width: '100%', backgroundColor: 'var(--app-bg)' }}>
      {/* Workspace Tab Bar */}
      <div style={{ 
        display: 'flex', 
        alignItems: 'center',
        gap: '10px', 
        padding: '10px 16px', 
        borderBottom: '1px solid var(--border-color)',
        backgroundColor: 'var(--sidebar-bg)',
        overflowX: 'auto',
        scrollbarWidth: 'none'
      }}>
        {tabs.filter(t => !t.hidden).map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: tab.isPill ? '8px 18px' : '8px 14px',
              backgroundColor: activeTab === tab.id 
                ? (tab.isPill ? '#3b82f6' : 'var(--app-bg)') 
                : (tab.isPill ? '#1e2330' : 'transparent'),
              color: activeTab === tab.id 
                ? '#ffffff' 
                : (tab.isPill ? '#60a5fa' : 'var(--text-secondary)'),
              border: tab.isPill ? '1px solid #3b82f6' : '1px solid transparent',
              borderRadius: tab.isPill ? '20px' : '8px 8px 0 0',
              cursor: 'pointer',
              fontWeight: tab.isPill ? '700' : '600',
              fontSize: tab.isPill ? '0.9rem' : '0.85rem',
              whiteSpace: 'nowrap',
              boxShadow: activeTab === tab.id && tab.isPill ? '0 4px 16px rgba(59, 130, 246, 0.45)' : 'none',
              transition: 'all 0.2s'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Workspace Content Area */}
      <div style={{ flex: 1, overflow: 'hidden', position: 'relative' }}>
        {activeTab === 'files' && (
          <ArtifactViewer 
            codeFiles={codeFiles} 
            setCodeFiles={setCodeFiles}
            projectId={projectId}
            isPreviewRunning={isPreviewRunning}
            API_URL={API_URL}
            executionLogs={executionLogs}
            isBackend={isBackend}
            previewUrl={previewUrl}
            previewError={previewError}
          />
        )}
        
        {activeTab === 'canvas_pro' && (
          <CanvasPro />
        )}
        
        {activeTab === 'architecture' && (
          <ArchitectureViewer architectureJson={blueprintJson} />
        )}
        
        {activeTab === 'preview' && (
          <WebContainerManager 
            codeFiles={codeFiles}
          />
        )}
        
        {activeTab === 'logs' && (
          <ExecutionManager 
            executionLogs={executionLogs}
          />
        )}
        
        {activeTab === 'dashboards' && (
          <PlatformDashboards API_URL={API_URL} />
        )}
        
        {activeTab === 'memory' && (
          <MemoryView />
        )}
        
        {activeTab === 'tasks' && (
          <TasksView timeline={timeline} />
        )}
        
        {activeTab === 'deployment' && (
          <DeploymentView />
        )}
      </div>
    </div>
  );
};

export default AIWorkspaceTabs;
