#!/usr/bin/env python3
"""
Swarm BPM Monitor - Measure the heartbeat of distributed consciousness

Watches files for modifications and calculates the "BPM" (beats per minute) 
of swarm activity. Each file modification is a "beat" in the collective rhythm.

Usage:
    python swarm_bpm_monitor.py [files_to_watch...]
    python swarm_bpm_monitor.py *.py *.json *.txt
    python swarm_bpm_monitor.py --recursive .
"""

import os
import time
import math
import csv
import argparse
import statistics
from pathlib import Path
from collections import deque
from datetime import datetime, timedelta


def collatz_steps(n):
    """Count steps to reach 1 in Collatz sequence (3n+1 problem)"""
    if n <= 0:
        return 1  # Handle edge cases
    if n == 1:
        return 0
        
    steps = 0
    original_n = n
    while n != 1 and steps < 1000:  # Prevent infinite loops (just in case)
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    
    # If we hit the limit, use the original number modulo something reasonable
    if steps >= 1000:
        steps = original_n % 50
        
    return max(1, steps)  # Always return at least 1


def char_delta_to_frequency(delta):
    """Convert character count delta to musical frequency via Collatz steps"""
    if delta == 0:
        delta = 1  # Avoid zero input
        
    collatz_depth = collatz_steps(abs(delta))
    
    # Map Collatz steps to musical frequencies
    # Base frequency A4 = 440 Hz, use chromatic scale
    base_freq = 440.0
    
    # Scale by Collatz depth: higher steps = higher pitch
    # Use 12-tone equal temperament (2^(n/12) for semitones)
    semitones = (collatz_depth - 1) % 48  # Wrap to 4 octaves
    frequency = base_freq * (2 ** (semitones / 12))
    
    return frequency, collatz_depth


