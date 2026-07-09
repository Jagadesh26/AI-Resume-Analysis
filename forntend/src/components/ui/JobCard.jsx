import React from "react";
import Card from "./Card";
import Badge from "./Badge";
import Button from "./Button";

const JobCard = ({ job }) => {
  return (
    <Card className="hover:shadow-md transition-shadow border-l-4 border-l-blue-500">
      <div className="flex flex-col md:flex-row justify-between items-start gap-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-900">{job.job_title}</h3>
          <p className="text-blue-600 font-semibold">{job.company}</p>

          <div className="flex flex-wrap gap-4 mt-2 text-sm text-gray-500">
            <span className="flex items-center gap-1">
              📍 {job.location || "Remote"}
            </span>
            <span className="flex items-center gap-1">
              💼 {job.employment_type || "Full-time"}
            </span>
            <span className="text-green-600 font-bold">
              Match: {job.match_score}%
            </span>
          </div>

          <div className="mt-4 flex flex-wrap gap-1">
            {job.skills?.slice(0, 5).map((skill, i) => (
              <Badge key={i} text={skill} variant="gray" />
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-2 w-full md:w-auto">
          <Button
            onClick={() => window.open(job.apply_url, "_blank")}
            className="whitespace-nowrap"
          >
            Apply Now
          </Button>
          <p className="text-xs text-gray-400 text-center">
            Source: {job.source}
          </p>
        </div>
      </div>
    </Card>
  );
};

export default JobCard;
