import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRightIcon } from '@heroicons/react/24/outline';
import useApi from '../hooks/useApi';

function Home() {
    const [topic, setTopic] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const { startResearchJob, error } = useApi();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!topic.trim()) return;
        
        setIsSubmitting(true);
        try {
            const result = await startResearchJob(topic);
            if (result && result.job_id) {
                navigate(`/research/${result.job_id}`);
            }
        } catch (err) {
            console.error("Failed to start research:", err);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="container mx-auto max-w-5xl px-4 py-12">
            <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mb-16"
            >
                <h1 className="text-5xl font-bold mb-6 bg-gradient-to-br from-white to-slate-400 bg-clip-text text-transparent">
                    AI Research Agent
                </h1>
                <p className="text-xl text-slate-300 max-w-3xl mx-auto">
                    Generate comprehensive, well-structured research papers on any topic using the power of Google's Agent Development Kit (ADK).
                </p>
            </motion.div>

            <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="card max-w-3xl mx-auto"
            >
                <h2 className="text-2xl font-bold mb-6">Start Your Research</h2>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="topic" className="block text-sm font-medium text-slate-300 mb-2">
                            Research Topic
                        </label>
                        <input
                            type="text"
                            id="topic"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            className="w-full p-3 bg-slate-800 border border-slate-700 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="Enter your research topic (e.g., 'Recent advancements in quantum computing')"
                            disabled={isSubmitting}
                        />
                    </div>

                    {error && (
                        <div className="p-3 bg-red-900/30 border border-red-800 rounded-md text-red-400 text-sm">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={!topic.trim() || isSubmitting}
                        className={`button-primary w-full py-3 flex items-center justify-center ${
                            !topic.trim() || isSubmitting ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                    >
                        {isSubmitting ? (
                            <>
                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Processing...
                            </>
                        ) : (
                            <>
                                Begin Research <ArrowRightIcon className="ml-2 h-5 w-5" />
                            </>
                        )}
                    </button>
                </form>
            </motion.div>

            <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="mt-12 max-w-4xl mx-auto"
            >
                <h3 className="text-xl font-bold mb-4 text-center">How It Works</h3>
                <div className="grid md:grid-cols-3 gap-6">
                    {[
                        {
                            title: "Gather Information",
                            description: "Our agents search academic sources like arXiv and Semantic Scholar to find relevant papers and research."
                        },
                        {
                            title: "Analyze & Draft",
                            description: "The information is analyzed, structured, and drafted into a cohesive research paper with proper citations."
                        },
                        {
                            title: "Generate PDF",
                            description: "A beautifully formatted PDF is created with academic styling, ready for download and use."
                        }
                    ].map((step, i) => (
                        <motion.div 
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.5 + (i * 0.1) }}
                            className="card"
                        >
                            <div className="text-primary-500 text-lg font-bold mb-2">{`Step ${i+1}`}</div>
                            <h4 className="text-lg font-semibold mb-2">{step.title}</h4>
                            <p className="text-slate-400">{step.description}</p>
                        </motion.div>
                    ))}
                </div>
            </motion.div>
        </div>
    );
}

export default Home;