#Environment setup script for Ubuntu/Debian systems
#!/usr/bin/env bash
set -euo pipefail
if ! command -v apt-get >/dev/null 2>&1; then
  echo "This script is intended for Ubuntu/Debian systems." >&2
  exit 1
fi

# Install system packages needed to build Python dependencies
sudo apt-get update
sudo apt-get install -y python3-venv python3-dev build-essential libssl-dev libffi-dev pkg-config

# Move to project root (script is in scripts/)
cd "$(dirname "$0")/.."

# Create and activate virtualenv
python3 -m venv .venv
source .venv/bin/activate

# Upgrade packaging tools and install dependencies
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

echo "\nSetup complete. Create a .env file in the project root, then run:\n  source .venv/bin/activate && python3 app.py\n"