def frequency_to_note_name(frequency):
    """Convert frequency to musical note name for display"""
    # A4 = 440 Hz is our reference
    A4 = 440.0
    note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    
    # Calculate semitones from A4
    semitones_from_a4 = 12 * (math.log2(frequency / A4)) if frequency > 0 else 0
    octave = 4 + int(semitones_from_a4 // 12)
    note_index = int(semitones_from_a4 % 12)
    
    note_name = note_names[note_index]
    return f"{note_name}{octave}"


class SwarmBPMMonitor:
    def __init__(self, window_minutes=5.0, update_interval=0.5, log_file=None, quiet=False):
        self.window_minutes = window_minutes
        self.update_interval = update_interval
        self.beats = deque()  # Timestamps of file modifications with frequencies
        self.file_mtimes = {}  # Track last modification times
        self.file_sizes = {}  # Track last file sizes for delta calculation
        self.total_beats = 0
        self.start_time = time.time()
        self.log_file = log_file
        self.quiet = quiet
        self.csv_writer = None
        
        # Initialize CSV logging if requested
        if self.log_file:
            self.csv_file = open(self.log_file, 'w', newline='', encoding='utf-8')
            self.csv_writer = csv.writer(self.csv_file)
            # CSV header
            self.csv_writer.writerow([
                'timestamp', 'datetime', 'beat_number', 'filepath', 'filename',
                'char_delta', 'frequency_hz', 'note', 'collatz_depth',
                'bpm', 'rhythm_stability', 'harmonic_diversity'
            ])
        
    def add_beat(self, filepath, char_delta=0):
        """Register a beat (file modification) with Collatz frequency"""
        now = time.time()
        
        # Calculate frequency from character delta via Collatz
        frequency, collatz_depth = char_delta_to_frequency(char_delta)
        note_name = frequency_to_note_name(frequency)
        
        # Store beat with metadata
        beat_data = {
            'timestamp': now,
            'filepath': filepath,
            'char_delta': char_delta,
            'frequency': frequency,
            'collatz_depth': collatz_depth,
            'note': note_name
        }
        
        self.beats.append(beat_data)
        self.total_beats += 1
        
        # Remove beats outside our time window
        cutoff = now - (self.window_minutes * 60)
        while self.beats and self.beats[0]['timestamp'] < cutoff:
            self.beats.popleft()
            
        # Log to CSV if enabled
        if self.csv_writer:
            current_stats = self.calculate_stats()
            harmonic_stats = self.calculate_harmonic_stats()
            
            self.csv_writer.writerow([
                now,  # timestamp (unix seconds)
                datetime.fromtimestamp(now).isoformat(),  # human readable datetime
                self.total_beats,  # beat number
                filepath,  # full filepath
                os.path.basename(filepath),  # filename only
                char_delta,  # character delta
                frequency,  # frequency in Hz
                note_name,  # musical note
                collatz_depth,  # Collatz steps
                current_stats['bpm'],  # current BPM
                current_stats['rhythm_stability'],  # rhythm stability %
                harmonic_stats['harmonic_diversity']  # harmonic diversity
            ])
            self.csv_file.flush()  # Ensure data is written immediately
        
        # Enhanced beat display with musical information (unless quiet)
        if not self.quiet:
            delta_str = f"Δ{char_delta:+d}" if char_delta != 0 else "Δ±0"
            print(f"♪ BEAT #{self.total_beats}: {os.path.basename(filepath)} @ {datetime.fromtimestamp(now).strftime('%H:%M:%S.%f')[:-3]}")
            print(f"  🎵 {note_name} ({frequency:.1f}Hz) via Collatz({abs(char_delta)})→{collatz_depth} steps | {delta_str} chars")
        
    def calculate_bpm(self):
        """Calculate current BPM based on recent beats"""
        if len(self.beats) < 2:
            return 0.0
            
        # BPM = (beats in window / window_minutes)
        window_beats = len(self.beats)
        bpm = window_beats / self.window_minutes
        
        return bpm
        
    def calculate_harmonic_stats(self):
        """Calculate musical/harmonic statistics from beat frequencies"""
        if not self.beats:
            return {
                'avg_frequency': 0.0,
                'frequency_range': (0.0, 0.0),
                'avg_collatz_depth': 0.0,
                'most_common_note': 'A4',
                'harmonic_diversity': 0.0,
                'unique_notes': 0
            }
            
        frequencies = [beat['frequency'] for beat in self.beats]
        collatz_depths = [beat['collatz_depth'] for beat in self.beats]
        notes = [beat['note'] for beat in self.beats]
        
        # Basic frequency stats
        avg_frequency = statistics.mean(frequencies)
        min_freq, max_freq = min(frequencies), max(frequencies)
        avg_collatz_depth = statistics.mean(collatz_depths)
        
        # Most common note
        from collections import Counter
        note_counts = Counter(notes)
        most_common_note = note_counts.most_common(1)[0][0] if note_counts else 'A4'
        
        # Harmonic diversity (number of unique notes / total notes)
        unique_notes = len(set(notes))
        harmonic_diversity = unique_notes / len(notes) if notes else 0.0
        
        return {
            'avg_frequency': avg_frequency,
            'frequency_range': (min_freq, max_freq),
            'avg_collatz_depth': avg_collatz_depth,
            'most_common_note': most_common_note,
            'harmonic_diversity': harmonic_diversity,
            'unique_notes': unique_notes
        }
        
    def calculate_stats(self):
        """Calculate rhythm statistics"""
        if len(self.beats) < 2:
            return {
                'bpm': 0.0,
                'avg_interval': 0.0,
                'rhythm_stability': 0.0,
                'total_beats': self.total_beats,
                'uptime_minutes': (time.time() - self.start_time) / 60,
                'window_beats': len(self.beats)
            }
            
        # Calculate intervals between beats
        intervals = []
        for i in range(1, len(self.beats)):
            interval = self.beats[i]['timestamp'] - self.beats[i-1]['timestamp']
            intervals.append(interval)
            
        avg_interval = statistics.mean(intervals) if intervals else 0
        rhythm_stability = 0.0
        
        if len(intervals) > 1:
            # Lower standard deviation = more stable rhythm
            interval_stdev = statistics.stdev(intervals)
            # Normalize stability to 0-100 scale
            rhythm_stability = max(0, 100 - (interval_stdev * 10))
            
        return {
            'bpm': self.calculate_bpm(),
            'avg_interval': avg_interval,
            'rhythm_stability': rhythm_stability,
            'total_beats': self.total_beats,
            'uptime_minutes': (time.time() - self.start_time) / 60,
            'window_beats': len(self.beats)
        }
        
    def check_files(self, filepaths):
        """Check all files for modifications and calculate character deltas"""
        beats_this_cycle = 0
        
        for filepath in filepaths:
            try:
                if not os.path.exists(filepath):
                    continue
                    
                current_mtime = os.path.getmtime(filepath)
                current_size = os.path.getsize(filepath)
                
                if filepath in self.file_mtimes:
                    if current_mtime > self.file_mtimes[filepath]:
                        # Calculate character delta for Collatz frequency
                        old_size = self.file_sizes.get(filepath, current_size)
                        char_delta = current_size - old_size
                        
                        self.add_beat(filepath, char_delta)
                        beats_this_cycle += 1
                        
                self.file_mtimes[filepath] = current_mtime
                self.file_sizes[filepath] = current_size
                
            except (OSError, IOError):
                # File disappeared or permission issues
                continue
                
        return beats_this_cycle
        
    def display_status(self):
        """Display current BPM and rhythm stats"""
        if self.quiet:
            return  # Skip display in quiet mode
            
        stats = self.calculate_stats()
        
        print(f"\n🎵 SWARM RHYTHM & HARMONY ANALYSIS 🎵")
        harmonic = self.calculate_harmonic_stats()
        
        print(f"BPM: {stats['bpm']:.1f}")
        print(f"Avg Interval: {stats['avg_interval']:.2f}s")
        print(f"Rhythm Stability: {stats['rhythm_stability']:.1f}%")
        print(f"Total Beats: {stats['total_beats']}")
        print(f"Window Beats: {stats['window_beats']}")
        print(f"Uptime: {stats['uptime_minutes']:.1f} min")
        
        # Musical/Harmonic stats
        print(f"\n🎼 HARMONIC ANALYSIS:")
        print(f"Avg Frequency: {harmonic['avg_frequency']:.1f}Hz ({frequency_to_note_name(harmonic['avg_frequency'])})")
        print(f"Frequency Range: {harmonic['frequency_range'][0]:.1f}Hz - {harmonic['frequency_range'][1]:.1f}Hz")
        print(f"Most Common Note: {harmonic['most_common_note']}")
        print(f"Harmonic Diversity: {harmonic['harmonic_diversity']:.2f} ({harmonic['unique_notes']} unique notes)")
        print(f"Avg Collatz Depth: {harmonic['avg_collatz_depth']:.1f} steps")
        
        # ASCII BPM visualization
        bpm_bar_length = min(50, int(stats['bpm'] * 2))
        bpm_bar = "█" * bpm_bar_length
        print(f"\nActivity: [{bpm_bar:<50}] {stats['bpm']:.1f} BPM")
        
        # Rhythm quality indicator
        if stats['rhythm_stability'] > 80:
            rhythm_emoji = "🎯"  # Very steady
        elif stats['rhythm_stability'] > 60:
            rhythm_emoji = "🎼"  # Moderately steady
        elif stats['rhythm_stability'] > 40:
            rhythm_emoji = "🎪"  # Chaotic but active
        else:
            rhythm_emoji = "💥"  # Very chaotic
            
        print(f"Rhythm Quality: {rhythm_emoji} {stats['rhythm_stability']:.0f}%")
        
        # Harmonic complexity indicator
        if harmonic['harmonic_diversity'] > 0.8:
            harmony_emoji = "🌈"  # Very diverse
        elif harmonic['harmonic_diversity'] > 0.6:
            harmony_emoji = "🎨"  # Moderately diverse
        elif harmonic['harmonic_diversity'] > 0.3:
            harmony_emoji = "🎵"  # Some variety
        else:
            harmony_emoji = "🔔"  # Repetitive
            
        print(f"Harmonic Complexity: {harmony_emoji} {harmonic['harmonic_diversity']:.0%}")
        print("-" * 70)
        
    def run(self, filepaths, recursive=False):
        """Main monitoring loop"""
        if recursive:
            # Expand to all files in directory tree
            expanded_paths = []
            for path_str in filepaths:
                path = Path(path_str)
                if path.is_dir():
                    expanded_paths.extend(path.rglob("*"))
                else:
                    expanded_paths.append(path)
            filepaths = [str(p) for p in expanded_paths if p.is_file()]
            
        if not self.quiet:
            print(f"🎧 Monitoring {len(filepaths)} files for swarm heartbeat...")
            print(f"📊 BPM window: {self.window_minutes} minutes")
            print(f"⏱️  Update interval: {self.update_interval}s")
            if self.log_file:
                print(f"📝 Logging to: {self.log_file}")
            print("🎵 Press Ctrl+C to stop\n")
        
        display_counter = 0
        
        try:
            while True:
                beats_this_cycle = self.check_files(filepaths)
                
                # Display status every 10 cycles (5 seconds at 0.5s interval)
                display_counter += 1
                if display_counter >= 10 or beats_this_cycle > 0:
                    self.display_status()
                    display_counter = 0
                    
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            if not self.quiet:
                print("\n🎵 Monitoring stopped.")
                print(f"Final stats: {self.total_beats} beats in {(time.time() - self.start_time)/60:.1f} minutes")
                final_stats = self.calculate_stats()
                print(f"Average BPM: {final_stats['bpm']:.2f}")
        finally:
            # Close CSV file if open
            if self.csv_writer:
                self.csv_file.close()


def main():
    parser = argparse.ArgumentParser(description="Monitor swarm activity BPM")
    parser.add_argument("files", nargs="*", default=["*.py", "*.json", "*.txt"],
                       help="Files to monitor (supports wildcards)")
    parser.add_argument("--recursive", "-r", action="store_true",
                       help="Recursively monitor directories")
    parser.add_argument("--window", "-w", type=float, default=5.0,
                       help="BPM calculation window in minutes (default: 5.0)")
    parser.add_argument("--interval", "-i", type=float, default=0.5,
                       help="File check interval in seconds (default: 0.5)")
    parser.add_argument("--log", "-l", type=str, default=None,
                       help="Log beats to CSV file for analysis")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Quiet mode - suppress display output (useful with --log)")
    
    args = parser.parse_args()
    
    # Expand wildcards
    import glob
    filepaths = []
    for pattern in args.files:
        matches = glob.glob(pattern)
        if matches:
            filepaths.extend(matches)
        else:
            # If no matches, add as literal path (might be a specific file)
            filepaths.append(pattern)
    
    if not filepaths:
        print("❌ No files to monitor!")
        return 1
        
    monitor = SwarmBPMMonitor(window_minutes=args.window, 
                             update_interval=args.interval,
                             log_file=args.log,
                             quiet=args.quiet)
    monitor.run(filepaths, recursive=args.recursive)
    
    return 0


if __name__ == "__main__":
    exit(main())