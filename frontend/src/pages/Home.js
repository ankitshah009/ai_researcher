import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  BeakerIcon, 
  BoltIcon, 
  DocumentTextIcon, 
  RocketLaunchIcon 
} from '@heroicons/react/24/outline';
import useApi from '../hooks/useApi';

const Home = () => {
  const [topic, setTopic] = useState('');
  const [filename, setFilename] = useState('research_paper.pdf');
  const [apiStatus, setApiStatus] = useState(null);
  
  const navigate = useNavigate();
  const { startResearchJob, checkHealth, loading } = useApi();
  
  // Check API health on component mount
  useEffect(() => {
    const checkApiHealth = async () => {
      const status = await checkHealth();
      setApiStatus(status);
    };
    
    checkApiHealth();
  }, [checkHealth]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!topic.trim()) return;
    
    const result = await startResearchJob(topic, filename);
    if (result && result.job_id) {
      navigate(`/research/${result.job_id}`);
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-primary-400 to-secondary-400 text-transparent bg-clip-text">
            AI Research Agent
          </h1>
          <p className="text-xl text-slate-300 mb-8">
            Generate comprehensive research papers on any topic using AI
          </p>
        </motion.div>
        
        {apiStatus && (
          <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
            apiStatus.status === 'ok' 
              ? 'bg-green-950/50 text-green-500 border border-green-800/50' 
              : 'bg-red-950/50 text-red-500 border border-red-800/50'
          }`}>
            <span className={`inline-block w-2 h-2 rounded-full mr-2 ${
              apiStatus.status === 'ok' ? 'bg-green-500' : 'bg-red-500'
            }`}></span>
            {apiStatus.status === 'ok' ? 'API Ready' : 'API Offline'}
          </div>
        )}
      </div>
      
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="card mb-12"
      >
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label htmlFor="topic" className="block text-white font-medium mb-2">
              Research Topic
            </label>
            <textarea
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter a research topic (e.g., 'The impact of quantum computing on modern cryptography')"
              rows={3}
              className="input w-full"
              required
            />
          </div>
          
          <div className="mb-6">
            <label htmlFor="filename" className="block text-white font-medium mb-2">
              Output Filename
            </label>
            <input
              type="text"
              id="filename"
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              className="input w-full"
            />
            <p className="mt-1 text-sm text-slate-400">
              The filename for the generated PDF (must end with .pdf)
            </p>
          </div>
          
          <button
            type="submit"
            disabled={loading || !apiStatus || apiStatus.status !== 'ok'}
            className="button-primary w-full flex items-center justify-center"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </>
            ) : (
              <>
                <RocketLaunchIcon className="h-5 w-5 mr-2" />
                Generate Research Paper
              </>
            )}
          </button>
        </form>
      </motion.div>
      
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <h2 className="text-2xl font-bold mb-6">How It Works</h2>
        
        <div className="grid md:grid-cols-3 gap-6">
          <div className="card bg-slate-900/50 hover:bg-slate-900/70 transition-colors duration-200">
            <div className="flex items-center justify-center mb-4">
              <div className="h-12 w-12 rounded-full bg-primary-900/50 flex items-center justify-center">
                <BeakerIcon className="h-6 w-6 text-primary-400" />
              </div>
            </div>
            <h3 className="text-lg font-semibold text-center mb-2">Enter a Topic</h3>
            <p className="text-slate-400 text-center">
              Specify any research topic for the AI to explore and analyze
            </p>
          </div>
          
          <div className="card bg-slate-900/50 hover:bg-slate-900/70 transition-colors duration-200">
            <div className="flex items-center justify-center mb-4">
              <div className="h-12 w-12 rounded-full bg-primary-900/50 flex items-center justify-center">
                <BoltIcon className="h-6 w-6 text-primary-400" />
              </div>
            </div>
            <h3 className="text-lg font-semibold text-center mb-2">AI Research</h3>
            <p className="text-slate-400 text-center">
              The AI conducts thorough research, analyzing recent papers and sources
            </p>
          </div>
          
          <div className="card bg-slate-900/50 hover:bg-slate-900/70 transition-colors duration-200">
            <div className="flex items-center justify-center mb-4">
              <div className="h-12 w-12 rounded-full bg-primary-900/50 flex items-center justify-center">
                <DocumentTextIcon className="h-6 w-6 text-primary-400" />
              </div>
            </div>
            <h3 className="text-lg font-semibold text-center mb-2">Get Results</h3>
            <p className="text-slate-400 text-center">
              Download a complete, citation-rich academic paper on your topic
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Home; 