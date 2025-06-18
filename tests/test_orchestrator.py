from orchestrator.core import ScraperOrchestrator


def test_load_agents_handles_missing_dependencies():
    orch = ScraperOrchestrator()
    orch.load_agents()
    assert isinstance(orch.agents, dict)
