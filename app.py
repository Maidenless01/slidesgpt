"""
Flask Web Application for AI Slide Generator
Provides a simple web interface for generating presentations
"""

from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from free_slide_generator import FreeSlideGenerator
from datetime import datetime
import traceback

app = Flask(__name__, static_folder='static/frontend', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Enable CORS for development (React dev server on different port)
CORS(app)

# Create output directory if it doesn't exist
OUTPUT_DIR = 'output'
CACHE_DIR = 'cache'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# Initialize FREE generator (only needs Gemini API key)
try:
    generator = FreeSlideGenerator()
    print("✅ Free Slide Generator initialized successfully")
except Exception as e:
    print(f"⚠️  Error initializing generator: {e}")
    generator = None


@app.route('/')
def index():
    """Serve React app"""
    frontend_path = os.path.join(app.static_folder, 'index.html')
    if os.path.exists(frontend_path):
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return jsonify({
            'error': 'Frontend not built. Run: cd frontend && npm run build'
        }), 500


@app.route('/api/themes', methods=['GET'])
def get_themes():
    """Get available themes"""
    if not generator:
        return jsonify({'error': 'Generator not initialized'}), 500
    
    themes = []
    for key, config in FreeSlideGenerator.THEMES.items():
        themes.append({
            'id': key,
            'name': config['name'],
            'primary': f"rgb({config['primary'][0]}, {config['primary'][1]}, {config['primary'][2]})",
            'secondary': f"rgb({config['secondary'][0]}, {config['secondary'][1]}, {config['secondary'][2]})",
            'accent': f"rgb({config['accent'][0]}, {config['accent'][1]}, {config['accent'][2]})"
        })
    return jsonify({'themes': themes})


@app.route('/generate', methods=['POST'])
def generate_presentation():
    """Generate presentation with FREE tools only"""
    try:
        if not generator:
            return jsonify({'error': 'Generator not initialized. Check GEMINI_API_KEY in .env'}), 500
        
        # Get form data
        data = request.get_json()
        topic = data.get('prompt', data.get('topic', '')).strip()
        num_slides = int(data.get('num_slides', data.get('slides', 8)))
        style = data.get('style', 'professional')
        audience = data.get('audience', '').strip()
        include_images = data.get('include_images', False)
        use_ai_images = data.get('use_ai_images', False)  # NEW: AI image generation
        include_code = data.get('include_code', False)
        theme = data.get('theme', 'modern_blue')
        
        # Validate input
        if not topic:
            return jsonify({'error': 'Please provide a topic'}), 400
        
        if num_slides < 3 or num_slides > 30:
            return jsonify({'error': 'Number of slides must be between 3 and 30'}), 400
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_topic = safe_topic.replace(' ', '_')[:50]
        output_filename = f"{safe_topic}_{timestamp}.pptx"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        print(f"\n{'='*60}")
        print(f"🎯 Generating FREE presentation:")
        print(f"   Prompt: {topic}")
        print(f"   Slides: {num_slides}")
        print(f"   Theme: {theme}")
        print(f"   Style: {style}")
        print(f"   Images: {'AI Generated' if use_ai_images else 'Stock Photos' if include_images else 'None'}")
        print(f"   Diagrams: Enabled (auto-generated)")
        print(f"{'='*60}\n")
        
        # Generate presentation (100% FREE with diagrams & AI images)
        result = generator.generate_presentation(
            prompt=topic,
            num_slides=num_slides,
            output_path=output_path,
            style=style,
            audience=audience,
            include_code=include_code,
            include_images=include_images or use_ai_images,
            use_ai_images=use_ai_images,
            theme=theme
        )
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'num_slides': result['num_slides'],
            'slides_data': result['slides_data'],
            'theme': result['theme'],
            'message': f'Presentation generated successfully with diagrams and {"AI images" if use_ai_images else "stock images" if include_images else "no images"}!'
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/slides/<filename>')
def get_slides_data(filename):
    """Get slide data for a presentation (for viewer)"""
    try:
        # Convert .pptx filename to .json cache filename
        cache_filename = filename.replace('.pptx', '.json')
        cache_path = os.path.join(CACHE_DIR, cache_filename)
        
        if not os.path.exists(cache_path):
            return jsonify({
                'error': 'Slide data not found. This presentation may have been generated in an older session.',
                'filename': filename
            }), 404
        
        with open(cache_path, 'r', encoding='utf-8') as f:
            slides_data = json.load(f)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'slides': slides_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/viewer/<filename>')
def viewer(filename):
    """Render the presentation viewer"""
    return render_template('viewer.html', filename=filename)


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated presentation"""
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 SlidesGPT FREE Edition - AI Slide Generator")
    print("=" * 60)
    print("� 100% FREE - No paid APIs required!")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"💾 Cache directory: {CACHE_DIR}")
    if generator:
        print(f"🎨 Available themes: {len(FreeSlideGenerator.THEMES)}")
    print(f"🖼️  Free images: Unsplash (unlimited)")
    print("🌐 Open http://localhost:5000 in your browser")
    print("=" * 60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
