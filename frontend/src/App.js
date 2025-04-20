import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';

// Pages
import Home from './pages/Home';
import ResearchPage from './pages/ResearchPage';
import TestPage from './pages/TestPage';

// Components
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/research/:jobId" element={<ResearchPage />} />
            <Route path="/test" element={<TestPage />} />
          </Routes>
        </motion.div>
      </main>
      
      <Footer />
    </div>
  );
}

export default App; 