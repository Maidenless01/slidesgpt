"""Test script to generate a simple presentation"""
from slide_generator import SlideGenerator

generator = SlideGenerator()

try:
    output_path, slides_data = generator.generate_presentation(
        topic="Create a 3-slide presentation about Python basics",
        num_slides=3,
        output_file="test.pptx",
        include_images=False,
        include_code=False,
        style="educational",
        audience="beginners"
    )
    print(f"✅ Success! Created {output_path}")
except Exception as e:
    print(f"❌ Failed: {e}")
