from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import config

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=False)
    deadline = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resumes = relationship("Resume", back_populates="role")
    
    def __repr__(self):
        return f"<Role {self.title}>"


class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    file_path = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    content_text = Column(Text, nullable=True)
    similarity_score = Column(Float, nullable=True)
    is_shortlisted = Column(Boolean, default=False)
    submitted_at = Column(DateTime, default=datetime.now)  # Add this column
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    role = relationship("Role", back_populates="resumes")
    
    def __repr__(self):
        return f"<Resume {self.filename} for {self.role.title}>"


# Create the database and tables
def init_db():
    engine = create_engine(config.DATABASE_URL)
    Base.metadata.create_all(engine)