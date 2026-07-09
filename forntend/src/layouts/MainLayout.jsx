import React from "react";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";

const MainLayout = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />

      {/* The main content area takes up the remaining height so the footer is pushed down */}
      <main className="flex-grow">{children}</main>

      <Footer />
    </div>
  );
};

export default MainLayout;
