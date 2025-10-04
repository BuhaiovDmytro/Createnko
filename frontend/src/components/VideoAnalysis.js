import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Play, 
  Eye, 
  Calendar,
  Globe,
  Users,
  MessageSquare,
  TrendingUp,
  Info,
  Brain,
  CheckCircle,
  Clock
} from 'lucide-react';

const VideoAnalysis = ({ videoInsights = [], reasoning }) => {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(true);
  const [showReasoning, setShowReasoning] = useState(false);

  const formatDate = (dateString) => {
    if (!dateString) return 'Не вказано';
    try {
      return new Date(dateString).toLocaleDateString('uk-UA');
    } catch {
      return 'Не вказано';
    }
  };

  const formatNumber = (num) => {
    if (!num) return 'Не вказано';
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const handleVideoSelect = (video) => {
    setSelectedVideo(video);
    setIsPlaying(false);
  };

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
  };

  if (!videoInsights || videoInsights.length === 0) {
    return (
      <div className="card bg-gray-50 border-gray-200">
        <div className="text-center text-gray-500 py-8">
          <Eye className="w-12 h-12 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-medium mb-2">Інсайти не знайдено</h3>
          <p className="text-sm">
            Аналіз відео ще не завершено або не знайдено відео для аналізу
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Reasoning Panel */}
      {reasoning && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card bg-blue-50 border-blue-200"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-blue-900 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2" />
              Аналіз та Reasoning
            </h3>
            <button
              onClick={() => setShowReasoning(!showReasoning)}
              className="btn-secondary flex items-center space-x-2"
            >
              <Info className="w-4 h-4" />
              <span>{showReasoning ? 'Приховати' : 'Показати'} деталі</span>
            </button>
          </div>

          <div className="text-blue-800 mb-4">
            <p className="font-medium">{reasoning.analysis_summary}</p>
          </div>

          {showReasoning && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="space-y-4"
            >
              {/* Data Breakdown */}
              <div className="bg-white rounded-lg p-4 border border-blue-200">
                <h4 className="font-semibold text-blue-900 mb-3">Розподіл даних</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-blue-600">Всього оголошень:</p>
                    <p className="font-bold text-blue-900">{reasoning.data_breakdown?.total_ads || 0}</p>
                  </div>
                  <div>
                    <p className="text-blue-600">Відео:</p>
                    <p className="font-bold text-blue-900">{reasoning.data_breakdown?.video_ads || 0}</p>
                  </div>
                  <div>
                    <p className="text-blue-600">Зображення:</p>
                    <p className="font-bold text-blue-900">{reasoning.data_breakdown?.image_ads || 0}</p>
                  </div>
                  <div>
                    <p className="text-blue-600">% відео:</p>
                    <p className="font-bold text-blue-900">{reasoning.data_breakdown?.video_percentage || 0}%</p>
                  </div>
                </div>
              </div>

              {/* Key Findings */}
              {reasoning.key_findings && reasoning.key_findings.length > 0 && (
                <div className="bg-white rounded-lg p-4 border border-blue-200">
                  <h4 className="font-semibold text-blue-900 mb-3">Ключові висновки</h4>
                  <ul className="space-y-2">
                    {reasoning.key_findings.map((finding, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-blue-800">{finding}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Competitive Analysis */}
              {reasoning.competitive_analysis && (
                <div className="bg-white rounded-lg p-4 border border-blue-200">
                  <h4 className="font-semibold text-blue-900 mb-3">Конкурентний аналіз</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-blue-600">Конкурентів:</p>
                      <p className="font-bold text-blue-900">{reasoning.competitive_analysis.total_competitors}</p>
                    </div>
                    <div>
                      <p className="text-blue-600">Інтенсивність:</p>
                      <p className="font-bold text-blue-900">{reasoning.competitive_analysis.competitive_intensity}</p>
                    </div>
                  </div>
                  <div className="mt-3">
                    <p className="text-blue-600 text-sm">Концентрація ринку:</p>
                    <p className="text-blue-800 text-sm">{reasoning.competitive_analysis.market_concentration}</p>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </motion.div>
      )}

      {/* Video Insights Grid */}
      <div className="space-y-8">
        {videoInsights.map((insight, index) => (
          <motion.div
            key={insight.ad_id || index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card"
          >
            {/* Video Header */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <Play className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">
                    {insight.page_name || 'Невідомий бренд'}
                  </h4>
                  <p className="text-sm text-gray-600">
                    {formatDate(insight.analysis_timestamp)} • {insight.model_used}
                  </p>
                </div>
              </div>
              
              {/* Analysis Status */}
              <div className="flex items-center space-x-2">
                <div className="flex items-center space-x-2 text-green-600">
                  <CheckCircle className="w-4 h-4" />
                  <span className="text-sm">Проаналізовано</span>
                </div>
              </div>
            </div>

            {/* Video Player */}
            <div className="relative bg-gray-100 rounded-lg mb-4 aspect-video overflow-hidden">
              {insight.media_url ? (
                <video
                  className="w-full h-full object-cover cursor-pointer"
                  muted={isMuted}
                  controls={true}
                  onClick={() => handleVideoSelect(insight)}
                >
                  <source src={insight.media_url} type="video/mp4" />
                </video>
              ) : (
                <div className="w-full h-full flex items-center justify-center bg-gray-200">
                  <Play className="w-12 h-12 text-gray-400" />
                </div>
              )}
            </div>

            {/* Video Analysis Results */}
            <div className="mt-4 p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200">
              <div className="flex items-center mb-3">
                <Brain className="w-5 h-5 text-green-600 mr-2" />
                <h5 className="font-semibold text-green-900">Аналіз відео</h5>
              </div>
              
              {/* Video Metadata */}
              {insight.video_metadata && (
                <div className="mb-3 text-xs text-green-800">
                  <div className="flex space-x-4">
                    {insight.video_metadata.file_size_mb && (
                      <span>Розмір: {insight.video_metadata.file_size_mb} MB</span>
                    )}
                    {insight.video_metadata.duration_seconds && (
                      <span>Тривалість: {insight.video_metadata.duration_seconds}с</span>
                    )}
                    <span>Модель: {insight.model_used}</span>
                  </div>
                </div>
              )}

              {/* Analysis Content */}
              <div className="bg-white rounded-lg p-3 border border-green-200 max-h-64 overflow-y-auto">
                <pre className="text-xs text-gray-700 whitespace-pre-wrap leading-relaxed">
                  {insight.insights?.raw_analysis || 'Аналіз недоступний'}
                </pre>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Video Player Modal */}
      {selectedVideo && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedVideo(null)}
        >
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Video Player */}
            <div className="relative bg-black aspect-video">
              <video
                className="w-full h-full"
                controls
                autoPlay={isPlaying}
                muted={isMuted}
                src={selectedVideo.media_url}
              >
                Ваш браузер не підтримує відео тег.
              </video>
            </div>

            {/* Video Info */}
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {selectedVideo.page_name || 'Невідомий бренд'}
                  </h3>
                  <p className="text-gray-600 mb-4">
                    {formatDate(selectedVideo.analysis_timestamp)} • {selectedVideo.model_used}
                  </p>
                </div>
                <button
                  onClick={() => setSelectedVideo(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              {/* Video Analysis Results */}
              <div className="mt-6">
                <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      <div className="flex items-center justify-center w-10 h-10 bg-purple-100 rounded-lg mr-3">
                        <Brain className="w-5 h-5 text-purple-600" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          Аналіз відео
                        </h3>
                        <p className="text-sm text-gray-500">
                          Детальні інсайти з Gemini
                        </p>
                      </div>
                    </div>
                    
                    {/* Analysis Status */}
                    <div className="flex items-center space-x-2">
                      <div className="flex items-center space-x-2 text-green-600">
                        <CheckCircle className="w-4 h-4" />
                        <span className="text-sm">Проаналізовано</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    {/* Success Message */}
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-center">
                        <CheckCircle className="w-5 h-5 text-green-600 mr-3" />
                        <p className="text-green-800 text-sm font-medium">
                          Аналіз завершено успішно!
                        </p>
                      </div>
                    </div>

                    {/* Video Metadata */}
                    {selectedVideo.video_metadata && (
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h4 className="font-medium text-blue-900 mb-2">Інформація про відео</h4>
                        <div className="grid grid-cols-2 gap-2 text-sm text-blue-800">
                          {selectedVideo.video_metadata.file_size_mb && (
                            <div>Розмір: {selectedVideo.video_metadata.file_size_mb} MB</div>
                          )}
                          {selectedVideo.video_metadata.duration_seconds && (
                            <div>Тривалість: {selectedVideo.video_metadata.duration_seconds}с</div>
                          )}
                          <div>Модель: {selectedVideo.model_used}</div>
                          <div>Дата: {new Date(selectedVideo.analysis_timestamp).toLocaleDateString()}</div>
                        </div>
                      </div>
                    )}

                    {/* Analysis Content */}
                    <div className="bg-gray-50 rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-3 flex items-center">
                        <TrendingUp className="w-4 h-4 mr-2" />
                        Детальний аналіз відео
                      </h4>
                      <div className="bg-white rounded-lg p-4 border max-h-96 overflow-y-auto">
                        <pre className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
                          {selectedVideo.insights?.raw_analysis || 'Аналіз недоступний'}
                        </pre>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
};

export default VideoAnalysis;