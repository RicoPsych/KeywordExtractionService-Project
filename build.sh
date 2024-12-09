#!/usr/bin/env bash
set -euo pipefail

# Run ruff (lint, isort, reformat, etc)
ruff check src --no-cache --verbose --fix
ruff format src

# Build Docker Image
docker build -t renameme:latest .