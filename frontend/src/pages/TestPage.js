import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MagnifyingGlassIcon, DocumentTextIcon } from '@heroicons/react/24/outline';
import useApi from '../hooks/useApi';

const TestPage = () => {
  const [query, setQuery] = useState('');
  const [limit, setLimit] = useState(5);
  const [results, setResults] = useState(null);
  const { testArxivSearch, loading, error } = useApi();
  
  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    const searchResults = await testArxivSearch(query, limit);
    if (searchResults) {
      setResults(searchResults.results);
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">Test arXiv Search</h1>
        <p className="text-slate-400">
          Test the arXiv search functionality used by the research agent
        </p>
      </div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card mb-8"
      >
        <form onSubmit={handleSearch} className="space-y-4">
          <div>
            <label htmlFor="query" className="block text-white font-medium mb-2">
              Search Query
            </label>
            <input
              type="text"
              id="query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., Graph Neural Networks, Transformer Architecture"
              className="input w-full"
              required
            />
          </div>
          
          <div>
            <label htmlFor="limit" className="block text-white font-medium mb-2">
              Result Limit
            </label>
            <input
              type="number"
              id="limit"
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              min="1"
              max="20"
              className="input w-full"
            />
            <p className="mt-1 text-sm text-slate-400">
              Maximum number of results to return (1-20)
            </p>
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="button-primary flex items-center justify-center w-full"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Searching...
              </>
            ) : (
              <>
                <MagnifyingGlassIcon className="h-5 w-5 mr-2" />
                Search arXiv
              </>
            )}
          </button>
        </form>
      </motion.div>
      
      {error && (
        <div className="bg-red-950/30 border border-red-800/50 text-red-500 p-4 rounded-md mb-8">
          {error}
        </div>
      )}
      
      {results && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-6"
        >
          <h2 className="text-2xl font-bold mb-4">Search Results</h2>
          
          {results.length === 0 ? (
            <div className="card text-center py-8">
              <p className="text-slate-400">No results found for your query</p>
            </div>
          ) : (
            <div className="space-y-4">
              {results.map((paper, index) => (
                <motion.div 
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="card bg-slate-900/70 hover:bg-slate-900/90 transition-colors duration-200"
                >
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 pt-1">
                      <DocumentTextIcon className="h-6 w-6 text-primary-500" />
                    </div>
                    
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold mb-2">
                        <a 
                          href={paper.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-primary-400 hover:text-primary-300 transition-colors duration-200"
                        >
                          {paper.title}
                        </a>
                      </h3>
                      
                      <div className="mb-2 text-sm flex flex-wrap gap-2">
                        {paper.authors && paper.authors.map((author, i) => (
                          <span key={i} className="bg-slate-800/70 px-2 py-1 rounded text-slate-300">
                            {author}
                          </span>
                        ))}
                      </div>
                      
                      <div className="text-sm text-slate-400 mb-3">
                        Published: {paper.published || 'Unknown date'}
                      </div>
                      
                      <p className="text-slate-300 text-sm">
                        {paper.summary?.substring(0, 300)}
                        {paper.summary && paper.summary.length > 300 ? '...' : ''}
                      </p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
};

export default TestPage; 