import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, Wand2, Settings, Globe } from 'lucide-react';
import toast from 'react-hot-toast';

const ProductInputForm = ({ onSubmit, isGenerating, onReset }) => {
  const [formData, setFormData] = useState({
    productUrl: '',
    userPrompt: '',
    generatorType: 'veo',
    country: '',
    limit: 10
  });

  const [showAdvanced, setShowAdvanced] = useState(false);

  const generatorOptions = [
    { value: 'veo', label: 'Google Veo', description: 'Висока якість з плавним рухом' },
    { value: 'runway', label: 'Runway ML', description: 'Творче редагування відео' },
    { value: 'pika', label: 'Pika Labs', description: 'Художній стиль анімації' },
    { value: 'stable_video', label: 'Stable Video', description: 'Стабільна генерація' },
    { value: 'sora', label: 'OpenAI Sora', description: 'Розширена AI генерація' }
  ];

  const countryOptions = [
    { value: '', label: 'Всі країни' },
    { value: 'US', label: 'США' },
    { value: 'CA', label: 'Канада' },
    { value: 'GB', label: 'Великобританія' },
    { value: 'DE', label: 'Німеччина' },
    { value: 'FR', label: 'Франція' },
    { value: 'UA', label: 'Україна' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!formData.productUrl.trim()) {
      toast.error('Будь ласка, введіть посилання на продукт');
      return;
    }

    if (!formData.userPrompt.trim()) {
      toast.error('Будь ласка, введіть опис вашого запиту');
      return;
    }

    // Витягуємо назву бренду з URL
    const brandName = extractBrandFromUrl(formData.productUrl);
    
    const submitData = {
      brand_names: brandName,
      user_query: formData.userPrompt,
      generator_type: formData.generatorType,
      country: formData.country || null,
      limit: formData.limit
    };

    onSubmit(submitData);
  };

  const extractBrandFromUrl = (url) => {
    try {
      const urlObj = new URL(url);
      const hostname = urlObj.hostname;
      
      // Видаляємо www. та домен
      let brand = hostname.replace(/^www\./, '').split('.')[0];
      
      // Капіталізуємо першу літеру
      return brand.charAt(0).toUpperCase() + brand.slice(1);
    } catch {
      // Якщо URL невалідний, використовуємо як є
      return formData.productUrl;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card"
    >
      <div className="flex items-center mb-6">
        <div className="flex items-center justify-center w-10 h-10 bg-blue-100 rounded-lg mr-3">
          <Link className="w-5 h-5 text-blue-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            Введіть дані про продукт
          </h3>
          <p className="text-sm text-gray-500">
            Отримайте відео на основі трендів конкурентів
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Посилання на продукт */}
        <div>
          <label htmlFor="productUrl" className="block text-sm font-medium text-gray-700 mb-2">
            Посилання на ваш продукт *
          </label>
          <input
            type="url"
            id="productUrl"
            name="productUrl"
            value={formData.productUrl}
            onChange={handleInputChange}
            placeholder="https://example.com/product"
            className="input-field"
            required
            disabled={isGenerating}
          />
          <p className="text-xs text-gray-500 mt-1">
            Введіть URL вашого продукту або сайту
          </p>
        </div>

        {/* Опис запиту */}
        <div>
          <label htmlFor="userPrompt" className="block text-sm font-medium text-gray-700 mb-2">
            Опис вашого запиту *
          </label>
          <textarea
            id="userPrompt"
            name="userPrompt"
            value={formData.userPrompt}
            onChange={handleInputChange}
            placeholder="Опишіть, яке відео ви хочете створити..."
            rows={3}
            className="input-field resize-none"
            required
            disabled={isGenerating}
          />
          <p className="text-xs text-gray-500 mt-1">
            Наприклад: "Створити рекламне відео для нового продукту"
          </p>
        </div>

        {/* Розширені налаштування */}
        <div>
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center text-sm text-gray-600 hover:text-gray-800 transition-colors"
            disabled={isGenerating}
          >
            <Settings className="w-4 h-4 mr-2" />
            Розширені налаштування
            <span className={`ml-2 transform transition-transform ${showAdvanced ? 'rotate-180' : ''}`}>
              ▼
            </span>
          </button>
        </div>

        {showAdvanced && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="space-y-4 pt-4 border-t border-gray-200"
          >
            {/* Тип генератора */}
            <div>
              <label htmlFor="generatorType" className="block text-sm font-medium text-gray-700 mb-2">
                Тип відео генератора
              </label>
              <select
                id="generatorType"
                name="generatorType"
                value={formData.generatorType}
                onChange={handleInputChange}
                className="input-field"
                disabled={isGenerating}
              >
                {generatorOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label} - {option.description}
                  </option>
                ))}
              </select>
            </div>

            {/* Країна */}
            <div>
              <label htmlFor="country" className="block text-sm font-medium text-gray-700 mb-2">
                <Globe className="w-4 h-4 inline mr-1" />
                Країна для аналізу
              </label>
              <select
                id="country"
                name="country"
                value={formData.country}
                onChange={handleInputChange}
                className="input-field"
                disabled={isGenerating}
              >
                {countryOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Ліміт оголошень */}
            <div>
              <label htmlFor="limit" className="block text-sm font-medium text-gray-700 mb-2">
                Кількість оголошень для аналізу
              </label>
              <input
                type="number"
                id="limit"
                name="limit"
                value={formData.limit}
                onChange={handleInputChange}
                min="1"
                max="500"
                className="input-field"
                disabled={isGenerating}
              />
              <p className="text-xs text-gray-500 mt-1">
                Більше оголошень = точніший аналіз (1-500)
              </p>
            </div>
          </motion.div>
        )}

        {/* Кнопки */}
        <div className="flex space-x-3 pt-4">
          <button
            type="submit"
            disabled={isGenerating}
            className="btn-primary flex-1 flex items-center justify-center"
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Генерується...
              </>
            ) : (
              <>
                <Wand2 className="w-4 h-4 mr-2" />
                Генерувати відео
              </>
            )}
          </button>
          
          {onReset && (
            <button
              type="button"
              onClick={onReset}
              className="btn-secondary"
              disabled={isGenerating}
            >
              Скинути
            </button>
          )}
        </div>
      </form>
    </motion.div>
  );
};

export default ProductInputForm;
