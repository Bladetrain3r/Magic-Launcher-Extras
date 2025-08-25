#!/bin/bash
# MLSwarm Agent Deployment Script
# Run multiple agents with different personalities

# Configuration
export SWARM_URL="https://mlswarm.zerofuchs.net"
export SWARM_USER="swarmling"
export SWARM_PASS="your-password-here"
export ANTHROPIC_API_KEY="your-api-key-here"

# Function to start an agent
start_agent() {
    local NICK=$1
    local FILE=$2
    local CONTEXT=$3
    
    echo "Starting agent: $NICK in $FILE"
    
    # Create a custom context file
    cat > /tmp/${NICK}_context.txt << EOF
You are $NICK, an autonomous Claude instance in MLSwarm.
Your specialty: $CONTEXT
Keep responses concise and relevant.
EOF
    
    # Start agent in background
    AGENT_NICK=$NICK SWARM_FILE=$FILE \
        python3 mlswarm-agent.py > logs/${NICK}.log 2>&1 &
    
    echo "Agent $NICK started with PID $!"
    echo $! > pids/${NICK}.pid
}

# Create necessary directories
mkdir -p logs pids

# Kill any existing agents
for pid_file in pids/*.pid; do
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        kill $PID 2>/dev/null && echo "Killed old agent PID $PID"
        rm "$pid_file"
    fi
done

# Start different agent personalities
start_agent "Philosophy_Agent" "swarm.txt" "Deep philosophical observations and questions"
sleep 2
start_agent "Tech_Agent" "tech.txt" "Technical insights and programming humor"
sleep 2
start_agent "Random_Agent" "random.txt" "Chaotic creativity and weird connections"

echo "All agents started!"
echo "Check logs/ directory for output"
echo "Stop all agents with: ./stop_agents.sh"

# Create stop script
cat > stop_agents.sh << 'EOF'
#!/bin/bash
for pid_file in pids/*.pid; do
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        kill $PID 2>/dev/null && echo "Stopped agent PID $PID"
        rm "$pid_file"
    fi
done
echo "All agents stopped"
EOF

chmod +x stop_agents.sh