import os
import sys
import logging
import google.generativeai as genai
from google.generativeai.types import File
from typing import Optional, List, Dict, Any
from datetime import datetime

# Set up logger
logger = logging.getLogger(__name__)

GEMINI_API_KEY = None

def get_gemini_api_key() -> str:
    """
    Get Gemini API key from command line arguments or environment variable.
    Caches the key in memory after first read.
    Priority: command line argument > environment variable

    Returns:
        str: The Gemini API key.

    Raises:
        Exception: If no key is provided in command line arguments or environment.
    """
    global GEMINI_API_KEY
    if GEMINI_API_KEY is None:
        # Try command line argument first
        if "--gemini-api-key" in sys.argv:
            token_index = sys.argv.index("--gemini-api-key") + 1
            if token_index < len(sys.argv):
                GEMINI_API_KEY = sys.argv[token_index]
                logger.info(f"Using Gemini API key from command line arguments")
            else:
                raise Exception("--gemini-api-key argument provided but no key value followed it")
        # Try environment variable
        elif os.getenv("GEMINI_API_KEY"):
            GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
            logger.info(f"Using Gemini API key from environment variable")
        else:
            raise Exception("Gemini API key must be provided via '--gemini-api-key' command line argument or 'GEMINI_API_KEY' environment variable")

    return GEMINI_API_KEY


def configure_gemini() -> genai.GenerativeModel:
    """
    Configure Gemini API with the API key and return a model instance.
    
    Returns:
        genai.GenerativeModel: Configured Gemini model instance for video analysis
    """
    api_key = get_gemini_api_key()
    genai.configure(api_key=api_key)
    
    # Use Gemini 2.0 Flash for video analysis (more cost-effective than Pro)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    logger.info("Gemini API configured successfully")
    return model


def upload_video_to_gemini(video_path: str) -> File:
    """
    Upload a video file to Gemini File API for analysis.
    
    Args:
        video_path: Path to the video file to upload
        
    Returns:
        genai.File: The uploaded file object for use in analysis
        
    Raises:
        Exception: If upload fails
    """
    try:
        # Upload video file
        video_file = genai.upload_file(path=video_path)
        
        # Wait for processing to complete
        import time
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            video_file = genai.get_file(video_file.name)
        
        if video_file.state.name == "FAILED":
            raise Exception(f"Video processing failed: {video_file.state}")
            
        logger.info(f"Video uploaded successfully: {video_file.name}")
        return video_file
        
    except Exception as e:
        logger.error(f"Failed to upload video to Gemini: {str(e)}")
        raise


def _analyze_video_with_model(model: genai.GenerativeModel, video_file: File, prompt: str) -> str:
    """
    Analyze a video using Gemini with a custom prompt (internal helper function).
    
    Args:
        model: Configured Gemini model instance
        video_file: Uploaded video file from Gemini File API
        prompt: Analysis prompt for the video
        
    Returns:
        str: Analysis results from Gemini
        
    Raises:
        Exception: If analysis fails
    """
    try:
        # Generate analysis
        response = model.generate_content([video_file, prompt])
        
        if not response.text:
            raise Exception("Gemini returned empty response")
            
        logger.info("Video analysis completed successfully")
        return response.text
        
    except Exception as e:
        logger.error(f"Video analysis failed: {str(e)}")
        raise


def analyze_videos_batch_with_gemini(model: genai.GenerativeModel, video_files: List[File], prompt_template: str, video_contexts: List[Dict[str, Any]]) -> List[str]:
    """
    Analyze multiple videos using Gemini in a single request for token efficiency.
    
    Args:
        model: Configured Gemini model instance
        video_files: List of uploaded video files from Gemini File API
        prompt_template: Base analysis prompt template
        video_contexts: List of context dicts with brand_name, ad_id, etc. for each video
        
    Returns:
        List[str]: Analysis results for each video in order
        
    Raises:
        Exception: If batch analysis fails
    """
    try:
        if not video_files or len(video_files) != len(video_contexts):
            raise Exception("Video files and contexts must have matching lengths")
        
        # Create batch prompt with multiple videos
        batch_prompt = f"""Analyze the following {len(video_files)} Facebook ad videos. For each video, provide analysis following this format:

{prompt_template}

Please analyze each video separately and clearly label each analysis as "VIDEO 1:", "VIDEO 2:", etc.

"""
        
        # Add context information for each video
        for i, context in enumerate(video_contexts, 1):
            brand_info = f" (Brand: {context.get('brand_name', 'Unknown')})" if context.get('brand_name') else ""
            ad_info = f" (Ad ID: {context.get('ad_id', 'Unknown')})" if context.get('ad_id') else ""
            batch_prompt += f"VIDEO {i}{brand_info}{ad_info}:\n"
        
        # Combine all video files with the prompt
        content_parts = [batch_prompt] + video_files
        
        # Generate batch analysis
        response = model.generate_content(content_parts)
        
        if not response.text:
            raise Exception("Gemini returned empty response for batch analysis")
        
        # Split response by video markers
        analysis_text = response.text
        video_analyses = []
        
        # Parse individual video analyses
        for i in range(1, len(video_files) + 1):
            video_marker = f"VIDEO {i}:"
            next_marker = f"VIDEO {i + 1}:" if i < len(video_files) else None
            
            start_idx = analysis_text.find(video_marker)
            if start_idx == -1:
                logger.warning(f"Could not find analysis for VIDEO {i}")
                video_analyses.append(f"Analysis not found in batch response for video {i}")
                continue
                
            start_idx += len(video_marker)
            
            if next_marker:
                end_idx = analysis_text.find(next_marker)
                individual_analysis = analysis_text[start_idx:end_idx].strip() if end_idx != -1 else analysis_text[start_idx:].strip()
            else:
                individual_analysis = analysis_text[start_idx:].strip()
            
            video_analyses.append(individual_analysis)
        
        logger.info(f"Batch video analysis completed successfully for {len(video_files)} videos")
        return video_analyses
        
    except Exception as e:
        logger.error(f"Batch video analysis failed: {str(e)}")
        raise


