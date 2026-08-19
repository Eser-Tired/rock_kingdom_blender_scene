# Rock Kingdom Fantasy Plaza Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and render an editable stylized fantasy plaza matching the six supplied references, with a highly detailed central character.

**Architecture:** A deterministic Blender-Python pipeline builds the scene in five stages: shared utilities, scene setup, architecture, environment, character, and final lighting/rendering. A Blender-side contract test validates semantic object names and scene complexity; a host-side verifier validates saved deliverables.

**Tech Stack:** Blender 5.2 LTS, Blender Python API (`bpy`), Eevee Next, native mesh/curve/material nodes, Python standard library.

---

### Task 1: Establish the failing scene contract

**Files:**
- Create: `tests/test_scene_contract.py`
- Create: `tests/verify_outputs.py`

- [x] **Step 1: Write the failing Blender contract**

The contract requires the named collections, landmark objects, hero facial components, at least 12 hair locks, a companion, minimum object/material/light/camera counts, and a saved project-local `.blend` path.

- [x] **Step 2: Run the contract against Blender's default scene**

Run through Blender MCP:

```python
exec(compile(open(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene\tests\test_scene_contract.py", encoding="utf-8").read(), "test_scene_contract.py", "exec"))
```

Expected: `AssertionError` listing missing collections, landmarks and complexity thresholds.

### Task 2: Build shared primitives and scene foundation

**Files:**
- Create: `scripts/common.py`
- Create: `scripts/01_setup.py`

- [x] **Step 1: Implement reusable native primitives**

Expose deterministic helpers for materials, boxes, spheres, cylinders, prisms, curves, arch segments, roofs, collection linking, camera tracking and named parenting. Every created datablock uses the `RK_` namespace.

- [x] **Step 2: Build the plaza and render foundation**

Clear the default scene, configure units/world/Eevee/compositor, create all collections and palette materials, then construct tiled plaza slabs, inlaid rings and a star medallion.

- [x] **Step 3: Execute both scripts through Blender MCP**

Expected: Blender scene contains the project collections and plaza foundation without Python exceptions.

### Task 3: Build architecture and street dressing

**Files:**
- Create: `scripts/02_architecture.py`
- Create: `scripts/03_environment.py`

- [x] **Step 1: Construct the warm guild hall and castle gate**

Build façade masses, gables, roofs, chimneys, towers, battlements, arch voussoirs, stairs, windows, doors and trims as separately named editable objects.

- [x] **Step 2: Construct environmental repetition**

Add autumn trees, hedges, planters, flowers, spiral lamps, emissive lantern crystals, banners, secondary walls and stylized guards. Use deterministic seeds for leaf clusters.

- [x] **Step 3: Execute through Blender MCP and inspect a viewport capture**

Expected: architecture establishes a U-shaped plaza silhouette and warm/cool depth separation.

### Task 4: Build the detailed hero and companion

**Files:**
- Create: `scripts/04_character.py`

- [x] **Step 1: Build the hero from named editable parts**

Create chibi anatomy, layered face, pointed ears, articulated limbs, clothing panels, belts, gloves, boots, bow, crown and 12+ individually shaped curve hair locks. Create a named armature and parent the hero assembly to it.

- [x] **Step 2: Build the companion and floating sprite**

Create the purple/white long-eared creature, leaf clothing, two tails, expressive face and cyan emissive sprite.

- [x] **Step 3: Execute through Blender MCP and run the contract**

Expected: the contract may still fail only for final cameras/lights/render state; all hero-specific checks pass.

### Task 5: Light, render, and verify

**Files:**
- Create: `scripts/05_lighting_render.py`

- [x] **Step 1: Configure lighting and three cameras**

Add moon key, blue fill, warm building and lantern lights, hero rim lights, three cameras and compositor glow. Configure 960×600 PNG rendering.

- [x] **Step 2: Save and render**

Save `rock_kingdom_fantasy_plaza.blend`; render `final_hero.png`, `character_closeup.png`, and `plaza_wide.png` into `renders/`.

- [x] **Step 3: Run fresh verification**

Run the Blender scene contract and:

```powershell
python tests/verify_outputs.py
```

Expected: both commands report zero failures and all three PNG files have non-trivial byte size.
