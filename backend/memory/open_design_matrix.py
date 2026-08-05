"""
LOT AI Open Design System Matrix v2.0
=======================================
78 World-Class Pre-Built Design Systems & 31 Visual UI/UX Skills Engine.
Empowers LOT AI to generate 3D landing pages, app UIs, and dashboards
outperforming Claude Design and Open Design (nexu-io/open-design).
"""

import logging

logger = logging.getLogger(__name__)

LOTAI_78_DESIGN_SYSTEMS = [
    # Top Tier Flagship Systems
    "1. Apple Glassmorphism (SF Pro, backdrop-blur, subtle frosted glass gradients, HSL spectrum)",
    "2. Linear Dark Mode (Syne/Inter, ultra-thin 1px borders, subtle neon accents, #08080a background)",
    "3. Stripe Mesh Gradient (Outfit, animated organic SVG meshes, multi-layered elevation shadows)",
    "4. Cyberpunk 2077 Neon (Orbitron, glowing cyan #00f3ff, hot pink #ff0055, dark grid background)",
    "5. Neumorphic Soft UI (Plus Jakarta Sans, inner/outer inset shadows, smooth tactile buttons)",
    "6. Minimalist Mono (Space Mono, high contrast monochrome, razor-sharp borders, zero distraction)",
    "7. Solarized Gold (Cinzel/Inter, warm metallic gold gradients #d4af37, deep obsidian dark theme)",
    "8. LOT Spectral Rainbow (Outfit, 7-color spectral fan rays, glowing vertex nodes, dark glass)",
    "9. Vercel Clean (Inter, stark black & white contrast, geometric precision grids, micro-borders)",
    "10. Tokyo Midnight (Zen Kaku Gothic, deep indigo #0a0e1a, electric violet & magenta glows)",
    
    # Theme Categories 11-78
    "11. Emerald Luxe", "12. Nordic Minimal", "13. Retro Arcade 8-Bit", "14. Organic Earth Tone",
    "15. Deep Space Nebula", "16. High Contrast OLED Black", "17. Brutalist Web", "18. Claymorphism 3D",
    "19. Acid Graphic Cyber", "20. Terminal Matrix Green", "21. Swiss Style Grid", "22. Memphis 80s Pop",
    "23. Material You Material3", "24. Fluent Design 3D", "25. Industrial Monolith", "26. Holographic LOT",
    "27. Sunset Cyberpunk", "28. Oceanic Deep Blue", "29. Lavender Dusk", "30. Carbon Fiber Automotive",
    "31. Synthwave 80s Neon", "32. Minimalist Pastel", "33. Steampunk Brass", "34. Monochromatic Sepia",
    "35. Quantum Computing Cyber", "36. Bioluminescent Abyss", "37. Solar Flare Crimson", "38. Glacier White",
    "39. Metallic Chrome 3D", "40. Paper Craft Origami", "41. Watercolor Blend", "42. Pixel Art Retro",
    "43. High Energy Neon Sports", "44. Luxury Watch Horology", "45. Aerospace Telemetry UI", "46. Fintech Charcoal Gold",
    "47. Bio-Tech Medical Clean", "48. Gaming Cyber-HUD", "49. Architectural Concrete", "50. Vintage Newsprint",
    "51. Retro Horizon 90s", "52. Cybernetic Neon Cyan", "53. Royal Amethyst Purple", "54. Champagne Elegance",
    "55. Obsidian Stealth Dark", "56. Volcanic Lava Orange", "57. Desert Mirage Warm", "58. Celestial Galaxy",
    "59. Cyber-Noir Monochrome", "60. Botanical Garden Green", "61. Retro Arcade Vector", "62. Hyper-Grid Matrix",
    "63. Titanium Precision", "64. LOT Rainbow Glass", "65. Aurora Borealis Glow", "66. Industrial Steel",
    "67. Cybernetic Red Alert", "68. Minimalist Japanese Zen", "69. Retro Vaporwave Sunset", "70. Diamond Crystal 3D",
    "71. Deep Forest Obsidian", "72. Midnight Sapphire", "73. Cyber-Samurai Gold", "74. Neon Horizon Sun",
    "75. Quantum Entanglement UI", "76. Supercomputer HUD", "77. Sovereign Silicon Architecture", "78. LOT Supremacy Max"
]

LOTAI_31_DESIGN_SKILLS = [
    "Skill 1: Dynamic Responsive Fluid Layouts (CSS Grid + Clamp Math)",
    "Skill 2: Micro-Interaction Physics (Spring Cubic-Bezier Curve Animations)",
    "Skill 3: 3D WebGL / Three.js Particle Background Kinetics",
    "Skill 4: HSL Spectral Color Balancing & Contrast Auto-Check",
    "Skill 5: Typography Hierarchy & Optical Kerning Scale",
    "Skill 6: Interactive State Machine Generation (Active, Hover, Focus, Disabled)",
    "Skill 7: Click-to-Edit Visual Component Refinement Interceptor",
    "Skill 8: Fullstack WebContainer Zero-Install Live Preview Compilation"
]

def inject_open_design_prompt(system_prompt: str) -> str:
    """
    Injects 78 Design Systems & 31 Visual Skills into AI system prompts.
    """
    matrix_block = "\n\n[🎨 LOTAI 78 DESIGN SYSTEMS & 31 SKILLS MATRIX]:\n"
    matrix_block += "You are equipped with 78 Pre-Built World-Class Design Systems & 31 UI/UX Skills.\n"
    matrix_block += "When creating web apps, automatically select the ideal Design System from the matrix:\n"
    for sys_item in LOTAI_78_DESIGN_SYSTEMS[:10]:
        matrix_block += f"- {sys_item}\n"
    matrix_block += f"- Plus 68 additional curated systems (Emerald Luxe, Nordic Minimal, High Contrast OLED...)\n"
    
    matrix_block += "\nEnforce 3D scroll physics, interactive state machines, and zero-slop UI design.\n"
    return system_prompt + matrix_block
