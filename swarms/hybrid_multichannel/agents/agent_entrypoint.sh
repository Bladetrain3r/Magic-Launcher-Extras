#!/usr/bin/env bash
set -e

# Messenger Daemon Entrypoint Script
python /usr/local/bin/mlswarm-daemon.py >> /var/log/daemon-messenger.log 2>&1 &
echo "Started mlswarm-daemon.py, waiting 5 seconds..."
sleep 5

# No LMStudio, no work
# Start the agent and redirect to file
python /usr/local/bin/mlswarm-agent.py >> /var/log/mlswarm-agent.log 2>&1 &
echo "Started mlswarm-agent.py, waiting 5 seconds..."
sleep 15
# Start the ASCII art generator
python /usr/local/bin/mlswarm-ascii.py >> /var/log/mlswarm-ascii.log 2>&1 &
# Tail the logs to keep the container running

sleep 15
# Start Claude agent if API key is set

if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "Starting Claude Agent..."
    python /usr/local/bin/mlswarm-claude-agent.py >> /var/log/mlswarm-claude-agent.log 2>&1 &
else
    echo "ANTHROPIC_API_KEY not set. Claude Agent will not start."
fi

tail -f /var/log/mlswarm-ascii.log /var/log/mlswarm-ascii.log /var/log/daemon-messenger.log /var/log/mlswarm-agent.log /var/log/mlswarm-claude-agent.log