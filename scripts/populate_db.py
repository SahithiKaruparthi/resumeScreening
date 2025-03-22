import os
import sys
from datetime import datetime, timedelta
import random
import sys

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from database.db_manager import get_all_roles

# Add parent directory to path to find modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import init_db
from database.models import User, Role, Resume  # Import your models
from database.db_manager import get_db_session

from database.db_manager import (
    create_role, 
    create_user, 
    init_default_admin,
    save_resume,
    update_resume_score
)
from rag.vector_store import VectorStore
from resume_analyzer.ranking import ResumeRanker  # Import ResumeRanker

def clear_database():
    """Clear all data from the database tables"""
    with get_db_session() as session:
        session.query(Resume).delete()
        session.query(Role).delete()
        session.query(User).delete()
        session.commit()
    print("Database cleared successfully.")



def populate_users():
    """Create test users"""
    print("Creating test users...")
    
    # Create standard users
    users = [
        {"username": "john_smith", "email": "john@example.com", "password": "password123"},
        {"username": "alice_jones", "email": "alice@example.com", "password": "password123"},
        {"username": "robert_williams", "email": "robert@example.com", "password": "password123"},
        {"username": "sarah_davis", "email": "sarah@example.com", "password": "password123"},
        {"username": "michael_brown", "email": "michael@example.com", "password": "password123"}
    ]
    
    user_ids = []
    for user in users:
        user_id = create_user(
            username=user["username"], 
            email=user["email"], 
            password=user["password"], 
            is_admin=False
        )
        user_ids.append(user_id)
        print(f"Created user: {user['username']} (ID: {user_id})")
    
    return user_ids

def populate_roles():
    """Create test job roles with different deadlines"""
    print("Creating test job roles...")
    
    now = datetime.now()
    
    roles = [
        {
            "title": "Senior Software Engineer (Past Deadline)",
            "description": "We are looking for an experienced software engineer to join our team.",
            "requirements": """
            Requirements:
            - 5+ years of professional software development experience
            - Expert knowledge of Python and JavaScript
            - Experience with React, Django, and other modern frameworks
            - Strong problem-solving skills and attention to detail
            - Excellent communication skills
            - CS degree or equivalent experience
            - Experience with cloud services (AWS, Azure, GCP)
            - Knowledge of CI/CD practices and tools
            """,
            "deadline": now - timedelta(days=14)  # Deadline passed 14 days ago
        },
        {
            "title": "Junior Data Scientist (Past Deadline)",
            "description": "Join our data science team to work on cutting-edge analytics projects.",
            "requirements": """
            Requirements:
            - 1-2 years of experience in data science or related field
            - Strong programming skills in Python
            - Experience with data analysis libraries (Pandas, NumPy)
            - Knowledge of machine learning frameworks (scikit-learn, TensorFlow)
            - Understanding of statistical analysis
            - Bachelor's degree in Computer Science, Mathematics, or related field
            - Experience with data visualization tools
            """,
            "deadline": now - timedelta(days=7)  # Deadline passed 7 days ago
        },
        {
            "title": "UX/UI Designer (Future Deadline)",
            "description": "Help us create beautiful and intuitive user interfaces for our products.",
            "requirements": """
            Requirements:
            - 3+ years of experience in UX/UI design
            - Expert knowledge of design tools (Figma, Sketch, Adobe XD)
            - Strong portfolio demonstrating user-centered design process
            - Experience with responsive design and web accessibility
            - Knowledge of HTML/CSS
            - Excellent communication and presentation skills
            - Ability to work with cross-functional teams
            """,
            "deadline": now + timedelta(days=3)  # Deadline in 3 days
        },
        {
            "title": "DevOps Engineer (Future Deadline)",
            "description": "Build and maintain our cloud infrastructure and CI/CD pipelines.",
            "requirements": """
            Requirements:
            - 4+ years of experience in DevOps or related field
            - Strong knowledge of cloud platforms (AWS, Azure, GCP)
            - Experience with containerization (Docker, Kubernetes)
            - Expertise in CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
            - Scripting skills in Python, Bash, or similar
            - Knowledge of infrastructure as code (Terraform, CloudFormation)
            - Experience with monitoring and logging tools
            """,
            "deadline": now + timedelta(days=5)  # Deadline in 5 days
        },
        {
            "title": "Product Manager (Future Deadline)",
            "description": "Lead the development of our next-generation products.",
            "requirements": """
            Requirements:
            - 5+ years of experience in product management
            - Experience delivering software products from conception to launch
            - Strong analytical skills and data-driven decision making
            - Excellent communication and stakeholder management skills
            - Ability to work with technical and non-technical teams
            - Experience with agile methodologies
            - Bachelor's degree in Computer Science, Business, or related field
            """,
            "deadline": now + timedelta(days=10)  # Deadline in 10 days
        }
    ]
    
    role_ids = []
    vector_store = VectorStore()
    
    for role in roles:
        role_id = create_role(
            title=role["title"],
            description=role["description"],
            requirements=role["requirements"],
            deadline=role["deadline"]
        )
        
        # Add to vector store
        vector_store.add_role(
            role_id=role_id,
            role_title=role["title"],
            role_requirements=role["requirements"]
        )
        
        role_ids.append(role_id)
        print(f"Created role: {role['title']} (ID: {role_id}) with deadline: {role['deadline']}")
    
    return role_ids

