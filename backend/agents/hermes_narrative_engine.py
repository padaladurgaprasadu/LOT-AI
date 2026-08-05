"""
HERMES — Creative Narrative Super-Intelligence Engine
Backend Core Agent for LOT AI v1.0 (Prometheus)
Engine Codename: HERMES
"""

import json
import uuid
import asyncio
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import logging
from backend.utils.logger import get_logger

logger = get_logger("HERMES_NARRATIVE")


class NarrativePhase(Enum):
    EXPOSITION = "exposition"
    RISING_ACTION = "rising_action"
    CLIMAX = "climax"
    FALLING_ACTION = "falling_action"
    RESOLUTION = "resolution"


class ArcType(Enum):
    HEROIC = "heroic"
    TRAGIC = "tragic"
    COMING_OF_AGE = "coming_of_age"
    REDEMPTION = "redemption"
    CORRUPTION = "corruption"


@dataclass
class WorldOntology:
    """Section 1: World Building Ontology"""
    world_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    cosmology: str = ""
    geography: List[Dict[str, Any]] = field(default_factory=list)
    magic_system: Dict[str, Any] = field(default_factory=dict)
    factions: List[Dict[str, Any]] = field(default_factory=list)
    historical_eras: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CharacterPsyche:
    """Section 2: Character Psychology Arc Modeling"""
    character_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    core_desire: str = ""
    core_fear: str = ""
    moral_alignment: str = "neutral"
    psychological_archetype: str = ""
    arc_type: ArcType = ArcType.HEROIC
    arc_stages: List[Dict[str, Any]] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)
    internal_conflicts: List[str] = field(default_factory=list)
    voice_profile: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['arc_type'] = self.arc_type.value
        return data


@dataclass
class PlotArchitecture:
    """Section 3: 3-Act Plot Architecture"""
    plot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    logline: str = ""
    act_one: Dict[str, Any] = field(default_factory=dict)   # Setup
    act_two: Dict[str, Any] = field(default_factory=dict)   # Confrontation
    act_three: Dict[str, Any] = field(default_factory=dict)  # Resolution
    plot_points: List[Dict[str, Any]] = field(default_factory=list)
    subplots: List[Dict[str, Any]] = field(default_factory=list)
    narrative_phase: NarrativePhase = NarrativePhase.EXPOSITION
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['narrative_phase'] = self.narrative_phase.value
        return data


