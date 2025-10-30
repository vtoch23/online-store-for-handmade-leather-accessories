"""
Migration script to add profile columns to users table
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def migrate():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Add phone column
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR(20)"))
            print("✓ Added phone column")
        except Exception as e:
            if "already exists" in str(e):
                print("✓ Phone column already exists")
            else:
                print(f"✗ Error adding phone column: {e}")
        
        # Add birthday column
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN birthday VARCHAR(10)"))
            print("✓ Added birthday column")
        except Exception as e:
            if "already exists" in str(e):
                print("✓ Birthday column already exists")
            else:
                print(f"✗ Error adding birthday column: {e}")
        
        # Add address column
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN address VARCHAR(500)"))
            print("✓ Added address column")
        except Exception as e:
            if "already exists" in str(e):
                print("✓ Address column already exists")
            else:
                print(f"✗ Error adding address column: {e}")
        
        conn.commit()
    
    print("\n✓ Migration completed successfully!")

if __name__ == "__main__":
    migrate()
