# Currency & News MCP Server

A **Model Context Protocol (MCP)** server that connects an AI assistant (like Claude) to **live internet data**: real-time currency exchange rates and related news headlines — through natural language, with no API key required.

This project builds on the same MCP pattern as [notes-mcp-server](https://github.com/BaharAbbasiDEV/notes-mcp-server), but demonstrates a more advanced and business-relevant skill: **calling external REST APIs and parsing live data** for an AI assistant to use.

## What it does

- "What's the USD to EUR exchange rate?" → fetches the live rate instantly
- "Show me recent news about gold prices" → pulls current headlines related to that topic

No manual searching, no copy-pasting from a currency site — the AI fetches and reports the data directly.

## Why this matters

Many real business use cases (e-commerce pricing, invoicing, financial dashboards, trading tools) need live external data inside an AI workflow. This project is a clean, minimal example of wiring a language model to a real-time data source using the open MCP standard — a pattern that can be extended to almost any REST API (payment gateways, CRMs, inventory systems, etc.).

## Tech stack

- Python 3.10+
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (`mcp[cli]`, v1.x)
- [open.er-api.com](https://www.exchangerate-api.com/docs/free) — free, no-key exchange rate API
- Google News RSS — free, no-key news search
- Only Python's built-in `urllib` and `xml.etree` — no extra dependencies beyond the MCP SDK

## Project structure

```
currency-news-server/
├── currency_news_server.py   # the MCP server and its tools
└── README.md
```

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/BaharAbbasiDEV/currency-news-mcp-server.git
   cd currency-news-mcp-server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install "mcp[cli]<2"
   ```

4. Connect it to Claude Desktop by adding this to your `claude_desktop_config.json` (find it via Claude Desktop → Settings → Developer → Edit Config):
   ```json
   {
     "mcpServers": {
       "currency-news": {
         "command": "/absolute/path/to/venv/python",
         "args": ["/absolute/path/to/currency_news_server.py"]
       }
     }
   }
   ```

5. Restart Claude Desktop and try: *"What's the exchange rate from USD to EUR?"*

## Available tools

| Tool | Description |
|------|-------------|
| `get_exchange_rate(base_currency, target_currency)` | Returns the live exchange rate between two 3-letter currency codes (e.g. USD, EUR, IRR) |
| `get_currency_news(topic, max_results=5)` | Returns recent news headlines related to a currency or economic topic |

## Possible extensions

- Add historical exchange rate charts
- Support cryptocurrency rates
- Filter news by date or source
- Deploy as a remote server (Streamable HTTP) so it works with ChatGPT and other MCP clients, not just local desktop apps

## License

MIT
