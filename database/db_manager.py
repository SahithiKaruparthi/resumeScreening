from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import bcrypt
import config
from database.models import Base, User, Role, Resume
from rag.vector_store import VectorStore
from database.models import Resume
from datetime import datetime
from sqlalchemy.orm import joinedload

# Create database engine
engine = create_engine(config.DATABASE_URL)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(SessionFactory)

@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# User Management Functions
def create_user(username, email, password, is_admin=False):
    """Create a new user with hashed password"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    with get_db_session() as session:
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password.decode('utf-8'),
            is_admin=is_admin
        )
        session.add(new_user)
        session.commit()  # This must be called after add to get the ID

        return new_user.id

def authenticate_user(username, password):
    """Authenticate a user by username and password"""
    with get_db_session() as session:
        user = session.query(User).filter(User.username == username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return user
        return None

def get_user(user_id):
    """Get user by ID"""
    with get_db_session() as session:
        return session.query(User).filter(User.id == user_id).first()

# Role Management Functions
def create_role(title, description, requirements, deadline):
    """Create a new job role"""
    with get_db_session() as session:
        new_role = Role(
            title=title,
            description=description,
            requirements=requirements,
            deadline=deadline
        )
        session.add(new_role)
        session.flush()  # Flush to get the ID
        return new_role.id

def get_all_roles():
    """Get all job roles"""
    with get_db_session() as session:
        return session.query(Role).all()

def get_active_roles():
    """Get active job roles"""
    with get_db_session() as session:
        return session.query(Role).filter(Role.is_active == True).all()

def get_role(role_id):
    """Get role by ID"""
    with get_db_session() as session:
        return session.query(Role).filter(Role.id == role_id).first()

def update_role(role_id, title=None, description=None, requirements=None, deadline=None, is_active=None):
    """Update a job role"""
    with get_db_session() as session:
        role = session.query(Role).filter(Role.id == role_id).first()
        if not role:
            return False
            
        if title:
            role.title = title
        if description:
            role.description = description
        if requirements:
            role.requirements = requirements
        if deadline:
            role.deadline = deadline
        if is_active is not None:
            role.is_active = is_active
            
        return True

# Resume Management Functions
def save_resume(user_id, role_id, file_path, filename, content_text=None, submitted_at=None):
    """Save a resume submission"""

    if submitted_at is None:
        submitted_at = datetime.now()

    with get_db_session() as session:
        new_resume = Resume(
            user_id=user_id,
            role_id=role_id,
            file_path=file_path,
            filename=filename,
            content_text=content_text,
            submitted_at=submitted_at
        )
        session.add(new_resume)
        session.flush()  # Flush to get the ID
        return new_resume.id

def update_resume_score(resume_id, similarity_score):
    """Update a resume's similarity score"""
    with get_db_session() as session:
        resume = session.query(Resume).filter(Resume.id == resume_id).first()
        if resume:
            resume.similarity_score = similarity_score
            return True
        return False

def get_resumes_by_role(role_id):
    """Get all resumes for a specific role"""
    with get_db_session() as session:
        resumes = session.query(Resume).options(joinedload(Resume.user)).filter(Resume.role_id == role_id).all()
        return resumes

    
def get_resumes_for_role(role_id):
    """
    Get all resumes for a role with their similarity scores.
    
    Args:
        role_id (int): ID of the role
        
    Returns:
        List[Resume]: List of resumes sorted by similarity score (descending)
    """
    
    # Get a database session
    with get_db_session() as session:
        # Fetch resumes from the database using session.query instead of Resume.query
        resumes = session.query(Resume).filter_by(role_id=role_id).all()
        
        # Calculate similarity scores
        vector_store = VectorStore()
        for resume in resumes:
            # Only calculate if not already calculated
            if resume.similarity_score is None:
                resume.similarity_score = vector_store.calculate_similarity_score(resume.content_text, role_id)
        
        # Sort resumes by similarity score (descending)
        return sorted(resumes, key=lambda x: x.similarity_score if x.similarity_score is not None else 0, reverse=True)

def get_top_resumes_by_role(role_id, limit=10):
    """Get top N resumes for a specific role based on similarity score"""
    with get_db_session() as session:
        return session.query(Resume)\
            .filter(Resume.role_id == role_id)\
            .order_by(desc(Resume.similarity_score))\
            .limit(limit)\
            .all()

def mark_as_shortlisted(resume_id):
    """Mark a resume as shortlisted"""
    with get_db_session() as session:
        resume = session.query(Resume).filter(Resume.id == resume_id).first()
        if resume:
            resume.is_shortlisted = True
            return True
        return False

def get_resumes_by_user(user_id):
    """Get all resumes submitted by a user"""
    with get_db_session() as session:
        return session.query(Resume).filter(Resume.user_id == user_id).all()

def init_default_admin():
    """Create a default admin user if none exists"""
    with get_db_session() as session:
        admin = session.query(User).filter(User.is_admin == True).first()
        if not admin:
            try:
                create_user(
                    username="admin",
                    email="admin@example.com",
                    password="adminpassword",
                    is_admin=True
                )
                print("Default admin user created")
            except SQLAlchemyError as e:
                print(f"Error creating default admin: {e}")