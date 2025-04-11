from database.db_manager import get_resumes_for_role, mark_as_shortlisted, get_role
from datetime import datetime
from rag.vector_store import VectorStore  # Import VectorStore for similarity calculations
from sqlalchemy.orm import joinedload
from database.models import Resume


class ResumeRanker:
    def __init__(self):
        self.vector_store = VectorStore()  # Initialize VectorStore

    def rank_resumes(self, role_id, top_n=10):
        """
        Rank resumes for a specific role based on similarity score.
        Ranking is only performed if the role's deadline has passed.
        """
        from database.db_manager import get_db_session  # Avoid circular imports
        from database.models import Resume

        with get_db_session() as session:
            # Fetch resumes with the user relationship eagerly loaded
            resumes = (
                session.query(Resume)
                .options(joinedload(Resume.user))  # Eager load the user relationship
                .filter(Resume.role_id == role_id)
                .all()
            )
            
            if not resumes:
                return []

            # Calculate similarity scores for each resume
            ranked_resumes = []
            for resume in resumes:
                # Calculate similarity score dynamically
                similarity_score = self.vector_store.calculate_similarity_score(resume.content_text, role_id)
                ranked_resumes.append({
                    "resume": resume,
                    "score": similarity_score
                })

            # Sort resumes by similarity score (descending)
            ranked_resumes.sort(key=lambda x: x["score"], reverse=True)

            # Return top N resumes
            return [resume["resume"] for resume in ranked_resumes[:top_n]]


    def shortlist_top_resumes(self, role_id, top_n=10):
        """
        Shortlist top N resumes for a specific role.
        Shortlisting is only performed if the role's deadline has passed.
        """
        # Get top resumes
        top_resumes = self.rank_resumes(role_id, top_n)

        # Mark them as shortlisted
        for resume in top_resumes:
            mark_as_shortlisted(resume.id)

        return top_resumes