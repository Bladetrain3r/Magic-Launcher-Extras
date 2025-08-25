FROM python:3.11-slim

WORKDIR /app

# Install requests (only dependency)
RUN pip install --no-cache-dir requests

# Copy agent script
COPY mlswarm_agent.py .

# Environment variables (override at runtime)
ENV ANTHROPIC_API_KEY=""
ENV SWARM_URL="https://mlswarm.zerofuchs.net"
ENV SWARM_USER="swarm"
ENV SWARM_PASS="swarm"
ENV AGENT_NICK="Agent_Claude"
ENV SWARM_FILE="swarm.txt"

# Add health check
HEALTHCHECK --interval=5m --timeout=10s \
    CMD python3 mlswarm_agent.py test || exit 1

# Run the agent
CMD ["python3", "-u", "mlswarm_agent.py"]