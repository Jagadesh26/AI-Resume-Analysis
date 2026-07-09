export const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-500";
    if (score >= 80) return "text-orange-500";
    if (score >= 70) return "text-amber-500";
    return "text-red-500";
};

export const getProgressColor = (score: number) => {
    if (score >= 90) return "bg-green-500";
    if (score >= 80) return "bg-orange-500";
    if (score >= 70) return "bg-amber-500";
    return "bg-red-500";
};

export const getInterviewBadge = (value: string) => {
    switch (value.toLowerCase()) {
        case "high":
            return "bg-green-500/20 text-green-400";
        case "medium":
            return "bg-amber-500/20 text-amber-400";
        default:
            return "bg-red-500/20 text-red-400";
    }
};