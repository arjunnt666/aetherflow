# AetherFlow Architecture Overview

## High-Level Design

AetherFlow is organized around a **Control Plane** and an **Agent Runtime Mesh**.

### Control Plane
- Orchestrator: Task routing, dependency resolution, failure handling
- Scheduler: Cron & event triggers
- Registry: Agent and tool discovery
- Security: RBAC, sandboxing, audit
- Observability: Traces, metrics, logs

### Agent Runtime Mesh
Agents are lightweight units of cognition that share a common Memory Fabric
and communicate through configurable protocols.

### Memory Fabric
Four complementary stores: Working, Episodic, Semantic, and Graph (optional).
