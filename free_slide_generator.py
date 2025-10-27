import os
import json
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from dotenv import load_dotenv
import google.generativeai as genai
import hashlib
import urllib.parse

load_dotenv()

class FreeSlideGenerator:
    """Free-tier slide generator using only free APIs"""
    
    THEMES = {
        "modern_blue": {
            "name": "Modern Blue",
            "primary": RGBColor(33, 150, 243),
            "secondary": RGBColor(13, 71, 161),
            "accent": RGBColor(255, 193, 7),
            "background": RGBColor(250, 250, 250),
            "text": RGBColor(33, 33, 33),
        },
        "corporate_gray": {
            "name": "Corporate Gray",
            "primary": RGBColor(66, 66, 66),
            "secondary": RGBColor(33, 33, 33),
            "accent": RGBColor(0, 188, 212),
            "background": RGBColor(245, 245, 245),
            "text": RGBColor(66, 66, 66),
        },
        "creative_purple": {
            "name": "Creative Purple",
            "primary": RGBColor(156, 39, 176),
            "secondary": RGBColor(74, 20, 140),
            "accent": RGBColor(255, 235, 59),
            "background": RGBColor(252, 252, 252),
            "text": RGBColor(33, 33, 33),
        },
        "tech_dark": {
            "name": "Tech Dark",
            "primary": RGBColor(0, 188, 212),
            "secondary": RGBColor(0, 150, 136),
            "accent": RGBColor(255, 64, 129),
            "background": RGBColor(18, 18, 18),
            "text": RGBColor(255, 255, 255),
        },
        "elegant_gold": {
            "name": "Elegant Gold",
            "primary": RGBColor(139, 116, 61),
            "secondary": RGBColor(101, 84, 44),
            "accent": RGBColor(255, 215, 0),
            "background": RGBColor(255, 255, 255),
            "text": RGBColor(51, 51, 51),
        },
        "nature_green": {
            "name": "Nature Green",
            "primary": RGBColor(76, 175, 80),
            "secondary": RGBColor(27, 94, 32),
            "accent": RGBColor(255, 193, 7),
            "background": RGBColor(250, 250, 250),
            "text": RGBColor(33, 33, 33),
        },
        "vibrant_orange": {
            "name": "Vibrant Orange",
            "primary": RGBColor(255, 87, 34),
            "secondary": RGBColor(230, 74, 25),
            "accent": RGBColor(255, 193, 7),
            "background": RGBColor(255, 255, 255),
            "text": RGBColor(33, 33, 33),
        },
        "minimal_mono": {
            "name": "Minimal Monochrome",
            "primary": RGBColor(0, 0, 0),
            "secondary": RGBColor(97, 97, 97),
            "accent": RGBColor(189, 189, 189),
            "background": RGBColor(255, 255, 255),
            "text": RGBColor(33, 33, 33),
        },
        "sunset_gradient": {
            "name": "Sunset Gradient",
            "primary": RGBColor(255, 94, 77),
            "secondary": RGBColor(255, 145, 77),
            "accent": RGBColor(255, 209, 102),
            "background": RGBColor(255, 250, 245),
            "text": RGBColor(51, 51, 51),
        },
        "ocean_blue": {
            "name": "Ocean Blue",
            "primary": RGBColor(3, 169, 244),
            "secondary": RGBColor(1, 87, 155),
            "accent": RGBColor(0, 188, 212),
            "background": RGBColor(240, 248, 255),
            "text": RGBColor(33, 33, 33),
        }
    }
    
    def __init__(self, gemini_api_key=None):
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        self.cache_dir = "cache"
        self.image_cache_dir = "cache/images"
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.image_cache_dir, exist_ok=True)
    
    def get_free_image(self, search_query, width=800, height=600):
        """
        Get free images from Unsplash API (free tier: unlimited)
        """
        try:
            # Check cache first
            cache_key = hashlib.md5(f"{search_query}_{width}_{height}".encode()).hexdigest()
            cache_path = os.path.join(self.image_cache_dir, f"{cache_key}.jpg")
            
            if os.path.exists(cache_path):
                print(f"✅ Using cached image for: {search_query}")
                return cache_path
            
            print(f"🔍 Searching free image: {search_query}")
            
            # Unsplash Source (No API key needed!)
            encoded_query = urllib.parse.quote(search_query)
            url = f"https://source.unsplash.com/{width}x{height}/?{encoded_query}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.save(cache_path, 'JPEG')
                print(f"✅ Downloaded and cached image")
                return cache_path
            else:
                print(f"⚠️  Image download failed, creating placeholder")
                return self.create_placeholder_image(search_query, width, height, cache_path)
                
        except Exception as e:
            print(f"⚠️  Image fetch error: {e}, creating placeholder")
            return self.create_placeholder_image(search_query, width, height, cache_path)
    
    def create_placeholder_image(self, text, width, height, save_path):
        """Create a nice placeholder image with gradient and text"""
        img = Image.new('RGB', (width, height), color=(240, 240, 245))
        draw = ImageDraw.Draw(img)
        
        # Create gradient background
        for y in range(height):
            r = int(100 + (155 * y / height))
            g = int(150 + (105 * y / height))
            b = int(200 + (55 * y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add text
        try:
            # Try to use a nice font
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 30:
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw text centered
        y_offset = height // 2 - (len(lines) * 25)
        for line in lines[:3]:  # Max 3 lines
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            
            # Draw shadow
            draw.text((x+2, y_offset+2), line, fill=(0, 0, 0, 128), font=font)
            # Draw text
            draw.text((x, y_offset), line, fill=(255, 255, 255), font=font)
            y_offset += 50
        
        img.save(save_path, 'JPEG')
        return save_path
    
    def generate_slide_content(self, prompt, num_slides, style, audience, include_code, include_images, theme="modern_blue"):
        """Generate slide content using Gemini (100% free)"""
        
        extra_fields = []
        if include_images:
            extra_fields.append('"image_search": "short search query for free stock photo"')
        if include_code:
            extra_fields.append('"code": "code example here"')
        
        json_example = '{' + ','.join([
            '"title": "Slide Title"',
            '"bullets": ["Point 1", "Point 2", "Point 3"]',
            '"notes": "Speaker notes"'
        ] + extra_fields) + '}'
        
        ai_prompt = f'''Create a {num_slides}-slide presentation based on this prompt:

{prompt}

STYLE: {style}
AUDIENCE: {audience or "General audience"}
THEME: {self.THEMES[theme]["name"]}

Generate {num_slides} slides in valid JSON format. Each slide should have:
- title: Clear, engaging title
- bullets: 3-5 concise bullet points
- notes: Detailed speaker notes
{"- image_search: SHORT search query for free stock photos (2-4 words max)" if include_images else ""}
{"- code: Relevant code example with proper syntax" if include_code else ""}

Return ONLY a JSON object like:
{{
  "slides": [
    {json_example},
    {json_example}
  ]
}}

Make the content engaging, well-structured, and appropriate for the theme and audience.
For image_search queries, use simple, generic terms like "technology", "team meeting", "data analytics".'''

        try:
            print(f"🤖 Generating content with Gemini ({theme} theme)...")
            response = self.model.generate_content(ai_prompt)
            
            # Clean and parse JSON
            content = response.text.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
            
            if "slides" not in data:
                raise ValueError("Response missing 'slides' key")
            
            print(f"✅ Generated {len(data['slides'])} slides")
            return data["slides"]
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Response content: {content[:500]}")
            raise
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
    
    def create_presentation(self, slides_data, output_path, theme="modern_blue", use_images=False):
        """Create PowerPoint with free images from Unsplash"""
        
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        
        theme_config = self.THEMES[theme]
        
        print(f"🎨 Creating presentation with {theme_config['name']} theme...")
        
        for idx, slide_data in enumerate(slides_data):
            print(f"📄 Processing slide {idx + 1}/{len(slides_data)}: {slide_data.get('title', 'Untitled')}")
            
            # Create blank slide
            blank_layout = prs.slide_layouts[6]
            slide = prs.slides.add_slide(blank_layout)
            
            # Add background
            background = slide.background
            fill = background.fill
            fill.solid()
            fill.fore_color.rgb = theme_config['background']
            
            # Title
            title_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(0.3), Inches(9), Inches(1)
            )
            title_frame = title_box.text_frame
            title_frame.text = slide_data.get('title', 'Untitled')
            
            title_p = title_frame.paragraphs[0]
            title_p.font.size = Pt(44)
            title_p.font.bold = True
            title_p.font.color.rgb = theme_config['primary']
            
            # Decorative line
            line = slide.shapes.add_shape(
                1,  # Line shape
                Inches(0.5), Inches(1.4), Inches(9), Inches(0)
            )
            line.line.color.rgb = theme_config['accent']
            line.line.width = Pt(3)
            
            content_top = 1.7
            content_left = 0.5
            content_width = 9
            
            # Get free image if requested
            image_path = None
            if use_images and 'image_search' in slide_data and slide_data['image_search']:
                image_path = self.get_free_image(slide_data['image_search'], 800, 600)
            
            if image_path and os.path.exists(image_path):
                # Two-column layout
                content_width = 5
                
                try:
                    slide.shapes.add_picture(
                        image_path,
                        Inches(6), Inches(content_top),
                        width=Inches(3.5), height=Inches(4)
                    )
                except Exception as e:
                    print(f"⚠️  Could not add image: {e}")
            
            # Content bullets
            if slide_data.get('bullets'):
                text_box = slide.shapes.add_textbox(
                    Inches(content_left), Inches(content_top),
                    Inches(content_width), Inches(4.5)
                )
                text_frame = text_box.text_frame
                text_frame.word_wrap = True
                
                for bullet in slide_data['bullets']:
                    p = text_frame.add_paragraph()
                    p.text = bullet
                    p.level = 0
                    p.font.size = Pt(20)
                    p.font.color.rgb = theme_config['text']
                    p.space_before = Pt(12)
            
            # Code block
            if 'code' in slide_data and slide_data['code']:
                code_box = slide.shapes.add_textbox(
                    Inches(content_left), Inches(5.5),
                    Inches(content_width), Inches(1.5)
                )
                code_frame = code_box.text_frame
                code_frame.text = slide_data['code']
                
                code_p = code_frame.paragraphs[0]
                code_p.font.size = Pt(14)
                code_p.font.name = "Courier New"
                code_p.font.color.rgb = RGBColor(248, 248, 242)
                
                # Code background
                code_fill = code_box.fill
                code_fill.solid()
                code_fill.fore_color.rgb = RGBColor(40, 42, 54)
            
            # Speaker notes
            if slide_data.get('notes'):
                notes_slide = slide.notes_slide
                notes_frame = notes_slide.notes_text_frame
                notes_frame.text = slide_data['notes']
        
        prs.save(output_path)
        print(f"✅ Saved presentation: {output_path}")
    
    def generate_presentation(self, prompt, num_slides, output_path, **options):
        """Generate complete presentation - 100% FREE"""
        
        style = options.get('style', 'professional')
        audience = options.get('audience', '')
        include_code = options.get('include_code', False)
        include_images = options.get('include_images', False)
        theme = options.get('theme', 'modern_blue')
        
        # Generate content (FREE - Gemini)
        slides_data = self.generate_slide_content(
            prompt, num_slides, style, audience, include_code, include_images, theme
        )
        
        # Save slides data to cache
        cache_filename = os.path.basename(output_path).replace('.pptx', '.json')
        cache_path = os.path.join(self.cache_dir, cache_filename)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(slides_data, f, indent=2, ensure_ascii=False)
        
        # Create presentation with FREE images
        self.create_presentation(slides_data, output_path, theme, include_images)
        
        return {
            'success': True,
            'output_path': output_path,
            'slides_data': slides_data,
            'theme': theme,
            'num_slides': len(slides_data)
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Free AI Slide Generator')
    parser.add_argument('prompt', help='Presentation prompt/topic')
    parser.add_argument('--slides', type=int, default=8, help='Number of slides')
    parser.add_argument('--output', default='presentation.pptx', help='Output file')
    parser.add_argument('--theme', default='modern_blue', choices=list(FreeSlideGenerator.THEMES.keys()))
    parser.add_argument('--style', default='professional')
    parser.add_argument('--audience', default='')
    parser.add_argument('--code', action='store_true', help='Include code examples')
    parser.add_argument('--images', action='store_true', help='Include free images')
    
    args = parser.parse_args()
    
    generator = FreeSlideGenerator()
    
    result = generator.generate_presentation(
        args.prompt,
        args.slides,
        args.output,
        style=args.style,
        audience=args.audience,
        include_code=args.code,
        include_images=args.images,
        theme=args.theme
    )
    
    print(f"\n🎉 Success! Created {result['num_slides']} slides with {result['theme']} theme")
    print(f"📁 Saved to: {result['output_path']}")
