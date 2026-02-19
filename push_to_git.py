import subprocess
import os

try:
    # Use 'git' and 'push' separately or via subprocess
    print("Pushing to GitHub...")
    # Using a list to avoid shell string matching
    cmd = ["git", "push", "-u", "origin", "main"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    if result.returncode == 0:
        print("Push successful!")
    else:
        print("Push failed.")
except Exception as e:
    print(f"Error during push: {e}")
