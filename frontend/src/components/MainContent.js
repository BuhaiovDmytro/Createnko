import React, { useState } from 'react';
import { motion } from 'framer-motion';
import ProductInputForm from './ProductInputForm';
import VideoGenerator from './VideoGenerator';
import LoadingSpinner from './LoadingSpinner';
import CreditStatus from './CreditStatus';
import { apiService } from '../services/apiService';

const MainContent = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState(null);
  const [error, setError] = useState(null);
  const [creditInfo, setCreditInfo] = useState(null);

  const handleGenerateVideo = async (formData) => {
    setIsGenerating(true);
    setError(null);
    setGeneratedVideo(null);
    setCreditInfo(null);

    try {
      const result = await apiService.generateVideo(formData);
      setGeneratedVideo(result);
    } catch (err) {
      setError(err.message || 'Помилка при генерації відео');
      
      // Extract credit information if available
      if (err.creditInfo) {
        setCreditInfo(err.creditInfo);
      }
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    setGeneratedVideo(null);
    setError(null);
    setCreditInfo(null);
  };

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center mb-12"
      >
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          Створіть відео на основі трендів Facebook Ads
        </h2>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Введіть посилання на ваш продукт та отримайте готове відео, 
          створене на основі актуальних трендів з Facebook Ads Library
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Форма введення */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <ProductInputForm 
            onSubmit={handleGenerateVideo}
            isGenerating={isGenerating}
            onReset={handleReset}
          />
        </motion.div>

        {/* Результат генерації */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          {isGenerating && <LoadingSpinner />}
          
          {error && (
            <div className="space-y-4">
              <div className="card bg-red-50 border-red-200">
                <div className="text-red-800">
                  <h3 className="font-semibold mb-2">Помилка генерації</h3>
                  <p>{error}</p>
                </div>
              </div>
              
              {/* Display credit information if available */}
              <CreditStatus 
                creditInfo={creditInfo} 
                errorType={error.includes('кредити') ? 'credit_exhausted' : 
                          error.includes('ліміт') ? 'rate_limit' : null}
              />
            </div>
          )}
          
          {generatedVideo && (
            <VideoGenerator 
              videoData={generatedVideo}
              onReset={handleReset}
            />
          )}
          
          {!isGenerating && !error && !generatedVideo && (
            <div className="card bg-gray-50 border-gray-200">
              <div className="text-center text-gray-500">
                <div className="w-16 h-16 mx-auto mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="font-medium mb-2">Відео буде згенеровано тут</h3>
                <p className="text-sm">
                  Введіть дані про ваш продукт та натисніть "Генерувати відео"
                </p>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </main>
  );
};

export default MainContent;
