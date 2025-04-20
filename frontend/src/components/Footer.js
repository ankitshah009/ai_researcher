import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-slate-900/80 backdrop-blur-sm border-t border-slate-800 py-6 mt-auto">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="text-slate-400 text-sm">
            &copy; {new Date().getFullYear()} AI Research Agent. All rights reserved.
          </div>
          
          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            <a 
              href="#" 
              className="text-slate-400 hover:text-white transition-colors duration-200 text-sm"
            >
              Privacy Policy
            </a>
            <a 
              href="#" 
              className="text-slate-400 hover:text-white transition-colors duration-200 text-sm"
            >
              Terms of Service
            </a>
            <a 
              href="https://github.com/yourusername/ai-research-agent" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-slate-400 hover:text-white transition-colors duration-200 text-sm"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 