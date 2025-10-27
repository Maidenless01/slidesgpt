# 🚀 Quick Start Guide - Using Google Gemini

## Get Your FREE Gemini API Key

1. **Go to Google AI Studio**: https://aistudio.google.com/app/apikey

2. **Sign in** with your Google account

3. **Click "Create API Key"** button

4. **Copy your API key**

5. **Open the `.env` file** in this project

6. **Replace** `your_gemini_api_key_here` with your actual API key:
   ```
   GEMINI_API_KEY=AIzaSyD...your-actual-key-here
   ```

## Run the Application

### Web Interface (Recommended)
```bash
python app.py
```
Then open http://localhost:5000 in your browser

### Command Line
```bash
python slide_generator.py "Your Topic Here" --slides 10
```

## Why Gemini?

✅ **FREE** - No credit card required  
✅ **Fast** - Quick response times  
✅ **Powerful** - High-quality content generation  
✅ **Easy** - Simple setup process  

## Examples

```bash
# Generate a presentation about AI
python slide_generator.py "Introduction to AI" --slides 8

# Business presentation
python slide_generator.py "Marketing Strategy 2024" --slides 12

# Educational content
python slide_generator.py "Python Programming" --slides 15
```

Enjoy creating amazing presentations! 🎨
