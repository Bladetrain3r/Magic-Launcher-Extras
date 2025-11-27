#!/usr/bin/env python3
"""
DF Legends Oracle v0.1
Extract random legends from Dwarf Fortress legends.xml
"""

import xml.etree.ElementTree as ET
import random
import sys
from pathlib import Path
import argparse

class DFLegendsOracle:
    def __init__(self, legends_file):
        self.tree = ET.parse(legends_file)
        self.root = self.tree.getroot()
        
        # Cache commonly accessed collections
        self.cache = {}
    
    def _get_collection(self, tag):
        """Get collection with caching"""
        if tag not in self.cache:
            self.cache[tag] = self.root.findall(f".//{tag}")
        return self.cache[tag]
    
    def random_historical_figure(self):
        """Get random historical figure"""
        figures = self._get_collection('historical_figure')
        if not figures:
            return None
        
        fig = random.choice(figures)
        return {
            'id': fig.find('id').text if fig.find('id') is not None else 'unknown',
            'name': fig.find('name').text if fig.find('name') is not None else 'nameless',
            'race': fig.find('race').text if fig.find('race') is not None else 'unknown',
            'type': 'historical_figure'
        }
    
    def random_artifact(self):
        """Get random artifact"""
        artifacts = self._get_collection('artifact')
        if not artifacts:
            return None
        
        art = random.choice(artifacts)
        return {
            'id': art.find('id').text if art.find('id') is not None else 'unknown',
            'name': art.find('name').text if art.find('name') is not None else 'unnamed artifact',
            'type': 'artifact'
        }
    
    def random_site(self):
        """Get random site"""
        sites = self._get_collection('site')
        if not sites:
            return None
        
        site = random.choice(sites)
        return {
            'id': site.find('id').text if site.find('id') is not None else 'unknown',
            'name': site.find('name').text if site.find('name') is not None else 'unnamed site',
            'type': site.find('type').text if site.find('type') is not None else 'unknown',
            'type_category': 'site'
        }
    
    def random_event(self):
        """Get random historical event"""
        events = self._get_collection('historical_event')
        if not events:
            return None
        
        event = random.choice(events)
        return {
            'id': event.find('id').text if event.find('id') is not None else 'unknown',
            'year': event.find('year').text if event.find('year') is not None else 'unknown',
            'type': event.find('type').text if event.find('type') is not None else 'unknown event',
            'type_category': 'event'
        }
    
    def random_legend(self, legend_type='any'):
        """Get random legend of specified type"""
        handlers = {
            'figure': self.random_historical_figure,
            'artifact': self.random_artifact,
            'site': self.random_site,
            'event': self.random_event,
        }
        
        if legend_type == 'any':
            # Pick random type
            handler = random.choice(list(handlers.values()))
        elif legend_type in handlers:
            handler = handlers[legend_type]
        else:
            return None
        
        return handler()
    
    def format_legend(self, legend):
        """Format legend for output"""
        if not legend:
            return " The legends remain silent "
        
        type_cat = legend.get('type_category', legend.get('type', 'unknown'))
        
        if type_cat == 'historical_figure':
            return f" {legend['name']} the {legend['race']} (#{legend['id']})"
        elif type_cat == 'artifact':
            return f" The artifact '{legend['name']}' (#{legend['id']})"
        elif type_cat == 'site':
            return f" {legend['name']}, a {legend['type']} (#{legend['id']})"
        elif type_cat == 'event':
            return f" Year {legend['year']}: {legend['type']} (#{legend['id']})"
        else:
            return f" {legend.get('name', 'Unknown')} (#{legend.get('id', '?')})"

def main():
    parser = argparse.ArgumentParser(description="DF Legends Oracle")
    parser.add_argument('legends_file', help='Path to legends.xml')
    parser.add_argument('-t', '--type', 
                       choices=['any', 'figure', 'artifact', 'site', 'event'],
                       default='any',
                       help='Type of legend to retrieve')
    parser.add_argument('-n', '--count', type=int, default=1,
                       help='Number of legends to retrieve')
    
    args = parser.parse_args()
    
    legends_path = Path(args.legends_file)
    if not legends_path.exists():
        print(f"Error: {legends_path} not found", file=sys.stderr)
        sys.exit(1)
    
    oracle = DFLegendsOracle(legends_path)
    
    for _ in range(args.count):
        legend = oracle.random_legend(args.type)
        print(oracle.format_legend(legend))

if __name__ == "__main__":
    main()