import { motion } from "framer-motion";

import { useAnalyzeResume } from "@/hooks/useAnalyzeResume";

import { ResumeUploadForm } from "@/components/upload/ResumeUploadForm";

import { ResumeDashboard } from "@/components/dashboard/ResumeDashboard";

import { AILoadingState } from "@/components/upload/AILoadingState";

export const AnalyzerPage = () => {

    const {

        mutate: analyze,

        isPending,

        data,

    } = useAnalyzeResume();

    if (isPending) {

        return (

            <div className="min-h-screen flex items-center justify-center">

                <AILoadingState />

            </div>

        );

    }

    return (

        <motion.div

            initial={{ opacity: 0 }}

            animate={{ opacity: 1 }}

            className="min-h-screen bg-background"

        >

            {

                !data ?

                (

                    <ResumeUploadForm

                        onSubmit={analyze}

                    />

                )

                :

                (

                    <ResumeDashboard

                        data={data}

                    />

                )

            }

        </motion.div>

    );

};