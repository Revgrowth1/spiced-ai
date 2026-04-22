#!/usr/bin/env python3
"""
spiced-ai CLI - analyze sales calls without Claude Code.

Usage:
  analyze.py --mode post_call --transcript call.txt --config revgrowth --deal-size MID
  analyze.py --mode coaching --transcript call.txt --rep "Alex Chen" --tenure 14
  analyze.py --mode pre_call --prior prior_calls.json --meeting meeting.json
  analyze.py --mode red_flags --transcript call.txt --prior prior_calls.json

Requires:
  ANTHROPIC_API_KEY environment variable
  pip install anthropic pyyaml
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import yaml
    from anthropic import Anthropic
except ImportError as e:
    sys.exit(f"Missing dependency: {e}. Run: pip install anthropic pyyaml")


REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"
CONFIG_DIR = REPO_ROOT / "config"

MODE_TO_PROMPT = {
    "post_call": "post-call-analysis.md",
    "coaching": "coaching.md",
    "pre_call": "pre-call-brief.md",
    "red_flags": "red-flags.md",
}

DEFAULT_MODEL = "claude-opus-4-7"  # switch to claude-sonnet-4-6 for cheaper/faster runs
DEFAULT_MAX_TOKENS = 8000


def load_prompt(mode: str) -> str:
    path = PROMPTS_DIR / MODE_TO_PROMPT[mode]
    if not path.exists():
        sys.exit(f"Prompt not found: {path}")
    return path.read_text()


def load_config(name: str) -> dict:
    path = CONFIG_DIR / f"{name}.yaml"
    if not path.exists():
        sys.exit(f"Config not found: {path}. Available: {[p.stem for p in CONFIG_DIR.glob('*.yaml')]}")
    with path.open() as f:
        return yaml.safe_load(f)


def read_input(path_or_dash: str) -> str:
    if path_or_dash == "-":
        return sys.stdin.read()
    p = Path(path_or_dash).expanduser()
    if not p.exists():
        sys.exit(f"Input not found: {p}")
    return p.read_text()


def build_user_message(args, prompt_text: str, config: dict) -> str:
    """Substitute inputs into the prompt's placeholders and return the user message."""
    substitutions = {
        "{{CONFIG_YAML}}": yaml.safe_dump(config, default_flow_style=False),
    }

    if args.transcript:
        substitutions["{{TRANSCRIPT}}"] = read_input(args.transcript)

    if args.company_context:
        substitutions["{{COMPANY_CONTEXT}}"] = read_input(args.company_context)
    else:
        substitutions["{{COMPANY_CONTEXT}}"] = "(not provided)"

    if args.mode == "post_call":
        deal_context = {
            "deal_size_band": args.deal_size or "MID",
            "prior_calls": args.prior_calls or 0,
            "solution_offered": args.solution or config.get("profile", {}).get("product_one_liner", ""),
        }
        substitutions["{{SMB|MID|ENTERPRISE}}"] = deal_context["deal_size_band"]
        substitutions["{{N}}"] = str(deal_context["prior_calls"])
        substitutions["{{SOLUTION_DESC}}"] = deal_context["solution_offered"]
        substitutions["{{slack|crm|internal}}"] = args.output_format

    elif args.mode == "coaching":
        substitutions["{{REP_NAME}}"] = args.rep or "(not provided)"
        substitutions["{{MONTHS}}"] = str(args.tenure or 0)
        substitutions["{{discovery|demo|proposal|closing}}"] = args.stage or "discovery"
        substitutions["{{optional_focus_areas}}"] = args.focus or ""
        substitutions["{{slack|crm|internal}}"] = args.output_format

    elif args.mode == "pre_call":
        if args.prior:
            substitutions["{{PRIOR_CALL_SUMMARIES}}"] = read_input(args.prior)
        else:
            substitutions["{{PRIOR_CALL_SUMMARIES}}"] = "(first call - no prior)"
        if args.meeting:
            substitutions["{{meeting_json}}"] = read_input(args.meeting)

    elif args.mode == "red_flags":
        if args.prior:
            substitutions["{{LAST_3_CALLS_SPICED_SCORES}}"] = read_input(args.prior)
        else:
            substitutions["{{LAST_3_CALLS_SPICED_SCORES}}"] = "(no prior analyses provided)"

    # Apply substitutions
    body = prompt_text
    for k, v in substitutions.items():
        body = body.replace(k, str(v))

    # Tag with user request at the top
    return (
        f"Run the {args.mode} analysis defined above. "
        f"Output format: {args.output_format}. "
        f"Use the inputs substituted inline. Return only the requested output - no preamble.\n\n"
        + body
    )


def call_claude(system: str, user: str, model: str, max_tokens: int) -> str:
    client = Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in msg.content if hasattr(block, "text"))


def parse_args():
    p = argparse.ArgumentParser(description="spiced-ai CLI - B2B sales call analysis")
    p.add_argument("--mode", required=True, choices=list(MODE_TO_PROMPT))
    p.add_argument("--config", default="default", help="Config name from config/ (default: 'default')")
    p.add_argument("--output-format", default="internal", choices=["slack", "crm", "internal"])
    p.add_argument("--transcript", help="Path to transcript file, or '-' for stdin")
    p.add_argument("--company-context", help="Path to company research / notes")
    p.add_argument("--prior", help="Path to prior analyses / summaries (JSON or markdown)")
    p.add_argument("--meeting", help="Path to meeting context JSON (for pre_call mode)")

    # post_call specific
    p.add_argument("--deal-size", choices=["SMB", "MID", "ENTERPRISE"], help="Deal size band")
    p.add_argument("--prior-calls", type=int, default=0, help="Number of prior calls")
    p.add_argument("--solution", help="One-liner on what you're selling")

    # coaching specific
    p.add_argument("--rep", help="Rep name")
    p.add_argument("--tenure", type=int, help="Rep tenure in months")
    p.add_argument("--stage", choices=["discovery", "demo", "proposal", "closing"])
    p.add_argument("--focus", help="Coaching focus areas")

    # model
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"Anthropic model ID (default: {DEFAULT_MODEL})")
    p.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)

    # output
    p.add_argument("-o", "--output", help="Write result to file instead of stdout")

    return p.parse_args()


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY not set")

    args = parse_args()
    prompt_text = load_prompt(args.mode)
    config = load_config(args.config)

    # Validate mode-specific required args
    if args.mode in ("post_call", "coaching", "red_flags") and not args.transcript:
        sys.exit(f"--transcript required for mode={args.mode}")
    if args.mode == "pre_call" and not args.prior and not args.meeting:
        sys.exit("--prior or --meeting required for mode=pre_call (give me something to prep against)")

    user_msg = build_user_message(args, prompt_text, config)

    # The full prompt becomes the system prompt; user message carries the inputs + request
    result = call_claude(
        system=prompt_text.split("## Inputs")[0] if "## Inputs" in prompt_text else prompt_text,
        user=user_msg,
        model=args.model,
        max_tokens=args.max_tokens,
    )

    if args.output:
        Path(args.output).write_text(result)
        print(f"Wrote {len(result)} chars to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
