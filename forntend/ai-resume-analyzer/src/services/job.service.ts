import { apiClient } from '@/api/axios';
import type { ApiResponse, JobSearchPayload, JobSearchResponse, JobRecommendation } from '@/types';

type BackendJobRecommendation = {
  job_title?: string;
  title?: string;
  company?: string;
  location?: string;
  experience?: string;
  employment_type?: string;
  work_mode?: string;
  salary?: string;
  description?: string;
  skills?: string[];
  posted_date?: string;
  apply_url?: string;
  source?: string;
  match_score?: number;
  match_reason?: string;
};

const normalizeJob = (job: BackendJobRecommendation): JobRecommendation => ({
  title: job.job_title ?? job.title ?? '',
  company: job.company ?? '',
  location: job.location ?? '',
  experience: job.experience ?? '',
  employmentType: job.employment_type ?? '',
  workMode: job.work_mode ?? '',
  salary: job.salary ?? '',
  description: job.description ?? '',
  requiredSkills: Array.isArray(job.skills) ? job.skills : [],
  postedDate: job.posted_date ?? '',
  applyUrl: job.apply_url ?? '',
  source: job.source ?? '',
  matchScore: typeof job.match_score === 'number' ? job.match_score : 0,
  matchReason: job.match_reason ?? '',
});

export const JobService = {
  search: async (payload: JobSearchPayload): Promise<JobRecommendation[]> => {
    const response = await apiClient.post<ApiResponse<JobSearchResponse>>(
      '/jobs/search/',
      payload
    );

    const jobs = response.data?.data?.recommended_jobs ?? [];
    return jobs.map(normalizeJob);
  },
};