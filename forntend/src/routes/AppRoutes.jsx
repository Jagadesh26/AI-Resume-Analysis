import React from "react";
import { Routes, Route } from "react-router-dom";
import LandingPage from "../pages/Landing";
import ResultsPage from "../pages/Results"; // Now Imported!

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/results" element={<ResultsPage />} />
      <Route
        path="*"
        element={
          <div className="p-10 text-center text-2xl">404 - Page Not Found</div>
        }
      />
    </Routes>
  );
};

export default AppRoutes;
