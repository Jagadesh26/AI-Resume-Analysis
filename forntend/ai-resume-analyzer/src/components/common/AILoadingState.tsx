import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BrainCircuit, CheckCircle2, Cpu, Sparkles } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const loadingSteps = [
  "Uploading Resume",
  "Extracting Resume",
  "Reading Experience",
  "Analyzing ATS",
  "Checking Skills",
  "Finding Missing Keywords",
  "Generating Recommendations",
  "Preparing Recruiter Feedback",
  "Searching Jobs",
  "Preparing Dashboard"
];

export const AILoadingState: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    // Calculate an interval so the entire animation spans a realistic API wait time (e.g., ~15-20 seconds)
    // 1800ms per step feels substantial but responsive
    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < loadingSteps.length - 1) {
          return prev + 1;
        }
        // Once it hits the end, it stays on the last step until the API resolves and unmounts it
        clearInterval(interval);
        return prev;
      });
    }, 1800);

    return () => clearInterval(interval);
  }, []);

  const progressPercentage = ((currentStep + 1) / loadingSteps.length) * 100;

  return (
    <div className="flex flex-col items-center justify-center w-full min-h-[400px] p-8">
      
      {/* --- Central Glowing AI Orb --- */}
      <div className="relative flex items-center justify-center mb-12">
        {/* Outer rotating dashed ring */}
        <motion.div 
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 8, ease: "linear" }}
          className="absolute w-32 h-32 rounded-full border-2 border-dashed border-primary/40"
        />
        
        {/* Inner pulsing glow */}
        <motion.div 
          animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0.8, 0.5] }}
          transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
          className="absolute w-24 h-24 rounded-full bg-accent/20 blur-xl"
        />
        
        {/* Core Icon Hub */}
        <div className="relative z-10 w-20 h-20 bg-slate-900 border border-slate-700 rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(37,99,235,0.3)]">
          <motion.div
            animate={{ rotate: [0, -10, 10, 0] }}
            transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
          >
            <BrainCircuit className="w-10 h-10 text-cyan-400" />
          </motion.div>
        </div>
      </div>

      <div className="w-full max-w-md">
        {/* --- Dynamic Status Text --- */}
        <div className="h-10 relative flex items-center justify-center overflow-hidden mb-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="absolute flex items-center gap-2 text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent"
            >
              <Sparkles className="w-5 h-5 text-accent" />
              {loadingSteps[currentStep]}...
            </motion.div>
          </AnimatePresence>
        </div>

        {/* --- Glowing Progress Bar --- */}
        <div className="relative w-full h-2 bg-slate-900 rounded-full overflow-hidden mb-8 border border-slate-800">
          <motion.div 
            className="absolute top-0 left-0 h-full bg-gradient-to-r from-primary via-accent to-primary rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${progressPercentage}%` }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
          >
            {/* Shimmer effect inside progress bar */}
            <motion.div 
              className="absolute inset-0 w-full h-full bg-white/20"
              animate={{ x: ['-100%', '100%'] }}
              transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
            />
          </motion.div>
        </div>

        {/* --- Progress Steps List --- */}
        <div className="space-y-3 bg-slate-900/50 p-6 rounded-2xl border border-slate-800 backdrop-blur-sm">
          {loadingSteps.map((step, index) => {
            const isCompleted = index < currentStep;
            const isCurrent = index === currentStep;
            const isPending = index > currentStep;

            return (
              <motion.div 
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: isPending ? 0.3 : 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className={cn(
                  "flex items-center space-x-3 text-sm transition-colors duration-300",
                  isCurrent ? "text-white" : isCompleted ? "text-slate-300" : "text-slate-600"
                )}
              >
                {/* Step Icon */}
                <div className="w-6 h-6 flex items-center justify-center shrink-0">
                  {isCompleted ? (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: "spring", stiffness: 200, damping: 10 }}
                    >
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    </motion.div>
                  ) : isCurrent ? (
                    <motion.div 
                      animate={{ rotate: 360 }}
                      transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                      className="p-1 rounded-full bg-primary/20"
                    >
                      <Cpu className="w-3.5 h-3.5 text-accent" />
                    </motion.div>
                  ) : (
                    <div className="w-2 h-2 rounded-full bg-slate-700" />
                  )}
                </div>

                {/* Step Text */}
                <span className={cn(
                  "font-medium",
                  isCurrent && "text-accent drop-shadow-[0_0_8px_rgba(6,182,212,0.5)]"
                )}>
                  {step}
                </span>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
};