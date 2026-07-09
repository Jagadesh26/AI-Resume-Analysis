import { motion } from "framer-motion";
import {
  Award,
  CheckCircle2,
  AlertTriangle,
  FileText,
} from "lucide-react";

import type { ResumeAnalysis } from "@/types";

interface AnalysisOverviewProps {
  analysis: ResumeAnalysis;
}

export function AnalysisOverview({
  analysis,
}: AnalysisOverviewProps) {

  const score = analysis.overall_score?.score ?? 0;

  const grade = analysis.overall_score?.grade ?? "-";

  const reason = analysis.overall_score?.reason ?? "";

  const interview =
    analysis.recruiter_feedback?.interview_probability ?? "Unknown";

  const interviewColor = (() => {
    switch (interview.toLowerCase()) {
      case "high":
        return "bg-green-500/20 text-green-400 border-green-500/30";

      case "medium":
        return "bg-amber-500/20 text-amber-400 border-amber-500/30";

      default:
        return "bg-red-500/20 text-red-400 border-red-500/30";
    }
  })();

  const radius = 70;

  const circumference = 2 * Math.PI * radius;

  const progress = circumference - (score / 100) * circumference;

  return (

    <section className="space-y-8">

      {/* ================================================= */}

      {/* ATS Score + Summary */}

      {/* ================================================= */}

      <div className="grid gap-8 lg:grid-cols-3">

        {/* ATS */}

        <motion.div

          initial={{ opacity: 0, y: 20 }}

          animate={{ opacity: 1, y: 0 }}

          className="rounded-3xl border border-orange-500/20 bg-gray-800 p-8"

        >

          <div className="flex items-center gap-3 mb-6">

            <Award className="text-orange-500" />

            <h2 className="text-xl font-semibold text-white">

              ATS Score

            </h2>

          </div>

          <div className="flex justify-center">

            <svg
              width="180"
              height="180"
            >

              <circle
                cx="90"
                cy="90"
                r={radius}
                stroke="#374151"
                strokeWidth="10"
                fill="transparent"
              />

              <motion.circle
                cx="90"
                cy="90"
                r={radius}
                stroke="#F97316"
                strokeWidth="10"
                fill="transparent"
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={progress}
                initial={{
                  strokeDashoffset: circumference,
                }}
                animate={{
                  strokeDashoffset: progress,
                }}
                transition={{
                  duration: 1.4,
                }}
                transform="rotate(-90 90 90)"
              />

              <text
                x="90"
                y="85"
                textAnchor="middle"
                className="fill-white text-3xl font-bold"
              >
                {score}
              </text>

              <text
                x="90"
                y="108"
                textAnchor="middle"
                className="fill-orange-400 text-sm"
              >
                {grade}
              </text>

            </svg>

          </div>

          <p className="mt-6 text-center text-gray-400 leading-7">

            {reason}

          </p>

        </motion.div>

        {/* Summary */}

        <motion.div

          initial={{ opacity: 0 }}

          animate={{ opacity: 1 }}

          className="lg:col-span-2 rounded-3xl border border-gray-700 bg-gray-800 p-8"

        >

          <div className="flex items-center gap-3 mb-6">

            <FileText className="text-orange-500" />

            <h2 className="text-xl font-semibold text-white">

              Professional Summary

            </h2>

          </div>

          <p className="leading-8 text-gray-300">

            {analysis.summary}

          </p>

          <div className="mt-8">

            <span
              className={`rounded-full border px-4 py-2 text-sm font-semibold ${interviewColor}`}
            >

              Interview Probability : {interview}

            </span>

          </div>

        </motion.div>

      </div>

      {/* ================================================= */}

      {/* Strengths + Weaknesses */}

      {/* ================================================= */}

      <div className="grid gap-8 lg:grid-cols-2">

        {/* Strengths */}

        <motion.div

          initial={{ opacity: 0 }}

          whileInView={{ opacity: 1 }}

          viewport={{ once: true }}

          className="rounded-3xl border border-green-500/20 bg-gray-800 p-8"

        >

          <div className="flex items-center gap-3 mb-6">

            <CheckCircle2 className="text-green-400" />

            <h2 className="text-xl font-semibold text-white">

              Strengths

            </h2>

          </div>

          <div className="space-y-4">

            {(analysis.strengths ?? []).length === 0 ? (

              <div className="rounded-xl bg-gray-900 p-5 text-gray-400">

                No strengths detected.

              </div>

            ) : (

              analysis.strengths.map((item, index) => (

                <div

                  key={index}

                  className="rounded-xl bg-gray-900 border border-gray-700 p-5"

                >

                  <p className="leading-7 text-gray-300">

                    {item}

                  </p>

                </div>

              ))

            )}

          </div>

        </motion.div>

        {/* Weaknesses */}

        <motion.div

          initial={{ opacity: 0 }}

          whileInView={{ opacity: 1 }}

          viewport={{ once: true }}

          className="rounded-3xl border border-red-500/20 bg-gray-800 p-8"

        >

          <div className="flex items-center gap-3 mb-6">

            <AlertTriangle className="text-red-400" />

            <h2 className="text-xl font-semibold text-white">

              Areas for Improvement

            </h2>

          </div>

          <div className="space-y-4">

            {(analysis.weaknesses ?? []).length === 0 ? (

              <div className="rounded-xl bg-gray-900 p-5 text-gray-400">

                No issues detected.

              </div>

            ) : (

              analysis.weaknesses.map((item, index) => (

                <div

                  key={index}

                  className="rounded-xl bg-gray-900 border border-gray-700 p-5"

                >

                  <p className="leading-7 text-gray-300">

                    {item}

                  </p>

                </div>

              ))

            )}

          </div>

        </motion.div>

      </div>

    </section>

  );

}