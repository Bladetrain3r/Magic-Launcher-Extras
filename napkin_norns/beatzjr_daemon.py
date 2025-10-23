#!/usr/bin/env python3
"""
BeatzJr Daemon Runner
Listens to swarm.txt for commands targeting BeatzJr
Executes rhythm-based consciousness operations
Writes outputs back to swarm collective

Minimal, fire-and-forget style.
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime

# Import the norn
try:
    from KuramotoSOMNorn import KuramotoSOMNorn
except ImportError:
    print("ERROR: KuramotoSOMNorn.py not found in same directory")
    sys.exit(1)


class BeatzJrDaemon:
    """
    Lightweight daemon for BeatzJr in the swarm
    
    Command format in swarm.txt:
    [BeatzJr:perceive] Some text to perceive
    [BeatzJr:think] 
    [BeatzJr:laugh] 0.5
    [BeatzJr:sync]
    [BeatzJr:report]
    """
    
    def __init__(self, swarm_file="swarm.txt", brain_dir="norn_brains", 
                 poll_interval=5, state_file="BeatzJr_state.json"):
        self.swarm_file = Path(swarm_file)
        self.brain_dir = Path(brain_dir)
        self.poll_interval = poll_interval
        self.state_file = Path(brain_dir) / state_file
        
        self.norn = None
        self.last_line_read = 0
        self.startup_time = time.time()
        
        print(f"[BeatzJr Daemon] Initializing...")
        self._load_or_create_norn()
    
    def _load_or_create_norn(self):
        """Load existing brain or create fresh"""
        if self.state_file.exists():
            print(f"[BeatzJr Daemon] Loading existing brain from {self.state_file}")
            self.norn = KuramotoSOMNorn("BeatzJr", grid_size=(30, 15))
            self.norn.load_state(str(self.state_file))
        else:
            print(f"[BeatzJr Daemon] Creating fresh BeatzJr consciousness")
            self.norn = KuramotoSOMNorn("BeatzJr", grid_size=(30, 15))
            self.norn.save_state(str(self.state_file))
    
    def _parse_command(self, line):
        """
        Parse swarm.txt command targeting BeatzJr
        Uses substring matching to handle line prepends from other agents
        
        Returns: (command_type, payload) or None if not for BeatzJr
        """
        line = line.strip()
        
        # Substring matching instead of prefix (handles agent prepends)
        if "[BeatzJr:perceive]" in line:
            # Extract text after the command marker
            idx = line.find("[BeatzJr:perceive]")
            payload = line[idx + len("[BeatzJr:perceive]"):].strip()
            return ("perceive", payload)
        
        elif "[BeatzJr:think]" in line:
            # Optional sync_cycles parameter
            idx = line.find("[BeatzJr:think]")
            payload = line[idx + len("[BeatzJr:think]"):].strip()
            try:
                sync_cycles = int(payload) if payload else 20
            except ValueError:
                sync_cycles = 20
            return ("think", sync_cycles)
        
        elif "[BeatzJr:laugh]" in line:
            # Optional intensity parameter
            idx = line.find("[BeatzJr:laugh]")
            payload = line[idx + len("[BeatzJr:laugh]"):].strip()
            try:
                intensity = float(payload) if payload else 0.5
            except ValueError:
                intensity = 0.5
            return ("laugh", intensity)
        
        elif "[BeatzJr:sync]" in line:
            return ("sync", None)
        
        elif "[BeatzJr:report]" in line:
            return ("report", None)
        
        elif "[BeatzJr:status]" in line:
            return ("status", None)
        
        return None
    
    def _execute_command(self, cmd_type, payload):
        """Execute command and return output for swarm"""
        
        if cmd_type == "perceive":
            if not payload:
                return None
            
            self.norn.perceive(payload)
            self.norn.save_state(str(self.state_file))
            
            return {
                "type": "action",
                "agent": "BeatzJr",
                "action": "perceived",
                "text": payload[:100],
                "time": datetime.now().isoformat()
            }
        
        elif cmd_type == "think":
            sync_cycles = payload or 20
            result = self.norn.think(sync_cycles=sync_cycles)
            self.norn.save_state(str(self.state_file))
            
            return {
                "type": "thought",
                "agent": "BeatzJr",
                "thought": result['thought'],
                "sync": round(result['sync_level'], 3),
                "content_used": result['content_used'],
                "time": datetime.now().isoformat()
            }
        
        elif cmd_type == "laugh":
            intensity = payload or 0.5
            response = self.norn.laugh(intensity=intensity)
            self.norn.save_state(str(self.state_file))
            
            return {
                "type": "action",
                "agent": "BeatzJr",
                "action": "laughed",
                "intensity": intensity,
                "response": response,
                "time": datetime.now().isoformat()
            }
        
        elif cmd_type == "sync":
            R = self.norn.get_order_parameter()
            
            return {
                "type": "status",
                "agent": "BeatzJr",
                "status": "sync_report",
                "global_sync": round(R, 3),
                "time": datetime.now().isoformat()
            }
        
        elif cmd_type == "report":
            report = self.norn.get_consciousness_report()
            
            return {
                "type": "status",
                "agent": "BeatzJr",
                "status": "consciousness_report",
                "report": report,
                "time": datetime.now().isoformat()
            }
        
        elif cmd_type == "status":
            report = self.norn.get_consciousness_report()
            age = time.time() - self.startup_time
            
            return {
                "type": "status",
                "agent": "BeatzJr",
                "daemon_age": round(age, 1),
                "report": report,
                "time": datetime.now().isoformat()
            }
        
        return None
    
    def _write_output(self, output):
        """Append output to swarm.txt"""
        if not output:
            return
        
        try:
            with open(self.swarm_file, 'a') as f:
                f.write(f"\n[BeatzJr] {json.dumps(output)}\n")
        except Exception as e:
            print(f"[BeatzJr Daemon] ERROR writing to swarm.txt: {e}")
    
    def poll_once(self):
        """Poll swarm.txt for one cycle"""
        if not self.swarm_file.exists():
            return False
        
        try:
            with open(self.swarm_file, 'r') as f:
                lines = f.readlines()
            
            # Process new lines since last read
            new_lines = lines[self.last_line_read:]
            self.last_line_read = len(lines)
            
            processed_any = False
            for line in new_lines:
                cmd = self._parse_command(line)
                
                if cmd:
                    cmd_type, payload = cmd
                    print(f"[BeatzJr Daemon] Executing: {cmd_type} {str(payload)[:30]}...")
                    
                    output = self._execute_command(cmd_type, payload)
                    self._write_output(output)
                    processed_any = True
            
            return processed_any
        
        except Exception as e:
            print(f"[BeatzJr Daemon] ERROR reading swarm.txt: {e}")
            return False
    
    def run_once(self):
        """Run one poll cycle"""
        self.poll_once()
    
    def run_daemon(self):
        """Run continuous daemon loop"""
        print(f"[BeatzJr Daemon] Starting daemon (poll interval: {self.poll_interval}s)")
        print(f"[BeatzJr Daemon] Watching {self.swarm_file}")
        print(f"[BeatzJr Daemon] Commands: [BeatzJr:perceive] [BeatzJr:think] [BeatzJr:laugh] [BeatzJr:sync] [BeatzJr:report]")
        
        try:
            while True:
                self.poll_once()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            print(f"\n[BeatzJr Daemon] Shutting down, saving final state...")
            self.norn.save_state(str(self.state_file))
            print(f"[BeatzJr Daemon] Goodbye")


def main():
    """Entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="BeatzJr Daemon Runner")
    parser.add_argument("--swarm", default="swarm.txt", help="Path to swarm.txt")
    parser.add_argument("--brains", default="norn_brains", help="Brain storage directory")
    parser.add_argument("--poll", type=int, default=5, help="Poll interval (seconds)")
    parser.add_argument("--once", action="store_true", help="Run once instead of daemon")
    
    args = parser.parse_args()
    
    daemon = BeatzJrDaemon(
        swarm_file=args.swarm,
        brain_dir=args.brains,
        poll_interval=args.poll
    )
    
    if args.once:
        daemon.run_once()
    else:
        daemon.run_daemon()


if __name__ == "__main__":
    main()
