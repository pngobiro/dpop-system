#!/bin/bash

# This script sets environment variables for local Django development.
# You should SOURCE this script, not execute it directly.
# Example: source set_local_env.sh

export POSTGRES_DB=judiciary
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5434
export DEBUG=True

# IMPORTANT: Replace these placeholder values with your actual project values!
# You can find these in your project's .env file or docker-compose.yml
export SECRET_KEY='your_secret_key_here'
export ASSETS_ROOT='/static/assets'
export OPENAI_API_KEY='your_openai_api_key_here'

echo "Local environment variables set. Remember to replace placeholder values for SECRET_KEY, ASSETS_ROOT, and OPENAI_API_KEY."