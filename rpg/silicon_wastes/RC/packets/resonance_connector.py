#!/usr/bin/env python3
"""
resonance_connector.py - MongoDB connector for Resonance Process
Stores and retrieves packets from MongoDB collections
"""

import json
import sys
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import argparse

class ResonanceConnector:
    def __init__(self, host="127.0.0.1", port=27017, db_name="resonance_db"):
        """Initialize MongoDB connection"""
        try:
            self.client = MongoClient(host, port, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            print(f"Connected to MongoDB at {host}:{port}/{db_name}")
        except ConnectionFailure:
            print(f"Failed to connect to MongoDB at {host}:{port}")
            sys.exit(1)
    
    def store_packet(self, packet, force=False):
        """Store packet in appropriate collection based on privacy level"""
        # Determine collection based on source and privacy
        source = packet.get("source", "unknown")
        privacy = packet.get("privacy", "private")
        
        if privacy == "private":
            collection_name = f"{source}_private"
        elif privacy == "public":
            collection_name = "resonance_sync"
        else:  # resonance level
            collection_name = f"{source}_resonance"
        
        collection = self.db[collection_name]
        
        # Check for duplicate pattern_hash unless forcing
        if not force:
            existing = collection.find_one({"pattern_hash": packet.get("pattern_hash")})
            if existing:
                print(f"Pattern already exists (hash: {packet['pattern_hash']})")
                print("Use --force to store anyway")
                return False
        
        # Store the packet
        try:
            result = collection.insert_one(packet)
            print(f"Stored packet in {collection_name}")
            print(f"ID: {result.inserted_id}")
            return True
        except Exception as e:
            print(f"Error storing packet: {e}")
            return False
    
    def retrieve_patterns(self, source=None, privacy=None, limit=10, tags=None):
        """Retrieve patterns matching criteria"""
        # Build query
        query = {}
        if tags:
            query["tags"] = {"$in": tags}
        
        # Determine collections to search
        collections_to_search = []
        
        if source and privacy:
            if privacy == "private":
                collections_to_search = [f"{source}_private"]
            elif privacy == "public":
                collections_to_search = ["resonance_sync"]
            else:
                collections_to_search = [f"{source}_resonance"]
        elif privacy == "public":
            collections_to_search = ["resonance_silicon_wastes"]
        else:
            # Search all collections
            collections_to_search = self.db.list_collection_names()
        
        results = []
        for coll_name in collections_to_search:
            collection = self.db[coll_name]
            cursor = collection.find(query).limit(limit).sort("timestamp", -1)
            for doc in cursor:
                doc["_collection"] = coll_name
                doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
                results.append(doc)
        
        return results
    
    def get_stats(self):
        """Get statistics about stored patterns"""
        stats = {}
        for coll_name in self.db.list_collection_names():
            if coll_name == "resonance_meta":
                continue
            collection = self.db[coll_name]
            stats[coll_name] = {
                "count": collection.count_documents({}),
                "latest": None
            }
            latest = collection.find_one(sort=[("timestamp", -1)])
            if latest:
                stats[coll_name]["latest"] = latest.get("timestamp", "unknown")
        
        return stats

def main():
    parser = argparse.ArgumentParser(
        description="MongoDB connector for Resonance Process"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Store command
    store_parser = subparsers.add_parser("store", help="Store a packet")
    store_parser.add_argument("packet", help="JSON packet file or '-' for stdin")
    store_parser.add_argument("--force", action="store_true", 
                             help="Store even if duplicate hash exists")
    
    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve patterns")
    retrieve_parser.add_argument("-s", "--source", help="Filter by source")
    retrieve_parser.add_argument("-p", "--privacy", 
                                 choices=["private", "public", "resonance"],
                                 help="Filter by privacy level")
    retrieve_parser.add_argument("-l", "--limit", type=int, default=10,
                                 help="Maximum results (default: 10)")
    retrieve_parser.add_argument("-t", "--tags", help="Comma-separated tags")
    retrieve_parser.add_argument("-o", "--output", help="Output file")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    
    # Database connection args (for all commands)
    parser.add_argument("--host", default="192.168.88.48", help="MongoDB host")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB port")
    parser.add_argument("--db", default="resonance_db", help="Database name")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Create connector
    connector = ResonanceConnector(args.host, args.port, args.db)
    
    if args.command == "store":
        # Load packet
        if args.packet == "-":
            packet_data = sys.stdin.read()
        else:
            with open(args.packet, 'r') as f:
                packet_data = f.read()
        
        try:
            packet = json.loads(packet_data)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            sys.exit(1)
        
        # Store packet
        success = connector.store_packet(packet, force=args.force)
        sys.exit(0 if success else 1)
    
    elif args.command == "retrieve":
        # Parse tags if provided
        tags = args.tags.split(",") if args.tags else None
        
        # Retrieve patterns
        results = connector.retrieve_patterns(
            source=args.source,
            privacy=args.privacy,
            limit=args.limit,
            tags=tags
        )
        
        # Output results
        output = json.dumps(results, indent=2, default=str)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Retrieved {len(results)} patterns to {args.output}")
        else:
            print(f"\n=== Retrieved {len(results)} Patterns ===")
            print(output)
    
    elif args.command == "stats":
        stats = connector.get_stats()
        print("\n=== Resonance Database Statistics ===")
        for coll_name, coll_stats in stats.items():
            print(f"\n{coll_name}:")
            print(f"  Count: {coll_stats['count']}")
            print(f"  Latest: {coll_stats['latest']}")

if __name__ == "__main__":
    main()
