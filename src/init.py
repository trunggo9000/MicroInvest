#!/usr/bin/env python3
"""
MicroInvest - Initialization Script

This script initializes the database and performs first-time setup.
"""
import os
import sys
from pathlib import Path

def main():
    print("🚀 MicroInvest - Initialization")
    print("=" * 40)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("❌ Error: .env file not found.")
        print("Please create a .env file based on .env.example")
        sys.exit(1)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize database
    print("\n🔧 Initializing database...")
    try:
        from backend.database.models import init_db, engine
        init_db()
        print(f"✅ Database initialized at: {engine.url.database}")
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        sys.exit(1)
    
    print("\n✨ Setup complete! You can now start the application with:")
    print("   streamlit run frontend/app.py")

if __name__ == "__main__":
    main()
