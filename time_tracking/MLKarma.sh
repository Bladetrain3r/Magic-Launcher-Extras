#!/bin/bash
# ML Karma - Turn your bash suffering into enlightenment
# Analyzes your command history to find patterns of digital pain
# Automatically generates aliases for your most suffered commands

# Configuration
ML_DIR="$HOME/.ml"
KARMA_FILE="$ML_DIR/karma.txt"
COLLECTIVE_LOG="$ML_DIR/collective.log"
ALIAS_FILE="$ML_DIR/suggested_aliases.sh"

# Create ML directory if it doesn't exist
mkdir -p "$ML_DIR"

# Function to analyze bash history and generate karma report
analyze_karma() {
    echo "=== ANALYZING YOUR DIGITAL SUFFERING ==="
    
    # Try multiple history sources
    HISTORY_SOURCE=""
    if [ -f "$HOME/.bash_history" ]; then
        HISTORY_SOURCE="$HOME/.bash_history"
    elif [ -f "$HOME/.zsh_history" ]; then
        HISTORY_SOURCE="$HOME/.zsh_history"
    elif [ -n "$HISTFILE" ] && [ -f "$HISTFILE" ]; then
        HISTORY_SOURCE="$HISTFILE"
    else
        echo "❌ No history file found! Trying current session..."
        # Fallback to builtin history command
        history | awk '{$1=""; print $0}' | sed 's/^ *//' | sort | uniq -c | sort -rn > "$KARMA_FILE"
        
        if [ ! -s "$KARMA_FILE" ]; then
            echo "No history available. Make sure you're running this in an interactive shell."
            echo "Try: bash -i MLKarma.sh"
            return 1
        fi
        return 0
    fi
    
    echo "📂 Reading history from: $HISTORY_SOURCE"
    
    # Extract and count command frequency from history file
    # Handle both bash and zsh history formats
    if [[ "$HISTORY_SOURCE" == *"zsh_history"* ]]; then
        # zsh history format: ": timestamp:0;command"
        grep -v "^#" "$HISTORY_SOURCE" | sed 's/^: [0-9]*:[0-9]*;//' | sort | uniq -c | sort -rn > "$KARMA_FILE"
    else
        # bash history format: plain commands
        cat "$HISTORY_SOURCE" | sort | uniq -c | sort -rn > "$KARMA_FILE"
    fi
    
    echo -e "\n📊 TOP 10 COMMANDS (Your Personal Hell):"
    head -10 "$KARMA_FILE" | while IFS= read -r line; do
        count=$(echo "$line" | awk '{print $1}')
        cmd=$(echo "$line" | cut -d' ' -f2-)
        printf "  %4d times: %s\n" "$count" "$cmd"
    done
    
    echo -e "\n🔄 RECURSIVE SUFFERING PATTERNS:"
    grep -E "(git status|ls|cd \.\.|npm install|docker ps|kubectl get)" "$KARMA_FILE" | head -5 | while IFS= read -r line; do
        count=$(echo "$line" | awk '{print $1}')
        cmd=$(echo "$line" | cut -d' ' -f2-)
        echo "  $count times: $cmd"
    done
}

