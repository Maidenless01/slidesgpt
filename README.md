# SlidesGPT - AI-Powered Slide Generator

An intelligent application that automatically generates professional PowerPoint presentations using AI.

## Features

- **AI-Powered Content Generation**: Uses Google Gemini AI to create slide content
- **Automatic Slide Structure**: Intelligently organizes content into slides
- **Professional Templates**: Creates visually appealing presentations
- **Easy to Use**: Simple web interface or command-line usage
- **Customizable**: Adjust number of slides, topics, and presentation style

## Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Gemini API key**:
   - Copy `.env.example` to `.env`
   - Get your free API key from https://aistudio.google.com/app/apikey
   - Add your Gemini API key to the `.env` file

3. **Run the application**:
   
   **Web Interface**:
   ```bash
   python app.py
   ```
   Then open http://localhost:5000 in your browser

   **Command Line**:
   ```bash
   python slide_generator.py "Your presentation topic" --slides 10
   ```

## Usage

### Web Interface
1. Navigate to http://localhost:5000
2. Enter your presentation topic
3. Specify the number of slides (optional)
4. Click "Generate Presentation"
5. Download your PowerPoint file

### Command Line
```bash
python slide_generator.py "Introduction to Machine Learning" --slides 8 --output my_presentation.pptx
```

## Examples

```bash
# Generate a 10-slide presentation on AI
python slide_generator.py "Artificial Intelligence in Healthcare" --slides 10

# Generate a business presentation
python slide_generator.py "Q4 2024 Marketing Strategy" --slides 12
```

## Requirements

- Python 3.8+
- Google Gemini API key (free tier available)
- Internet connection

## License

MIT License
