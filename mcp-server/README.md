# Executive Market Research - MCP Server

A bundled Model Context Protocol server that exposes the report pipeline as
tools any MCP client (Claude Code, Claude Desktop, Cursor, etc.) can call.

## Tools

| Tool | Purpose |
|------|---------|
| `get_country_macro(iso2)` | Macro indicators (GDP, population, inflation, trade) from World Bank Open Data |
| `get_trade_data(reporter_iso2, hs_code, partner_iso2, years, flow)` | Import/export flows from UN Comtrade public API |
| `search_market_data(product, country, language, sector)` | Structured research workplan + sector-preset suggestions |
| `generate_report(engagement_json, language, output_dir, quick, no_pdf)` | Render the full HTML + PDF deliverable |


## Requirements

- **Python 3.10+** (the official `mcp` SDK requires it)
- Network access to api.worldbank.org and comtradeapi.un.org

## Install

```bash
cd mcp-server
pip install -r requirements.txt
```

## Run standalone (for testing)

```bash
python3 server.py
```

## Wire to Claude Code

Add the server to your Claude Code MCP config (or rely on the bundled
`.claude-plugin/plugin.json`):

```json
{
  "mcpServers": {
    "executive-market-research": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-server/server.py"]
    }
  }
}
```

## Wire to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "executive-market-research": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-server/server.py"]
    }
  }
}
```

## Notes

- World Bank API and UN Comtrade preview endpoints are public and
  rate-limited. For production volumes consider an API key (UN Comtrade
  Premium) and a request-cache layer.
- The `generate_report` tool shells out to `scripts/generate_report.py`,
  so the same Python environment must have Playwright installed for PDF
  rendering. Pass `no_pdf=True` to skip it.
