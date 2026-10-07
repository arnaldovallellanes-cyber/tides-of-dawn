import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / "tools/tides/bootstrap_source.py"


class BootstrapTests(unittest.TestCase):
    def test_import_keeps_source_edits_assets_and_upstream_ancestry(self):
        with tempfile.TemporaryDirectory() as tmp:
            upstream = Path(tmp) / "upstream"
            project = Path(tmp) / "project"

            def git(folder, *args):
                return subprocess.check_output(["git", "-C", str(folder), *args], stderr=subprocess.DEVNULL)

            for folder in (upstream, project):
                folder.mkdir()
                git(folder, "init", "-b", "main")
                git(folder, "config", "user.name", "Tides Test")
                git(folder, "config", "user.email", "test@example.invalid")
            (upstream / "src").mkdir()
            (upstream / ".github").mkdir()
            (upstream / "Makefile").write_text("all:\n")
            (upstream / "README.md").write_text("Upstream attribution\n")
            (upstream / ".gitignore").write_text("*.bin\n")
            (upstream / "src/starter_choose.c").write_text("upstream starter\n")
            (upstream / "sprite.bin").write_bytes(b"\x00\xff")
            (upstream / ".github/upstream.yml").write_text("excluded workflow")
            git(upstream, "add", "-f", ".")
            git(upstream, "commit", "-m", "upstream fixture")
            sha = git(upstream, "rev-parse", "HEAD").decode().strip()
            git(upstream, "tag", "expansion/1.17.1")
            (project / "tools/tides").mkdir(parents=True)
            (project / "docs/tides-of-dawn").mkdir(parents=True)
            (project / "src").mkdir()
            shutil.copyfile(SCRIPT, project / "tools/tides/bootstrap_source.py")
            (project / "docs/tides-of-dawn/upstream.json").write_text(json.dumps({
                "repository": str(upstream), "tag": "expansion/1.17.1", "commit": sha}))
            (project / "README.md").write_text("Tides README\n")
            (project / "src/starter_choose.c").write_text("modern starter\n")
            git(project, "add", ".")
            git(project, "commit", "-m", "project fixture")
            subprocess.run(["python3", str(project / "tools/tides/bootstrap_source.py")],
                           check=True, capture_output=True)
            self.assertTrue((project / "Makefile").exists())
            self.assertEqual((project / "src/starter_choose.c").read_text(), "modern starter\n")
            self.assertEqual((project / "README.md").read_text(), "Tides README\n")
            self.assertEqual(git(project, "show", "HEAD:sprite.bin"), b"\x00\xff")
            self.assertFalse((project / ".github/upstream.yml").exists())
            self.assertEqual(git(project, "rev-parse", "HEAD^2").decode().strip(), sha)
            self.assertEqual(git(project, "status", "--porcelain"), b"")
            before = git(project, "rev-parse", "HEAD")
            subprocess.run(["python3", str(project / "tools/tides/bootstrap_source.py")],
                           check=True, capture_output=True)
            self.assertEqual(git(project, "rev-parse", "HEAD"), before)


if __name__ == "__main__":
    unittest.main()
