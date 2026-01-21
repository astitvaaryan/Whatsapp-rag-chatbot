from sqlalchemy.orm import Session
from app.db.models import FAQ, Contact

def get_all_faqs(db: Session):
    return db.query(FAQ).all()

def search_faqs(db: Session, query: str):
    # Basic keyword search using LIKE
    return db.query(FAQ).filter(FAQ.question.ilike(f"%{query}%")).all()

def get_contact_by_role(db: Session, role: str):
    return db.query(Contact).filter(Contact.role.ilike(f"%{role}%")).first()

def get_all_contacts(db: Session):
    return db.query(Contact).all()
