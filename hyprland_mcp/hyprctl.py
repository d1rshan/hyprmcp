"""Async wrappers for hyprctl IPC commands."""

import asyncio
import json

from .errors import HyprctlError, require_tool


async def query(command: str) -> dict | list:
    """Run a hyprctl query command and return parsed JSON.

    Example: query("monitors") → list of monitor dicts
    """
    require_tool("hyprctl")
    proc = await asyncio.create_subprocess_exec(
        "hyprctl", command, "-j",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise HyprctlError(f"hyprctl {command} failed: {stderr.decode().strip()}")
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as e:
        raise HyprctlError(f"Failed to parse hyprctl {command} output: {e}") from e


async def dispatch(expr: str) -> str:
    """Run a Lua dispatcher expression via hyprctl.

    Hyprland 0.56+ dispatches via Lua: pass an ``hl.dsp.*`` expression.
    Example: dispatch("hl.dsp.focus({workspace = 1})")
    """
    require_tool("hyprctl")
    proc = await asyncio.create_subprocess_exec(
        "hyprctl", "dispatch", expr,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise HyprctlError(
            f"hyprctl dispatch {expr} failed: {stderr.decode().strip()}"
        )
    return stdout.decode().strip()


def lua(value) -> str:
    """Serialize a Python value as a Lua literal."""
    if value is None:
        return "nil"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def spec(**fields) -> str:
    """Build a Lua table literal, dropping fields whose value is None.

    Example: spec(workspace=3, window="class:firefox") -> '{workspace = 3, window = "class:firefox"}'
    """
    return "{" + ", ".join(
        f"{k} = {lua(v)}" for k, v in fields.items() if v is not None
    ) + "}"
