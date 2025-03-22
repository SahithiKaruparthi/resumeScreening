# from rag.retriever import RagRetriever
# from resume_analyzer.analyzer import ResumeAnalyzer
# from database.db_manager import update_resume_score

# class ResumeScorer:
#     def __init__(self):
#         self.retriever = RagRetriever()
#         self.analyzer = ResumeAnalyzer(self.retriever)
    
#     def score_resume(self, resume_id, file_path, role_id):
#         """Score a resume based on its similarity to role requirements"""
#         # Analyze resume
#         analysis_result = self.analyzer.analyze_resume(file_path, role_id)
        
#         if not analysis_result["success"]:
#             return {
#                 "success": False,
#                 "error": analysis_result["error"],
#                 "score": 0.0
#             }
        
#         # Get the similarity score
#         similarity_score = analysis_result["score"]
        
#         # Update the score in the database
#         update_success = update_resume_score(resume_id, similarity_score)
        
#         if not update_success:
#             return {
#                 "success": False,
#                 "error": "Failed to update resume score in database",
#                 "score": similarity_score
#             }
        
#         return {
#             "success": True,
#             "score": similarity_score,
#             "text": analysis_result["text"]
#         }

from rag.retriever import RagRetriever
from resume_analyzer.analyzer import ResumeParser, ResumeAnalyzer
from database.db_manager import update_resume_score

class ResumeScorer:
    def __init__(self):
        self.retriever = RagRetriever()
        self.analyzer = ResumeAnalyzer(retriever=self.retriever)
    
    def score_resume(self, resume_id, file_path, role_id):
        """Score a resume based on its similarity to role requirements"""
        # Analyze resume
        analysis_result = self.analyzer.analyze_resume(file_path, role_id)
        
        if not analysis_result["success"]:
            return {
                "success": False,
                "error": analysis_result["error"],
                "score": 0.0
            }
        
        # Get the similarity score
        similarity_score = analysis_result["score"]
        
        # Update the score in the database
        update_success = update_resume_score(resume_id, similarity_score)
        
        if not update_success:
            return {
                "success": False,
                "error": "Failed to update resume score in database",
                "score": similarity_score
            }
        
        return {
            "success": True,
            "score": similarity_score,
            "text": analysis_result["text"]
        }