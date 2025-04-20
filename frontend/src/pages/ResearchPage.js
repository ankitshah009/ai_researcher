import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowPathIcon, 
  CheckCircleIcon, 
  ClockIcon, 
  DocumentArrowDownIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import useApi from '../hooks/useApi';

// Stages of research with icons and colors
const RESEARCH_STAGES = [
  { name: 'Initializing', color: 'primary' },
  { name: 'Creating outline', color: 'primary' },
  { name: 'Gathering literature', color: 'primary' },
  { name: 'Analyzing sources', color: 'primary' },
  { name: 'Drafting content', color: 'secondary' },
  { name: 'Adding citations', color: 'secondary' },
  { name: 'Formatting document', color: 'accent' },
  { name: 'Generating PDF', color: 'accent' },
  { name: 'Complete', color: 'green' }
];

// Message patterns to detect stages
const STAGE_PATTERNS = [
  { pattern: 'initializing', stage: 0 },
  { pattern: 'outline', stage: 1 },
  { pattern: 'gathering literature', stage: 2 },
  { pattern: 'search arxiv', stage: 2 },
  { pattern: 'analyzing', stage: 3 },
  { pattern: 'drafting', stage: 4 },
  { pattern: 'writing', stage: 4 },
  { pattern: 'citation', stage: 5 },
  { pattern: 'formatting', stage: 6 },
  { pattern: 'latex', stage: 6 },
  { pattern: 'generating pdf', stage: 7 },
  { pattern: 'complete', stage: 8 },
  { pattern: 'finished', stage: 8 }
];

// Helper to detect stage from message
const detectStage = (message) => {
  if (!message) return null;
  
  const lowerMessage = message.toLowerCase();
  
  for (const { pattern, stage } of STAGE_PATTERNS) {
    if (lowerMessage.includes(pattern)) {
      return stage;
    }
  }
  
  return null;
};

