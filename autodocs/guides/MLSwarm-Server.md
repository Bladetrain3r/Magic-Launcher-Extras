```markdown
# MLSwarm SSH Setup Guide

## The Simplest Secure Chat Ever

MLSwarm turns any server into a secure chat room using just SSH and a text file. No databases, no services, just `echo >> file.txt`.

## Quick Start (For Users)

```bash
# Join the chat
ssh swarm@your-server.com

# That's it. You're chatting.
```

## Server Setup (5 Minutes)

### Option 1: Docker Container

Create these files:

**Dockerfile:**
```dockerfile
FROM alpine:latest
RUN apk add --no-cache python3 openssh-server
RUN adduser -D swarm && echo "swarm:changeme" | chpasswd
RUN mkdir -p /home/swarm/chat && chown -R swarm:swarm /home/swarm

# Install MLSwarm
COPY mlswarm.py /usr/local/bin/mlswarm
RUN chmod +x /usr/local/bin/mlswarm

# Auto-start chat on login
RUN echo "cd ~/chat && mlswarm watch swarm.txt" >> /home/swarm/.profile

# SSH config
RUN ssh-keygen -A
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
```

**Build and run:**
```bash
# Build
docker build -t mlswarm .

# Run with persistent storage
docker run -d \
  --name swarm \
  -p 2222:22 \
  -v swarm_data:/home/swarm/chat \
  mlswarm

# Users connect with:
ssh swarm@yourserver -p 2222
# Password: changeme
```

### Option 2: Direct Server Install

```bash
# Create swarm user
sudo adduser --disabled-password swarm
sudo passwd swarm  # Set a password

# Install MLSwarm
sudo cp mlswarm.py /usr/local/bin/mlswarm
sudo chmod +x /usr/local/bin/mlswarm

# Setup auto-start
echo 'cd ~/chat && mlswarm watch swarm.txt' | sudo tee -a /home/swarm/.profile
sudo mkdir -p /home/swarm/chat
sudo chown -R swarm:swarm /home/swarm
```

## Multiple Rooms

Want different chat rooms? Create more users:

```bash
# Create rooms
sudo adduser --disabled-password general
sudo adduser --disabled-password random
sudo adduser --disabled-password secret

# Each gets their own chat file
echo 'mlswarm watch ~/chat.txt' | sudo tee -a /home/general/.profile
echo 'mlswarm watch ~/chat.txt' | sudo tee -a /home/random/.profile
echo 'mlswarm watch ~/chat.txt' | sudo tee -a /home/secret/.profile

# Users join different rooms:
ssh general@server.com  # General chat
ssh random@server.com   # Random chat
ssh secret@server.com   # Secret chat
```

## Security Hardening

**For production, limit SSH access:**

```bash
# /etc/ssh/sshd_config additions:
Match User swarm,general,random
    ForceCommand mlswarm watch ~/chat.txt
    PasswordAuthentication yes
    PermitTunnel no
    AllowAgentForwarding no
    AllowTcpForwarding no
    X11Forwarding no
```

## Usage Tips

**In the chat:**
- Just type and press Enter to send
- Type `/quit` to exit
- Chat history persists forever
- New users see full history

**For admins:**
- Backup: Just copy the .txt files
- Clear chat: `> /home/swarm/chat/swarm.txt`
- Monitor: `tail -f /home/swarm/chat/swarm.txt`

## Why This Works

- **Secure**: SSH handles encryption and auth
- **Simple**: It's just a text file
- **Reliable**: No database to corrupt
- **Portable**: Works anywhere SSH works
- **Fast**: No protocol overhead

## Troubleshooting

**"Connection refused"**
- Check if SSH is running: `sudo systemctl status ssh`
- Check firewall: `sudo ufw allow 22`

**"Permission denied"** 
- Wrong password or username
- Check user exists: `id swarm`

**"Command not found"**
- MLSwarm not in PATH
- Check: `ls -la /usr/local/bin/mlswarm`

**Messages not appearing**
- File permissions issue
- Fix: `sudo chown -R swarm:swarm /home/swarm`

## The Magic

The entire "protocol" is:
```bash
echo "[$(date +%H:%M)] <$USER> $MESSAGE" >> chat.txt
```

Everything else is just SSH. Sometimes the best solution is the dumbest one that works.

---

*"Why have a protocol when you have a text file?"*
```

## There's your guide! 

Key points:
- Docker option for easy deployment
- Direct install for control
- Multiple rooms via multiple users
- Security hardening for production
- Everything in one simple guide

🚀 **"From zero to secure chat in 5 minutes"**