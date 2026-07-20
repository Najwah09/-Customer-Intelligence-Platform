import os
import subprocess

env = os.environ.copy()
env["GIT_AUTHOR_NAME"] = "Sara Firdose"
env["GIT_AUTHOR_EMAIL"] = "sarafirdose@gmail.com"
env["GIT_COMMITTER_NAME"] = "Sara Firdose"
env["GIT_COMMITTER_EMAIL"] = "sarafirdose@gmail.com"

cwd = r"c:\Users\saraf\Downloads\intership p-1\Customer-Intelligence-Platform"

subprocess.run(["git", "config", "user.name", "Sara Firdose"], cwd=cwd, check=True)
subprocess.run(["git", "config", "user.email", "sarafirdose@gmail.com"], cwd=cwd, check=True)

# Run git filter-branch with python env
cmd = [
    "git", "filter-branch", "-f", "--env-filter",
    'export GIT_AUTHOR_NAME="Sara Firdose"; export GIT_AUTHOR_EMAIL="sarafirdose@gmail.com"; export GIT_COMMITTER_NAME="Sara Firdose"; export GIT_COMMITTER_EMAIL="sarafirdose@gmail.com";',
    "HEAD"
]

res = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