const ResearchPage = () => {
  const { jobId } = useParams();
  const [status, setStatus] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentStage, setCurrentStage] = useState(0);
  const [outputFile, setOutputFile] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);
  
  const messagesEndRef = useRef(null);
  const { getJobStatus, getDownloadUrl, loading } = useApi();
  
  // Fetch job status
  const fetchStatus = async () => {
    if (!jobId) return;
    
    const result = await getJobStatus(jobId);
    if (result) {
      setStatus(result);
      
      // Add new messages
      if (result.updates && result.updates.length > 0) {
        const newMessages = [...messages];
        
        result.updates.forEach(update => {
          if (update.message) {
            newMessages.push(update.message);
            
            // Check for output file
            if (update.output_file) {
              setOutputFile(update.output_file);
            }
            
            // Detect stage from message
            const detectedStage = detectStage(update.message);
            if (detectedStage !== null) {
              setCurrentStage(Math.max(currentStage, detectedStage));
            }
          }
        });
        
        // Update messages state
        setMessages(newMessages);
      }
    }
  };
  
  // Initialize and set up refresh
  useEffect(() => {
    fetchStatus();
    
    // Set up auto-refresh if job is active
    let interval;
    if (autoRefresh) {
      interval = setInterval(fetchStatus, 3000);
    }
    
    return () => clearInterval(interval);
  }, [jobId, autoRefresh]);
  
  // Scroll to bottom when messages update
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);
  
  // Main render
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <Link to="/" className="text-primary-400 hover:text-primary-300 transition-colors duration-200">
          &larr; Back to Home
        </Link>
        
        <h1 className="text-3xl font-bold mt-4 mb-2">Research Progress</h1>
        <div className="flex items-center space-x-4">
          <div className="text-sm text-slate-400">Job ID: {jobId}</div>
          
          {status && (
            <div className={`flex items-center px-3 py-1 rounded-full text-xs ${
              !status.active && outputFile 
                ? 'bg-green-950/50 text-green-500 border border-green-800/50' 
                : status.active 
                  ? 'bg-primary-950/50 text-primary-500 border border-primary-800/50'
                  : 'bg-red-950/50 text-red-500 border border-red-800/50'
            }`}>
              <span className={`inline-block w-2 h-2 rounded-full mr-2 ${
                !status.active && outputFile 
                  ? 'bg-green-500' 
                  : status.active 
                    ? 'bg-primary-500 animate-pulse'
                    : 'bg-red-500'
              }`}></span>
              {!status.active && outputFile 
                ? 'Complete' 
                : status.active 
                  ? 'Running'
                  : 'Error'}
            </div>
          )}
          
          <button 
            onClick={fetchStatus} 
            disabled={loading}
            className="text-slate-400 hover:text-white transition-colors duration-200"
            title="Refresh Status"
          >
            <ArrowPathIcon className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`text-xs px-2 py-1 rounded border ${
              autoRefresh 
                ? 'border-primary-700 text-primary-400 hover:bg-primary-900/30' 
                : 'border-slate-700 text-slate-400 hover:bg-slate-800'
            } transition-colors duration-200`}
          >
            {autoRefresh ? 'Auto-Refresh On' : 'Auto-Refresh Off'}
          </button>
        </div>
      </div>
      
      {/* Progress Tracking */}
      <div className="card mb-8">
        <h2 className="text-xl font-bold mb-4">Research Progress</h2>
        
        <div className="relative">
          <div className="absolute left-3 inset-y-0 w-0.5 bg-slate-800"></div>
          
          <div className="space-y-4">
            {RESEARCH_STAGES.map((stage, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`flex items-center pl-8 relative ${index > currentStage ? 'opacity-40' : ''}`}
              >
                <div className={`absolute left-0 w-6 h-6 rounded-full flex items-center justify-center ${
                  index < currentStage 
                    ? `bg-${stage.color}-900/50 text-${stage.color}-500 border border-${stage.color}-700/50` 
                    : index === currentStage
                      ? `bg-${stage.color}-900/50 text-${stage.color}-500 border border-${stage.color}-700 animate-pulse` 
                      : 'bg-slate-900/50 text-slate-500 border border-slate-800'
                }`}>
                  {index < currentStage ? (
                    <CheckCircleIcon className="h-4 w-4" />
                  ) : index === currentStage ? (
                    <ClockIcon className="h-4 w-4" />
                  ) : (
                    <span className="h-1.5 w-1.5 rounded-full bg-slate-700"></span>
                  )}
                </div>
                
                <div className="text-sm">
                  {stage.name}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Output File */}
      {outputFile && (
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="card mb-8 border-green-800/30 bg-green-950/20"
        >
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-green-400 mb-2">Research Complete!</h3>
              <p className="text-slate-300">Your research paper has been generated successfully.</p>
            </div>
            
            <a 
              href={getDownloadUrl(outputFile)}
              target="_blank"
              rel="noopener noreferrer"
              className="button-primary bg-green-700 hover:bg-green-600 flex items-center"
            >
              <DocumentArrowDownIcon className="h-5 w-5 mr-2" />
              Download PDF
            </a>
          </div>
        </motion.div>
      )}
      
      {/* Status Messages */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">Status Updates</h2>
          
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${status?.active ? 'bg-primary-500 animate-pulse' : 'bg-slate-500'}`}></div>
            <span className="text-sm text-slate-400">
              {status?.active ? 'Processing' : outputFile ? 'Complete' : 'Inactive'}
            </span>
          </div>
        </div>
        
        <div className="bg-slate-950 rounded-md border border-slate-800 p-4 h-80 overflow-y-auto font-mono text-sm">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-slate-500">
              <div className="text-center">
                <ExclamationTriangleIcon className="h-8 w-8 mx-auto mb-2" />
                <p>No status updates yet</p>
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              {messages.map((message, index) => (
                <div key={index} className="pb-2 border-b border-slate-800/50 last:border-0">
                  {message}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default ResearchPage; 