// =============================================
// Upload Request
// =============================================

import { z } from "zod";

export const UploadSchema = z.object({
  resume: z.instanceof(File, {
    message: "Resume file is required.",
  }),
  provider: z.string().min(1, "Provider is required."),
  targetRole: z.string().min(2, "Target role is required."),
});

export type UploadFormData = z.infer<typeof UploadSchema>;


// =============================================
// Generic API Response
// =============================================

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}


// =============================================
// ATS Score
// =============================================

export interface OverallScore {
  score: number;
  grade: string;
  reason: string;
}


// =============================================
// Grammar
// =============================================

export interface GrammarAnalysis {
  score: number;
  issues: string[];
}


// =============================================
// Formatting
// =============================================

export interface FormattingAnalysis {
  score: number;
  issues: string[];
}


// =============================================
// Section Score
// =============================================

export interface SectionScore {
  score: number;
  reason: string;
}

export interface SectionScores {
  summary: SectionScore;
  experience: SectionScore;
  projects: SectionScore;
  skills: SectionScore;
  education: SectionScore;
}


// =============================================
// Keyword Analysis
// =============================================

export interface KeywordAnalysis {
  detected_keywords: string[];
  missing_keywords: string[];
  keyword_density: number;
}


// =============================================
// Resume Rewrite
// =============================================

export interface ResumeRewrite {
  before: string;
  after: string;
}


// =============================================
// Role Match
// =============================================

export interface RoleMatch {

  role: string;

  weight?: number;

  match_percentage?: number;

}


// =============================================
// Recruiter Feedback
// =============================================

export interface RecruiterFeedback {

  interview_probability: string;

  feedback: string;

}


// =============================================
// Job Search Criteria
// =============================================

export interface JobSearch {

  roles: string[];

  preferred_location: string;

  experience_level: string;

  employment_types: string[];

  work_modes: string[];

  skills: string[];

}


// =============================================
// Recommended Job
// =============================================

export interface RecommendedJob {

  job_title: string;

  company: string;

  location: string;

  employment_type: string;

  work_mode: string;

  salary: string;

  skills: string[];

  description: string;

  posted_date: string;

  apply_url: string;

  source: string;

  match_score: number;

  match_reason: string;

}


// =============================================
// Analysis
// =============================================

export interface ResumeAnalysis {

  overall_score: OverallScore;

  summary: string;

  strengths: string[];

  weaknesses: string[];

  detected_skills: string[];

  missing_skills: string[];

  grammar: GrammarAnalysis;

  formatting: FormattingAnalysis;

  section_scores: SectionScores;

  keyword_analysis: KeywordAnalysis;

  achievement_suggestions: string[];

  resume_rewrites: ResumeRewrite[];

  recommendations: string[];

  role_match: RoleMatch[];

  recruiter_feedback: RecruiterFeedback;

  recommended_jobs: RecommendedJob[];

  job_search: JobSearch;

}


// =============================================
// Final Response
// =============================================

export interface ResumeAnalysisResponse {

  provider: string;

  model: string;

  usage: unknown;

  analysis: ResumeAnalysis;

}