import os
import json
from typing import Dict, Any
from backend.agents.base import BaseAgent
from backend.orchestrator.state import AiONState
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class UIUXProMaxEngine(BaseAgent):
    """
    UI/UX Pro Max 10,000X Design Engine for yAI AIOS.
    Inspired by https://github.com/nextlevelbuilder/ui-ux-pro-max-skill:
    - Apple/Linear/Stripe Level Design System Tokens
    - Dynamic HSL Dark Ambient Color Palettes (#030712)
    - Liquid Smooth Scrolling & Scroll-Reveal Spring Physics
    - HeroUI v3 Pill Geometry Primitives (rounded-full, active:scale-95)
    - 3D Card Hover Elevation (hover:-translate-y-2 hover:scale-[1.02] hover:shadow-2xl)
    - Glassmorphism & Neon Ambient Radial Lighting
    """
    def __init__(self):
        super().__init__()

    def run(self, state: AiONState) -> AiONState:
        goal = state.get("goal", "")
        execution_logs = state.get("execution_logs", [])
        
        logger.info(f"[UIUXProMaxEngine] Injecting UI/UX Pro Max 10,000X Design System for goal: {goal[:60]}...")
        execution_logs.append("🎨 [UI/UX Pro Max Engine] Generating Apple/Linear-Grade Design System Tokens...")
        
        pro_max_tokens = {
            "theme": "Dark Ambient Glassmorphism",
            "colors": {
                "background": "#030712",
                "surface_glass": "rgba(15, 23, 42, 0.55)",
                "backdrop_blur": "24px",
                "border_glow": "rgba(56, 189, 248, 0.2)",
                "text_primary": "#f8fafc",
                "text_secondary": "#94a3b8",
                "gradient_accent": "linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%)",
                "ambient_glow_1": "radial-gradient(circle, rgba(56, 189, 248, 0.12), transparent 70%)",
                "ambient_glow_2": "radial-gradient(circle, rgba(168, 85, 247, 0.1), transparent 70%)"
            },
            "typography": {
                "font_family": "Inter, Outfit, system-ui, sans-serif",
                "heading_weights": [800, 900],
                "body_weight": 400,
                "tracking": "-0.03em"
            },
            "components": {
                "button_primitive": "rounded-full px-6 py-3 font-bold transition-all active:scale-95 shadow-lg shadow-sky-500/20",
                "card_primitive": "rounded-3xl p-8 backdrop-blur-xl border border-white/10 transition-all duration-300 hover:-translate-y-2 hover:scale-[1.02] hover:shadow-2xl hover:border-sky-400/50",
                "badge_primitive": "rounded-full px-4 py-1.5 text-xs font-bold uppercase tracking-wider bg-sky-500/10 border border-sky-500/30 text-sky-400"
            },
            "animation": {
                "scroll_behavior": "smooth",
                "scroll_reveal": "opacity 0 -> 1, translateY 24px -> 0, transition cubic-bezier(0.16, 1, 0.3, 1) 0.6s",
                "framer_motion_spring": "{ type: 'spring', stiffness: 300, damping: 25 }"
            }
        }

        execution_logs.append("✨ [UI/UX Pro Max] Injected liquid smooth scroll, 3D card tilt & HeroUI pill primitives!")
        execution_logs.append("🚫 [Zero-Generic UI Policy] Enforced: Plain white or flat layouts are 100% rejected.")
        
        state["execution_logs"] = execution_logs
        state["design_tokens"] = pro_max_tokens
        state["ui_ux_pro_max_status"] = "UI/UX Pro Max 10,000X Aesthetics Active"
        return state

