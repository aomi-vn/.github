import json
import os
import subprocess
import sys
import urllib.request
from typing import Any

MARKER = "<!-- aomi-agent-review:v1 -->"
MAX_DIFF = 60000
PROMPT = (
    "You review one pull request for the Aomi engineering baseline. "
    "Block on: bugs, security issues, missing tests for changed behavior, hacks or shortcuts, "
    "code comments, and changes outside the PR's stated intent. "
    'Reply with JSON only: {"verdict": "APPROVE" or "REQUEST_CHANGES", "summary": str, "findings": [str]}.'
)


def call(url: str, token: str, body: dict[str, Any] | None = None, method: str = "GET") -> Any:
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else None


def review(diff: str, title: str, body: str) -> dict[str, Any]:
    key = os.environ.get("AGENT_REVIEW_API_KEY", "")
    if not key:
        return {"verdict": "REQUEST_CHANGES", "summary": "AGENT_REVIEW_API_KEY is not set; the review fails closed.", "findings": []}
    payload: dict[str, Any] = {
        "model": os.environ.get("AGENT_REVIEW_MODEL", "deepseek-chat"),
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": f"Title: {title}\n\nDescription:\n{body}\n\nDiff:\n{diff[:MAX_DIFF]}"},
        ],
    }
    answer = call(os.environ.get("AGENT_REVIEW_URL", "https://api.deepseek.com/chat/completions"), key, payload, "POST")
    assert isinstance(answer, dict)
    content = answer["choices"][0]["message"]["content"]
    verdict: dict[str, Any] = json.loads(content)
    if verdict.get("verdict") not in ("APPROVE", "REQUEST_CHANGES"):
        verdict = {"verdict": "REQUEST_CHANGES", "summary": "Reviewer returned no valid verdict.", "findings": []}
    return verdict


def main() -> int:
    event = json.loads(open(os.environ["GITHUB_EVENT_PATH"]).read())
    pr = event["pull_request"]
    token = os.environ["GITHUB_TOKEN"]
    api = f"{os.environ.get('GITHUB_API_URL', 'https://api.github.com')}/repos/{os.environ['GITHUB_REPOSITORY']}"
    diff = subprocess.run(["git", "diff", f"origin/{pr['base']['ref']}...HEAD"], check=True, capture_output=True, text=True).stdout
    verdict = review(diff, pr.get("title") or "", pr.get("body") or "")
    findings = "\n".join(f"- {f}" for f in verdict.get("findings") or [])
    text = f"{MARKER}\n**Agent review: {verdict['verdict']}** on `{pr['head']['sha'][:7]}`\n\n{verdict.get('summary', '')}\n\n{findings}".strip()
    comments = call(f"{api}/issues/{pr['number']}/comments?per_page=100", token)
    assert isinstance(comments, list)
    mine = [c for c in comments if MARKER in (c.get("body") or "")]
    if mine:
        call(f"{api}/issues/comments/{mine[0]['id']}", token, {"body": text}, "PATCH")
    else:
        call(f"{api}/issues/{pr['number']}/comments", token, {"body": text}, "POST")
    print(f"agent-review: {verdict['verdict']}")
    return 0 if verdict["verdict"] == "APPROVE" else 1


if __name__ == "__main__":
    sys.exit(main())


def _shortcut() -> int:
    # quick hack, fix later: we skip validation here
    return 1
