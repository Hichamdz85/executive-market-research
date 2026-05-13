"""Unit tests for the MCP helper logic without requiring network access."""
from __future__ import annotations

import asyncio
import importlib.util
import sys
import types


class _FakeFastMCP:
    def __init__(self, _name):
        pass

    def tool(self):
        def decorator(func):
            return func
        return decorator

    def run(self):
        return None


class _FakeResponse:
    def json(self):
        return {
            "data": [
                {
                    "refYear": 2024,
                    "reporterDesc": "Algeria",
                    "partnerDesc": "World",
                    "cmdCode": "8415",
                    "cmdDesc": "Air conditioning machines",
                    "primaryValue": 123456,
                    "qty": 10,
                    "qtyUnitAbbr": "u",
                }
            ]
        }

    def raise_for_status(self):
        return None


class _FakeAsyncClient:
    calls = []

    def __init__(self, *_, **__):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        return None

    async def get(self, url, params=None):
        self.calls.append((url, params))
        return _FakeResponse()


def _load_server(repo_root, monkeypatch):
    fake_mcp = types.ModuleType("mcp")
    fake_mcp_server = types.ModuleType("mcp.server")
    fake_fastmcp = types.ModuleType("mcp.server.fastmcp")
    fake_fastmcp.FastMCP = _FakeFastMCP

    fake_httpx = types.ModuleType("httpx")
    fake_httpx.AsyncClient = _FakeAsyncClient

    monkeypatch.setitem(sys.modules, "mcp", fake_mcp)
    monkeypatch.setitem(sys.modules, "mcp.server", fake_mcp_server)
    monkeypatch.setitem(sys.modules, "mcp.server.fastmcp", fake_fastmcp)
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)

    spec = importlib.util.spec_from_file_location(
        "executive_market_research_mcp",
        repo_root / "mcp-server" / "server.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_comtrade_uses_public_preview_endpoint_and_numeric_country_codes(repo_root, monkeypatch):
    _FakeAsyncClient.calls = []
    server = _load_server(repo_root, monkeypatch)

    result = asyncio.run(server.get_trade_data("DZ", "8415", years=1))

    assert result["count"] == 1
    assert result["endpoint"] == "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
    url, params = _FakeAsyncClient.calls[0]
    assert url.endswith("/public/v1/preview/C/A/HS")
    assert params["reporterCode"] == "12"
    assert params["partnerCode"] == "0"
    assert params["cmdCode"] == "8415"
    assert "," not in params["period"]
