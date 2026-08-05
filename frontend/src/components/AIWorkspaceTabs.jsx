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

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', width: '100%', backgroundColor: '#09090b' }}>
      {/* Workspace Tab Bar with Clean Code / Preview Pill Toggle */}
      <div style={{ 
        display: 'flex', 
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '10px 20px', 
        borderBottom: '1px solid #18181b',
        backgroundColor: '#09090b',
        gap: '16px'
      }}>
        
        {/* Clean Code / Preview Pill Toggle Container */}
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          backgroundColor: '#141417',
          border: '1px solid #27272a',
          borderRadius: '9999px',
          padding: '3px',
          gap: '2px'
        }}>
          {/* Code Pill */}
          <button
            onClick={() => setActiveTab('files')}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 18px',
              borderRadius: '9999px',
              border: 'none',
              backgroundColor: (activeTab === 'files' || activeTab === 'code') ? '#0284c7' : 'transparent',
              color: (activeTab === 'files' || activeTab === 'code') ? '#ffffff' : '#a1a1aa',
              fontWeight: '600',
              fontSize: '0.85rem',
              cursor: 'pointer',
              transition: 'all 0.2s cubic-bezier(0.16, 1, 0.3, 1)'
            }}
          >
            {(activeTab === 'files' || activeTab === 'code') && (
              <span style={{ fontSize: '0.8rem', fontWeight: '800' }}>✓</span>
            )}
            Code
          </button>

          {/* Preview Pill */}
          <button
            onClick={() => setActiveTab('preview')}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 18px',
              borderRadius: '9999px',
              border: 'none',
              backgroundColor: activeTab === 'preview' ? '#0284c7' : 'transparent',
              color: activeTab === 'preview' ? '#ffffff' : '#a1a1aa',
              fontWeight: '600',
              fontSize: '0.85rem',
              cursor: 'pointer',
              transition: 'all 0.2s cubic-bezier(0.16, 1, 0.3, 1)'
            }}
          >
            {activeTab === 'preview' && (
              <span style={{ fontSize: '0.8rem', fontWeight: '800' }}>✓</span>
            )}
            Preview
          </button>
        </div>

        {/* Secondary Workspace Views (Right-Aligned) */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflowX: 'auto' }}>
          {[
            { id: 'architecture', label: '📐 Architecture' },
            { id: 'canvas_pro', label: '🎨 Canvas Pro' },
            { id: 'logs', label: '📋 Logs' },
            { id: 'tasks', label: '📝 Tasks' },
            { id: 'memory', label: '🧠 Memory' },
            { id: 'deployment', label: '🚀 Deploy' },
            { id: 'dashboards', label: '📊 Dashboards' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                padding: '6px 12px',
                backgroundColor: activeTab === tab.id ? '#18181b' : 'transparent',
                color: activeTab === tab.id ? '#f4f4f5' : '#71717a',
                border: activeTab === tab.id ? '1px solid #27272a' : '1px solid transparent',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '500',
                fontSize: '0.8rem',
                whiteSpace: 'nowrap',
                transition: 'all 0.15s ease'
              }}
              onMouseEnter={(e) => {
                if (activeTab !== tab.id) e.currentTarget.style.color = '#d4d4d8';
              }}
              onMouseLeave={(e) => {
                if (activeTab !== tab.id) e.currentTarget.style.color = '#71717a';
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Tab Content Viewport */}
      <div style={{ flex: 1, position: 'relative', overflow: 'hidden', backgroundColor: '#09090b' }}>
        {(activeTab === 'files' || activeTab === 'code') && (
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

        {activeTab === 'preview' && (
          <WebContainerManager 
            codeFiles={codeFiles}
            isBackend={isBackend}
            projectId={projectId}
            API_URL={API_URL}
          />
        )}

        {activeTab === 'architecture' && (
          <ArchitectureViewer blueprintJson={blueprintJson} />
        )}

        {activeTab === 'canvas_pro' && (
          <CanvasPro codeFiles={codeFiles} />
        )}

        {activeTab === 'logs' && (
          <ExecutionManager 
            logs={executionLogs} 
            isPreviewRunning={isPreviewRunning}
            codeFiles={codeFiles}
            previewUrl={previewUrl}
          />
        )}

        {activeTab === 'tasks' && (
          <TasksView timeline={timeline} />
        )}

        {activeTab === 'memory' && (
          <MemoryView projectId={projectId} API_URL={API_URL} />
        )}

        {activeTab === 'deployment' && (
          <DeploymentView projectId={projectId} API_URL={API_URL} codeFiles={codeFiles} />
        )}

        {activeTab === 'dashboards' && (
          <PlatformDashboards projectId={projectId} API_URL={API_URL} />
        )}
      </div>
    </div>
  );
};

export default AIWorkspaceTabs;
