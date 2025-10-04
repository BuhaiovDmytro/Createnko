import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, ExternalLink, CreditCard, Clock } from 'lucide-react';

const CreditStatus = ({ creditInfo, errorType }) => {
  if (!creditInfo && !errorType) return null;

  const isCreditExhausted = errorType === 'credit_exhausted' || errorType === '402';
  const isRateLimited = errorType === 'rate_limit' || errorType === '429';

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`card ${
        isCreditExhausted 
          ? 'bg-red-50 border-red-200' 
          : isRateLimited 
          ? 'bg-yellow-50 border-yellow-200'
          : 'bg-blue-50 border-blue-200'
      }`}
    >
      <div className="flex items-start">
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
          isCreditExhausted 
            ? 'bg-red-100' 
            : isRateLimited 
            ? 'bg-yellow-100'
            : 'bg-blue-100'
        }`}>
          {isCreditExhausted ? (
            <CreditCard className="w-4 h-4 text-red-600" />
          ) : isRateLimited ? (
            <Clock className="w-4 h-4 text-yellow-600" />
          ) : (
            <AlertTriangle className="w-4 h-4 text-blue-600" />
          )}
        </div>
        
        <div className="flex-1">
          <h3 className={`font-semibold mb-2 ${
            isCreditExhausted 
              ? 'text-red-800' 
              : isRateLimited 
              ? 'text-yellow-800'
              : 'text-blue-800'
          }`}>
            {isCreditExhausted ? 'Вичерпано кредити ScrapeCreators API' : 
             isRateLimited ? 'Перевищено ліміт запитів' : 
             'Інформація про кредити'}
          </h3>
          
          {isCreditExhausted ? (
            <div className="space-y-3">
              <p className="text-red-700 text-sm">
                Для роботи з Facebook Ads Library потрібні кредити ScrapeCreators API. 
                Ваші кредити вичерпано.
              </p>
              
              {creditInfo?.credits_remaining !== undefined && (
                <div className="bg-red-100 rounded-lg p-3">
                  <p className="text-red-800 text-sm font-medium">
                    Кредитів залишилось: {creditInfo.credits_remaining}
                  </p>
                </div>
              )}
              
              {creditInfo?.topup_url && (
                <div className="flex items-center space-x-2">
                  <a
                    href={creditInfo.topup_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-lg hover:bg-red-700 transition-colors"
                  >
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Поповнити рахунок
                  </a>
                </div>
              )}
              
              <div className="bg-red-100 rounded-lg p-3 mt-3">
                <h4 className="text-red-800 font-medium text-sm mb-2">Що таке ScrapeCreators API?</h4>
                <p className="text-red-700 text-xs">
                  ScrapeCreators API - це сервіс для отримання даних з Facebook Ads Library. 
                  Він дозволяє аналізувати рекламні оголошення конкурентів та створювати 
                  відео на основі актуальних трендів.
                </p>
              </div>
            </div>
          ) : isRateLimited ? (
            <div className="space-y-3">
              <p className="text-yellow-700 text-sm">
                Перевищено ліміт запитів до ScrapeCreators API. Спробуйте пізніше.
              </p>
              
              {creditInfo?.retry_after && (
                <div className="bg-yellow-100 rounded-lg p-3">
                  <p className="text-yellow-800 text-sm font-medium">
                    Спробуйте через: {creditInfo.retry_after} секунд
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-3">
              <p className="text-blue-700 text-sm">
                Інформація про статус кредитів ScrapeCreators API.
              </p>
              
              {creditInfo?.credits_remaining !== undefined && (
                <div className="bg-blue-100 rounded-lg p-3">
                  <p className="text-blue-800 text-sm font-medium">
                    Кредитів залишилось: {creditInfo.credits_remaining}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default CreditStatus;
