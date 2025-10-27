import { useState, useEffect } from 'react'
import { generatePresentation, getDownloadUrl, getViewerUrl, APIError } from './api'

function App() {
  const [formData, setFormData] = useState({
    prompt: '',
    numSlides: 8,
    style: 'professional',
    audience: '',
    includeImages: false,
    useAiImages: false,  // NEW: AI image generation
    includeCode: false,
    theme: 'modern_blue',
  })

  const [themes, setThemes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  // Fetch available themes on mount
  useEffect(() => {
    const fetchThemes = async () => {
      try {
        const response = await fetch('/api/themes')
        const data = await response.json()
        if (data.themes) {
          setThemes(data.themes)
        }
      } catch (err) {
        console.error('Failed to fetch themes:', err)
      }
    }
    fetchThemes()
  }, [])

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.prompt.trim()) {
      setError({ message: 'Please enter a prompt for your presentation' })
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await generatePresentation(formData)
      setResult(data)
    } catch (err) {
      if (err instanceof APIError) {
        setError({
          message: err.message,
          details: err.details
        })
      } else {
        setError({
          message: 'An unexpected error occurred',
          details: err.toString()
        })
      }
    } finally {
      setLoading(false)
    }
  }

  const handleNewPresentation = () => {
    setResult(null)
    setError(null)
    setFormData(prev => ({ ...prev, prompt: '' }))
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🎨 SlidesGPT FREE</h1>
        <p>100% Free AI-Powered Presentation Generator</p>
        <p className="free-badge">✨ No Paid APIs • Smart Diagrams • AI Images • Free Themes</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="prompt">
            Presentation Prompt
          </label>
          <textarea
            id="prompt"
            name="prompt"
            value={formData.prompt}
            onChange={handleChange}
            placeholder="Describe your presentation in detail. Example: Create a comprehensive presentation about climate change for high school students, covering causes, effects, and solutions with engaging examples..."
            disabled={loading}
            rows={4}
          />
        </div>

        <div className="form-group">
          <label htmlFor="numSlides">
            Number of Slides
          </label>
          <input
            type="number"
            id="numSlides"
            name="numSlides"
            value={formData.numSlides}
            onChange={handleChange}
            min="3"
            max="30"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="style">
            Presentation Style
          </label>
          <select
            id="style"
            name="style"
            value={formData.style}
            onChange={handleChange}
            disabled={loading}
          >
            <option value="professional">Professional</option>
            <option value="educational">Educational</option>
            <option value="technical">Technical</option>
            <option value="creative">Creative</option>
            <option value="minimalist">Minimalist</option>
            <option value="playful">Playful</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="audience">
            Target Audience (Optional)
          </label>
          <input
            type="text"
            id="audience"
            name="audience"
            value={formData.audience}
            onChange={handleChange}
            placeholder="e.g., High school students, Business executives, Developers..."
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>
            🎨 Choose Theme
          </label>
          <div className="theme-grid">
            {themes.map(theme => (
              <div
                key={theme.id}
                className={`theme-card ${formData.theme === theme.id ? 'selected' : ''}`}
                onClick={() => setFormData(prev => ({ ...prev, theme: theme.id }))}
              >
                <div className="theme-colors">
                  <div className="color-bar" style={{ backgroundColor: theme.primary }}></div>
                  <div className="color-bar" style={{ backgroundColor: theme.secondary }}></div>
                  <div className="color-bar" style={{ backgroundColor: theme.accent }}></div>
                </div>
                <div className="theme-name">{theme.name}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="checkbox-group">
          <div className="checkbox-item">
            <input
              type="checkbox"
              id="includeImages"
              name="includeImages"
              checked={formData.includeImages}
              onChange={handleChange}
              disabled={loading || formData.useAiImages}
            />
            <label htmlFor="includeImages">
              🖼️ Include Free Stock Images (Unsplash)
            </label>
          </div>

          <div className="checkbox-item">
            <input
              type="checkbox"
              id="useAiImages"
              name="useAiImages"
              checked={formData.useAiImages}
              onChange={handleChange}
              disabled={loading}
            />
            <label htmlFor="useAiImages">
              🎨 Use AI-Generated Images (Pollinations.ai)
            </label>
          </div>

          <div className="checkbox-item">
            <input
              type="checkbox"
              id="includeCode"
              name="includeCode"
              checked={formData.includeCode}
              onChange={handleChange}
              disabled={loading}
            />
            <label htmlFor="includeCode">
              💻 Include Code Examples
            </label>
          </div>
        </div>

        <button 
          type="submit" 
          className="btn-primary"
          disabled={loading}
        >
          {loading ? 'Generating...' : '✨ Generate Presentation'}
        </button>
      </form>

      {loading && (
        <div className="progress">
          <div className="progress-message">
            🤖 AI is creating your presentation...
          </div>
          <div className="spinner"></div>
        </div>
      )}

      {error && (
        <div className="error">
          <h3>❌ Error</h3>
          <p>{error.message}</p>
          {error.details && (
            <details>
              <summary>Technical Details</summary>
              <pre>{error.details}</pre>
            </details>
          )}
        </div>
      )}

      {result && (
        <div className="success">
          <h3>✅ Presentation Created Successfully!</h3>
          <p>Your presentation has been generated with {result.num_slides} slides using the {result.theme.replace('_', ' ')} theme.</p>
          
          <div className="feature-notice">
            <strong>📊 What's included:</strong>
            <ul style={{textAlign: 'left', marginTop: '10px', lineHeight: '1.8'}}>
              <li>✅ AI-generated slide content and speaker notes</li>
              <li>✅ Professional theme with custom colors</li>
              {formData.useAiImages && <li>✅ <strong>AI-generated custom images</strong></li>}
              {formData.includeImages && !formData.useAiImages && <li>✅ <strong>Free stock photos</strong></li>}
              <li>✅ <strong>Interactive diagrams</strong> (flowcharts, timelines, comparisons, cycles, pyramids)</li>
              {formData.includeCode && <li>✅ <strong>Syntax-highlighted code examples</strong></li>}
            </ul>
            <p style={{marginTop: '15px', padding: '12px', background: 'rgba(102, 126, 234, 0.1)', borderRadius: '8px', fontSize: '0.95em'}}>
              💡 <strong>Note:</strong> The browser preview now shows <strong>diagrams and text</strong>. Download the PowerPoint file to see AI-generated images and full formatting!
            </p>
          </div>

          <div className="btn-group">
            <a
              href={getDownloadUrl(result.filename)}
              className="btn-secondary"
              download
              style={{fontSize: '1.1em', padding: '14px 28px'}}
            >
              📥 Download PowerPoint (Full Version)
            </a>
            <a
              href={getViewerUrl(result.filename, result.slides_data, result.theme)}
              className="btn-secondary"
              target="_blank"
              rel="noopener noreferrer"
              style={{fontSize: '1.1em', padding: '14px 28px'}}
            >
              👁️ Preview (Text + Diagrams)
            </a>
            <button
              onClick={handleNewPresentation}
              className="btn-secondary"
            >
              🆕 New Presentation
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
