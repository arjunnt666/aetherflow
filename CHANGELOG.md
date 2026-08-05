# Changelog

All notable changes to AetherFlow will be documented in this file.

## [0.9.2] - 2026-07-15

### Added
- Hybrid MemoryFabric with working / episodic / semantic stores
- Declarative pipeline DSL v2 with quality gates
- Built-in tool registry (web_search, calculator, current_time, echo)
- CLI commands: run, serve, list-tools, doctor
- OpenTelemetry-style tracer and Prometheus metrics collector
- Kubernetes manifests and Helm chart
- Comprehensive agent factory and team topologies

### Changed
- Improved AgentConfig schema with nested LLM settings
- Refactored orchestrator for better stage dependency handling

### Fixed
- Memory eviction edge cases in WorkingMemory
- CLI help text formatting

## [0.8.0] - 2026-03-01

### Added
- Initial public beta
- Core multi-agent runtime
- Planner / Executor / Critic agents
- Basic pipeline support
