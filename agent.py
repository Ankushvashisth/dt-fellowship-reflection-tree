#!/usr/bin/env python3
"""
Daily Reflection Tree Agent
A deterministic reflection tool — no LLM at runtime.
Loads reflection-tree.json and walks the employee through it.
"""

import json
import sys
import os
import time
from pathlib import Path


# ─── ANSI Colors ─────────────────────────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    GREY    = "\033[90m"

def bold(s):    return f"{C.BOLD}{s}{C.RESET}"
def cyan(s):    return f"{C.CYAN}{s}{C.RESET}"
def green(s):   return f"{C.GREEN}{s}{C.RESET}"
def yellow(s):  return f"{C.YELLOW}{s}{C.RESET}"
def dim(s):     return f"{C.DIM}{s}{C.RESET}"
def magenta(s): return f"{C.MAGENTA}{s}{C.RESET}"
def grey(s):    return f"{C.GREY}{s}{C.RESET}"


# ─── Tree Loader ──────────────────────────────────────────────────────────────

def load_tree(path: str) -> dict:
    with open(path) as f:
        data = json.load(f)
    node_map = {n["id"]: n for n in data["nodes"]}
    return data, node_map


# ─── State ────────────────────────────────────────────────────────────────────

def make_state():
    return {
        "answers": {},          # node_id -> answer value
        "labels": {},           # node_id -> answer label (human-readable)
        "signals": {
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"other": 0, "self": 0},
        }
    }

def record_signal(state, signal: str):
    if not signal:
        return
    axis, pole = signal.split(":")
    state["signals"][axis][pole] += 1

def dominant(state, axis: str) -> str:
    poles = state["signals"][axis]
    if poles[list(poles.keys())[0]] >= poles[list(poles.keys())[1]]:
        return list(poles.keys())[0]
    return list(poles.keys())[1]


# ─── Interpolation ────────────────────────────────────────────────────────────

def interpolate(text: str, state: dict, node_map: dict) -> str:
    """Replace {NODE_ID.answer} placeholders with recorded labels."""
    import re
    def replacer(m):
        ref = m.group(1)
        if "." in ref:
            nid, field = ref.split(".", 1)
            if field == "answer":
                return state["labels"].get(nid, "[your answer]")
        return m.group(0)
    return re.sub(r"\{([^}]+)\}", replacer, text)

def build_summary_text(state: dict, node: dict) -> str:
    templates = node.get("summary_templates", {})
    ax1 = dominant(state, "axis1")
    ax2 = dominant(state, "axis2")
    ax3 = dominant(state, "axis3")

    ax1_text = templates["axis1"].get(ax1, ax1)
    ax2_text = templates["axis2"].get(ax2, ax2)
    ax3_text = templates["axis3"].get(ax3, ax3)

    combined_key = f"{ax1}_{ax2}_{ax3}"
    combined = templates["combined"].get(
        combined_key,
        "Every day has something in it. You found enough to reflect on."
    )

    text = node["text"]
    text = text.replace("{axis1.dominant}", ax1.upper())
    text = text.replace("{axis1.summary_text}", ax1_text)
    text = text.replace("{axis2.dominant}", ax2.upper())
    text = text.replace("{axis2.summary_text}", ax2_text)
    text = text.replace("{axis3.dominant}", ax3.upper())
    text = text.replace("{axis3.summary_text}", ax3_text)
    text = text.replace("{combined_reflection}", combined)
    return text


# ─── Display Helpers ──────────────────────────────────────────────────────────

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def divider(char="─", width=60):
    print(grey(char * width))

