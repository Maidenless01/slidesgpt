"""
Quick setup script for SlidesGPT
"""
import os
import sys

def setup():
    print("=" * 60)
    print("🚀 SlidesGPT Setup")
    print("=" * 60)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\n⚠️  No .env file found!")
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Get your Gemini API key from: https://aistudio.google.com/app/apikey")
        print("3. Add your API key to the .env file")
        print("\nExample .env file:")
        print("GEMINI_API_KEY=your-api-key-here")
        
        create_env = input("\n\nWould you like me to create a .env file now? (y/n): ")
        if create_env.lower() == 'y':
            api_key = input("Enter your Gemini API key: ").strip()
            with open('.env', 'w') as f:
                f.write(f"GEMINI_API_KEY={api_key}\n")
            print("✅ .env file created!")
    else:
        print("✅ .env file found")
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    print("✅ Output directory ready")
    
    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run web app: python app.py")
    print("3. Or use CLI: python slide_generator.py \"Your Topic\"")
    print("=" * 60)

if __name__ == '__main__':
    setup()
