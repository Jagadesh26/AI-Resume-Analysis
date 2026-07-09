import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Sparkles, 
  Briefcase, 
  Cpu, 
  ArrowRight, 
} from 'lucide-react';

// --- Animation Variants ---
const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.15, delayChildren: 0.2 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: 'spring' as const, stiffness: 50 } },
} as const;

const featureCards = [
  {
    title: 'ATS Analysis',
    description: 'Get an instant ATS compatibility score with detailed breakdown and keyword density checks.',
    icon: FileText,
  },
  {
    title: 'Resume Improvements',
    description: 'Receive AI-driven suggestions to rewrite bullet points, fix grammar, and highlight achievements.',
    icon: Sparkles,
  },
  {
    title: 'Job Recommendations',
    description: 'Discover real-time job openings perfectly matched to your newly analyzed resume and skills.',
    icon: Briefcase,
  },
  {
    title: 'Multi AI Providers',
    description: 'Choose your preferred intelligence engine: Gemini, Groq, OpenAI, Claude, or OpenRouter.',
    icon: Cpu,
  },
];

export const LandingPage = () => {
  return (
    <div className="relative min-h-screen overflow-hidden bg-background flex flex-col">
      {/* --- Animated Ambient Background --- */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.2, 0.3],
            rotate: [0, 90, 0],
          }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute -top-[20%] -left-[10%] w-[50rem] h-[50rem] rounded-full bg-primary/10 blur-[120px]"
        />
        <motion.div
          animate={{
            scale: [1, 1.5, 1],
            opacity: [0.2, 0.4, 0.2],
            rotate: [0, -90, 0],
          }}
          transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
          className="absolute top-[40%] -right-[20%] w-[60rem] h-[60rem] rounded-full bg-accent/10 blur-[150px]"
        />
      </div>

      {/* --- Main Content --- */}
      <main className="flex-1 relative z-10 container mx-auto px-6 pt-32 pb-16 flex flex-col items-center text-center">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="max-w-4xl mx-auto flex flex-col items-center"
        >
          {/* Hero Section */}
          <motion.div variants={itemVariants} className="inline-flex items-center rounded-full border border-accent/30 bg-accent/10 px-3 py-1 text-sm font-medium text-accent mb-8 backdrop-blur-sm">
            <Sparkles className="mr-2 h-4 w-4" />
            Production-Ready AI Analysis
          </motion.div>

          <motion.h1 
            variants={itemVariants}
            className="text-5xl md:text-7xl font-extrabold tracking-tight text-foreground mb-6"
          >
            AI Resume{' '}
            <span className="bg-gradient-to-r from-primary via-accent to-primary bg-[length:200%_auto] animate-gradient text-transparent bg-clip-text">
              Analyzer
            </span>
          </motion.h1>

          <motion.p 
            variants={itemVariants}
            className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10 leading-relaxed"
          >
            Upload your resume and receive AI-powered ATS analysis, recruiter feedback, resume improvements and job recommendations.
          </motion.p>

          <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <Link 
              to="/upload" 
              className="group relative inline-flex items-center justify-center gap-2 overflow-hidden rounded-lg bg-primary px-8 py-4 font-semibold text-primary-foreground shadow-[0_0_20px_rgba(37,99,235,0.3)] transition-all hover:scale-105 hover:shadow-[0_0_30px_rgba(37,99,235,0.5)]"
            >
              <span>Analyze Resume</span>
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Link>
            
            <a 
              href="https://github.com" 
              target="_blank" 
              rel="noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-border bg-background/50 backdrop-blur-md px-8 py-4 font-semibold text-foreground transition-all hover:bg-muted hover:text-foreground"
            >
              <span>GitHub</span>
            </a>
          </motion.div>
        </motion.div>

        {/* Features Section */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-100px" }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-32 w-full max-w-6xl"
        >
          {featureCards.map((feature, idx) => (
            <motion.div 
              key={idx} 
              variants={itemVariants}
              className="group relative flex flex-col items-start p-8 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md shadow-2xl transition-all hover:bg-white/10 hover:border-white/20 hover:-translate-y-1"
            >
              <div className="mb-5 inline-flex p-3 rounded-xl bg-primary/10 text-primary group-hover:scale-110 group-hover:bg-primary/20 transition-all">
                <feature.icon className="h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold text-foreground mb-3">{feature.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed text-left">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </main>

      {/* --- Footer --- */}
      <footer className="relative z-10 border-t border-white/10 bg-background/50 backdrop-blur-lg">
        <div className="container mx-auto px-6 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Cpu className="h-5 w-5 text-accent" />
            <span className="font-semibold text-foreground tracking-wide">AI Resume Analyzer</span>
          </div>
          <p className="text-sm text-muted-foreground">
            Built for modern SaaS architectures.
          </p>
          <div className="flex gap-4">
            <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Privacy</a>
            <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Terms</a>
          </div>
        </div>
      </footer>
    </div>
  );
};