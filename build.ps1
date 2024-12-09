#!/usr/bin/env pwsh
# Enable strict error handling
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Run ruff (lint, isort, reformat, etc)
ruff check src --no-cache --verbose --fix
ruff format src

# Build Docker Image
docker build -t renameme:latest .