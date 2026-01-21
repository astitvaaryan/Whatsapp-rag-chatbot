import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine
from app.db.models import Base, FAQ, Contact

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if data exists
    if db.query(FAQ).first():
        print("Data already exists. Skipping seed.")
        db.close()
        return

    # Add FAQs
    faqs = [
        FAQ(question="What are the office timings?", answer="Monday to Friday, 9 AM to 5 PM."),
        FAQ(question="Is there a registration fee?", answer="Yes, the registration fee is $50."),
        FAQ(question="How do I apply?", answer="You can apply online through our portal at example.com/apply."),
    ]
    
    contacts = [
        Contact(name="Admin", role="Administrator", email="admin@example.com", phone_number="+1234567890"),
        Contact(name="Support", role="Help Desk", email="support@example.com", phone_number="+0987654321"),
    ]
    
    for f in faqs:
        db.add(f)
        
    for c in contacts:
        db.add(c)
        
    db.commit()
    print("Database seeded successfully.")
    db.close()

if __name__ == "__main__":
    seed()
