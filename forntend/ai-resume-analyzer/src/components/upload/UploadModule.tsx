import React, { useState, useRef, useCallback } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  UploadCloud, 
  FileText, 
  X, 
  Briefcase, 
  Cpu, 
  Sparkles,
  AlertCircle,
  CheckCircle2
} from 'lucide-react';
import { UploadSchema } from '@/types';
import type { UploadFormData } from '@/types';
import { useAnalyzeResume } from '@/hooks/useAnalyzeResume';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import toast from 'react-hot-toast';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const UploadModule = () => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Dedicated local state for immediate UI updates
  const [localFile, setLocalFile] = useState<File | null>(null);
  
  // Integrate TanStack Query Mutation
  const { mutate: analyzeResume, isPending } = useAnalyzeResume();

  const {
    register,
    handleSubmit,
    setValue,
    trigger,
    clearErrors,
    formState: { errors, isValid },
  } = useForm<UploadFormData>({
    resolver: zodResolver(UploadSchema),
    mode: 'onChange',
    defaultValues: {
      provider: 'Gemini', // Lowercase to match backend
      targetRole: '',
    },
  });

  const handleDragOver = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      e.stopPropagation();
      if (!isPending) setIsDragging(true);
    },
    [isPending]
  );

  const handleDragLeave = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
    },
    []
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLDivElement>) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        if (!isPending) fileInputRef.current?.click();
      }
    },
    [isPending]
  );

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (isPending) return;

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleFileSelection(files[0]);
    }
  };

  const handleFileSelection = async (file: File) => {
    setValue('resume', file, { shouldValidate: true });
    
    // Check if the file passes Zod validation (size, type)
    const isValidFile = await trigger('resume');
    
    if (isValidFile) {
      setLocalFile(file); // Instantly update UI
      toast.success("Resume attached successfully!");
    }
  };

  const removeFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (isPending) return;
    
    setLocalFile(null); // Clear UI state
    setValue('resume', undefined as any, { shouldValidate: true });
    
    if (fileInputRef.current) fileInputRef.current.value = '';
    clearErrors('resume');
  };

  const onSubmit = (data: UploadFormData) => {
    analyzeResume(data);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-2xl mx-auto"
    >
      <div className="bg-slate-900/40 backdrop-blur-xl border border-white/10 p-8 rounded-3xl shadow-2xl relative overflow-hidden">
        
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[120%] h-32 bg-primary/20 blur-[100px] pointer-events-none" />

        <div className="text-center mb-8 relative z-10">
          <h2 className="text-3xl font-bold text-foreground mb-2 flex items-center justify-center gap-2">
            <Sparkles className="h-6 w-6 text-accent" />
            Analyze Your Resume
          </h2>
          <p className="text-muted-foreground">Upload your document and configure your analysis parameters.</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 relative z-10">
          
          <div className="space-y-2">
            <div
              role="button"
              tabIndex={0}
              aria-label="Upload Resume File"
              onKeyDown={handleKeyDown}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => !isPending && fileInputRef.current?.click()}
              className={cn(
                "relative flex flex-col items-center justify-center w-full min-h-[200px] border-2 border-dashed rounded-2xl transition-all group overflow-hidden focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent",
                isPending ? "cursor-not-allowed opacity-60" : "cursor-pointer",
                isDragging ? "border-accent bg-accent/5" : "border-slate-700 hover:border-primary/50 hover:bg-slate-900/60",
                errors.resume ? "border-destructive/50 hover:border-destructive" : "",
                !isDragging && !errors.resume && "bg-slate-950/50"
              )}
            >
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                disabled={isPending}
                accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                onChange={(e) => {
                  if (e.target.files?.[0]) handleFileSelection(e.target.files[0]);
                }}
              />

              <AnimatePresence mode="wait">
                {!localFile ? (
                  <motion.div 
                    key="upload-prompt"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="flex flex-col items-center text-center p-6"
                  >
                    <div className="p-4 rounded-full bg-slate-800/50 text-muted-foreground group-hover:text-primary group-hover:scale-110 transition-all mb-4">
                      <UploadCloud className="w-8 h-8" />
                    </div>
                    <p className="text-foreground font-medium mb-1">
                      Drag & Drop your resume here
                    </p>
                    <p className="text-sm text-muted-foreground">
                      or click to browse from your computer
                    </p>
                    <div className="flex items-center gap-2 mt-4 text-xs font-medium text-slate-500">
                      <span className="bg-slate-800 px-2 py-1 rounded">PDF</span>
                      <span className="bg-slate-800 px-2 py-1 rounded">DOCX</span>
                      <span>• Max 5MB</span>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div 
                    key="file-selected"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="flex items-center gap-4 w-full p-6 bg-slate-900/80 border border-emerald-500/30 rounded-2xl"
                  >
                    <div className="relative p-3 bg-emerald-500/10 rounded-xl text-emerald-400">
                      <FileText className="w-8 h-8" />
                      <div className="absolute -top-2 -right-2 bg-slate-950 rounded-full">
                        <CheckCircle2 className="w-5 h-5 text-emerald-500 bg-white rounded-full" />
                      </div>
                    </div>
                    <div className="flex-1 min-w-0 text-left">
                      <p className="text-sm font-semibold text-emerald-400 truncate">
                        {localFile.name}
                      </p>
                      <p className="text-xs text-slate-400 mt-1">
                        {(localFile.size / 1024 / 1024).toFixed(2)} MB • Ready for analysis
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={removeFile}
                      disabled={isPending}
                      className="p-2 rounded-full hover:bg-rose-500/10 text-slate-400 hover:text-rose-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
            
            <AnimatePresence>
              {errors.resume && (
                <motion.div 
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="flex items-center gap-2 text-sm text-destructive mt-2"
                >
                  <AlertCircle className="w-4 h-4" />
                  <span>{errors.resume.message as string}</span>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div className="space-y-2 relative">
              <label className="text-sm font-medium text-slate-300 ml-1">Target Job Role</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-muted-foreground">
                  <Briefcase className="w-4 h-4" />
                </div>
                <input 
                  {...register('targetRole')}
                  type="text"
                  disabled={isPending}
                  placeholder="e.g., Senior React Developer"
                  className={cn(
                    "w-full bg-slate-950/50 border rounded-xl pl-10 pr-4 py-3 text-sm text-foreground placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed",
                    errors.targetRole 
                      ? "border-destructive focus:ring-destructive/20" 
                      : "border-slate-800 focus:ring-primary/50"
                  )}
                />
              </div>
              {errors.targetRole && (
                <p className="text-xs text-destructive ml-1">{errors.targetRole.message}</p>
              )}
            </div>

            <div className="space-y-2 relative">
              <label className="text-sm font-medium text-slate-300 ml-1">Intelligence Engine</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-muted-foreground">
                  <Cpu className="w-4 h-4" />
                </div>
                <select 
                  {...register('provider')}
                  disabled={isPending}
                  className={cn(
                    "w-full bg-slate-950/50 border rounded-xl pl-10 pr-4 py-3 text-sm text-foreground appearance-none focus:outline-none focus:ring-2 focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed",
                    errors.provider 
                      ? "border-destructive focus:ring-destructive/20" 
                      : "border-slate-800 focus:ring-primary/50"
                  )}
                >
                  <option value="gemini">Google Gemini (Recommended)</option>
                  <option value="claude">Anthropic Claude</option>
                  <option value="openai">OpenAI GPT-4o</option>
                  <option value="groq">Groq (Ultra-Fast)</option>
                  <option value="openrouter">OpenRouter (Dynamic)</option>
                </select>
                <div className="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none text-muted-foreground">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                </div>
              </div>
              {errors.provider && (
                <p className="text-xs text-destructive ml-1">{errors.provider.message}</p>
              )}
            </div>
          </div>

          <button
            type="submit"
            disabled={!isValid || isPending || !localFile}
            className="w-full relative group overflow-hidden rounded-xl bg-primary p-[1px] transition-all disabled:opacity-50 disabled:cursor-not-allowed mt-4"
          >
            {!isPending && (
              <span className="absolute inset-0 bg-gradient-to-r from-primary via-accent to-primary opacity-0 group-hover:opacity-100 group-hover:animate-gradient bg-[length:200%_auto] transition-opacity duration-500" />
            )}
            <div className={cn(
              "relative bg-primary transition-all duration-300 flex items-center justify-center py-4 rounded-xl",
              !isPending && "group-hover:bg-opacity-0"
            )}>
              <span className="text-primary-foreground font-semibold flex items-center gap-2">
                {isPending ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                    >
                      <Cpu className="w-5 h-5" />
                    </motion.div>
                    Analyzing Resume...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Analyze Resume
                  </>
                )}
              </span>
            </div>
          </button>
        </form>
      </div>
    </motion.div>
  );
};