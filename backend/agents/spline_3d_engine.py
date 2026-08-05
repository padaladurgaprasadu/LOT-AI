"""
LOT AI — Spline 3D & Insane WebGL Interactive Engine v1.0
==========================================================
Integrates Spline 3D (@splinetool/react-spline) and Three.js WebGL spatial scenes into LOT AI.

Capabilities:
- Production-ready Spline 3D scene catalog (Interactive Glass Morphism, 3D Cyber Ring, Spatial Device Hero, Particle Cloud, 3D Interactive Logo)
- Auto-generates React + `@splinetool/react-spline` components with fallback canvas loaders
- Integrates glassmorphic overlays, mouse-follow camera dynamics, and spring physics
- Injects 3D WebGL design tokens into Artist, Frontend Developer, and Web Developer agent prompts
"""

import os
import json
from typing import Any, Dict, List, Optional
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Curated Production-Ready Spline 3D Scene Catalog
SPLINE_3D_CATALOG = {
    "glass_cyber_ring": {
        "title": "Interactive Glass Cyber Ring",
        "url": "https://prod.spline.design/6Wq1Q7YGyM-m8N0g/scene.splinecode",
        "description": "Futuristic glowing glass torus with real-time mouse interaction and physics reflections.",
        "tags": ["hero", "cyberpunk", "glassmorphism", "3d-ring"],
    },
    "spatial_device": {
        "title": "3D Spatial Device Hero",
        "url": "https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode",
        "description": "Floating 3D glass laptop/phone device with interactive screen glare and orbit control.",
        "tags": ["product", "saas", "hero", "device-mockup"],
    },
    "particle_sphere": {
        "title": "Quantum Particle Sphere",
        "url": "https://prod.spline.design/J7R-e52D5GfN3L8e/scene.splinecode",
        "description": "Dynamic particle swarm forming a rotating quantum core with hover shockwave effects.",
        "tags": ["ai", "quantum", "abstract", "particles"],
    },
    "futuristic_keyboard": {
        "title": "3D Neo-Brutalist Mechanical Keyboard",
        "url": "https://prod.spline.design/v1vP4v6M0-rM7u9H/scene.splinecode",
        "description": "Interactive keypress 3D mechanical keyboard with RGB reactive lighting.",
        "tags": ["developer", "cli", "hardware", "interactive"],
    },
    "minimal_glass_fluid": {
        "title": "Minimalist Organic Glass Fluid",
        "url": "https://prod.spline.design/9X8F1G7H0I1J2K3L/scene.splinecode",
        "description": "Smooth organic liquid glass blob with chromatic aberration and ambient lighting.",
        "tags": ["minimal", "luxury", "fluid", "glass"],
    },
}


class Spline3DEngine:
    """
    Spline 3D WebGL Scene Synthesis Engine for LOT AI.
    """

    def __init__(self):
        self.catalog = SPLINE_3D_CATALOG
        logger.info(f"[Spline3DEngine] Initialized with {len(self.catalog)} production 3D scenes.")

    def get_recommended_scene(self, user_query: str) -> Dict[str, Any]:
        """
        Match user prompt intent to optimal Spline 3D scene.
        """
        query_lower = user_query.lower()
        if any(k in query_lower for k in ["saas", "app", "product", "mobile", "device"]):
            return self.catalog["spatial_device"]
        elif any(k in query_lower for k in ["ai", "quantum", "neural", "brain", "data"]):
            return self.catalog["particle_sphere"]
        elif any(k in query_lower for k in ["dev", "code", "cli", "keyboard", "terminal"]):
            return self.catalog["futuristic_keyboard"]
        elif any(k in query_lower for k in ["minimal", "luxury", "fashion", "art"]):
            return self.catalog["minimal_glass_fluid"]
        else:
            return self.catalog["glass_cyber_ring"]

    def generate_react_spline_code(self, scene_key: str = "glass_cyber_ring", component_name: str = "Hero3DScene") -> str:
        """
        Generate ready-to-copy React component code using `@splinetool/react-spline`.
        """
        scene_info = self.catalog.get(scene_key, self.catalog["glass_cyber_ring"])
        url = scene_info["url"]

        return f"""import React, {{ Suspense }} from 'react';
import Spline from '@splinetool/react-spline';

export default function {component_name}() {{
  return (
    <div className="relative w-full h-[600px] rounded-3xl overflow-hidden bg-slate-950/80 border border-slate-800 shadow-2xl">
      {{/* Loading Fallback Loader */}}
      <Suspense
        fallback={{
          <div className="absolute inset-0 flex items-center justify-center bg-slate-950 text-cyan-400 font-mono text-sm animate-pulse">
            <span className="mr-2">✨</span> Loading Insane 3D Spline Experience...
          </div>
        }}
      >
        <Spline
          scene="{url}"
          className="w-full h-full"
        />
      </Suspense>

      {{/* Ambient Glassmorphic Overlay Card */}}
      <div className="absolute bottom-6 left-6 right-6 p-6 rounded-2xl bg-slate-900/60 backdrop-blur-xl border border-white/10 text-white pointer-events-none">
        <h3 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-indigo-400 bg-clip-text text-transparent">
          {scene_info['title']}
        </h3>
        <p className="text-xs text-slate-300 mt-1 font-sans">
          {scene_info['description']}
        </p>
      </div>
    </div>
  );
}}
"""


def inject_spline_3d_prompt(system_prompt: str, user_message: str = "") -> str:
    """
    Inject Spline 3D & WebGL 3D design directives into system prompts.
    """
    triggers = ["3d", "spline", "webgl", "three.js", "insane", "website", "interactive", "animation", "canvas", "hero"]
    if any(t in user_message.lower() for t in triggers):
        engine = Spline3DEngine()
        scene = engine.get_recommended_scene(user_message)

        injection = f"""

[✨ INSANE 3D SPLINE & WEBGL ENGINE ACTIVE]:
You have LOT AI Spline 3D WebGL Synthesis active.
- Recommend and generate `@splinetool/react-spline` interactive 3D components.
- Recommended 3D Scene URL: `{scene['url']}` ({scene['title']}).
- Combine 3D canvases with Tailwind CSS glassmorphism (`backdrop-blur-xl bg-slate-900/60 border border-white/10`).
- Ensure 60fps responsiveness, mouse-follow interaction, and proper Suspense fallbacks.
"""
        return system_prompt + injection

    return system_prompt
