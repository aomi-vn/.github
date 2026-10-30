#!/usr/bin/env python3
"""AOMI-736: evidence + optional local A/B for org reusable CI dependency caches.

Decision target: setup-node `cache: npm` and setup-uv `enable-cache: true` in
`.github/workflows/ci.yml`. On default pr-sandbox runners, GitHub Actions cache
blob backends are denied (see aomi-ops prsandbox egress); npm/pip dirs are per-job
tmpfs with no cross-job reuse.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EGRESS_NOTE = (
    "aomi-ops infra/oracle-vps/prsandbox/README.md (Garlic): only "
    "productionresultssa<N>.blob.core.windows.net is allowed; other cache "
    "backends are denied fail-closed."
)
TMPFS_NOTE = (
    "aomi-ops prsandbox readback: /home/runner/.npm and pip cache live in "
    "per-job tmpfs only — no warm local cache on the next job."
)


@dataclass(frozen=True)
class BenchResult:
    label: str
    seconds: float


@dataclass(frozen=True)
class AbReport:
    task: str
    decision: str
    keep_cache: bool
    rationale: list[str]
    npm_ci_cold_s: float | None
    npm_ci_warm_s: float | None
    within_job_speedup_ratio: float | None
    cross_job_benefit_on_prsandbox: str


def _run(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def _time_npm_ci(repo: Path, *, label: str, clean_npm_cache: bool) -> BenchResult:
    env = os.environ.copy()
    npm_cache = repo / ".aomi736-npm-cache"
    if clean_npm_cache and npm_cache.exists():
        shutil.rmtree(npm_cache)
    npm_cache.mkdir(parents=True, exist_ok=True)
    env["npm_config_cache"] = str(npm_cache)
    node_modules = repo / "node_modules"
    if node_modules.exists():
        shutil.rmtree(node_modules)
    start = time.perf_counter()
    _run(["npm", "ci", "--ignore-scripts"], cwd=repo, env=env)
    elapsed = time.perf_counter() - start
    return BenchResult(label=label, seconds=round(elapsed, 2))


def run_bench(repo: Path) -> tuple[BenchResult, BenchResult]:
    if not (repo / "package-lock.json").is_file():
        raise SystemExit(f"no package-lock.json under {repo}")
    cold = _time_npm_ci(repo, label="npm_ci_cold", clean_npm_cache=True)
    warm = _time_npm_ci(repo, label="npm_ci_warm_local_cache", clean_npm_cache=False)
    return cold, warm


def build_report(cold: BenchResult | None, warm: BenchResult | None) -> AbReport:
    rationale = [EGRESS_NOTE, TMPFS_NOTE]
    npm_cold = cold.seconds if cold else None
    npm_warm = warm.seconds if warm else None
    ratio: float | None = None
    if cold and warm and warm.seconds > 0:
        ratio = round(cold.seconds / warm.seconds, 2)
        rationale.append(
            f"Local within-job npm cache speedup ~{ratio}x (cold {cold.seconds}s vs "
            f"warm {warm.seconds}s) — does not apply across pr-sandbox jobs."
        )
    cross = (
        "none: GHA cache blobs blocked and per-job tmpfs clears npm/pip between jobs"
    )
    keep = False
    decision = "remove_cache"
    rationale.append(
        "Net: cache hooks add restore/save work without cross-run hits on pr-sandbox; "
        "remove setup-node cache and setup-uv enable-cache from org reusable CI."
    )
    return AbReport(
        task="AOMI-736",
        decision=decision,
        keep_cache=keep,
        rationale=rationale,
        npm_ci_cold_s=npm_cold,
        npm_ci_warm_s=npm_warm,
        within_job_speedup_ratio=ratio,
        cross_job_benefit_on_prsandbox=cross,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bench-repo",
        type=Path,
        help="Path to an npm repo (package-lock.json) for local cold/warm npm ci timing",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON report on stdout")
    args = parser.parse_args()

    cold: BenchResult | None = None
    warm: BenchResult | None = None
    if args.bench_repo:
        cold, warm = run_bench(args.bench_repo.resolve())

    report = build_report(cold, warm)
    payload = asdict(report)
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"{report.task} decision={report.decision} keep_cache={report.keep_cache}")
        for line in report.rationale:
            print(f"  - {line}")
        if report.npm_ci_cold_s is not None:
            print(
                f"  npm_ci_cold_s={report.npm_ci_cold_s} "
                f"npm_ci_warm_s={report.npm_ci_warm_s} "
                f"within_job_speedup_ratio={report.within_job_speedup_ratio}"
            )
    return 0 if not report.keep_cache else 0


if __name__ == "__main__":
    sys.exit(main())
