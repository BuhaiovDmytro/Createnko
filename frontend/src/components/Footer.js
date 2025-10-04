import React from 'react';
import { Github, ExternalLink, Heart } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Про проект */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Createnko
            </h3>
            <p className="text-gray-600 text-sm leading-relaxed">
              AI-powered video script generator. Analyze competitor videos and your product to create concrete, actionable video scripts for AI generators.
            </p>
          </div>

          {/* Корисні посилання */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Корисні посилання
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a 
                  href="https://www.facebook.com/ads/library" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-primary-600 transition-colors flex items-center space-x-2"
                >
                  <ExternalLink className="w-3 h-3" />
                  <span>Facebook Ads Library</span>
                </a>
              </li>
              <li>
                <a 
                  href="https://ai.google.dev/gemini-api/docs" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-primary-600 transition-colors flex items-center space-x-2"
                >
                  <ExternalLink className="w-3 h-3" />
                  <span>Google Gemini API</span>
                </a>
              </li>
              <li>
                <a 
                  href="https://scrapecreators.com" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-primary-600 transition-colors flex items-center space-x-2"
                >
                  <ExternalLink className="w-3 h-3" />
                  <span>ScrapeCreators API</span>
                </a>
              </li>
            </ul>
          </div>

          {/* Технології */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Технології
            </h3>
            <div className="flex flex-wrap gap-2">
              <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                React
              </span>
              <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                FastAPI
              </span>
              <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
                Tailwind CSS
              </span>
              <span className="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded-full">
                Python
              </span>
              <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                Gemini AI
              </span>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-200 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 text-sm text-gray-600 mb-4 md:mb-0">
              <span>Зроблено з</span>
              <Heart className="w-4 h-4 text-red-500" />
              <span>для творців контенту</span>
            </div>
            
            <div className="flex items-center space-x-4">
              <a 
                href="https://github.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
              
              <span className="text-sm text-gray-500">
                © 2024 Createnko
              </span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
