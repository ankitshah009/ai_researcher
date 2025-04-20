import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import StatusUpdates from './StatusUpdates';
import { Box, Typography, Button, Container, Paper } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

const ResearchPage = () => {
  const { jobId } = useParams();
  const { getJobStatus, getDownloadUrl, loading, error } = useApi();
  const [status, setStatus] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [pdfFilename, setPdfFilename] = useState('research_paper.pdf');
  const [complete, setComplete] = useState(false);

  useEffect(() => {
    if (!jobId) return;

    const fetchStatus = async () => {
      const data = await getJobStatus(jobId);
      if (data) {
        setStatus(data);
        
        // Process updates array to find completed status
        if (data.updates && data.updates.length > 0) {
          // Look for completion message in updates
          const completedUpdate = data.updates.find(update => 
            update.status === 'completed' && update.output_file
          );
          
          if (completedUpdate) {
            setComplete(true);
            setPdfFilename(completedUpdate.output_file);
            setPdfUrl(getDownloadUrl(completedUpdate.output_file));
          }
        }
      }
    };

    fetchStatus();
    
    // Set up polling for status updates if not complete
    const interval = setInterval(() => {
      if (!complete) {
        fetchStatus();
      } else {
        clearInterval(interval);
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [jobId, getJobStatus, getDownloadUrl, complete]);

  const handleDownload = () => {
    if (pdfUrl) {
      // Create an anchor element and trigger download
      const link = document.createElement('a');
      link.href = pdfUrl;
      link.download = pdfFilename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  if (error) {
    return (
      <Box sx={{ mt: 4, p: 2 }}>
        <Typography color="error" variant="h6">Error: {error}</Typography>
      </Box>
    );
  }

  return (
    <Container>
      {complete ? (
        <Box textAlign="center" mt={4}>
          <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
            <Typography variant="h4" color="primary" gutterBottom>
              Research Complete!
            </Typography>
            <Typography variant="body1" paragraph>
              Your research paper has been generated successfully.
            </Typography>
            <Button 
              variant="contained" 
              color="primary" 
              startIcon={<DownloadIcon />}
              onClick={handleDownload}
              sx={{ mt: 2 }}
            >
              Download PDF
            </Button>
          </Paper>
        </Box>
      ) : (
        <Box textAlign="center" mt={4}>
          <Typography variant="h4" color="primary" gutterBottom>
            Generating Research...
          </Typography>
          <Typography variant="body1" paragraph>
            Please wait while we process your request.
          </Typography>
        </Box>
      )}

      <Box mt={4}>
        <StatusUpdates status={status} complete={complete} />
      </Box>

      {complete && pdfUrl && (
        <Box mt={4}>
          <Typography variant="h5" gutterBottom>
            Generated PDF
          </Typography>
          <Paper elevation={2} sx={{ 
            p: 2, 
            minHeight: '400px',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
          }}>
            <iframe 
              src={pdfUrl} 
              title="Research PDF"
              width="100%" 
              height="600px"
              style={{ border: 'none' }}
            />
          </Paper>
        </Box>
      )}
    </Container>
  );
};

export default ResearchPage; 