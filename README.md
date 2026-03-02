# hyprland-mcp

MCP server for [Hyprland](https://hyprland.org/) desktop automation. Lets AI assistants see the screen, drive mouse/keyboard, and manage windows — via native Wayland tools.

Built for Claude Code, works with any MCP client.

## (๑˃̵ᴗ˂̵) install

```bash
curl -sSL https://raw.githubusercontent.com/d1rshan/hyprmcp/main/install.sh | bash
```

Detects your package manager, installs missing deps (`grim`, `wtype`, `ydotool`, `wl-clipboard`, `tesseract`), installs via pipx, and registers with Claude Code. Restart, then check `claude mcp list` → `hyprland: ✓ Connected`.

<details>
<summary>manual</summary>

```bash
pipx install git+https://github.com/d1rshan/hyprmcp.git
claude mcp add --transport stdio --scope user hyprland -- hyprland-mcp
```

Needs Hyprland, Python 3.10+.

</details>

## (￣▽￣) tools

- **screenshot** `screenshot` `screenshot_with_ocr` — capture desktop/monitor/window/region, auto-scaled JPEG + coordinate mapping
- **ocr** `click_text` `find_text_on_screen` `type_into` — find/click/type text, auto-inverts dark themes, auto-scopes to active window
- **mouse** `mouse_move` `mouse_click` `mouse_scroll` `mouse_drag` — pixel-accurate via `movecursor`
- **keyboard** `type_text` `key_press` `send_shortcut`
- **windows** `list_windows` `get_active_window` `focus_window` `close_window` `move_window` `resize_window` `toggle_fullscreen` `toggle_floating`
- **workspaces & monitors** `list_monitors` `list_workspaces` `switch_workspace` `get_cursor_position`
- **system** `clipboard_read` `clipboard_write` `launch_app`

## (・_・) notes

- Screenshots include a coordinate mapping so the AI translates image pixels → screen coords correctly on multi-monitor setups.
- OCR inverts dark-background shots before Tesseract — big accuracy gain on dark themes.
- Screenshots default to ≤1024px wide, JPEG q60. Use `region`/`window` for fine text.
- `close_window` sends WM_CLOSE (apps may prompt to save); no force-kill. `launch_app` is detached, no shell expansion. No filesystem access.

## (⌐■_■) layout

```
hyprland_mcp/
  server.py      # FastMCP tools + entry point
  hyprctl.py     # async hyprctl IPC
  screenshot.py  # grim + Pillow + coord mapping
  input.py       # mouse + keyboard
  clipboard.py   # wl-copy / wl-paste
  ocr.py         # tesseract + preprocessing
  errors.py      # exceptions + tool checks
```

MIT
