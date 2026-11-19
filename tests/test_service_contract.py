from importlib import import_module
from pathlib import Path
import sys
from types import ModuleType

import pytest

from plugin_manager.plugin_loader import PluginLoader
from plugin_sdk.service_registry import ServiceRegistry


@pytest.mark.parametrize("legacy_file_loaded", [False, True])
def test_market_package_provides_history_service(qapp, monkeypatch, legacy_file_loaded):
    alias = "plugins.services.history"
    monkeypatch.delitem(sys.modules, alias, raising=False)
    if legacy_file_loaded:
        monkeypatch.setitem(sys.modules, alias, ModuleType(alias))

    package = Path(__file__).resolve().parents[1] / "history"
    market_name = "github_ljzloser_metasweeper_history"
    monkeypatch.delitem(sys.modules, market_name, raising=False)
    module = PluginLoader().load_module(package / "__init__.py", market_name)
    try:
        assert module is not None
        contract = import_module(alias)
        assert Path(contract.__file__) == package / "service.py"
        assert contract.GameRecord is module.plugin.GameRecord
        registry = ServiceRegistry()
        provider = object()
        registry.register(module.plugin.HistoryService, provider)
        assert registry.get(contract.HistoryService) is provider
    finally:
        for name in tuple(sys.modules):
            if name == market_name or name.startswith(market_name + "."):
                sys.modules.pop(name)
        sys.modules.pop(alias, None)
