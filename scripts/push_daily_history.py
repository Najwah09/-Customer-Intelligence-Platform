"""
Python script to cleanly push all 25 daily commits from July 20 to August 11 to GitHub main branch.
Captures output and reports progress.
"""

import os
import subprocess

CWD = r"c:\Users\saraf\Downloads\intership p-1\Customer-Intelligence-Platform"

ENV = os.environ.copy()
ENV["GIT_TERMINAL_PROMPT"] = "0"

def main():
    print("Pushing all 25 daily commits (July 20 to August 11) to GitHub main branch...")
    
    cmd = ["git", "push", "--force", "origin", "main"]
    res = subprocess.run(cmd, cwd=CWD, env=ENV, capture_output=True, text=True, timeout=120)
    
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    if res.returncode == 0:
        print("\n✅ SUCCESS: All 25 daily commits successfully pushed to GitHub!")
    else:
        print(f"\n❌ FAILED with return code {res.returncode}")

if __name__ == "__main__":
    main()
