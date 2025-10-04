# Createnko 🎬

**AI-powered video script generator based on competitor analysis**

Createnko analyzes successful Facebook Ads videos from competitors and your product webpage to generate concrete, actionable video scripts for AI video generators like Veo, Runway, Pika, and others.

## 🌟 Features

- **Webpage Analysis**: Extracts product information, target audience, and brand identity from your website
- **Competitor Video Analysis**: Uses Google Gemini to analyze successful competitor video ads from Facebook Ads Library
- **Concrete Video Scripts**: Generates step-by-step video scripts with specific scenes, timings, and techniques
- **Multiple AI Generators**: Supports Veo, Runway, Pika, Stable Video, and Sora
- **Real-time Analysis**: Processes videos in real-time with progress tracking

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key
- ScrapeCreators API key (for Facebook Ads data)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/BuhaiovDmytro/Createnko.git
cd createnko
```

2. **Install backend dependencies**
```bash
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SCRAPECREATORS_API_KEY=your_scrapecreators_api_key_here
```

### Running the Application

**Option 1: Using provided scripts (Windows)**
```bash
# Start both backend and frontend
cd scripts
start.bat
```

**Option 2: Manual start**

Terminal 1 (Backend):
```bash
python api_server.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📖 How It Works

1. **Input**: Enter competitor brand names and your product URL
2. **Analysis**: 
   - Fetches video ads from Facebook Ads Library
   - Analyzes your product webpage with Gemini
   - Analyzes competitor videos with Gemini
3. **Script Generation**: 
   - Extracts proven techniques from competitor videos
   - Combines with your product information
   - Generates scene-by-scene video script
4. **Output**: Concrete video script ready for AI video generators

## 🎯 Example Output

```
CREATE A VEO VIDEO SCRIPT

WHAT WE'RE ADVERTISING:
Product/Service: Your Amazing App
Target Audience: Young professionals aged 25-35

STEP-BY-STEP VIDEO SCRIPT:

SCENE 1: OPENING (0-3 seconds)
Visual: Show Your Amazing App prominently
Composition: Split-screen - app on one side, benefit on other

SCENE 2: PROBLEM/HOOK (3-5 seconds)
Visual: Show scenario that resonates with target audience
Text Overlay: Problem statement

SCENE 3: SOLUTION/PRODUCT SHOWCASE (5-15 seconds)
Visual: Demonstrate Your Amazing App in action
Show: Key features solving the problem

...
```

## 🛠️ Tech Stack

### Backend
- FastAPI - High-performance Python web framework
- Google Gemini AI - Video and webpage analysis
- BeautifulSoup4 - Web scraping
- ScrapeCreators API - Facebook Ads data

### Frontend
- React - UI framework
- Tailwind CSS - Styling
- Framer Motion - Animations
- Axios - API requests

## 📁 Project Structure

```
createnko/
├── api_server.py              # Main FastAPI server
├── mcp_server.py             # MCP protocol server
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .env.example             # Environment template
├── src/
│   ├── logger.py            # Logging configuration
│   └── services/
│       ├── gemini_service.py           # Gemini AI integration
│       ├── scrapecreators_service.py   # Facebook Ads API
│       ├── webpage_analyzer_service.py # Webpage analysis
│       ├── video_generator_service.py  # Video script generation
│       ├── trend_analysis_service.py   # Trend analysis
│       └── media_cache_service.py      # Media caching
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/         # React components
│   │   └── services/
│   │       └── apiService.js   # API client
│   ├── package.json
│   └── tailwind.config.js
└── scripts/
    ├── start.bat              # Windows startup script
    ├── start.ps1              # PowerShell startup script
    ├── start_frontend.bat     # Frontend only
    └── install.bat            # Windows installation script
```

## 🔧 Configuration

### API Keys

**Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

**ScrapeCreators API Key**: Get from [ScrapeCreators](https://scrapecreators.com)

### Video Generators

Supported generators:
- **Veo** (Google) - Cinematic, high-quality
- **Runway** (Gen-3) - Creative, realistic
- **Pika** - Artistic, fluid animations
- **Stable Video** - Controlled, stable output
- **Sora** (OpenAI) - Photorealistic

## 📝 API Endpoints

- `POST /api/v1/video/analyze-all` - Analyze videos and generate script
- `POST /api/v1/brands/search` - Search for brand platform IDs
- `GET /api/v1/generators/supported` - List supported generators
- `GET /health` - Health check

Full API documentation available at `/docs` when server is running.

## 🎥 Usage Example

1. Open http://localhost:3000
2. Enter competitor brand names (e.g., "Nike, Adidas")
3. Enter your product URL (e.g., "https://myshop.com/product")
4. Click "Generate Video Script"
5. Get a concrete, scene-by-scene video script
6. Use the script with AI video generators (Veo, Runway, etc.)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini for AI video analysis
- ScrapeCreators for Facebook Ads Library access
- React and FastAPI communities

## 📧 Support

For questions or support, please open an issue on GitHub.

## 🔮 Roadmap

- [ ] Support for more AI video generators
- [ ] Advanced script customization options
- [ ] Multi-language support
- [ ] Export scripts in various formats
- [ ] Integration with video editing tools

---

Made with ❤️ by Createnko Team
