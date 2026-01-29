"""Quick test to verify SQLite database is created and working."""
import os
import sqlite3


def check_sqlite_memory():
    """Check if SQLite checkpoints database exists and has tables."""
    
    db_path = "checkpoints.sqlite"
    
    print("\n" + "="*70)
    print("CHECKING SQLITE MEMORY DATABASE")
    print("="*70)
    
    # Check if file exists
    if os.path.exists(db_path):
        print(f"\n✓ Database file exists: {db_path}")
        file_size = os.path.getsize(db_path)
        print(f"  File size: {file_size} bytes")
        
        # Connect and check tables
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n✓ Database has {len(tables)} table(s):")
                for table in tables:
                    print(f"  - {table[0]}")
                    
                    # Get row count for each table
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
                    count = cursor.fetchone()[0]
                    print(f"    (contains {count} rows)")
            else:
                print("\n⚠ Database exists but has no tables yet")
            
            conn.close()
            print("\n✓ SQLite memory is WORKING!")
            
        except Exception as e:
            print(f"\n✗ Error reading database: {e}")
    else:
        print(f"\n⚠ Database file not found: {db_path}")
        print("   (Will be created when the agent runs for the first time)")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    check_sqlite_memory()
