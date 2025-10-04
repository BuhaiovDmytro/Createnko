import React from 'react';
import { motion } from 'framer-motion';
import { Loader2, TrendingUp, BarChart3, Target } from 'lucide-react';

const LoadingSpinner = () => {
  const steps = [
    { icon: TrendingUp, text: 'Аналізуємо тренди Facebook Ads...', color: 'text-blue-600' },
    { icon: BarChart3, text: 'Обробляємо дані конкурентів...', color: 'text-green-600' },
    { icon: Target, text: 'Генеруємо опис відео...', color: 'text-purple-600' }
  ];

  return (
    <div className="card bg-gradient-to-br from-blue-50 to-purple-50 border-blue-200">
      <div className="text-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-16 h-16 mx-auto mb-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center"
        >
          <Loader2 className="w-8 h-8 text-white" />
        </motion.div>
        
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Генеруємо ваше відео...
        </h3>
        
        <p className="text-gray-600 mb-6">
          Це може зайняти кілька хвилин. Ми аналізуємо тисячі оголошень 
          та створюємо унікальний контент для вас.
        </p>

        <div className="space-y-4">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.5 }}
              className="flex items-center justify-center space-x-3"
            >
              <div className={`w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-sm`}>
                <step.icon className={`w-4 h-4 ${step.color}`} />
              </div>
              <span className="text-sm text-gray-700">{step.text}</span>
            </motion.div>
          ))}
        </div>

        <div className="mt-6 bg-white rounded-lg p-4 border border-gray-200">
          <div className="flex items-center justify-between text-xs text-gray-500 mb-2">
            <span>Прогрес</span>
            <span>~2-3 хвилини</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <motion.div
              className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full"
              initial={{ width: "0%" }}
              animate={{ width: "100%" }}
              transition={{ duration: 180, ease: "linear" }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
