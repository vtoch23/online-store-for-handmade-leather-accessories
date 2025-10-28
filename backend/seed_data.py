"""Script to seed the database with sample data."""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.category import Category
from app.models.product import Product
from app.models.user import User

def seed_database():
    """Seed the database with initial data."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Category).first():
            print("Database already contains data. Skipping seed.")
            return

        # Create categories
        categories = [
            Category(
                name="Wallets",
                description="Handcrafted leather wallets",
                slug="wallets"
            ),
            Category(
                name="Bags",
                description="Premium leather bags and pouches",
                slug="bags"
            ),
            Category(
                name="Belts",
                description="Durable leather belts",
                slug="belts"
            ),
            Category(
                name="Accessories",
                description="Various leather accessories",
                slug="accessories"
            )
        ]

        for category in categories:
            db.add(category)

        db.commit()

        # Refresh to get IDs
        for category in categories:
            db.refresh(category)

        # Create sample products
        products = [
            # Wallets
            Product(
                name="Classic Bifold Wallet",
                description="A timeless bifold wallet crafted from premium full-grain leather. Features multiple card slots and a bill compartment.",
                price=79.99,
                stock_quantity=15,
                category_id=categories[0].id,
                sku="WALLET-001",
                image_url="https://via.placeholder.com/600x600?text=Bifold+Wallet"
            ),
            Product(
                name="Minimalist Card Holder",
                description="Sleek and compact card holder perfect for carrying essentials. Holds up to 8 cards.",
                price=49.99,
                stock_quantity=25,
                category_id=categories[0].id,
                sku="WALLET-002",
                image_url="https://via.placeholder.com/600x600?text=Card+Holder"
            ),
            # Bags
            Product(
                name="Messenger Bag",
                description="Spacious messenger bag with adjustable strap. Perfect for daily commute or travel.",
                price=189.99,
                stock_quantity=8,
                category_id=categories[1].id,
                sku="BAG-001",
                image_url="https://via.placeholder.com/600x600?text=Messenger+Bag"
            ),
            Product(
                name="Laptop Sleeve",
                description="Protective laptop sleeve for 15-inch devices. Soft interior lining.",
                price=69.99,
                stock_quantity=20,
                category_id=categories[1].id,
                sku="BAG-002",
                image_url="https://via.placeholder.com/600x600?text=Laptop+Sleeve"
            ),
            # Belts
            Product(
                name="Classic Dress Belt",
                description="Elegant dress belt with polished buckle. Available in multiple sizes.",
                price=59.99,
                stock_quantity=30,
                category_id=categories[2].id,
                sku="BELT-001",
                image_url="https://via.placeholder.com/600x600?text=Dress+Belt"
            ),
            Product(
                name="Casual Leather Belt",
                description="Versatile casual belt suitable for everyday wear.",
                price=49.99,
                stock_quantity=35,
                category_id=categories[2].id,
                sku="BELT-002",
                image_url="https://via.placeholder.com/600x600?text=Casual+Belt"
            ),
            # Accessories
            Product(
                name="Key Holder",
                description="Compact key holder that keeps your keys organized and quiet.",
                price=29.99,
                stock_quantity=40,
                category_id=categories[3].id,
                sku="ACC-001",
                image_url="https://via.placeholder.com/600x600?text=Key+Holder"
            ),
            Product(
                name="Leather Journal Cover",
                description="Beautiful leather cover for A5 journals. Refillable and durable.",
                price=89.99,
                stock_quantity=12,
                category_id=categories[3].id,
                sku="ACC-002",
                image_url="https://via.placeholder.com/600x600?text=Journal+Cover"
            )
        ]

        for product in products:
            db.add(product)

        # Create a demo user
        demo_user = User(
            email="demo@example.com",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqGkNe6FVK",  # password: demo123
            full_name="Demo User",
            is_active=True,
            is_admin=False
        )
        db.add(demo_user)

        db.commit()

        print("Database seeded successfully!")
        print(f"Created {len(categories)} categories")
        print(f"Created {len(products)} products")
        print("Created 1 demo user (email: demo@example.com, password: demo123)")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
