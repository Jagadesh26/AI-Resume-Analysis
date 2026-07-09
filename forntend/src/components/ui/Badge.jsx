import React from "react";

const Badge = ({ text, variant = "gray" }) => {
  const variants = {
    gray: "bg-gray-100 text-gray-700",
    green: "bg-green-100 text-green-700", // Good for detected skills
    red: "bg-red-100 text-red-700", // Good for missing skills
    blue: "bg-blue-100 text-blue-700",
  };

  return (
    <span
      className={`px-3 py-1 rounded-full text-sm font-medium ${variants[variant]}`}
    >
      {text}
    </span>
  );
};

export default Badge;
