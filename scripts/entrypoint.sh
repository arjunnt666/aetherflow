#!/bin/bash
set -e
echo "AetherFlow starting..."
echo "Environment: ${AETHERFLOW_ENV:-development}"
exec python -m aetherflow.cli.main "$@"
