1.0

# Changelog

All changes are listed new → old. The first non-empty line of this file is the canonical version string for programmatic detection.

## [1.0] - 2025-08-22

- Initial release (version 1.0)
  - Date: 2025-08-22
  - Changes implemented:
    - Added `fastmcp_style_server.py` — Offline FastMCP server implementation for Microsoft Writing Style Guide analysis.
    - Added `fastmcp_style_server_web.py` — Web-enabled FastMCP server with live Microsoft Learn integration.
    - Added `fastmcp_setup.py` — Interactive setup and configuration script.
    - Added `mcp_updater.py` — Auto-updater that checks GitHub releases/commits, creates backups, and applies updates.
    - Added `copilot_integration.py` — Copilot integration helpers and examples.
    - Added documentation: `readme.md`, `UPDATER_USAGE.md`, `COPILOT_USAGE.md` and `requirements.txt`.
    - Initial configuration files including `update_config.json` and test document `test_document.md`.
  - Notes: The version number "1.0" appears on the first line of this file so the MCP updater/server can detect the current release programmatically.


<!-- Future entries should be added at the top. Example entry format:
## [1.1] - YYYY-MM-DD
- Brief bullet describing change(s)
-->