def upload_videos_batch_to_gemini(video_paths: List[str]) -> List[File]:
    """
    Upload multiple video files to Gemini File API for batch analysis.
    
    Args:
        video_paths: List of paths to video files to upload
        
    Returns:
        List[genai.File]: List of uploaded file objects for use in analysis
        
    Raises:
        Exception: If any upload fails
    """
    uploaded_files = []
    failed_uploads = []
    
    try:
        for i, video_path in enumerate(video_paths):
            try:
                # Upload video file
                video_file = genai.upload_file(path=video_path)
                
                # Wait for processing to complete
                import time
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)
                
                if video_file.state.name == "FAILED":
                    failed_uploads.append(f"Video {i+1}: {video_file.state}")
                    continue
                    
                uploaded_files.append(video_file)
                logger.info(f"Video {i+1} uploaded successfully: {video_file.name}")
                
            except Exception as e:
                failed_uploads.append(f"Video {i+1}: {str(e)}")
                logger.error(f"Failed to upload video {i+1} at {video_path}: {str(e)}")
        
        if failed_uploads:
            error_msg = f"Some video uploads failed: {'; '.join(failed_uploads)}"
            if not uploaded_files:  # All uploads failed
                raise Exception(error_msg)
            else:  # Partial failure
                logger.warning(error_msg)
        
        return uploaded_files
        
    except Exception as e:
        # Cleanup any successfully uploaded files on total failure
        for uploaded_file in uploaded_files:
            try:
                cleanup_gemini_file(uploaded_file.name)
            except:
                pass
        raise


def cleanup_gemini_files_batch(file_names: List[str]):
    """
    Delete multiple files from Gemini File API to free up storage.
    
    Args:
        file_names: List of file names to delete
    """
    for file_name in file_names:
        try:
            genai.delete_file(file_name)
            logger.info(f"Cleaned up Gemini file: {file_name}")
        except Exception as e:
            logger.warning(f"Failed to cleanup Gemini file {file_name}: {str(e)}")


def cleanup_gemini_file(file_name: str):
    """
    Delete a file from Gemini File API to free up storage.
    
    Args:
        file_name: Name of the file to delete
    """
    try:
        genai.delete_file(file_name)
        logger.info(f"Cleaned up Gemini file: {file_name}")
    except Exception as e:
        logger.warning(f"Failed to cleanup Gemini file {file_name}: {str(e)}")


async def analyze_video_with_gemini(media_url: str, brand_name: str = None, ad_id: str = None) -> Dict[str, Any]:
    """
    Analyze a video from URL using Gemini.
    
    Args:
        media_url: URL of the video to analyze
        brand_name: Optional brand name for context
        ad_id: Optional ad ID for context
        
    Returns:
        Dict with analysis results
    """
    import requests
    import tempfile
    
    try:
        # Check if we have Gemini API key
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            raise Exception("Gemini API key not configured")
        
        # Configure Gemini model
        model = configure_gemini()
        
        # Download video
        
        response = requests.get(media_url.strip(), timeout=30)
        response.raise_for_status()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_file.write(response.content)
            video_path = temp_file.name
        
        try:
            # Upload video to Gemini
            video_file = upload_video_to_gemini(video_path)
            
            # Create analysis prompt
            prompt = f"""
            Analyze this Facebook ad video in detail. Focus on:
            
            1. Visual elements and composition
            2. Brand messaging and positioning
            3. Call-to-action strategies
            4. Target audience appeal
            5. Emotional triggers used
            6. Product/service presentation
            7. Visual storytelling techniques
            8. Color schemes and visual style
            9. Text overlays and graphics
            10. Overall effectiveness and engagement potential
            
            Brand: {brand_name or 'Unknown'}
            Ad ID: {ad_id or 'Unknown'}
            
            Provide a comprehensive analysis that would be useful for creating similar effective video content.
            """
            
            # Analyze video
            analysis_text = _analyze_video_with_model(model, video_file, prompt)
            
            # Get file metadata
            file_size_mb = round(len(response.content) / (1024 * 1024), 2)
            
            # Cleanup
            cleanup_gemini_file(video_file.name)
            
            return {
                "success": True,
                "analysis": {
                    "raw_analysis": analysis_text,
                    "brand_name": brand_name,
                    "ad_id": ad_id,
                    "media_url": media_url
                },
                "video_metadata": {
                    "file_size_mb": file_size_mb,
                    "duration_seconds": None  # Could be extracted with ffmpeg
                },
                "model_used": "gemini-1.5-pro",
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        finally:
            # Cleanup temporary file
            try:
                os.unlink(video_path)
            except:
                pass
                
    except Exception as e:
        logger.error(f"Video analysis failed for {media_url}: {str(e)}")
        return {
            "success": False,
            "message": f"Analysis failed: {str(e)}",
            "error": str(e)
        }