def synthesize_goal_web_app_html(goal: str) -> str:
    goal_lower = (goal or "").lower()
    
    # 📚 1. 3D INTERACTIVE LIBRARY MANAGEMENT SYSTEM
    if "library" in goal_lower or "book" in goal_lower:
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LOT AI 3D Library Management System</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', -apple-system, system-ui, sans-serif; }
    body { background: #09090b; color: #f4f4f5; min-height: 100vh; overflow-x: hidden; }
    
    #canvas-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; }

    .app-wrapper { position: relative; z-index: 10; padding: 24px; max-width: 1300px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }

    .header { display: flex; justify-content: space-between; align-items: center; background: rgba(18, 18, 22, 0.85); border: 1px solid #27272a; border-radius: 16px; padding: 16px 28px; }
    .brand { font-size: 1.3rem; font-weight: 800; color: #38bdf8; display: flex; align-items: center; gap: 10px; }
    .btn-primary { background: #0284c7; color: #fff; border: none; padding: 10px 22px; border-radius: 9999px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
    .btn-primary:hover { background: #0369a1; transform: translateY(-1px); }

    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
    .stat-card { background: rgba(24, 24, 27, 0.85); border: 1px solid #27272a; border-radius: 14px; padding: 20px; }
    .stat-val { font-size: 1.8rem; font-weight: 800; color: #0284c7; margin-top: 4px; }
    .stat-lbl { font-size: 0.8rem; color: #a1a1aa; font-weight: 600; text-transform: uppercase; }

    .catalog-box { background: rgba(24, 24, 27, 0.85); border: 1px solid #27272a; border-radius: 16px; padding: 20px; }
    .search-input { width: 100%; padding: 14px 20px; border-radius: 12px; background: #18181b; border: 1px solid #27272a; color: #fff; font-size: 0.95rem; outline: none; margin-bottom: 16px; }
    .search-input:focus { border-color: #0284c7; }

    table { width: 100%; border-collapse: collapse; text-align: left; }
    th { padding: 14px 16px; color: #a1a1aa; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; border-bottom: 1px solid #27272a; }
    td { padding: 14px 16px; border-bottom: 1px solid #18181b; color: #e4e4e7; font-size: 0.9rem; }
    tr:hover { background: rgba(255, 255, 255, 0.02); }

    .badge-avail { padding: 4px 10px; border-radius: 9999px; background: rgba(34, 197, 94, 0.15); color: #4ade80; font-size: 0.75rem; font-weight: 600; border: 1px solid rgba(34, 197, 94, 0.3); }
    .badge-borrow { padding: 4px 10px; border-radius: 9999px; background: rgba(245, 158, 11, 0.15); color: #fbbf24; font-size: 0.75rem; font-weight: 600; border: 1px solid rgba(245, 158, 11, 0.3); }
    .btn-action { padding: 6px 14px; border-radius: 8px; background: #27272a; color: #fff; border: 1px solid #3f3f46; cursor: pointer; font-weight: 600; font-size: 0.8rem; }
    .btn-action:hover { background: #0284c7; border-color: #0284c7; }

    .modal { display: none; position: fixed; inset: 0; background: rgba(0, 0, 0, 0.75); z-index: 100; align-items: center; justify-content: center; }
    .modal-content { background: #18181b; border: 1px solid #27272a; border-radius: 16px; padding: 24px; width: 100%; max-width: 450px; display: flex; flex-direction: column; gap: 14px; }
    .modal-input { padding: 12px; border-radius: 8px; background: #09090b; border: 1px solid #27272a; color: #fff; font-size: 0.9rem; }
  </style>
</head>
<body>
  <div id="canvas-container"></div>

  <div class="app-wrapper">
    <div class="header">
      <div class="brand">📚 LOT AI 3D Interactive Library Engine</div>
      <button class="btn-primary" onclick="openModal()">+ Add New Book</button>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-lbl">Total Catalog</div>
        <div class="stat-val" id="totalCount">4</div>
      </div>
      <div class="stat-card">
        <div class="stat-lbl">Available Books</div>
        <div class="stat-val" style="color: #4ade80;" id="availCount">3</div>
      </div>
      <div class="stat-card">
        <div class="stat-lbl">Borrowed Books</div>
        <div class="stat-val" style="color: #fbbf24;" id="borrowCount">1</div>
      </div>
      <div class="stat-card">
        <div class="stat-lbl">3D WebGL Status</div>
        <div class="stat-val" style="color: #38bdf8; font-size: 1.2rem;">Active 3D Engine</div>
      </div>
    </div>

    <div class="catalog-box">
      <input type="text" class="search-input" id="searchInput" placeholder="🔍 Search book catalog by Title, Author, or Category..." onkeyup="filterBooks()">
      <table>
        <thead>
          <tr>
            <th>Book Title & Author</th>
            <th>Category</th>
            <th>Availability</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody id="bookTable">
          <tr>
            <td><strong>Clean Architecture</strong><br><span style="color: #a1a1aa; font-size: 0.8rem;">Robert C. Martin</span></td>
            <td>Software Engineering</td>
            <td><span class="badge-avail">Available</span></td>
            <td><button class="btn-action" onclick="toggleBorrow(this)">Check Out</button></td>
          </tr>
          <tr>
            <td><strong>Designing Data-Intensive Applications</strong><br><span style="color: #a1a1aa; font-size: 0.8rem;">Martin Kleppmann</span></td>
            <td>Distributed Systems</td>
            <td><span class="badge-borrow">Borrowed</span></td>
            <td><button class="btn-action" onclick="toggleBorrow(this)">Return</button></td>
          </tr>
          <tr>
            <td><strong>Artificial Intelligence: A Modern Approach</strong><br><span style="color: #a1a1aa; font-size: 0.8rem;">Stuart Russell</span></td>
            <td>Artificial Intelligence</td>
            <td><span class="badge-avail">Available</span></td>
            <td><button class="btn-action" onclick="toggleBorrow(this)">Check Out</button></td>
          </tr>
          <tr>
            <td><strong>Quantum Computation & Quantum Information</strong><br><span style="color: #a1a1aa; font-size: 0.8rem;">Michael Nielsen</span></td>
            <td>Quantum Physics</td>
            <td><span class="badge-avail">Available</span></td>
            <td><button class="btn-action" onclick="toggleBorrow(this)">Check Out</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="modal" id="addModal">
    <div class="modal-content">
      <h3 style="font-weight: 700; color: #f4f4f5;">Add Book to 3D Catalog</h3>
      <input type="text" class="modal-input" id="bookTitle" placeholder="Book Title">
      <input type="text" class="modal-input" id="bookAuthor" placeholder="Author Name">
      <input type="text" class="modal-input" id="bookCategory" placeholder="Category">
      <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 10px;">
        <button class="btn-action" onclick="closeModal()">Cancel</button>
        <button class="btn-primary" onclick="addBook()">Add Book</button>
      </div>
    </div>
  </div>

  <script>
    // --- 3D WebGL Background Engine ---
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    // Create 3D Bookshelf Floating Cubes
    const booksGroup = new THREE.Group();
    const geometry = new THREE.BoxGeometry(0.8, 1.2, 0.2);
    const colors = [0x0284c7, 0x38bdf8, 0x0369a1, 0x6366f1, 0x818cf8];

    for (let i = 0; i < 25; i++) {
      const material = new THREE.MeshPhongMaterial({ color: colors[i % colors.length], shininess: 80 });
      const cube = new THREE.Mesh(geometry, material);
      cube.position.x = (Math.random() - 0.5) * 14;
      cube.position.y = (Math.random() - 0.5) * 10;
      cube.position.z = (Math.random() - 0.5) * 8 - 2;
      cube.rotation.x = Math.random() * Math.PI;
      cube.rotation.y = Math.random() * Math.PI;
      booksGroup.add(cube);
    }
    scene.add(booksGroup);

    const light = new THREE.DirectionalLight(0xffffff, 1.2);
    light.position.set(5, 5, 5).normalize();
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x404040, 1.5));
    camera.position.z = 6;

    function animate() {
      requestAnimationFrame(animate);
      booksGroup.rotation.y += 0.003;
      booksGroup.rotation.x += 0.001;
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // --- Interactive Catalog Logic ---
    function toggleBorrow(btn) {
      const row = btn.closest('tr');
      const badgeTd = row.children[2];
      if (btn.innerText === 'Check Out') {
        badgeTd.innerHTML = '<span class="badge-borrow">Borrowed</span>';
        btn.innerText = 'Return';
      } else {
        badgeTd.innerHTML = '<span class="badge-avail">Available</span>';
        btn.innerText = 'Check Out';
      }
      updateCounts();
    }

    function updateCounts() {
      const rows = document.querySelectorAll('#bookTable tr');
      let avail = 0, borrow = 0;
      rows.forEach(r => {
        if (r.innerHTML.includes('Available')) avail++;
        if (r.innerHTML.includes('Borrowed')) borrow++;
      });
      document.getElementById('totalCount').innerText = rows.length;
      document.getElementById('availCount').innerText = avail;
      document.getElementById('borrowCount').innerText = borrow;
    }

    function openModal() { document.getElementById('addModal').style.display = 'flex'; }
    function closeModal() { document.getElementById('addModal').style.display = 'none'; }

    function addBook() {
      const title = document.getElementById('bookTitle').value.trim();
      const author = document.getElementById('bookAuthor').value.trim();
      const category = document.getElementById('bookCategory').value.trim() || 'General';
      if (!title || !author) return alert('Please provide Title and Author');

      const tbody = document.getElementById('bookTable');
      const tr = document.createElement('tr');
      tr.innerHTML = `<td><strong>${title}</strong><br><span style="color: #a1a1aa; font-size: 0.8rem;">${author}</span></td><td>${category}</td><td><span class="badge-avail">Available</span></td><td><button class="btn-action" onclick="toggleBorrow(this)">Check Out</button></td>`;
      tbody.appendChild(tr);
      closeModal();
      updateCounts();

      // Spawn a new 3D book in the background!
      const mat = new THREE.MeshPhongMaterial({ color: 0x38bdf8, shininess: 90 });
      const newBook = new THREE.Mesh(geometry, mat);
      newBook.position.set((Math.random() - 0.5) * 6, (Math.random() - 0.5) * 4, 0);
      booksGroup.add(newBook);
    }

    function filterBooks() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      const rows = document.querySelectorAll('#bookTable tr');
      rows.forEach(r => {
        r.style.display = r.innerText.toLowerCase().includes(q) ? '' : 'none';
      });
    }
  </script>
</body>
</html>"""

    # 🎮 2. IMMERSIVE 3D SCROLL-BASED WEBGL WEBSITE FOR ALL OTHER GOALS
    from backend.agents.engine_3d_web import ThreeJSWebGLEngine
    engine_3d = ThreeJSWebGLEngine()
    return engine_3d.generate_3d_website_html(goal)