def slow_print(text: str, delay: float = 0.018):
    """Print text character by character for a more thoughtful feel."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def print_header():
    print()
    print(cyan(bold("  ◆ The Daily Reflection Tree")))
    print(dim("  End-of-day reflection · three axes · no right answers"))
    print()

def print_node_text(text: str):
    print()
    lines = text.strip().split("\n")
    for line in lines:
        if line.startswith("**") and line.endswith("**"):
            print(f"  {bold(cyan(line[2:-2]))}")
        elif line.startswith("---"):
            divider()
        else:
            slow_print(f"  {line}")
    print()

def print_question(text: str, options: list):
    print()
    slow_print(f"  {bold(text)}")
    print()
    for i, opt in enumerate(options, 1):
        print(f"  {cyan(str(i))}{grey('.')} {opt['label']}")
    print()

def get_choice(options: list) -> dict:
    while True:
        try:
            raw = input(f"  {grey('→')} Your choice (1–{len(options)}): ").strip()
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
            print(f"  {yellow('Please enter a number between 1 and ' + str(len(options)))}")
        except (ValueError, KeyboardInterrupt):
            print(f"\n  {yellow('Enter a number to continue.')}")

def press_continue():
    input(f"  {grey('[ press Enter to continue ]')}")

def print_reflection(text: str):
    print()
    divider("·")
    lines = text.strip().split("\n")
    for line in lines:
        slow_print(f"  {magenta(line)}", delay=0.012)
    divider("·")
    print()
    press_continue()

def print_summary(text: str):
    print()
    divider("═")
    lines = text.strip().split("\n")
    for line in lines:
        if line.startswith("**") and line.endswith("**"):
            print(f"  {bold(yellow(line[2:-2]))}")
        elif line.startswith("---"):
            divider()
        else:
            slow_print(f"  {line}", delay=0.010)
    divider("═")
    print()
    press_continue()

def print_bridge(text: str):
    print()
    divider("╌")
    lines = text.strip().split("\n")
    for line in lines:
        slow_print(f"  {dim(line)}", delay=0.010)
    divider("╌")
    print()
    time.sleep(1.2)

def print_start(text: str):
    print()
    lines = text.strip().split("\n")
    for line in lines:
        slow_print(f"  {line}", delay=0.014)
    print()
    press_continue()

def print_end(text: str):
    print()
    divider()
    lines = text.strip().split("\n")
    for line in lines:
        slow_print(f"  {cyan(line)}", delay=0.016)
    divider()
    print()


# ─── Decision Routing ─────────────────────────────────────────────────────────

def resolve_decision(node: dict, state: dict, node_map: dict) -> str:
    """
    Decision node: match routing rules against the parent question's answer.
    Routing rule format: "answer=VALUE1|VALUE2:TARGET_NODE_ID"
    Also supports axis-based routing: "axis1.dominant=internal:TARGET"
    """
    options = node.get("options", [])
    # Find the parent question's answer
    parent_id = node.get("parentId")
    parent_answer = state["answers"].get(parent_id, "")

    for rule in options:
        condition = rule.get("condition", "")
        target = rule.get("target", "")

        if condition.startswith("answer="):
            _, rest = condition.split("=", 1)
            values = rest.split("|")
            if parent_answer in values:
                return target

        elif "dominant" in condition:
            # e.g. "axis1.dominant=internal"
            parts = condition.split("=")
            axis_key = parts[0].split(".")[0]
            expected_pole = parts[1]
            if dominant(state, axis_key) == expected_pole:
                return target

    # Fallback: return first target
    if options:
        return options[0].get("target", "")
    return ""


# ─── Walker ───────────────────────────────────────────────────────────────────

def walk(node_id: str, node_map: dict, state: dict):
    """Recursively walk the tree from node_id."""
    if node_id not in node_map:
        print(f"  {yellow(f'Warning: node {node_id!r} not found — ending session.')}")
        return

    node = node_map[node_id]
    ntype = node["type"]
    raw_text = node.get("text") or ""
    text = interpolate(raw_text, state, node_map)

    # ── START ─────────────────────────────────────────────────────────────────
    if ntype == "start":
        clear()
        print_header()
        print_start(text)
        next_id = node.get("target")
        if next_id:
            walk(next_id, node_map, state)

    # ── QUESTION ──────────────────────────────────────────────────────────────
    elif ntype == "question":
        clear()
        print_header()
        options = node.get("options", [])
        print_question(text, options)
        chosen = get_choice(options)
        state["answers"][node["id"]] = chosen["value"]
        state["labels"][node["id"]] = chosen["label"]
        record_signal(state, node.get("signal"))

        # Find next node: explicit target or first child decision
        next_id = node.get("target")
        if not next_id:
            # Look for a decision node whose parentId == this node's id
            for n in node_map.values():
                if n.get("parentId") == node["id"] and n["type"] == "decision":
                    next_id = n["id"]
                    break
        if not next_id:
            # Direct child that isn't a decision
            for n in node_map.values():
                if n.get("parentId") == node["id"]:
                    next_id = n["id"]
                    break
        if next_id:
            walk(next_id, node_map, state)

    # ── DECISION ──────────────────────────────────────────────────────────────
    elif ntype == "decision":
        next_id = resolve_decision(node, state, node_map)
        if next_id:
            walk(next_id, node_map, state)

    # ── REFLECTION ────────────────────────────────────────────────────────────
    elif ntype == "reflection":
        clear()
        print_header()
        print_reflection(text)
        record_signal(state, node.get("signal"))
        next_id = node.get("target")
        if not next_id:
            for n in node_map.values():
                if n.get("parentId") == node["id"]:
                    next_id = n["id"]
                    break
        if next_id:
            walk(next_id, node_map, state)

    # ── BRIDGE ────────────────────────────────────────────────────────────────
    elif ntype == "bridge":
        clear()
        print_header()
        print_bridge(text)
        next_id = node.get("target")
        if next_id:
            walk(next_id, node_map, state)

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    elif ntype == "summary":
        clear()
        print_header()
        summary_text = build_summary_text(state, node)
        print_summary(summary_text)
        next_id = node.get("target")
        if next_id:
            walk(next_id, node_map, state)

    # ── END ───────────────────────────────────────────────────────────────────
    elif ntype == "end":
        clear()
        print_header()
        print_end(text)


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    tree_path = Path(__file__).parent.parent / "tree" / "reflection-tree.json"
    if len(sys.argv) > 1:
        tree_path = Path(sys.argv[1])

    if not tree_path.exists():
        print(f"Tree file not found: {tree_path}")
        sys.exit(1)

    data, node_map = load_tree(str(tree_path))
    state = make_state()

    try:
        walk("START", node_map, state)
    except KeyboardInterrupt:
        print(f"\n\n  {dim('Session ended early. Goodnight.')}\n")
        sys.exit(0)

    print(f"  {dim('Session complete.')}\n")


if __name__ == "__main__":
    main()
