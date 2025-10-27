# SlidesGPT - AI-Powered Presentation Generator# SlidesGPT - AI-Powered Slide Generator



Create professional PowerPoint presentations with AI using a modern React interface and Google Gemini.An intelligent application that automatically generates professional PowerPoint presentations using AI.



## ✨ Features## Features



- 🎨 **Modern React UI** - Beautiful, responsive interface built with React + Vite- **AI-Powered Content Generation**: Uses Google Gemini AI to create slide content

- 🤖 **AI-Powered Generation** - Uses Google Gemini API (gemini-2.5-flash) for intelligent content- **Automatic Slide Structure**: Intelligently organizes content into slides

- 🎭 **Multiple Styles** - Choose from 6 presentation styles:- **Professional Templates**: Creates visually appealing presentations

  - Professional- **Easy to Use**: Simple web interface or command-line usage

  - Educational- **Customizable**: Adjust number of slides, topics, and presentation style

  - Technical

  - Creative## Setup

  - Minimalist

  - Playful1. **Install Python dependencies**:

- 💻 **Code Examples** - Optional syntax-highlighted code snippets   ```bash

- 🖼️ **Image Suggestions** - AI suggests relevant images for slides   pip install -r requirements.txt

- 📱 **Presentation Viewer** - Built-in slide viewer with navigation, thumbnails, and speaker notes   ```

- 📥 **PowerPoint Export** - Download as fully-formatted .pptx files

- 🎯 **Audience Targeting** - Customize content for specific audiences2. **Set up your Gemini API key**:

- 📝 **Prompt-Based Input** - Describe your presentation in detail for better results   - Copy `.env.example` to `.env`

   - Get your free API key from https://aistudio.google.com/app/apikey

## 🚀 Quick Start   - Add your Gemini API key to the `.env` file



### 1. Install Dependencies3. **Run the application**:

   

**Python (Backend):**   **Web Interface**:

```bash   ```bash

pip install -r requirements.txt   python app.py

```   ```

   Then open http://localhost:5000 in your browser

**Node.js (Frontend):**

```bash   **Command Line**:

cd frontend   ```bash

npm install   python slide_generator.py "Your presentation topic" --slides 10

cd ..   ```

```

## Usage

### 2. Configure API Key

### Web Interface

Create a `.env` file in the root directory:1. Navigate to http://localhost:5000

2. Enter your presentation topic

```env3. Specify the number of slides (optional)

GEMINI_API_KEY=your_api_key_here4. Click "Generate Presentation"

```5. Download your PowerPoint file



Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)### Command Line

```bash

### 3. Run the Applicationpython slide_generator.py "Introduction to Machine Learning" --slides 8 --output my_presentation.pptx

```

**Production Mode (Recommended):**

```bash## Examples

# Build React frontend (first time only)

cd frontend```bash

npm run build# Generate a 10-slide presentation on AI

cd ..python slide_generator.py "Artificial Intelligence in Healthcare" --slides 10



# Start the server# Generate a business presentation

python app.pypython slide_generator.py "Q4 2024 Marketing Strategy" --slides 12

``````



Open http://localhost:5000 in your browser## Requirements



**Development Mode (with hot reload):**- Python 3.8+

- Google Gemini API key (free tier available)

Terminal 1 - Flask backend:- Internet connection

```bash

python app.py## License

```

MIT License

Terminal 2 - React dev server:
```bash
cd frontend
npm run dev
```

Open http://localhost:5173 (React dev server with hot reload)

## 📖 Usage

### Web Interface

1. **Enter a detailed prompt** describing your presentation
   - Example: "Create a comprehensive presentation about React for beginners, covering setup, components, state, and props with code examples"

2. **Configure options:**
   - Number of slides (3-30)
   - Presentation style
   - Target audience (optional)
   - Include code examples
   - Include image suggestions

3. **Generate** - Click the button and wait for AI to create your slides

4. **Download or View:**
   - 📥 Download PowerPoint file
   - 👁️ View in browser with full presentation mode
   - 🆕 Create another presentation

### Command Line (Legacy)

```bash
python slide_generator.py "Your presentation topic" --slides 10 --output presentation.pptx
```