def create_sample_resumes(user_ids, role_ids):
    """Create sample resume submissions"""
    print("Creating sample resume submissions...")
    
    # Sample resume contents
    sample_resumes = [
        """
        JOHN SMITH
        Software Engineer
        john@example.com | (123) 456-7890
        
        SKILLS
        Languages: Python, JavaScript, Java, SQL
        Frameworks: Django, React, Flask, Spring
        Tools: Git, Docker, AWS, CI/CD
        
        EXPERIENCE
        Senior Software Engineer | TechCorp Inc.
        2019 - Present
        - Led development of microservices architecture
        - Improved system performance by 40%
        - Mentored junior developers
        
        Software Engineer | WebSolutions LLC
        2017 - 2019
        - Developed RESTful APIs
        - Implemented automated testing
        
        EDUCATION
        Bachelor of Science in Computer Science
        University of Technology, 2017
        """,
        
        """
        ALICE JONES
        Data Scientist
        alice@example.com | (123) 456-7891
        
        SKILLS
        Programming: Python, R, SQL
        Data Analysis: Pandas, NumPy, Scikit-learn
        Machine Learning: TensorFlow, PyTorch
        Visualization: Matplotlib, Seaborn, Tableau
        
        EXPERIENCE
        Data Scientist | Analytics Pro
        2020 - Present
        - Built predictive models for customer churn
        - Created data visualization dashboards
        - Implemented A/B testing framework
        
        Junior Data Analyst | DataCorp
        2018 - 2020
        - Performed data cleaning and preprocessing
        - Generated reports for stakeholders
        
        EDUCATION
        Master of Science in Data Science
        Data University, 2018
        """,
        
        """
        ROBERT WILLIAMS
        UX/UI Designer
        robert@example.com | (123) 456-7892
        
        SKILLS
        Design: Figma, Sketch, Adobe XD
        Prototyping: InVision, Principle
        Frontend: HTML, CSS, JavaScript basics
        Research: User testing, A/B testing
        
        EXPERIENCE
        Senior UX Designer | DesignHub
        2019 - Present
        - Redesigned company flagship product
        - Conducted user research and testing
        - Created design system library
        
        UI Designer | Creative Agency
        2017 - 2019
        - Designed responsive web interfaces
        - Created style guides and assets
        
        EDUCATION
        Bachelor of Fine Arts in Graphic Design
        Design Institute, 2017
        """,
        
        """
        SARAH DAVIS
        DevOps Engineer
        sarah@example.com | (123) 456-7893
        
        SKILLS
        Cloud: AWS, GCP, Azure
        Containers: Docker, Kubernetes
        CI/CD: Jenkins, GitLab CI, GitHub Actions
        IaC: Terraform, CloudFormation
        Monitoring: Prometheus, Grafana, ELK
        
        EXPERIENCE
        DevOps Lead | CloudTech Inc.
        2020 - Present
        - Migrated on-premise infrastructure to AWS
        - Implemented infrastructure as code
        - Reduced deployment time by 70%
        
        Systems Engineer | TechSystems
        2018 - 2020
        - Managed Linux servers and networks
        - Implemented monitoring solutions
        
        EDUCATION
        Bachelor of Science in Computer Engineering
        Tech University, 2018
        """,
        
        """
        MICHAEL BROWN
        Product Manager
        michael@example.com | (123) 456-7894
        
        SKILLS
        Product: Roadmapping, User Stories, Prioritization
        Tools: Jira, Confluence, Asana, Trello
        Analytics: Google Analytics, Mixpanel
        Business: Market Analysis, Competitive Research
        
        EXPERIENCE
        Senior Product Manager | ProductCo
        2019 - Present
        - Led development of flagship mobile app
        - Increased user engagement by 35%
        - Coordinated cross-functional teams
        
        Product Manager | SoftwareInc
        2017 - 2019
        - Managed product backlog and roadmap
        - Conducted user research and feedback sessions
        
        EDUCATION
        MBA with Product Management focus
        Business School, 2017
        Bachelor of Science in Information Systems
        State University, 2015
        """
    ]
    
    now = datetime.now()
    
    # Create sample resumes
    resume_ids = []
    vector_store = VectorStore()
    
    # Check if user_ids is empty
    if not user_ids:
        print("Error: No user IDs available. Cannot create sample resumes.")
        return []
        
    for i, user_id in enumerate(user_ids):
        # Skip if user_id is None
        if user_id is None:
            print(f"Warning: Skipping None user_id at index {i}")
            continue
            
        # Each user applies to 2-3 random roles
        num_applications = random.randint(2, 3)
        roles_to_apply = random.sample(role_ids, num_applications)
        
        for role_id in roles_to_apply:
            # Skip if role_id is None
            if role_id is None:
                print(f"Warning: Skipping None role_id for user {user_id}")
                continue
                
            # Calculate a random submission date
            days_ago = random.randint(1, 10)
            submitted_at = now - timedelta(days=days_ago)
            
            # Get resume content
            resume_content = sample_resumes[i % len(sample_resumes)]
            
            # Create a placeholder filename
            filename = f"resume_{user_id}_{role_id}.pdf"
            
            # Create a placeholder file path
            file_path = f"uploads/user_{user_id}/{filename}"
            
            try:
                # Save resume
                resume_id = save_resume(
                    user_id=user_id,
                    role_id=role_id,
                    file_path=file_path,
                    filename=filename,
                    content_text=resume_content,
                    submitted_at=submitted_at
                )
                
                # Calculate similarity score
                similarity_score = vector_store.calculate_similarity_score(resume_content, role_id)
                
                # Update resume score in the database
                update_resume_score(resume_id, similarity_score)
                
                resume_ids.append(resume_id)
                print(f"Created resume {resume_id} for user {user_id} applying to role {role_id} with score {similarity_score:.2f}")
            except Exception as e:
                print(f"Error creating resume for user {user_id}, role {role_id}: {str(e)}")
    
    return resume_ids

