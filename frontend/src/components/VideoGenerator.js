import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Play, 
  Copy, 
  Download, 
  Share2, 
  TrendingUp, 
  BarChart3, 
  Target,
  CheckCircle,
  Clock,
  Users,
  Eye
} from 'lucide-react';
import toast from 'react-hot-toast';
import VideoAnalysis from './VideoAnalysis';

const VideoGenerator = ({ videoData, onReset }) => {
  const [activeTab, setActiveTab] = useState('description');
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      toast.success('Скопійовано в буфер обміну!');
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error('Помилка копіювання');
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'Недавно';
    return new Date(timestamp).toLocaleString('uk-UA');
  };

  const tabs = [
    { id: 'description', label: 'Опис відео', icon: Play },
    { id: 'videos', label: 'Відео конкурентів', icon: Eye },
    { id: 'trends', label: 'Аналіз трендів', icon: TrendingUp },
    { id: 'recommendations', label: 'Рекомендації', icon: Target },
    { id: 'technical', label: 'Технічні деталі', icon: BarChart3 }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Заголовок результату */}
      <div className="card bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                Відео успішно згенеровано!
              </h3>
              <p className="text-sm text-gray-600">
                Генератор: {videoData.analysis_metadata?.generator_type?.toUpperCase() || 'VEO'}
              </p>
            </div>
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={() => copyToClipboard(videoData.video_description)}
              className="btn-secondary flex items-center space-x-2"
            >
              <Copy className="w-4 h-4" />
              <span>Копіювати</span>
            </button>
            
            <button
              onClick={onReset}
              className="btn-secondary"
            >
              Новий запит
            </button>
          </div>
        </div>
      </div>

      {/* Статистика аналізу */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-center space-x-2">
            <Users className="w-5 h-5 text-blue-600" />
            <div>
              <p className="text-sm text-blue-600 font-medium">Бренди</p>
              <p className="text-lg font-bold text-blue-800">
                {videoData.analysis_metadata?.brands_analyzed?.length || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card bg-green-50 border-green-200">
          <div className="flex items-center space-x-2">
            <Eye className="w-5 h-5 text-green-600" />
            <div>
              <p className="text-sm text-green-600 font-medium">Оголошення</p>
              <p className="text-lg font-bold text-green-800">
                {videoData.analysis_metadata?.ads_analyzed || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card bg-purple-50 border-purple-200">
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-purple-600" />
            <div>
              <p className="text-sm text-purple-600 font-medium">Платформи</p>
              <p className="text-lg font-bold text-purple-800">
                {videoData.analysis_metadata?.platform_ids_found || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card bg-orange-50 border-orange-200">
          <div className="flex items-center space-x-2">
            <Clock className="w-5 h-5 text-orange-600" />
            <div>
              <p className="text-sm text-orange-600 font-medium">Час</p>
              <p className="text-lg font-bold text-orange-800">
                {formatTimestamp(videoData.analysis_metadata?.analysis_timestamp)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Таби з контентом */}
      <div className="card">
        <div className="border-b border-gray-200 mb-6">
          <nav className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Контент табів */}
        <div className="min-h-[400px]">
          {activeTab === 'description' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* Main Description */}
              <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h4 className="font-semibold text-gray-900 mb-3">Основний опис для генератора відео:</h4>
                <div className="bg-white rounded-lg p-4 border border-gray-200">
                  <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                    {videoData.video_description}
                  </p>
                </div>
                <div className="mt-3 flex justify-end">
                  <button
                    onClick={() => copyToClipboard(videoData.video_description)}
                    className="btn-secondary flex items-center space-x-2"
                  >
                    <Copy className="w-4 h-4" />
                    <span>Копіювати основний опис</span>
                  </button>
                </div>
              </div>

              {/* Variations */}
              {videoData.variations && videoData.variations.length > 0 && (
                <div className="space-y-4">
                  <h4 className="text-lg font-semibold text-gray-900 flex items-center">
                    <Play className="w-5 h-5 mr-2 text-blue-600" />
                    Альтернативні варіанти промптів
                  </h4>
                  
                  {videoData.variations.map((variation, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 border border-blue-200"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <h5 className="font-semibold text-blue-900">
                          Варіант {index + 1}: {
                            index === 0 ? 'Емоційний фокус' :
                            index === 1 ? 'Технічний фокус' :
                            'Конкурентна диференціація'
                          }
                        </h5>
                        <button
                          onClick={() => copyToClipboard(variation)}
                          className="btn-secondary flex items-center space-x-2 text-sm"
                        >
                          <Copy className="w-3 h-3" />
                          <span>Копіювати</span>
                        </button>
                      </div>
                      <div className="bg-white rounded-lg p-4 border border-blue-200">
                        <p className="text-gray-800 leading-relaxed whitespace-pre-wrap text-sm">
                          {variation}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'videos' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <VideoAnalysis 
                videoInsights={videoData.video_insights || []}
                reasoning={videoData.trend_analysis?.reasoning}
              />
            </motion.div>
          )}

          {activeTab === 'trends' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* Reasoning Section */}
              {videoData.trend_analysis?.reasoning && (
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 border border-blue-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2 text-blue-600" />
                    Детальний аналіз та Reasoning
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Analysis Summary */}
                    <div className="bg-white rounded-lg p-4 border border-blue-200">
                      <h4 className="font-semibold text-blue-900 mb-3">Підсумок аналізу</h4>
                      <p className="text-blue-800 text-sm">
                        {videoData.trend_analysis.reasoning.analysis_summary}
                      </p>
                    </div>

                    {/* Data Breakdown */}
                    <div className="bg-white rounded-lg p-4 border border-blue-200">
                      <h4 className="font-semibold text-blue-900 mb-3">Розподіл даних</h4>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-blue-600">Всього:</span>
                          <span className="font-bold text-blue-900 ml-2">
                            {videoData.trend_analysis.reasoning.data_breakdown?.total_ads || 0}
                          </span>
                        </div>
                        <div>
                          <span className="text-blue-600">Відео:</span>
                          <span className="font-bold text-blue-900 ml-2">
                            {videoData.trend_analysis.reasoning.data_breakdown?.video_ads || 0}
                          </span>
                        </div>
                        <div>
                          <span className="text-blue-600">Зображення:</span>
                          <span className="font-bold text-blue-900 ml-2">
                            {videoData.trend_analysis.reasoning.data_breakdown?.image_ads || 0}
                          </span>
                        </div>
                        <div>
                          <span className="text-blue-600">% відео:</span>
                          <span className="font-bold text-blue-900 ml-2">
                            {videoData.trend_analysis.reasoning.data_breakdown?.video_percentage || 0}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Key Findings */}
                  {videoData.trend_analysis.reasoning.key_findings && (
                    <div className="mt-6 bg-white rounded-lg p-4 border border-blue-200">
                      <h4 className="font-semibold text-blue-900 mb-3">Ключові висновки</h4>
                      <ul className="space-y-2">
                        {videoData.trend_analysis.reasoning.key_findings.map((finding, index) => (
                          <li key={index} className="flex items-start space-x-2">
                            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                            <span className="text-blue-800 text-sm">{finding}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Competitive Analysis */}
                  {videoData.trend_analysis.reasoning.competitive_analysis && (
                    <div className="mt-6 bg-white rounded-lg p-4 border border-blue-200">
                      <h4 className="font-semibold text-blue-900 mb-3">Конкурентний аналіз</h4>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <span className="text-blue-600">Конкурентів:</span>
                          <span className="font-bold text-blue-900 ml-2">
                            {videoData.trend_analysis.reasoning.competitive_analysis.total_competitors}
                          </span>
                        </div>
                        <div>
                          <span className="text-blue-600">Інтенсивність:</span>
                          <span className="font-bold text-blue-900 ml-2">
                            {videoData.trend_analysis.reasoning.competitive_analysis.competitive_intensity}
                          </span>
                        </div>
                        <div className="md:col-span-1">
                          <span className="text-blue-600">Концентрація:</span>
                          <span className="text-blue-800 text-xs block mt-1">
                            {videoData.trend_analysis.reasoning.competitive_analysis.market_concentration}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Traditional Trends */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Контентні тренди */}
                <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                  <h4 className="font-semibold text-blue-900 mb-3">Контентні тренди</h4>
                  <div className="space-y-2">
                    {videoData.trend_analysis?.content_trends?.common_themes?.slice(0, 5).map((theme, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                        <span className="text-sm text-blue-800">{theme}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Візуальні тренди */}
                <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                  <h4 className="font-semibold text-green-900 mb-3">Візуальні тренди</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-green-800">Відео контент:</span>
                      <span className="font-medium text-green-900">
                        {videoData.trend_analysis?.video_trends?.video_count || 0}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-green-800">Зображення:</span>
                      <span className="font-medium text-green-900">
                        {videoData.trend_analysis?.visual_trends?.image_count || 0}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Повідомлення */}
                <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                  <h4 className="font-semibold text-purple-900 mb-3">Повідомлення</h4>
                  <div className="space-y-2">
                    {videoData.trend_analysis?.messaging_trends?.messaging_strategies?.slice(0, 3).map((strategy, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                        <span className="text-sm text-purple-800">{strategy}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Формати */}
                <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
                  <h4 className="font-semibold text-orange-900 mb-3">Формати</h4>
                  <div className="space-y-2">
                    {Object.entries(videoData.trend_analysis?.format_trends?.format_distribution || {}).map(([format, count]) => (
                      <div key={format} className="flex justify-between text-sm">
                        <span className="text-orange-800">{format}:</span>
                        <span className="font-medium text-orange-900">{count}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'recommendations' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* Recommendation Rationale */}
              {videoData.trend_analysis?.reasoning?.recommendation_rationale && (
                <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6 border border-green-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Target className="w-5 h-5 mr-2 text-green-600" />
                    Обґрунтування рекомендацій
                  </h3>
                  
                  <div className="bg-white rounded-lg p-4 border border-green-200">
                    <h4 className="font-semibold text-green-900 mb-3">Чому ці рекомендації?</h4>
                    <ul className="space-y-2">
                      {videoData.trend_analysis.reasoning.recommendation_rationale.map((rationale, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-green-800 text-sm">{rationale}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {Object.entries(videoData.recommendations || {}).map(([category, recommendations]) => (
                  <div key={category} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <h4 className="font-semibold text-gray-900 mb-3 capitalize">
                      {category.replace('_', ' ')}
                    </h4>
                    <ul className="space-y-2">
                      {recommendations.map((rec, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <CheckCircle className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-700 text-sm">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {activeTab === 'technical' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h4 className="font-semibold text-gray-900 mb-3">Технічні специфікації</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Тип генератора:</p>
                    <p className="font-medium text-gray-900">
                      {videoData.technical_specifications?.generator_type?.toUpperCase() || 'VEO'}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Рекомендоване співвідношення:</p>
                    <p className="font-medium text-gray-900">
                      {videoData.technical_specifications?.recommended_aspect_ratio || '16:9'}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Рекомендована роздільність:</p>
                    <p className="font-medium text-gray-900">
                      {videoData.technical_specifications?.recommended_resolution || '1080p'}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Рекомендована тривалість:</p>
                    <p className="font-medium text-gray-900">
                      {videoData.technical_specifications?.recommended_duration || '5-15 секунд'}
                    </p>
                  </div>
                </div>
              </div>

              {videoData.technical_specifications?.optimization_tips && (
                <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                  <h4 className="font-semibold text-blue-900 mb-3">Поради з оптимізації</h4>
                  <ul className="space-y-2">
                    {videoData.technical_specifications.optimization_tips.map((tip, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-blue-800">{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default VideoGenerator;
