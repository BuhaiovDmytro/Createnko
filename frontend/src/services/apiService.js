import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 300000, // 5 minutes timeout for video generation
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for logging
    this.client.interceptors.request.use(
      (config) => {
        console.log(`Making ${config.method.toUpperCase()} request to ${config.url}`);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(this.handleError(error));
      }
    );
  }

  handleError(error) {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      // Create enhanced error object with credit info
      const enhancedError = new Error();
      enhancedError.status = status;
      enhancedError.data = data;
      
      switch (status) {
        case 401:
          enhancedError.message = 'Помилка авторизації. Перевірте налаштування API ключа.';
          enhancedError.type = 'auth_error';
          break;
        case 402:
          enhancedError.message = 'Вичерпано кредити ScrapeCreators API. Будь ласка, поповніть рахунок.';
          enhancedError.type = 'credit_exhausted';
          enhancedError.creditInfo = {
            credits_remaining: data?.credits_remaining || 0,
            topup_url: data?.topup_url || 'https://scrapecreators.com'
          };
          break;
        case 404:
          enhancedError.message = 'Не знайдено відповідних даних для аналізу.';
          enhancedError.type = 'not_found';
          break;
        case 429:
          enhancedError.message = 'Перевищено ліміт запитів ScrapeCreators API. Спробуйте пізніше.';
          enhancedError.type = 'rate_limit';
          enhancedError.creditInfo = {
            retry_after: data?.retry_after || null
          };
          break;
        case 500:
          enhancedError.message = 'Внутрішня помилка сервера. Спробуйте пізніше.';
          enhancedError.type = 'server_error';
          break;
        default:
          enhancedError.message = data?.detail || data?.message || 'Сталася невідома помилка.';
          enhancedError.type = 'unknown_error';
      }
      
      return enhancedError;
    } else if (error.request) {
      // Network error
      const networkError = new Error('Помилка мережі. Перевірте підключення до інтернету.');
      networkError.type = 'network_error';
      return networkError;
    } else {
      // Other error
      const otherError = new Error(error.message || 'Сталася невідома помилка.');
      otherError.type = 'unknown_error';
      return otherError;
    }
  }

  // Health check
  async healthCheck() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Get supported generators
  async getSupportedGenerators() {
    try {
      const response = await this.client.get('/api/v1/generators/supported');
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Search for brands
  async searchBrands(brandNames, options = {}) {
    try {
      const payload = {
        brand_names: brandNames,
        limit: options.limit || 50,
        country: options.country || null
      };

      const response = await this.client.post('/api/v1/brands/search', payload);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Get ads for brands
  async getAds(brandNames, options = {}) {
    try {
      const payload = {
        brand_names: brandNames,
        limit: options.limit || 50,
        country: options.country || null
      };

      const response = await this.client.post('/api/v1/ads/get', payload);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Analyze trends
  async analyzeTrends(adsData, analysisType = 'comprehensive') {
    try {
      const payload = {
        ads_data: adsData,
        analysis_type: analysisType
      };

      const response = await this.client.post('/api/v1/trends/analyze', payload);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Generate video description (full workflow with video analysis)
  async generateVideo(formData) {
    try {
      const payload = {
        brand_names: formData.brand_names,
        user_query: formData.user_query,
        generator_type: formData.generator_type || 'veo',
        limit: formData.limit || 50,
        country: formData.country || null,
        style_preferences: formData.style_preferences || null
      };

      console.log('Sending video generation request with analysis:', payload);

      const response = await this.client.post('/api/v1/video/analyze-all', payload);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Generate video description from existing ads data
  async generateVideoFromAds(adsData, userQuery, generatorType = 'veo', stylePreferences = null) {
    try {
      const payload = {
        ads_data: adsData,
        user_query: userQuery,
        generator_type: generatorType,
        style_preferences: stylePreferences
      };

      const response = await this.client.post('/api/v1/video/describe', payload);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Get cache statistics
  async getCacheStats() {
    try {
      const response = await this.client.get('/api/v1/cache/stats');
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Cleanup cache
  async cleanupCache(maxAgeDays = 30) {
    try {
      const response = await this.client.post('/api/v1/cache/cleanup', null, {
        params: { max_age_days: maxAgeDays }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Analyze video
  async analyzeVideo(mediaUrl, brandName = null, adId = null) {
    try {
      const payload = {
        media_url: mediaUrl,
        brand_name: brandName,
        ad_id: adId
      };

      const response = await this.client.post('/api/v1/video/analyze', payload);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }
}

// Create singleton instance
export const apiService = new ApiService();
export default apiService;
