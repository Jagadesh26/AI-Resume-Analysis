import { AnalysisOverview } from "./AnalysisOverview";
import { SkillsAnalysis } from "./SkillsAnalysis";
import { Recommendations } from "./Recommendations";
import { JobRecommendation } from "./JobRecommendation";

import type { ResumeAnalysisResponse } from "@/types";

interface ResumeDashboardProps {
  data: ResumeAnalysisResponse;
}

export default function ResumeDashboard({
  data,
}: ResumeDashboardProps) {
  const analysis = data.analysis;

  return (
    <main className="min-h-screen bg-gray-900 py-10">
      <div className="mx-auto max-w-7xl space-y-8 px-4 sm:px-6 lg:px-8">

        {/* ============================
            Dashboard Header
        ============================ */}

        <div className="rounded-3xl border border-orange-500/20 bg-gray-800 p-8 shadow-xl">

          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">

            <div>

              <h1 className="text-4xl font-bold text-white">

                AI Resume Analysis

              </h1>

              <p className="mt-2 text-gray-400">

                ATS Analysis • Resume Review • Recruiter Insights • Job Recommendations

              </p>

            </div>

            <div className="grid grid-cols-2 gap-4">

              <div className="rounded-2xl bg-gray-900 px-5 py-4">

                <p className="text-xs uppercase tracking-wider text-gray-500">

                  Provider

                </p>

                <p className="mt-2 font-semibold text-orange-400">

                  {data.provider}

                </p>

              </div>

              <div className="rounded-2xl bg-gray-900 px-5 py-4">

                <p className="text-xs uppercase tracking-wider text-gray-500">

                  Model

                </p>

                <p className="mt-2 font-semibold text-orange-400">

                  {data.model}

                </p>

              </div>

            </div>

          </div>

        </div>

        {/* ================================= */}
        {/* Overview */}
        {/* ================================= */}

        <AnalysisOverview analysis={analysis} />

        {/* ================================= */}
        {/* Skills */}
        {/* ================================= */}

        <SkillsAnalysis analysis={analysis} />

        {/* ================================= */}
        {/* Recommendations */}
        {/* ================================= */}

        <Recommendations analysis={analysis} />

        {/* ================================= */}
        {/* Jobs */}
        {/* ================================= */}

        <JobRecommendation
          jobs={analysis.recommended_jobs ?? []}
        />

      </div>
    </main>
  );
}