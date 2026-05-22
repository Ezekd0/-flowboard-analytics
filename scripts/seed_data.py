from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.task import Task
from app.core.security import hash_password

def seed_data():
    """Seed the database with sample data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_user = db.query(User).filter(User.username == "demo").first()
        if existing_user:
            print("Sample data already exists in the database!")
            return
        
        # Create a sample user
        user = User(
            username="demo",
            email="demo@example.com",
            full_name="Demo User",
            hashed_password=hash_password("demo123"),
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create sample tasks
        tasks = [
            Task(
                title="Complete project documentation",
                description="Write comprehensive documentation for the TaskFlow project",
                status="in_progress",
                priority="high",
                owner_id=user.id
            ),
            Task(
                title="Fix login bug",
                description="Users cannot login on mobile devices",
                status="pending",
                priority="high",
                owner_id=user.id
            ),
            Task(
                title="Update dashboard UI",
                description="Improve dashboard design and user experience",
                status="pending",
                priority="medium",
                owner_id=user.id
            ),
            Task(
                title="Write unit tests",
                description="Add unit tests for API endpoints",
                status="completed",
                priority="medium",
                owner_id=user.id
            ),
            Task(
                title="Review pull requests",
                description="Review and merge pending pull requests",
                status="pending",
                priority="low",
                owner_id=user.id
            ),
        ]
        
        db.add_all(tasks)
        db.commit()
        
        print("✓ Database seeded with sample data!")
        print(f"✓ Created user: {user.username} ({user.email})")
        print(f"✓ Created {len(tasks)} sample tasks")
        print(f"\nYou can now login with:")
        print(f"  Username: {user.username}")
        print(f"  Password: demo123")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