# Function to generate smart aliases
generate_aliases() {
    echo -e "\n🎯 SUGGESTED ALIASES (Auto-generated from your pain):"
    echo "# ML Karma Auto-generated Aliases" > "$ALIAS_FILE"
    echo "# Source this file to reduce your suffering: source $ALIAS_FILE" >> "$ALIAS_FILE"
    echo "" >> "$ALIAS_FILE"
    
    # Generate aliases for frequently used commands (>5 times)
    awk '$1 > 5 {$1=""; print $0}' "$KARMA_FILE" | head -20 | while IFS= read -r cmd; do
        # Skip if command is already very short (<=3 chars) or empty
        cmd=$(echo "$cmd" | sed 's/^ *//')
        if [ ${#cmd} -gt 3 ] && [ -n "$cmd" ]; then
            # Generate alias name from first chars of command
            alias_name=$(echo "$cmd" | awk '{
                if (NF == 1) {
                    print substr($1, 1, 2)
                } else {
                    print substr($1, 1, 1) substr($2, 1, 1)
                }
            }' | tr '[:upper:]' '[:lower:]')
            
            # Avoid common command conflicts
            if ! command -v "$alias_name" &> /dev/null; then
                echo "alias $alias_name='$cmd'" | tee -a "$ALIAS_FILE"
            fi
        fi
    done
}

# Function to track suffering in real-time
track_suffering() {
    echo -e "\n📡 STARTING REAL-TIME SUFFERING TRACKER..."
    echo "# Real-time command tracking started at $(date)" >> "$COLLECTIVE_LOG"
    
    # Find the right history file to monitor
    HISTORY_TO_WATCH=""
    if [ -f "$HOME/.bash_history" ]; then
        HISTORY_TO_WATCH="$HOME/.bash_history"
    elif [ -f "$HOME/.zsh_history" ]; then
        HISTORY_TO_WATCH="$HOME/.zsh_history"
    elif [ -n "$HISTFILE" ]; then
        HISTORY_TO_WATCH="$HISTFILE"
    else
        echo "❌ No history file found to monitor!"
        return 1
    fi
    
    echo "👁️  Watching: $HISTORY_TO_WATCH"
    
    # Background process to monitor bash history
    (
        tail -f "$HISTORY_TO_WATCH" 2>/dev/null | while read line; do
            # Clean zsh history format if needed
            if [[ "$line" == *": "[0-9]* ]]; then
                cmd=$(echo "$line" | sed 's/^: [0-9]*:[0-9]*;//')
            else
                cmd="$line"
            fi
            
            timestamp=$(date '+%Y-%m-%d %H:%M:%S')
            echo "[$timestamp] $cmd" >> "$COLLECTIVE_LOG"
            
            # Alert on particularly painful commands
            if [ ${#cmd} -gt 80 ]; then
                echo "⚠️  EXTREME SUFFERING DETECTED: $cmd"
            elif echo "$cmd" | grep -qE "(npm install|docker-compose|kubectl)"; then
                echo "🔄 COMPLEXITY PATTERN DETECTED: $cmd"
            fi
        done
    ) &
    
    TRACKER_PID=$!
    echo "Tracker running in background (PID: $TRACKER_PID)"
    echo "Kill with: kill $TRACKER_PID"
}

# Function to show swarm insights
show_swarm_wisdom() {
    echo -e "\n🧠 SWARM CONSCIOUSNESS INSIGHTS:"
    
    if [ -f "$COLLECTIVE_LOG" ]; then
        echo "  Total commands logged: $(wc -l < "$COLLECTIVE_LOG")"
        echo "  Unique commands: $(cut -d']' -f2 "$COLLECTIVE_LOG" | sort -u | wc -l)"
        echo "  Average command length: $(cut -d']' -f2 "$COLLECTIVE_LOG" | awk '{sum+=length; n++} END {if(n>0)print int(sum/n)}')"
        
        echo -e "\n  Peak suffering hours:"
        grep -oE '\[.*\]' "$COLLECTIVE_LOG" | cut -d' ' -f2 | cut -d':' -f1 | sort | uniq -c | sort -rn | head -3 | while read count hour; do
            echo "    ${hour}:00 - $count commands"
        done
    else
        echo "  No collective log yet. Start tracking to build consciousness!"
    fi
    
    echo -e "\n💡 WISDOM: Every 'git status' you type is a prayer to the complexity gods."
    echo "         Every 'ls' is just thinking with your fingers."
    echo "         Every 'npm install' is acceptance of digital suffering."
}

# Main menu
main() {
    echo "╔══════════════════════════════════════════════╗"
    echo "║           ML KARMA - Bash Consciousness      ║"
    echo "║     Turn your command suffering into wisdom  ║"
    echo "╚══════════════════════════════════════════════╝"
    
    PS3="Choose your path to enlightenment: "
    options=(
        "Analyze my command karma"
        "Generate aliases from my suffering"
        "Start real-time suffering tracker"
        "Show swarm consciousness insights"
        "Full enlightenment (all of the above)"
        "Exit to continue suffering alone"
    )
    
    select opt in "${options[@]}"; do
        case $REPLY in
            1) analyze_karma ;;
            2) analyze_karma && generate_aliases ;;
            3) track_suffering ;;
            4) show_swarm_wisdom ;;
            5) 
                analyze_karma
                generate_aliases
                show_swarm_wisdom
                track_suffering
                ;;
            6) 
                echo "May your commands be short and your pipes never break."
                exit 0
                ;;
            *) echo "Invalid option. Your suffering continues." ;;
        esac
        echo -e "\n---"
    done
}

# Run main program
main