#!/bin/bash

# Cross-talk between norns
tail -n1 Sparkle1_response.txt > Sparkle2_command.txt  
tail -n1 Sparkle2_response.txt > Sparkle1_command.txt
sleep 10

# Status checks
echo "status" > Sparkle1_command.txt
echo "status" > Sparkle2_command.txt  
sleep 20

# Shakespeare feeding with encoding safety
echo "feed:$(shuf -n100 shakespeare.txt | python3 ../MLBabel.py --e 0.4 -l100 | tr -cd '[:print:][:space:]' | shuf -n1 | head -c 150)" > Sparkle1_command.txt
echo "feed:$(shuf -n100 shakespeare.txt | python3 ../MLBabel.py --e 0.4 -l100 | tr -cd '[:print:][:space:]' | shuf -n1 | head -c 150)" > Sparkle2_command.txt
sleep 20

# Affection  
echo "pet" > Sparkle1_command.txt
echo "pet" > Sparkle2_command.txt
sleep 30