## 🏗️ Project Structure

```
slidesgpt/
├── frontend/                    # React frontend (Vite)
│   ├── src/
│   │   ├── App.jsx             # Main UI component
│   │   ├── api.js              # API client with error handling
│   │   ├── main.jsx            # React entry point
│   │   └── index.css           # Styles
│   ├── index.html              # HTML template
│   ├── vite.config.js          # Vite build configuration
│   └── package.json            # Node dependencies
├── static/
│   └── frontend/               # Built React app (generated by npm run build)
├── templates/                  # Flask templates
│   ├── index.html              # Fallback template
│   └── viewer.html             # Presentation viewer
├── output/                     # Generated PowerPoint files
├── cache/                      # Cached slide data (JSON)
├── app.py                      # Flask backend API
├── slide_generator.py          # AI slide generation logic
├── requirements.txt            # Python dependencies
├── .env                        # API keys (create this)
└── README.md                   # This file
```

## 🔌 API Endpoints

- `GET /` - Serve React frontend
- `POST /generate` - Generate presentation
  ```json
  {
    "prompt": "Your detailed description",
    "num_slides": 8,
    "style": "professional",
    "audience": "business executives",
    "include_images": true,
    "include_code": false
  }
  ```
- `GET /download/<filename>` - Download PowerPoint file
- `GET /viewer/<filename>?slides=<json>` - View presentation
- `GET /api/slides/<filename>` - Get cached slide data
- `GET /health` - Health check

## 🛠️ Technologies

**Frontend:**
- React 18
- Vite 5
- Modern ES6+ JavaScript
- CSS3 with gradients and animations

**Backend:**
- Flask 3.0
- Python 3.8+
- python-pptx (PowerPoint generation)
- flask-cors (CORS support)

**AI:**
- Google Gemini API (gemini-2.5-flash model)
- REST API approach (not SDK)

## 🔧 Development

### Rebuild Frontend
```bash
cd frontend
npm run build
```

### Run React Dev Server
```bash
cd frontend
npm run dev
```
React will be available at http://localhost:5173 with API proxying to Flask

### Modify UI Styles
Edit `frontend/src/index.css` or `frontend/src/App.jsx`

### Update AI Prompts
Edit `slide_generator.py` - modify the `generate_slide_content()` method

## 🐛 Troubleshooting

**"Module not found" errors:**
```bash
pip install -r requirements.txt
cd frontend && npm install
```

**CORS errors in dev mode:**
```bash
pip install flask-cors
```

**Viewer not working:**
- Generate a new presentation (slides data is cached)
- Check browser console for JavaScript errors
- Ensure slides data is being passed in URL

**React build issues:**
```bash
cd frontend
rm -rf node_modules dist
npm install
npm run build
```

**API/Generation errors:**
- Verify `.env` file has correct `GEMINI_API_KEY`
- Check API key at https://aistudio.google.com/app/apikey
- Test internet connection
- Check terminal output for detailed error messages

## 📝 Examples

**Educational presentation:**
```
Prompt: "Create an educational presentation about photosynthesis for high school students, 
including diagrams, step-by-step process, and real-world applications"
Style: Educational
Audience: High school students
Slides: 10
Images: ✓ Include image suggestions
```

**Technical presentation:**
```
Prompt: "Comprehensive guide to Docker containerization for developers, covering installation, 
basic commands, Dockerfile creation, and docker-compose with practical examples"
Style: Technical
Audience: Software developers
Slides: 12
Code: ✓ Include code examples
```

**Business presentation:**
```
Prompt: "Q4 2025 marketing strategy review with KPIs, campaign performance, budget allocation, 
and 2026 roadmap for executive stakeholders"
Style: Professional
Audience: C-suite executives
Slides: 8
```

## 📦 Requirements

- Python 3.8 or higher
- Node.js 18 or higher
- Google Gemini API key (free tier available)
- Internet connection
- Modern web browser (Chrome, Firefox, Edge, Safari)

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments

- Google Gemini AI for content generation
- React team for the amazing framework
- python-pptx library for PowerPoint creation
- Flask for the simple and powerful backend
