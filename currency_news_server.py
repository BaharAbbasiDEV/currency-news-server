"""
Currency & News MCP Server
---------------------------
A Model Context Protocol (MCP) server with two tools:

1. get_exchange_rate  -> live currency conversion rate (no API key needed)
2. get_currency_news  -> recent news headlines about a currency/topic (no API key needed)

This project demonstrates a core freelance AI-automation skill: connecting
an AI assistant to REAL, live internet data sources (not just local files).

Only Python's built-in libraries are used for the HTTP requests and parsing,
so no extra installation beyond `mcp[cli]` (which you already installed for
project 1) is required.
"""

from mcp.server.fastmcp import FastMCP
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET

mcp = FastMCP("currency-news-server")


@mcp.tool()
def get_exchange_rate(base_currency: str, target_currency: str) -> str:
    """Get the current exchange rate between two currencies.

    Args:
        base_currency: 3-letter currency code, e.g. "USD"
        target_currency: 3-letter currency code, e.g. "EUR"
    """
    base = base_currency.strip().upper()
    target = target_currency.strip().upper()
    url = f"https://open.er-api.com/v6/latest/{base}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        return f"Error contacting the exchange rate service: {e}"

    if data.get("result") != "success":
        return f"Could not fetch rates for currency code '{base}'. Check that it's a valid 3-letter code."

    rates = data.get("rates", {})
    if target not in rates:
        return f"Currency code '{target}' was not found in the results."

    rate = rates[target]
    updated = data.get("time_last_update_utc", "unknown time")
    return f"1 {base} = {rate} {target}\n(Rates last updated: {updated})"


@mcp.tool()
def get_currency_news(topic: str, max_results: int = 5) -> str:
    """Get recent news headlines related to a currency or economic topic.

    Args:
        topic: search term, e.g. "US dollar", "euro inflation", "gold price"
        max_results: how many headlines to return (default 5, max recommended 10)
    """
    query = urllib.parse.quote(topic)
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            xml_data = response.read()
    except Exception as e:
        return f"Error contacting the news service: {e}"

    try:
        root = ET.fromstring(xml_data)
        items = root.findall(".//item")[: max(1, min(max_results, 10))]
    except Exception as e:
        return f"Error parsing news results: {e}"

    if not items:
        return f"No news found for '{topic}'."

    lines = []
    for i, item in enumerate(items, start=1):
        title = item.findtext("title", default="(no title)")
        link = item.findtext("link", default="")
        lines.append(f"{i}. {title}\n   {link}")

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
