/**
 * API client for SlidesGPT backend
 */

export class APIError extends Error {
  constructor(message, details) {
    super(message);
    this.name = 'APIError';
    this.details = details;
  }
}

export async function generatePresentation(formData) {
  try {
    const response = await fetch('/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: formData.prompt,
        num_slides: parseInt(formData.numSlides),
        style: formData.style,
        audience: formData.audience,
        include_images: formData.includeImages,
        include_code: formData.includeCode,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new APIError(
        `Server error: ${response.status} ${response.statusText}`,
        errorText
      );
    }

    const data = await response.json();
    
    if (data.error) {
      throw new APIError('Generation failed', data.error);
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    
    // Network or JSON parsing error
    throw new APIError(
      'Failed to connect to server or parse response',
      error.message
    );
  }
}

export function getDownloadUrl(filename) {
  return `/download/${encodeURIComponent(filename)}`;
}

export function getViewerUrl(filename, slidesData) {
  // Pass slides data as JSON string in URL parameter
  // Note: We only encode the JSON once, the browser will decode it
  const slidesJson = JSON.stringify(slidesData);
  return `/viewer/${encodeURIComponent(filename)}?slides=${encodeURIComponent(slidesJson)}`;
}
