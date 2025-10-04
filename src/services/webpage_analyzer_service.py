"""
Service for analyzing user's webpage to extract product/service information.
"""
import os
import logging
import re
from typing import Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime

logger = logging.getLogger(__name__)


def extract_webpage_content(url: str) -> Dict[str, Any]:
    """
    Extract content from a webpage.
    
    Args:
        url: URL of the webpage to analyze
        
    Returns:
        Dictionary with extracted content
    """
    try:
        # Add headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = '\n'.join(lines)
        
        # Limit to first 5000 characters for Gemini
        text = text[:5000]
        
        # Extract meta information
        title = soup.find('title')
        title_text = title.string if title else ''
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'] if meta_desc and 'content' in meta_desc.attrs else ''
        
        # Extract headings
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3']):
            heading_text = h.get_text(strip=True)
            if heading_text:
                headings.append(heading_text)
        
        return {
            'success': True,
            'url': url,
            'title': title_text,
            'description': description,
            'headings': headings[:10],  # Top 10 headings
            'content': text,
            'content_length': len(text)
        }
        
    except Exception as e:
        logger.error(f"Failed to extract webpage content from {url}: {str(e)}")
        return {
            'success': False,
            'url': url,
            'error': str(e)
        }


async def analyze_webpage_with_gemini(url: str) -> Dict[str, Any]:
    """
    Analyze a webpage using Gemini to extract product/service information.
    
    Args:
        url: URL of the webpage to analyze
        
    Returns:
        Dictionary with analyzed information
    """
    try:
        # Extract webpage content
        webpage_data = extract_webpage_content(url)
        
        if not webpage_data.get('success'):
            return {
                'success': False,
                'message': f"Failed to extract webpage: {webpage_data.get('error')}"
            }
        
        # Configure Gemini
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            return {
                'success': False,
                'message': "Gemini API key not configured"
            }
        
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create analysis prompt
        prompt = f"""
Analyze this webpage and extract detailed information about the product or service being offered.

URL: {url}
Title: {webpage_data.get('title', '')}
Meta Description: {webpage_data.get('description', '')}
Main Headings: {', '.join(webpage_data.get('headings', []))}

Webpage Content:
{webpage_data.get('content', '')}

Please provide a comprehensive analysis covering:

1. PRODUCT/SERVICE OVERVIEW:
   - What is the main product or service?
   - Key features and benefits
   - Unique value proposition

2. TARGET AUDIENCE:
   - Who is this for?
   - What problems does it solve?
   - Demographics and psychographics

3. BRAND IDENTITY:
   - Brand personality and tone
   - Visual style indicators
   - Brand messaging approach

4. KEY SELLING POINTS:
   - Main benefits emphasized
   - Competitive advantages
   - Social proof or credibility elements

5. DESIRED EMOTIONAL RESPONSE:
   - What feelings should the video evoke?
   - Aspirational elements
   - Pain points addressed

6. CALL-TO-ACTION:
   - What action should viewers take?
   - Urgency or incentive elements

7. VIDEO DIRECTION RECOMMENDATIONS:
   - Suggested visual style based on brand
   - Key scenes or moments to include
   - Tone and pacing suggestions

Please be specific and detailed, extracting actual information from the webpage content.
"""
        
        # Generate analysis
        response = model.generate_content(prompt)
        
        if not response.text:
            return {
                'success': False,
                'message': "Gemini returned empty response"
            }
        
        logger.info(f"Successfully analyzed webpage: {url}")
        
        return {
            'success': True,
            'url': url,
            'webpage_data': {
                'title': webpage_data.get('title', ''),
                'description': webpage_data.get('description', ''),
                'headings': webpage_data.get('headings', [])
            },
            'analysis': response.text,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Webpage analysis failed for {url}: {str(e)}")
        return {
            'success': False,
            'message': f"Analysis failed: {str(e)}",
            'error': str(e)
        }


def is_valid_url(text: str) -> bool:
    """
    Check if text contains or is a valid URL.
    
    Args:
        text: Text to check
        
    Returns:
        True if text contains a valid URL
    """
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return bool(url_pattern.search(text))


def extract_url_from_text(text: str) -> Optional[str]:
    """
    Extract URL from text.
    
    Args:
        text: Text containing URL
        
    Returns:
        Extracted URL or None
    """
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    match = url_pattern.search(text)
    return match.group(0) if match else None

