"""Import the pinned Expansion source; retain upstream history and project C edits."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def run(*args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    if (ROOT / "Makefile").exists():
        print("Full source already present; no import or push needed.")
        return
    config = json.loads((ROOT / "docs/tides-of-dawn/upstream.json").read_text())
    if run("git", "status", "--porcelain", capture_output=True, text=True).stdout:
        raise SystemExit("Commit local changes before importing upstream.")
    if args.publish:
        branch = run("git", "branch", "--show-current", capture_output=True, text=True).stdout.strip()
        if branch != "main":
            raise SystemExit("Automatic source publication is only allowed on main.")
    run("git", "fetch", "--no-tags", config["repository"], "refs/tags/" + config["tag"])
    sha = run("git", "rev-parse", "FETCH_HEAD^{commit}", capture_output=True, text=True).stdout.strip()
    if sha != config["commit"]:
        raise SystemExit(f"Upstream tag moved: expected {config['commit']}, found {sha}")
    run("git", "merge", "--strategy=ours", "--no-commit", "--allow-unrelated-histories", sha)
    # Preserve project source edits. Never import upstream workflows into our CI.
    archive = subprocess.Popen(
        ["git", "archive", sha, ".", ":(exclude).github", ":(exclude)README.md"],
        cwd=ROOT, stdout=subprocess.PIPE,
    )
    try:
        run("tar", "--skip-old-files", "-xf", "-", stdin=archive.stdout)
    finally:
        archive.stdout.close()
    if archive.wait() != 0:
        raise SystemExit("Upstream archive failed; source import not committed.")
    # Include upstream's tracked assets even when their own .gitignore ignores them.
    raw_paths = run("git", "ls-tree", "-r", "--name-only", "-z", sha, capture_output=True).stdout
    paths = b"\0".join(p for p in raw_paths.split(b"\0")
                         if p and not p.startswith(b".github/") and p != b"README.md") + b"\0"
    run("git", "add", "-f", "--pathspec-from-file=-", "--pathspec-file-nul", input=paths)
    upstream_readme = run("git", "show", sha + ":README.md", capture_output=True).stdout
    (ROOT / "docs/tides-of-dawn/UPSTREAM_README.md").write_bytes(upstream_readme)
    run("git", "add", "docs/tides-of-dawn/UPSTREAM_README.md")
    run("git", "commit", "-m", "Import Expansion 1.17.1 source and modern Tides starters")
    if args.publish:
        run("git", "push", "origin", "HEAD:refs/heads/main")
    print(f"Imported {config['tag']} at {sha}.")


if __name__ == "__main__":
    main()
