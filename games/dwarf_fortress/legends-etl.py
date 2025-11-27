#!/usr/bin/env python3
"""
DF Legends ETL - Extract legends.xml to SQLite
One-time conversion for faster random access
"""

import xml.etree.ElementTree as ET
import sqlite3
from pathlib import Path

def etl_legends(xml_file, db_file='legends.db'):
    """Convert legends.xml to SQLite"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS historical_figures
                 (id INTEGER PRIMARY KEY, name TEXT, race TEXT, birth_year INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS artifacts
                 (id INTEGER PRIMARY KEY, name TEXT, item_type TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS sites
                 (id INTEGER PRIMARY KEY, name TEXT, type TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY, year INTEGER, type TEXT)''')
    
    # Extract figures
    for fig in root.findall('.//historical_figure'):
        id_elem = fig.find('id')
        name_elem = fig.find('name')
        race_elem = fig.find('race')
        birth_elem = fig.find('birth_year')
        
        if id_elem is not None:
            c.execute('INSERT OR REPLACE INTO historical_figures VALUES (?,?,?,?)',
                     (int(id_elem.text),
                      name_elem.text if name_elem is not None else 'nameless',
                      race_elem.text if race_elem is not None else 'unknown',
                      int(birth_elem.text) if birth_elem is not None else -1))
    
    # Similar for artifacts, sites, events...
    
    conn.commit()
    conn.close()
    print(f"ETL complete: {db_file}")

# Then oracle queries SQLite instead
class DFLegendsSQLOracle:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
    
    def random_historical_figure(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM historical_figures ORDER BY RANDOM() LIMIT 1')
        return dict(c.fetchone()) if c.fetchone() else None