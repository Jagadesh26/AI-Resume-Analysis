import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Briefcase, 
  MapPin, 
  DollarSign, 
  Globe, 
  ExternalLink, 
  Building2, 
  Search,
  Sparkles,
  Target
} from 'lucide-react';
import { useSearchJobs } from '@/hooks/useSearchJobs';
import { ResumeAnalysisResponse } from '@/types';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const containerVariants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } },
};

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 50 } },
};

interface JobRecommendationsProps {
  analysisData: ResumeAnalysisResponse;
}

export const JobRecommendations: React.FC<JobRecommendationsProps> = ({ analysisData }) => {
  const { mutate: searchJobs, data: jobs, isPending } = useSearchJobs();
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = () => {
    setHasSearched(true);
    
    // FIX: Safely access the nested '.analysis' object and snake_case keys
    const roles = analysisData?.analysis?.role_match?.map(r => r.role) || [];
    const skills = analysisData?.analysis?.detected_skills || [];

    searchJobs({
      roles: roles,
      skills: skills,
      work_modes: ['Remote', 'Hybrid'], 
    });
  };

  return (
    <div className="w-full max-w-7xl mx-auto mt-12 space-y-8">
      
      <div className="flex flex-col md:flex-row items-center justify-between bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2 mb-2">
            <Briefcase className="w-6 h-6 text-primary" />
            AI Job Matchmaker
          </h2>
          <p className="text-sm text-slate-400">
            Find roles perfectly aligned with your newly analyzed ATS profile and detected skills.
          </p>
        </div>
        
        <button
          onClick={handleSearch}
          disabled={isPending}
          className="mt-4 md:mt-0 relative group overflow-hidden rounded-xl bg-primary p-[1px] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {!isPending && (
            <span className="absolute inset-0 bg-gradient-to-r from-primary via-accent to-primary opacity-0 group-hover:opacity-100 group-hover:animate-gradient bg-[length:200%_auto] transition-opacity duration-500" />
          )}
          <div className="relative bg-primary group-hover:bg-opacity-0 transition-all duration-300 flex items-center justify-center py-3 px-6 rounded-xl">
            <span className="text-primary-foreground font-semibold flex items-center gap-2">
              {isPending ? (
                <>
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}>
                    <Search className="w-4 h-4" />
                  </motion.div>
                  Scanning Markets...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  Find Matched Jobs
                </>
              )}
            </span>
          </div>
        </button>
      </div>

      <AnimatePresence>
        {/* FIX: Ensure jobs is defined before mapping to prevent crashes */}
        {hasSearched && !isPending && jobs && jobs.length > 0 && (
          <motion.div 
            variants={containerVariants}
            initial="hidden"
            animate="show"
            className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6"
          >
            {jobs.map((job, idx) => (
              <motion.div 
                key={idx}
                variants={cardVariants}
                whileHover={{ y: -5 }}
                className="group flex flex-col bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-2xl p-6 shadow-xl hover:border-primary/50 hover:shadow-[0_0_30px_rgba(37,99,235,0.15)] transition-all duration-300"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    {/* FIX: Use job_title */}
                    <h3 className="text-lg font-bold text-slate-100 line-clamp-1 group-hover:text-primary transition-colors">
                      {job.job_title}
                    </h3>
                    <div className="flex items-center text-sm text-slate-400 mt-1 gap-1.5">
                      <Building2 className="w-4 h-4 text-slate-500" />
                      <span className="truncate">{job.company}</span>
                    </div>
                  </div>
                  
                  <div className="flex flex-col items-center justify-center bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 ml-3 shrink-0">
                    <span className="text-xs text-slate-400 mb-0.5 flex items-center gap-1">
                      <Target className="w-3 h-3 text-emerald-400" /> Match
                    </span>
                    {/* FIX: Use match_score */}
                    <span className={cn(
                      "font-bold text-lg leading-none",
                      job.match_score >= 85 ? "text-emerald-400" : job.match_score >= 70 ? "text-amber-400" : "text-rose-400"
                    )}>
                      {job.match_score}%
                    </span>
                  </div>
                </div>

                <div className="flex flex-wrap gap-y-3 gap-x-4 mb-6 text-sm text-slate-300">
                  <div className="flex items-center gap-1.5">
                    <MapPin className="w-4 h-4 text-accent" /> {job.location}
                  </div>
                  <div className="flex items-center gap-1.5">
                    {/* FIX: Use work_mode */}
                    <Globe className="w-4 h-4 text-blue-400" /> {job.work_mode}
                  </div>
                  <div className="flex items-center gap-1.5">
                    {/* FIX: Use employment_type */}
                    <Briefcase className="w-4 h-4 text-purple-400" /> {job.employment_type || "N/A"}
                  </div>
                  <div className="flex items-center gap-1.5 font-medium text-emerald-400">
                    <DollarSign className="w-4 h-4" /> {job.salary || "Not Specified"}
                  </div>
                </div>

                <div className="mb-6 flex-1">
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Required Skills</p>
                  <div className="flex flex-wrap gap-2">
                    {/* FIX: Safe rendering of skills array */}
                    {job.skills && job.skills.slice(0, 5).map((skill, i) => (
                      <span key={i} className="px-2.5 py-1 rounded-md bg-slate-800/50 border border-slate-700/50 text-slate-300 text-xs">
                        {skill}
                      </span>
                    ))}
                    {job.skills && job.skills.length > 5 && (
                      <span className="px-2.5 py-1 rounded-md bg-slate-950 border border-slate-800 text-slate-500 text-xs">
                        +{job.skills.length - 5}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-slate-800/50 mt-auto">
                  <span className="text-xs text-slate-500">
                    Source: <span className="text-slate-400">{job.source}</span>
                  </span>
                  {/* FIX: Use apply_url */}
                  <a
                    href={job.apply_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center justify-center gap-2 px-4 py-2 text-sm font-semibold text-primary bg-primary/10 hover:bg-primary/20 rounded-lg transition-colors"
                  >
                    Apply Now
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}

        {hasSearched && !isPending && (!jobs || jobs.length === 0) && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12 bg-slate-900/20 rounded-2xl border border-slate-800 border-dashed"
          >
            <Briefcase className="w-12 h-12 text-slate-600 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-slate-300">No matching jobs found</h3>
            <p className="text-slate-500 mt-2">Try adjusting your profile or preferences.</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};