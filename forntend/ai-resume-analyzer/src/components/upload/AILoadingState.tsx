import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BrainCircuit, CheckCircle2 } from 'lucide-react';

const loadingSteps = [
  "Uploading Resume to Secure Vault...",
  "Extracting Document Text...",
  "Parsing Professional Experience...",
  "Running ATS Algorithm...",
  "Detecting Technical Skills...",
  "Cross-referencing Missing Keywords...",
  "Calculating Final ATS Score...",
  "Generating Recruiter Feedback...",
  "Finalizing Report..."
];

export const AILoadingState = () => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < loadingSteps.length - 1 ? prev + 1 : prev));
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center space-y-8 py-16">
      <motion.div 
        animate={{ rotate: 360, scale: [1, 1.1, 1] }}
        transition={{ repeat: Infinity, duration: 4, ease: "linear" }}
        className="relative flex items-center justify-center w-24 h-24 rounded-full bg-cyan-500/10 border border-cyan-500/30"
      >
        <BrainCircuit className="w-10 h-10 text-cyan-400" />
      </motion.div>

      <div className="w-full max-w-md space-y-4">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="text-center"
          >
            <h3 className="text-xl font-semibold text-gray-100">
              {loadingSteps[currentStep]}
            </h3>
          </motion.div>
        </AnimatePresence>

        {/* Progress Tracker */}
        <div className="space-y-2 mt-8">
          {loadingSteps.map((step, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0 }}
              animate={{ opacity: index <= currentStep ? 1 : 0.3 }}
              className="flex items-center space-x-3 text-sm"
            >
              {index < currentStep ? (
                <CheckCircle2 className="w-4 h-4 text-cyan-400" />
              ) : index === currentStep ? (
                <motion.div 
                  animate={{ scale: [1, 1.5, 1] }} 
                  transition={{ repeat: Infinity }}
                  className="w-2 h-2 rounded-full bg-blue-500 ml-1 mr-2" 
                />
              ) : (
                <div className="w-2 h-2 rounded-full bg-gray-700 ml-1 mr-2" />
              )}
              <span className={index === currentStep ? "text-cyan-300 font-medium" : "text-gray-400"}>
                {step}
              </span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};