#!/usr/bin/env python3
"""
CSV to MIDI Generator
Reads CSV with time, pitch, velocity, duration columns and generates MIDI file
"""

import csv
import sys
from pathlib import Path

# Simple MIDI file generator (no external dependencies)
class SimpleMIDI:
    def __init__(self):
        self.tracks = []
        self.ticks_per_quarter = 480
        
    def add_note(self, channel, pitch, velocity, start_time, duration):
        """Add a note to the MIDI track"""
        start_ticks = int(start_time * self.ticks_per_quarter)
        duration_ticks = int(duration * self.ticks_per_quarter)
        
        # Note on event
        note_on = {
            'time': start_ticks,
            'type': 'note_on',
            'channel': channel,
            'pitch': int(pitch),
            'velocity': int(velocity)
        }
        
        # Note off event  
        note_off = {
            'time': start_ticks + duration_ticks,
            'type': 'note_off', 
            'channel': channel,
            'pitch': int(pitch),
            'velocity': 0
        }
        
        self.tracks.extend([note_on, note_off])
    
    def write_midi_bytes(self):
        """Generate MIDI file bytes"""
        # Sort events by time
        self.tracks.sort(key=lambda x: x['time'])
        
        # MIDI Header
        header = b'MThd'  # Header chunk
        header += (6).to_bytes(4, 'big')  # Header length
        header += (0).to_bytes(2, 'big')  # Format type 0
        header += (1).to_bytes(2, 'big')  # Number of tracks
        header += self.ticks_per_quarter.to_bytes(2, 'big')  # Ticks per quarter note
        
        # Track data
        track_data = b''
        last_time = 0
        
        for event in self.tracks:
            # Delta time (variable length quantity)
            delta = event['time'] - last_time
            delta_bytes = self._encode_variable_length(delta)
            track_data += delta_bytes
            
            # MIDI event
            if event['type'] == 'note_on':
                track_data += bytes([0x90 | event['channel']])  # Note on
                track_data += bytes([event['pitch']])
                track_data += bytes([event['velocity']])
            elif event['type'] == 'note_off':
                track_data += bytes([0x80 | event['channel']])  # Note off
                track_data += bytes([event['pitch']])
                track_data += bytes([event['velocity']])
            
            last_time = event['time']
        
        # End of track
        track_data += b'\x00\xFF\x2F\x00'
        
        # Track header
        track_header = b'MTrk'
        track_header += len(track_data).to_bytes(4, 'big')
        
        return header + track_header + track_data
    
    def _encode_variable_length(self, value):
        """Encode integer as MIDI variable length quantity"""
        if value == 0:
            return b'\x00'
            
        result = []
        result.append(value & 0x7F)
        value >>= 7
        
        while value > 0:
            result.append((value & 0x7F) | 0x80)
            value >>= 7
            
        return bytes(reversed(result))

def csv_to_midi(csv_file, midi_file=None):
    """Convert CSV to MIDI file"""
    if midi_file is None:
        midi_file = csv_file.replace('.csv', '.mid')
    
    midi = SimpleMIDI()
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            note_count = 0
            
            for row in reader:
                time = float(row['time'])
                pitch = int(float(row['pitch']))
                velocity = int(float(row['velocity']))
                duration = float(row['duration'])
                
                # Clamp values to MIDI ranges
                pitch = max(0, min(127, pitch))
                velocity = max(1, min(127, velocity))
                
                midi.add_note(0, pitch, velocity, time, duration)
                note_count += 1
        
        # Write MIDI file
        with open(midi_file, 'wb') as f:
            f.write(midi.write_midi_bytes())
        
        print(f"✓ Converted {note_count} notes from {csv_file} to {midi_file}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting CSV to MIDI: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python csv_to_midi.py <csv_file> [output_midi_file]")
        print("Example: python csv_to_midi.py collatz_music.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    midi_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(csv_file).exists():
        print(f"✗ CSV file not found: {csv_file}")
        sys.exit(1)
    
    print(f"Converting {csv_file} to MIDI...")
    success = csv_to_midi(csv_file, midi_file)
    
    if success:
        print("🎵 MIDI file generated successfully!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()