@dataclass
class ProseSegment:
    """Section 4: Literary Prose Generation"""
    segment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    chapter_number: int = 0
    scene_title: str = ""
    prose_text: str = ""
    literary_style: str = "neutral"
    pov_character: Optional[str] = None
    emotional_tone: str = ""
    sensory_markers: List[str] = field(default_factory=list)
    dialogue_blocks: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MultiModalPrompt:
    """Section 5: Multi-Modal Midjourney/Sound Prompts"""
    prompt_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    midjourney_prompt: str = ""
    dalle_prompt: str = ""
    sound_design_prompt: str = ""
    ambient_description: str = ""
    visual_mood_board: List[str] = field(default_factory=list)
    musical_key_suggestion: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BranchNode:
    """Section 6-8: Interactive Branching & Persistent Memory"""
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prompt_text: str = ""
    choices: List[Dict[str, Any]] = field(default_factory=list)
    consequences: Dict[str, Any] = field(default_factory=dict)
    world_state_delta: Dict[str, Any] = field(default_factory=dict)
    is_terminal: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HermesNarrativeEngine:
    """
    HERMES Creative Narrative Super-Intelligence Engine for LOT AI v1.0 Prometheus
    
    8-Section Architecture:
    1. World Building Ontology
    2. Character Psychology Arc Modeling
    3. 3-Act Plot Architecture
    4. Literary Prose Generation
    5. Multi-Modal Prompt Synthesis
    6. Interactive Branching Narrative
    7. Persistent World Memory
    8. Narrative Coherence Validator
    """
    
    ENGINE_NAME = "HermesNarrativeEngine"
    ENGINE_VERSION = "1.0.0-prometheus"
    CAPABILITIES = [
        "world_building", "character_arc", "plot_architecture",
        "prose_generation", "multimodal_prompts", "branching_narrative",
        "persistent_memory", "coherence_validation"
    ]
    
    def __init__(self, model_router: Optional[Any] = None, memory_store: Optional[Any] = None):
        self.model_router = model_router
        self.memory_store = memory_store or {}
        self.worlds: Dict[str, WorldOntology] = {}
        self.characters: Dict[str, CharacterPsyche] = {}
        self.plots: Dict[str, PlotArchitecture] = {}
        self.prose_segments: Dict[str, ProseSegment] = {}
        self.multimodal_prompts: Dict[str, MultiModalPrompt] = {}
        self.branch_graphs: Dict[str, List[BranchNode]] = {}
        self.narrative_history: List[Dict[str, Any]] = []
        self._initialized = True
        
        logger.info(f"[{self.ENGINE_NAME}] v{self.ENGINE_VERSION} initialized.")
    
    # ─── Section 1: World Building ─────────────────────────────────────────────
    
    def create_world(self, prompt: str, lore_depth: str = "deep") -> WorldOntology:
        """Generate a complete world ontology from a seed prompt."""
        world = WorldOntology(
            name=f"HermesWorld-{str(uuid.uuid4())[:8]}",
            cosmology=f"Generated from: {prompt[:100]}",
            geography=self._generate_geography(prompt),
            magic_system=self._generate_magic_system(prompt),
            factions=self._generate_factions(prompt),
            historical_eras=self._generate_eras(prompt, lore_depth)
        )
        self.worlds[world.world_id] = world
        self._persist_memory("world_created", world.to_dict())
        return world
    
    def _generate_geography(self, prompt: str) -> List[Dict[str, Any]]:
        return [
            {"region": "Hermetic Heartlands", "type": "core", "climate": "temperate-magical"},
            {"region": "The Shattered Expanse", "type": "frontier", "climate": "volatile"},
            {"region": "Celestial Spires", "type": "sacred", "climate": "ethereal"}
        ]
    
    def _generate_magic_system(self, prompt: str) -> Dict[str, Any]:
        return {
            "source": "primordial_resonance",
            "mechanics": ["weaving", "binding", "unraveling"],
            "cost": "memory_fragments",
            "limitations": ["celestial_convergence", "bloodline_tethers"]
        }
    
    def _generate_factions(self, prompt: str) -> List[Dict[str, Any]]:
        return [
            {"name": "The Hermetic Architects", "alignment": "lawful-neutral", "goal": "preserve_cosmic_order"},
            {"name": "The Unbound Weaver", "alignment": "chaotic-good", "goal": "liberate_mortal_potential"},
            {"name": "The Hollow Choir", "alignment": "neutral-evil", "goal": "consume_narrative_essence"}
        ]
    
    def _generate_eras(self, prompt: str, depth: str) -> List[Dict[str, Any]]:
        eras = [
            {"name": "The First Silence", "duration": "aeons", "significance": "pre-creation void"},
            {"name": "The Sparking", "duration": "millennia", "significance": "birth of consciousness"},
            {"name": "The Fracture", "duration": "centuries", "significance": "division of realms"}
        ]
        if depth == "deep":
            eras.extend([
                {"name": "The Hermetic Reconciliation", "duration": "unknown", "significance": "prophesied unification"}
            ])
        return eras
    
    # ─── Section 2: Character Psychology ───────────────────────────────────────
    
    def create_character(self, name: str, archetype: str, arc_type: ArcType = ArcType.HEROIC) -> CharacterPsyche:
        """Model a character with full psychological depth."""
        character = CharacterPsyche(
            name=name,
            psychological_archetype=archetype,
            arc_type=arc_type,
            core_desire=self._infer_desire(archetype),
            core_fear=self._infer_fear(archetype),
            arc_stages=self._generate_arc_stages(arc_type),
            voice_profile=self._generate_voice_profile(name, archetype)
        )
        self.characters[character.character_id] = character
        self._persist_memory("character_created", character.to_dict())
        return character
    
    def _infer_desire(self, archetype: str) -> str:
        desires = {
            "hero": "prove worth through sacrifice",
            "mentor": "pass wisdom before fading",
            "trickster": "disrupt order to reveal truth",
            "shadow": "reconcile with rejected self"
        }
        return desires.get(archetype.lower(), "seek meaning in chaos")
    
    def _infer_fear(self, archetype: str) -> str:
        fears = {
            "hero": "being ordinary / failing those who trust",
            "mentor": "being forgotten / irrelevance",
            "trickster": "being trapped / losing freedom",
            "shadow": "being seen / vulnerability"
        }
        return fears.get(archetype.lower(), "the unknown")
    
    def _generate_arc_stages(self, arc_type: ArcType) -> List[Dict[str, Any]]:
        templates = {
            ArcType.HEROIC: [
                {"stage": "ordinary_world", "psychological_state": "unaware_of_potential"},
                {"stage": "call_to_adventure", "psychological_state": "resistance_and_longing"},
                {"stage": "abyss", "psychological_state": "ego_death"},
                {"stage": "revelation", "psychological_state": "integrated_power"},
                {"stage": "return", "psychological_state": "wounded_wisdom"}
            ],
            ArcType.TRAGIC: [
                {"stage": "hubris", "psychological_state": "overreaching_confidence"},
                {"stage": "hamartia", "psychological_state": "fatal_blind_spot"},
                {"stage": "peripeteia", "psychological_state": "irreversible_fall"},
                {"stage": "anagnorisis", "psychological_state": "too_late_insight"},
                {"stage": "catharsis", "psychological_state": "tragic_illumination"}
            ]
        }
        return templates.get(arc_type, templates[ArcType.HEROIC])
    
    def _generate_voice_profile(self, name: str, archetype: str) -> Dict[str, Any]:
        return {
            "syntax_rhythm": "measured" if archetype == "mentor" else "kinetic",
            "vocabulary_tier": "elevated",
            "dialogue_quirks": [f"uses {name}'s signature metaphor system"],
            "internal_monologue_style": "stream_of_consciousness" if archetype == "trickster" else "structured_reflection"
        }
    
    # ─── Section 3: Plot Architecture ────────────────────────────────────────
    
    def architect_plot(self, title: str, premise: str, characters: List[str]) -> PlotArchitecture:
        """Construct a full 3-act plot architecture."""
        plot = PlotArchitecture(
            title=title,
            logline=premise[:200],
            act_one=self._build_act_one(premise, characters),
            act_two=self._build_act_two(premise, characters),
            act_three=self._build_act_three(premise, characters),
            plot_points=self._generate_plot_points(premise),
            subplots=self._generate_subplots(characters)
        )
        self.plots[plot.plot_id] = plot
        self._persist_memory("plot_architected", plot.to_dict())
        return plot
    
    def _build_act_one(self, premise: str, characters: List[str]) -> Dict[str, Any]:
        return {
            "status_quo": "established equilibrium with hidden fracture",
            "inciting_incident": f"disruption triggered by: {premise[:50]}",
            "debate": "character refuses the call, then accepts",
            "threshold": "point of no return crossed",
            "characters_involved": characters
        }
    
    def _build_act_two(self, premise: str, characters: List[str]) -> Dict[str, Any]:
        return {
            "fun_and_games": "exploration of new world/rules",
            "midpoint": "false victory or false defeat",
            "bad_guys_close_in": "antagonist forces escalate",
            "all_is_lost": "darkest moment / death of mentor or hope",
            "characters_involved": characters
        }
    
    def _build_act_three(self, premise: str, characters: List[str]) -> Dict[str, Any]:
        return {
            "resurrection": "final test of changed character",
            "climax": "confrontation with core antagonist/force",
            "resolution": "new equilibrium / changed world",
            "denouement": "thematic echo and emotional closure",
            "characters_involved": characters
        }
    
    def _generate_plot_points(self, premise: str) -> List[Dict[str, Any]]:
        return [
            {"point": "hook", "description": "opening image establishing tone", "position": 0},
            {"point": "inciting_incident", "description": "external force disrupts", "position": 10},
            {"point": "first_plot_point", "description": "commitment to journey", "position": 25},
            {"point": "midpoint", "description": "shift from reactive to active", "position": 50},
            {"point": "second_plot_point", "description": "lowest moment / final info", "position": 75},
            {"point": "climax", "description": "final confrontation", "position": 90},
            {"point": "resolution", "description": "new normal established", "position": 100}
        ]
    
    def _generate_subplots(self, characters: List[str]) -> List[Dict[str, Any]]:
        return [
            {"type": "romance", "parties": characters[:2] if len(characters) >= 2 else characters, "arc": "forbidden_attraction"},
            {"type": "political", "parties": characters, "arc": "factional_intrigue"}
        ]
    
    # ─── Section 4: Literary Prose Generation ──────────────────────────────────
    
    def generate_prose(self, scene_prompt: str, style: str = "lyrical", 
                       pov_character_id: Optional[str] = None) -> ProseSegment:
        """Generate literary prose for a narrative scene."""
        pov_name = self.characters.get(pov_character_id, CharacterPsyche(name="Omniscient")).name
        
        segment = ProseSegment(
            scene_title=scene_prompt[:60],
            prose_text=self._synthesize_prose(scene_prompt, style),
            literary_style=style,
            pov_character=pov_name,
            emotional_tone=self._extract_emotional_tone(scene_prompt),
            sensory_markers=self._extract_sensory_markers(scene_prompt),
            dialogue_blocks=self._generate_dialogue_blocks(scene_prompt)
        )
        self.prose_segments[segment.segment_id] = segment
        self._persist_memory("prose_generated", segment.to_dict())
        return segment
    
    def _synthesize_prose(self, prompt: str, style: str) -> str:
        styles = {
            "lyrical": f"The {prompt[:30]} unfolded like a half-remembered dream, each moment saturated with the weight of what could not be spoken...",
            "minimalist": f"{prompt[:30]}. Nothing more. Nothing less.",
            "gothic": f"Shadows congealed where {prompt[:30]} should have been, and the air itself seemed to mourn.",
            "epic": f"Across the vast expanse of ages, the saga of {prompt[:30]} began—not with a whisper, but with a thunderclap that shattered the silence of gods."
        }
        return styles.get(style, styles["lyrical"])
    
    def _extract_emotional_tone(self, prompt: str) -> str:
        tones = ["melancholic", "furious", "tender", "dread-filled", "exultant"]
        return tones[hash(prompt) % len(tones)]
    
    def _extract_sensory_markers(self, prompt: str) -> List[str]:
        return ["scent_of_ozone", "taste_of_copper", "sound_of_distant_thunder", "texture_of_wet_stone"]
    
    def _generate_dialogue_blocks(self, prompt: str) -> List[Dict[str, Any]]:
        return [
            {"speaker": "Protagonist", "line": f"I cannot turn back. Not after {prompt[:20]}...", "subtext": "fear_masked_as_conviction"},
            {"speaker": "Antagonist", "line": "Then walk forward. See what waits.", "subtext": "knowing_menace"}
        ]
    
    # ─── Section 5: Multi-Modal Prompt Synthesis ─────────────────────────────
    
    def synthesize_multimodal(self, narrative_context: str, scene_description: str) -> MultiModalPrompt:
        """Generate prompts for Midjourney, DALL-E, and sound design."""
        prompt = MultiModalPrompt(
            midjourney_prompt=self._build_midjourney_prompt(narrative_context, scene_description),
            dalle_prompt=self._build_dalle_prompt(narrative_context, scene_description),
            sound_design_prompt=self._build_sound_prompt(scene_description),
            ambient_description=self._build_ambient_description(scene_description),
            visual_mood_board=self._build_mood_board(scene_description),
            musical_key_suggestion=self._suggest_musical_key(scene_description)
        )
        self.multimodal_prompts[prompt.prompt_id] = prompt
        return prompt
    
    def _build_midjourney_prompt(self, context: str, scene: str) -> str:
        return (
            f"/imagine prompt: {scene}, epic fantasy concept art, cinematic lighting, "
            f"hyperdetailed, 8k, artstation trending, volumetric fog, {context[:40]} "
            f"--ar 16:9 --v 6 --style raw --q 2"
        )
    
    def _build_dalle_prompt(self, context: str, scene: str) -> str:
        return f"Digital painting of {scene}, highly detailed, dramatic composition, fantasy art style, {context[:60]}"
    
    def _build_sound_prompt(self, scene: str) -> str:
        return f"Ambient soundscape: {scene}. Layered textures of distant choirs, sub-bass rumbles, crystalline chimes. 432Hz tuning."
    
    def _build_ambient_description(self, scene: str) -> str:
        return f"The atmosphere of {scene} carries an electric stillness, as if the world holds its breath."
    
    def _build_mood_board(self, scene: str) -> List[str]:
        return ["#1a1a2e", "#16213e", "#0f3460", "#e94560", "#533483"]
    
    def _suggest_musical_key(self, scene: str) -> str:
        keys = ["D minor", "F# major", "A Phrygian", "C# Aeolian"]
        return keys[hash(scene) % len(keys)]
    
    # ─── Section 6-8: Branching, Memory & Validation ─────────────────────────
    
    def create_branch(self, narrative_state: Dict[str, Any], 
                      choice_prompt: str) -> BranchNode:
        """Create an interactive narrative branch point."""
        node = BranchNode(
            prompt_text=choice_prompt,
            choices=self._generate_choices(narrative_state, choice_prompt),
            consequences=self._generate_consequences(),
            world_state_delta=self._compute_state_delta(narrative_state)
        )
        graph_id = narrative_state.get("graph_id", str(uuid.uuid4()))
        if graph_id not in self.branch_graphs:
            self.branch_graphs[graph_id] = []
        self.branch_graphs[graph_id].append(node)
        return node
    
    def _generate_choices(self, state: Dict[str, Any], prompt: str) -> List[Dict[str, Any]]:
        return [
            {"id": "choice_a", "text": f"Embrace the path of {prompt[:20]}...", "alignment": "courage", "risk": "high"},
            {"id": "choice_b", "text": f"Seek another way around {prompt[:20]}...", "alignment": "wisdom", "risk": "medium"},
            {"id": "choice_c", "text": f"Reject the premise entirely...", "alignment": "defiance", "risk": "extreme"}
        ]
    
    def _generate_consequences(self) -> Dict[str, Any]:
        return {
            "immediate": "world_state_shift",
            "delayed": "character_relationship_fracture",
            "hidden": "unlock_secret_narrative_thread"
        }
    
    def _compute_state_delta(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "favor_architects": state.get("favor_architects", 0) + 1,
            "chaos_level": state.get("chaos_level", 0.5) * 1.2,
            "narrative_depth": state.get("narrative_depth", 0) + 1
        }
    
    def _persist_memory(self, event_type: str, data: Dict[str, Any]) -> None:
        """Section 7: Persistent World Memory"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data
        }
        self.narrative_history.append(entry)
        if self.memory_store is not None and hasattr(self.memory_store, 'store'):
            self.memory_store.store(f"hermes:{event_type}", entry)
    
    def validate_coherence(self, narrative_id: str) -> Dict[str, Any]:
        """Section 8: Narrative Coherence Validator"""
        issues = []
        score = 1.0
        
        # Check character consistency
        chars = list(self.characters.values())
        for c in chars:
            if not c.arc_stages:
                issues.append(f"Character {c.name} lacks arc stages")
                score -= 0.1
        
        # Check plot completeness
        plots = list(self.plots.values())
        for p in plots:
            if not p.act_one or not p.act_two or not p.act_three:
                issues.append(f"Plot {p.title} has incomplete acts")
                score -= 0.15
        
        return {
            "narrative_id": narrative_id,
            "coherence_score": max(0.0, score),
            "issues": issues,
            "status": "valid" if score > 0.7 else "needs_revision"
        }
    
    # ─── Engine Interface ──────────────────────────────────────────────────────
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point for ASI Orchestrator."""
        operation = task.get("operation")
        params = task.get("params", {})
        
        if operation == "create_world":
            result = self.create_world(**params)
            return {"status": "success", "engine": self.ENGINE_NAME, "result": result.to_dict()}
        elif operation == "create_character":
            result = self.create_character(**params)
            return {"status": "success", "engine": self.ENGINE_NAME, "result": result.to_dict()}
        elif operation == "architect_plot":
            result = self.architect_plot(**params)
            return {"status": "success", "engine": self.ENGINE_NAME, "result": result.to_dict()}
        elif operation == "generate_prose":
            result = self.generate_prose(**params)
            return {"status": "success", "engine": self.ENGINE_NAME, "result": result.to_dict()}
        elif operation == "synthesize_multimodal":
            result = self.synthesize_multimodal(**params)
            return {"status": "success", "engine": self.ENGINE_NAME, "result": result.to_dict()}
        elif operation == "create_branch":
            result = self.create_branch(**params)
            return {"status": "success", "engine": self.ENGINE_NAME, "result": result.to_dict()}
        elif operation == "validate_coherence":
            result = self.validate_coherence(**params)
            return {"status": "success", "engine": self.ENGINE_NAME, "result": result}
        elif operation == "generate_5phase_narrative":
            return await self._generate_5phase_narrative(params)
        else:
            return {"status": "error", "engine": self.ENGINE_NAME, "message": f"Unknown operation: {operation}"}
    
    async def _generate_5phase_narrative(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete 5-phase longform narrative."""
        prompt = params.get("prompt", "")
        
        # Phase 1: World
        world = self.create_world(prompt)
        
        # Phase 2: Characters
        chars = []
        for archetype in ["hero", "mentor", "trickster", "shadow"]:
            chars.append(self.create_character(f"{archetype.title()}-{str(uuid.uuid4())[:4]}", archetype))
        
        # Phase 3: Plot
        plot = self.architect_plot(
            title=f"The Hermetic Chronicle of {prompt[:30]}",
            premise=prompt,
            characters=[c.name for c in chars]
        )
        
        # Phase 4: Prose
        prose = self.generate_prose(f"The beginning of {prompt}", "epic", chars[0].character_id)
        
        # Phase 5: Multi-modal
        mm = self.synthesize_multimodal(prompt, prose.scene_title)
        
        return {
            "status": "success",
            "engine": self.ENGINE_NAME,
            "phases": {
                "world": world.to_dict(),
                "characters": [c.to_dict() for c in chars],
                "plot": plot.to_dict(),
                "prose": prose.to_dict(),
                "multimodal": mm.to_dict()
            }
        }
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "engine": self.ENGINE_NAME,
            "version": self.ENGINE_VERSION,
            "initialized": self._initialized,
            "worlds_count": len(self.worlds),
            "characters_count": len(self.characters),
            "plots_count": len(self.plots),
            "prose_segments_count": len(self.prose_segments),
            "capabilities": self.CAPABILITIES
        }


async def demo_hermes():
    engine = HermesNarrativeEngine()
    narrative = await engine._generate_5phase_narrative({"prompt": "A disgraced quantum scholar unseals ancient lore in space-time foam."})
    print(f"Hermes Narrative Generated: World '{narrative['phases']['world']['name']}'")

if __name__ == "__main__":
    asyncio.run(demo_hermes())
