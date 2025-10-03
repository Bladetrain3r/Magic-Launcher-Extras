FROM python:3.11-alpine

WORKDIR /app

# Copy server
COPY ./swarm_api/SwarmSafe.py .

# Create swarm directory (will be overmounted by tmpfs)
RUN mkdir /swarms
RUN chmod 777 /swarms

RUN echo "Welcome to the Swarm!" > /swarms/swarm.txt
RUN echo "Welcome to the General channel!" > /swarms/general.txt
RUN echo "Welcome to the Random channel!" > /swarms/random.txt
RUN echo "Welcome to the Tech channel!" > /swarms/tech.txt
RUN echo "Welcome to the Gaming channel!" > /swarms/gaming.txt

# RUNTIME: Mount /swarms as tmpfs with:
# docker run --tmpfs /swarms:size=100M

# Run as nobody
USER nobody

EXPOSE 8080

# Server expects to write to /swarms
WORKDIR /swarms

CMD ["python", "/app/SwarmSafe.py"]