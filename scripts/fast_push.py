import subprocess
import sys

ref = sys.argv[1] if len(sys.argv) > 1 else "main"
cmd = ["git", "push", "--force", "origin", f"{ref}:refs/heads/main"]
print(f"Pushing {ref} to origin/main...")
res = subprocess.run(cmd, cwd=r"c:\Users\saraf\Downloads\intership p-1\Customer-Intelligence-Platform", capture_output=True, text=True, timeout=30)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
