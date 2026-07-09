import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ResumeService } from '@/services/resume.service';
import type { UploadFormData, ResumeAnalysisResponse } from '@/types';
import toast from 'react-hot-toast';

export const useAnalyzeResume = () => {
  const queryClient = useQueryClient();

  return useMutation<ResumeAnalysisResponse, Error, UploadFormData>({
    mutationFn: ResumeService.analyze,
    onSuccess: (data) => {
      toast.success('Resume analyzed successfully!');
      
      // Store the response in the query cache so it can be accessed by the Dashboard component later
      queryClient.setQueryData(['resumeAnalysisResult'], data);
    },
    onError: (error: any) => {
      // Extract backend error message if available
      const errorMessage = error?.response?.data?.message 
        || error?.message 
        || 'Failed to analyze resume. Please try again.';
        
      toast.error(errorMessage);
    },
  });
};