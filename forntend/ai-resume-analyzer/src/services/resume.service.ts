import { apiClient } from '@/api/axios';
import type { UploadFormData, ApiResponse, ResumeAnalysisResponse } from '@/types';

// const normalizeResumeAnalysis = (payload: any): ResumeAnalysisResponse => {
//   const analysis = payload?.analysis ?? {};
//   const overallScore = analysis?.overall_score ?? {};
//   const sectionScores = analysis?.section_scores ?? {};
//   const keywordAnalysis = analysis?.keyword_analysis ?? {};
//   const recruiterFeedback = analysis?.recruiter_feedback ?? {};

//   return {
//     provider: payload?.provider ?? '',
//     model: payload?.model ?? '',
//     atsScore: {
//       score: typeof overallScore?.score === 'number' ? overallScore.score : 0,
//       grade: overallScore?.grade ?? '',
//       reason: overallScore?.reason ?? '',
//     },
//     overallSummary: analysis?.summary ?? '',
//     strengths: Array.isArray(analysis?.strengths) ? analysis.strengths : [],
//     weaknesses: Array.isArray(analysis?.weaknesses) ? analysis.weaknesses : [],
//     skills: {
//       detected: Array.isArray(analysis?.detected_skills) ? analysis.detected_skills : [],
//       missing: Array.isArray(analysis?.missing_skills) ? analysis.missing_skills : [],
//     },
//     sectionScores: {
//       summary: sectionScores?.summary?.score ?? 0,
//       experience: sectionScores?.experience?.score ?? 0,
//       projects: sectionScores?.projects?.score ?? 0,
//       skills: sectionScores?.skills?.score ?? 0,
//       education: sectionScores?.education?.score ?? 0,
//     },
//     keywords: {
//       density: Object.fromEntries(
//         (Array.isArray(keywordAnalysis?.detected_keywords) ? keywordAnalysis.detected_keywords : []).map((keyword: string) => [keyword, 1])
//       ),
//     },
//     analysis: {
//       grammar: Array.isArray(analysis?.grammar?.issues) ? analysis.grammar.issues : [],
//       formatting: Array.isArray(analysis?.formatting?.issues) ? analysis.formatting.issues : [],
//     },
//     suggestions: {
//       rewrites: Array.isArray(analysis?.resume_rewrites)
//         ? analysis.resume_rewrites.map((item: any) => ({ before: item?.before ?? '', after: item?.after ?? '', reason: item?.reason ?? '' }))
//         : [],
//       achievements: Array.isArray(analysis?.achievement_suggestions) ? analysis.achievement_suggestions : [],
//     },
//     recommendations: Array.isArray(analysis?.recommendations) ? analysis.recommendations : [],
//     roleMatch: Array.isArray(analysis?.role_match)
//       ? analysis.role_match.map((item: any) => ({ role: item?.role ?? '', percentage: item?.match_percentage ?? 0 }))
//       : [],
//     recruiterFeedback: {
//       interviewProbability: recruiterFeedback?.interview_probability ?? '',
//       feedback: recruiterFeedback?.feedback ?? '',
//     },
//   };
// };

// export const ResumeService = {
//   analyze: async (data: UploadFormData): Promise<ResumeAnalysisResponse> => {
//     const formData = new FormData();
//     formData.append('resume', data.resume);
//     formData.append('provider', data.provider);
//     formData.append('targetRole', data.targetRole);

//     const response = await apiClient.post<ApiResponse<any>>(
//       '/resumes/analyze/',
//       formData,
//       { headers: { 'Content-Type': 'multipart/form-data' } }
//     );

//     return normalizeResumeAnalysis(response.data?.data);
//   },
// };




export const ResumeService = {
  analyze: async (data: UploadFormData): Promise<ResumeAnalysisResponse> => {
    const formData = new FormData();
    
    formData.append('resume', data.resume);
    // Convert provider to lowercase: 'Gemini' → 'gemini', 'OpenAI' → 'openai', etc.
    formData.append('provider', data.provider.toLowerCase());
    // Send as 'target_role' (snake_case) to match backend serializer
    formData.append('target_role', data.targetRole);

    const response = await apiClient.post<ApiResponse<ResumeAnalysisResponse>>(
      '/resumes/analyze/', 
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    
    return response.data.data;
  }
};