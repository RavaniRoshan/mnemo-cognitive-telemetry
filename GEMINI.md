# Project GEMINI.md

## Project Overview
`menimo-model` is the implementation of MOSA (Memory Operating System for Agents). 

MOSA is a cognition infrastructure layer that transforms LLMs from stateless token processors into persistent evolving reasoning systems without requiring frontier-scale pretraining. It focuses on persistent hierarchical memory systems rather than relying purely on context window scaling.

The core architecture introduces the Hierarchical Memory Consolidation Architecture (HMCA), structured into four layers:
1. Working Memory
2. Episodic Memory
3. Semantic Memory
4. Procedural Memory

For the complete thesis and architectural details, refer to `agent.md`.

## Technologies
*   **Primary Focus:** Memory infrastructure, LLM orchestration, Graph structures.
*   **Base Models:** Qwen, Gemma, Llama, Mistral (planned for Phase 1).
*   **Infrastructure:** TBD (Requires observability, graph storage, and compute for the consolidation engine).

## Building and Running
Since the project is in its early stages (Targeting MVP v1: episodic memory graph, memory decay, semantic consolidation, retrieval scoring, observability dashboard), build and execution commands have not yet been defined.

*   **Build:** `TODO: Add build command (e.g., npm run build, make, etc.)`
*   **Run:** `TODO: Add run command (e.g., python main.py, npm start, etc.)`
*   **Test:** `TODO: Add test command (e.g., pytest, npm test, etc.)`

## Development Conventions
*   **Coding Style:** Follow the standard conventions for the chosen language once established.
*   **Git Workflow:** Standard feature-branch workflow recommended.
*   **Documentation:** Maintain this `GEMINI.md` file as the primary source of project-wide instructions. The core thesis is located in `agent.md`.

## Key Files
*   `GEMINI.md`: This file, containing project overview and development instructions.
*   `agent.md`: The core thesis, architecture, and roadmap for the Memory Operating System for Agents (MOSA).
*   `TODO`: Add source directory and project configuration files once implementation begins.