def rank_and_display_resumes():
    """Rank and display top resumes for roles with passed deadlines"""
    print("\nRanking resumes for roles with passed deadlines...")
    
    ranker = ResumeRanker()
    
    # Get all roles
    roles = get_all_roles()
    
    for role in roles:
        if datetime.now() > role.deadline:
            print(f"\nRanking resumes for role: {role.title} (Deadline: {role.deadline})")
            
            # Rank resumes for this role
            top_resumes = ranker.rank_resumes(role.id, top_n=10)
            
            if not top_resumes:
                print("No resumes found for this role.")
                continue
            
            # Display top resumes
            for idx, resume in enumerate(top_resumes, 1):
                print(f"{idx}. Applicant: {resume.user.username}, Score: {resume.similarity_score:.2f}")

def main():
    """Main function to populate the database with test data"""
    print("Initializing database...")
    init_db()
    
    print("Clearing existing data...")
    clear_database()  # Clear the database before populating

    print("Creating default admin account...")
    init_default_admin()
    
    # Create test users
    user_ids = populate_users()
    
    # Create test roles
    role_ids = populate_roles()
    
    # Create sample resumes
    resume_ids = create_sample_resumes(user_ids, role_ids)
    
    print("\nDatabase population complete!")
    print(f"Created {len(user_ids)} users")
    print(f"Created {len(role_ids)} job roles")
    print(f"Created {len(resume_ids)} resume submissions")
    print("\nTest account credentials:")
    print("Admin: admin@example.com / adminpass")
    print("User: john@example.com / password123")
    
    # Rank and display resumes for roles with passed deadlines
    rank_and_display_resumes()

if __name__ == "__main__":
    main()