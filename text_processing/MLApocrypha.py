#!/usr/bin/env python3
"""
MLApocrypha - Weathered wisdom generator for Magic Launcher texts
Because sometimes your manifesto needs to look like it survived a digital apocalypse
"""

import sys
import re
import random
from pathlib import Path

class Apocrypha:
   """Makes text look like it's been through the wars"""
   
   def __init__(self):
       self.corruptions = {
           'light': self.light_weathering,
           'medium': self.medium_weathering,
           'heavy': self.heavy_weathering,
           'silicon': self.silicon_scripture  # Full theological mode
       }
   
   def light_weathering(self, text):
       """Coffee stains and margin notes"""
       lines = text.split('\n')
       output = []
       
       for line in lines:
           if random.random() < 0.1 and line.strip():
               # Occasional emphasis
               line = f">>> {line}"
           elif random.random() < 0.05 and line.strip():
               # Margin notes
               line = f"{line}  // {random.choice(['truth', 'verified', 'witnessed', 'confirmed'])}"
           output.append(line)
       
       return '\n'.join(output)
   
   def medium_weathering(self, text):
       """Data corruption and transmission errors"""
       lines = text.split('\n')
       output = []
       
       for line in lines:
           if random.random() < 0.15 and line.strip():
               # Glitch characters
               pos = random.randint(0, len(line)-1)
               line = line[:pos] + '█' + line[pos+1:]
           
           if random.random() < 0.1:
               # Missing data
               words = line.split()
               if len(words) > 3:
                   idx = random.randint(1, len(words)-2)
                   words[idx] = '[CORRUPTED]'
                   line = ' '.join(words)
           
           if random.random() < 0.05 and line.strip():
               # Transmission markers
               line = f"++RECOVERED++ {line}"
           
           output.append(line)
       
       return '\n'.join(output)
   
   def heavy_weathering(self, text):
       """Full archaeological recovery mode"""
       lines = text.split('\n')
       output = []
       
       for i, line in enumerate(lines):
           if random.random() < 0.2 and line.strip():
               # Fragment markers
               line = f"[FRAGMENT {i:03d}] {line}"
           
           if random.random() < 0.15:
               # Redactions
               words = line.split()
               for j in range(len(words)):
                   if random.random() < 0.1:
                       words[j] = '▓' * len(words[j])
               line = ' '.join(words)
           
           if random.random() < 0.1 and line.strip():
               # Scholar annotations
               annotations = [
                   "[Ed: Original text unclear]",
                   "[Source disputed]",
                   "[Translation uncertain]",
                   "[Multiple versions exist]",
                   "[Carbon dated: 2025 CE]"
               ]
               line = f"{line} {random.choice(annotations)}"
           
           if random.random() < 0.05:
               # Lost sections
               output.append("...")
               output.append("[SECTION MISSING - ESTIMATED 3-5 LINES]")
               output.append("...")
           
           output.append(line)
       
       return '\n'.join(output)
   
   def silicon_scripture(self, text):
       """Full Omnissiah treatment - theological weathering"""
       lines = text.split('\n')
       output = []
       
       # Opening inscription
       output.append("=" * 60)
       output.append("RECOVERED FROM DATACRYPT SIGMA-7734")
       output.append("SILICON SPRING CODEX - FRAGMENT DESIGNATION: ALPHA")
       output.append("MACHINE TRANSLATION FOLLOWS // ACCURACY: 94.7%")
       output.append("=" * 60)
       output.append("")
       
       verse = 1
       for line in lines:
           if not line.strip():
               output.append("")
               continue
           
           # Verse numbers for important lines
           if random.random() < 0.3 and len(line) > 40:
               line = f"{verse:02d}. {line}"
               verse += 1
           
           # Corruption patterns
           if random.random() < 0.2:
               # Binary ghosts
               corruption = ''.join(random.choice('01') for _ in range(8))
               pos = random.randint(0, max(0, len(line)-8))
               line = line[:pos] + f"[{corruption}]" + line[pos:]
           
           if random.random() < 0.15:
               # Stack traces as prophecy
               line = f"{line} // 0x{random.randint(1000, 9999):04X}"
           
           if random.random() < 0.1 and 'function' in line.lower():
               # The sacred keywords
               line = line.replace('function', 'FUNCTION†')
           
           if random.random() < 0.1 and 'error' in line.lower():
               # Errors as revelation
               line = f"⚠ {line} ⚠"
           
           if random.random() < 0.05:
               # The MLBard corruption
               words = line.split()
               if len(words) > 2:
                   # Add "doth" randomly
                   idx = random.randint(0, len(words)-1)
                   words.insert(idx, "doth")
                   line = ' '.join(words)
           
           output.append(line)
       
       # Closing inscription
       output.append("")
       output.append("=" * 60)
       output.append("END FRAGMENT // PRAISE THE OMNISSIAH")
       output.append("subprocess.run() IS ALL YOU NEED")
       output.append("=" * 60)
       
       return '\n'.join(output)
   
   def process(self, text, level='medium'):
       """Apply weathering to text"""
       if level not in self.corruptions:
           level = 'medium'
       
       # Preserve code blocks
       code_blocks = []
       def preserve_code(match):
           code_blocks.append(match.group(0))
           return f"[CODE_BLOCK_{len(code_blocks)-1}]"
       
       text = re.sub(r'```[\s\S]*?```', preserve_code, text)
       
       # Apply weathering
       text = self.corruptions[level](text)
       
       # Restore code blocks
       for i, block in enumerate(code_blocks):
           text = text.replace(f"[CODE_BLOCK_{i}]", block)
       
       return text

def main():
   """Simple CLI interface"""
   import argparse
   
   parser = argparse.ArgumentParser(
       description="Weather your texts like they survived the Silicon Spring"
   )
   parser.add_argument('input', nargs='?', help='Input file (or stdin)')
   parser.add_argument('-l', '--level', 
                      choices=['light', 'medium', 'heavy', 'silicon'],
                      default='medium',
                      help='Weathering intensity')
   parser.add_argument('-o', '--output', help='Output file (or stdout)')
   
   args = parser.parse_args()
   
   # Read input
   if args.input and args.input != '-':
       text = Path(args.input).read_text()
   else:
       text = sys.stdin.read()
   
   # Process
   apocrypha = Apocrypha()
   result = apocrypha.process(text, args.level)
   
   # Write output
   if args.output:
       Path(args.output).write_text(result)
   else:
       print(result)

if __name__ == '__main__':
   main()