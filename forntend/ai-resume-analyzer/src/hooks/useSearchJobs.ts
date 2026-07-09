import { useMutation } from '@tanstack/react-query';
import { JobService } from '@/services/job.service';
import type { JobSearchPayload, JobRecommendation } from '@/types';
import toast from 'react-hot-toast';

export const useSearchJobs = () => {
  return useMutation<JobRecommendation[], Error, JobSearchPayload>({
    mutationFn: JobService.search,
    onError: (error: any) => {
      const errorMessage = error?.response?.data?.message 
        || error?.message 
        || 'Failed to fetch job recommendations.';
      toast.error(errorMessage);
    },
  });
};