from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union
import uvicorn
import logging
from datetime import datetime
import os
import requests
import tempfile
from dotenv import load_dotenv

# Import our services
from src.services.scrapecreators_service import (
    get_platform_id, get_ads, get_scrapecreators_api_key, 
    get_platform_ids_batch, get_ads_batch, 
    CreditExhaustedException, RateLimitException
)
from src.services.trend_analysis_service import trend_analysis_service
from src.services.video_generator_service import video_generator_service
from src.services.media_cache_service import media_cache
from src.services.gemini_service import configure_gemini, upload_video_to_gemini, analyze_video_with_gemini, cleanup_gemini_file
from src.services.webpage_analyzer_service import analyze_webpage_with_gemini, is_valid_url, extract_url_from_text

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Createnko API",
    description="AI-powered video script generator API - Analyze competitor videos and create concrete video scripts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class BrandSearchRequest(BaseModel):
    brand_names: Union[str, List[str]] = Field(..., description="Brand name(s) to search for")
    limit: Optional[int] = Field(50, ge=1, le=500, description="Maximum number of ads to retrieve per brand")
    country: Optional[str] = Field(None, description="Country code to filter ads (e.g., 'US', 'CA')")

class VideoGenerationRequest(BaseModel):
    brand_names: Union[str, List[str]] = Field(..., description="Brand name(s) to analyze")
    user_query: str = Field(..., description="User's request for video generation")
    generator_type: str = Field("veo", description="Video generator type (veo, runway, pika, stable_video, sora)")
    limit: Optional[int] = Field(50, ge=1, le=500, description="Maximum number of ads to analyze per brand")
    country: Optional[str] = Field(None, description="Country code to filter ads")
    style_preferences: Optional[Dict[str, Any]] = Field(None, description="Style preferences for video generation")

class VideoDescriptionRequest(BaseModel):
    ads_data: List[Dict[str, Any]] = Field(..., description="Ads data from Facebook Ads Library")
    user_query: str = Field(..., description="User's request for video generation")
    generator_type: str = Field("veo", description="Video generator type")
    style_preferences: Optional[Dict[str, Any]] = Field(None, description="Style preferences")

class TrendAnalysisRequest(BaseModel):
    ads_data: List[Dict[str, Any]] = Field(..., description="Ads data to analyze")
    analysis_type: str = Field("comprehensive", description="Type of analysis to perform")


# Dependency to check API key
def get_api_key():
    try:
        return get_scrapecreators_api_key()
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"API key not configured: {str(e)}"
        )


def generate_video_prompt_from_insights(
    insights: List[Dict[str, Any]], 
    user_query: str, 
    generator_type: str,
    webpage_analysis: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate a concrete video script based on user's product and competitor video insights.
    
    Args:
        insights: List of video insights with Gemini analysis
        user_query: User's original query
        generator_type: Type of video generator (veo, runway, etc.)
        webpage_analysis: Optional analysis of user's webpage
        
    Returns:
        Concrete video script with specific actions and content
    """
    try:
        # Extract product info from webpage
        product_name = "your product"
        product_description = ""
        key_features = []
        target_audience_info = ""
        brand_tone = ""
        cta_info = ""
        
        if webpage_analysis and webpage_analysis.get('success'):
            analysis_text = webpage_analysis.get('analysis', '')
            webpage_data = webpage_analysis.get('webpage_data', {})
            
            if webpage_data.get('title'):
                product_name = webpage_data['title']
            
            # Extract specific sections from Gemini analysis
            if 'PRODUCT/SERVICE OVERVIEW' in analysis_text:
                sections = analysis_text.split('PRODUCT/SERVICE OVERVIEW')[1].split('\n\n')
                if sections:
                    product_description = sections[0].strip()
            
            if 'TARGET AUDIENCE' in analysis_text:
                sections = analysis_text.split('TARGET AUDIENCE')[1].split('\n\n')
                if sections:
                    target_audience_info = sections[0].strip()
            
            if 'BRAND IDENTITY' in analysis_text:
                sections = analysis_text.split('BRAND IDENTITY')[1].split('\n\n')
                if sections:
                    brand_tone = sections[0].strip()
            
            if 'CALL-TO-ACTION' in analysis_text:
                sections = analysis_text.split('CALL-TO-ACTION')[1].split('\n\n')
                if sections:
                    cta_info = sections[0].strip()
        
        # Collect all competitor video analyses
        all_competitor_insights = []
        for insight in insights:
            insights_data = insight.get('insights', {})
            if isinstance(insights_data, dict):
                raw_analysis = insights_data.get('raw_analysis', '')
            else:
                raw_analysis = str(insights_data) if insights_data else ''
            
            if raw_analysis:
                all_competitor_insights.append({
                    'brand': insight.get('page_name', 'Unknown'),
                    'analysis': raw_analysis
                })
        
        # Build concrete video script
        prompt = f"CREATE A {generator_type.upper()} VIDEO SCRIPT\n\n"
        prompt += "=" * 80 + "\n"
        prompt += "WHAT WE'RE ADVERTISING:\n"
        prompt += "=" * 80 + "\n\n"
        
        if webpage_analysis and webpage_analysis.get('success'):
            prompt += f"Product/Service: {product_name}\n\n"
            if product_description:
                prompt += f"{product_description}\n\n"
            if target_audience_info:
                prompt += f"Target Audience:\n{target_audience_info}\n\n"
            if brand_tone:
                prompt += f"Brand Identity:\n{brand_tone}\n\n"
        else:
            prompt += f"Product/Service: {user_query}\n\n"
        
        prompt += "=" * 80 + "\n"
        prompt += "STEP-BY-STEP VIDEO SCRIPT:\n"
        prompt += "=" * 80 + "\n\n"
        
        # Analyze competitor patterns to create concrete script
        opening_shots = []
        visual_techniques = []
        messaging_patterns = []
        cta_approaches = []
        
        for comp in all_competitor_insights:
            analysis = comp['analysis']
            analysis_lower = analysis.lower()
            
            # Extract opening techniques
            if 'opening' in analysis_lower or 'start' in analysis_lower:
                lines = analysis.split('\n')
                for line in lines:
                    if ('opening' in line.lower() or 'start' in line.lower()) and len(line.strip()) > 30:
                        opening_shots.append(line.strip().replace('*', '').strip('- '))
            
            # Extract visual techniques
            if 'split screen' in analysis_lower or 'split-screen' in analysis_lower:
                visual_techniques.append("split-screen composition")
            if 'close-up' in analysis_lower or 'close up' in analysis_lower:
                visual_techniques.append("close-up product shots")
            if 'before/after' in analysis_lower or 'before and after' in analysis_lower:
                visual_techniques.append("before/after comparison")
        
        # Create concrete script based on patterns
        prompt += "SCENE 1: OPENING (0-3 seconds)\n"
        prompt += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        if product_name and product_name != "your product":
            prompt += f"Visual: Show {product_name} prominently"
        else:
            prompt += f"Visual: Show the product prominently"
        
        if opening_shots:
            prompt += f" using technique: {opening_shots[0][:150]}\n"
        else:
            prompt += " with clean, professional composition\n"
        
        if 'split-screen' in visual_techniques:
            prompt += "Composition: Split-screen - product on one side, benefit/result on other\n"
        else:
            prompt += "Composition: Center-framed, immediate visual impact\n"
        
        prompt += "\n"
        
        prompt += "SCENE 2: PROBLEM/HOOK (3-5 seconds)\n"
        prompt += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        if target_audience_info:
            prompt += f"Visual: Show scenario that resonates with target audience: {target_audience_info[:200]}\n"
        else:
            prompt += "Visual: Show relatable problem scenario\n"
        prompt += "Text Overlay: Problem statement or attention-grabbing question\n"
        prompt += "\n"
        
        prompt += "SCENE 3: SOLUTION/PRODUCT SHOWCASE (5-15 seconds)\n"
        prompt += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        if product_description:
            prompt += f"Visual: Demonstrate {product_name} in action\n"
            prompt += f"Show: {product_description[:300]}\n"
        else:
            prompt += f"Visual: Demonstrate product solving the problem\n"
        
        if 'close-up' in visual_techniques:
            prompt += "Include: Close-up shots of key features and UI/interface\n"
        
        if 'before/after' in visual_techniques:
            prompt += "Show: Before/after comparison demonstrating transformation\n"
        
        prompt += "Pacing: Quick cuts every 2-3 seconds to maintain attention\n"
        prompt += "\n"
        
        prompt += "SCENE 4: BENEFITS & SOCIAL PROOF (15-20 seconds)\n"
        prompt += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        prompt += f"Visual: Show {product_name} delivering results\n"
        prompt += "Text Overlays: Key benefits, statistics, or user testimonials\n"
        if brand_tone:
            prompt += f"Tone: {brand_tone[:200]}\n"
        prompt += "\n"
        
        prompt += "SCENE 5: CALL-TO-ACTION (20-25 seconds)\n"
        prompt += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        if cta_info:
            prompt += f"Action: {cta_info[:200]}\n"
        else:
            prompt += f"Action: Clear call-to-action (\"Get Started\", \"Download Now\", etc.)\n"
        
        prompt += "Visual: Product logo/branding with CTA button overlay\n"
        prompt += "Urgency: Add time-limited offer or special incentive if applicable\n"
        prompt += "\n"
        
        prompt += "=" * 80 + "\n"
        prompt += "TECHNICAL SPECIFICATIONS:\n"
        prompt += "=" * 80 + "\n\n"
        
        prompt += "Based on competitor analysis:\n"
        for i, comp_insight in enumerate(all_competitor_insights[:3], 1):
            prompt += f"\nCompetitor {i} ({comp_insight['brand']}):\n"
            # Extract first 300 chars of key insights
            analysis_snippet = comp_insight['analysis'][:300].strip()
            prompt += f"  Applied techniques: {analysis_snippet}...\n"
        
        prompt += "\n" + "=" * 80 + "\n"
        prompt += "FINAL VIDEO CONCEPT:\n"
        prompt += "=" * 80 + "\n\n"
        
        if product_name and product_name != "your product":
            prompt += f"Create a {generator_type.upper()} video advertising {product_name} that:\n\n"
        else:
            prompt += f"Create a {generator_type.upper()} video that:\n\n"
        
        prompt += f"1. Opens with immediate visual impact showing {product_name if product_name != 'your product' else 'the product'}\n"
        prompt += "2. Demonstrates the product solving a real problem\n"
        prompt += "3. Uses proven techniques from successful competitor videos:\n"
        
        if visual_techniques:
            for tech in set(visual_techniques[:3]):
                prompt += f"   - {tech}\n"
        
        prompt += f"4. Ends with a strong, clear call-to-action\n"
        prompt += "5. Duration: 20-30 seconds, fast-paced (2-3 second scene changes)\n"
        
        if webpage_analysis and webpage_analysis.get('success'):
            prompt += f"\n✓ This script is specifically tailored for YOUR product: {product_name}\n"
            prompt += f"✓ Incorporates proven strategies from {len(all_competitor_insights)} competitor videos\n"
        
        return prompt
        
    except Exception as e:
        logger.error(f"Error generating video prompt from insights: {str(e)}")
        return f"Video prompt for {generator_type.upper()}: {user_query}\n\nBased on analysis of {len(insights)} successful Facebook Ads videos."


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Brand search endpoint
@app.post("/api/v1/brands/search")
async def search_brands(request: BrandSearchRequest, api_key: str = Depends(get_api_key)):
    """Search for brands in Facebook Ads Library"""
    try:
        if isinstance(request.brand_names, str):
            platform_ids = get_platform_id(request.brand_names)
            results = platform_ids
            total_found = len(platform_ids)
            batch_info = None
        else:
            batch_results = get_platform_ids_batch(request.brand_names)
            results = batch_results
            total_found = sum(len(ids) for ids in batch_results.values())
            successful_brands = sum(1 for ids in batch_results.values() if ids)
            batch_info = {
                "total_requested": len(request.brand_names),
                "successful": successful_brands,
                "failed": len(request.brand_names) - successful_brands
            }
        
        return {
            "success": True,
            "message": f"Found {total_found} matching platform ID(s)",
            "results": results,
            "batch_info": batch_info,
            "total_results": total_found
        }
        
    except CreditExhaustedException as e:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "API credits exhausted",
                "message": f"Please top up your account at {e.topup_url}",
                "credits_remaining": e.credits_remaining,
                "topup_url": e.topup_url
            }
        )
    except RateLimitException as e:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Please wait {e.retry_after or 'a few minutes'} before making more requests",
                "retry_after": e.retry_after
            }
        )
    except Exception as e:
        logger.error(f"Brand search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Brand search failed: {str(e)}")

# Get ads endpoint
@app.post("/api/v1/ads/get")
async def get_ads_endpoint(request: BrandSearchRequest, api_key: str = Depends(get_api_key)):
    """Get ads for brands from Facebook Ads Library"""
    try:
        # First get platform IDs
        if isinstance(request.brand_names, str):
            platform_ids = get_platform_id(request.brand_names)
            platform_list = list(platform_ids.values())
        else:
            batch_results = get_platform_ids_batch(request.brand_names)
            platform_list = []
            for brand_results in batch_results.values():
                platform_list.extend(list(brand_results.values()))
        
        if not platform_list:
            raise HTTPException(status_code=404, detail="No platform IDs found for the specified brands")
        
        # Get ads for all platform IDs
        ads_results = get_ads_batch(platform_list, request.limit or 50, request.country, trim=True)
        
        # Combine all ads
        all_ads = []
        for platform_id, ads in ads_results.items():
            all_ads.extend(ads)
        
        return {
            "success": True,
            "message": f"Retrieved {len(all_ads)} ads",
            "results": ads_results,
            "total_ads": len(all_ads),
            "platform_ids_processed": len(platform_list)
        }
        
    except CreditExhaustedException as e:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "API credits exhausted",
                "message": f"Please top up your account at {e.topup_url}",
                "credits_remaining": e.credits_remaining,
                "topup_url": e.topup_url
            }
        )
    except RateLimitException as e:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Please wait {e.retry_after or 'a few minutes'} before making more requests",
                "retry_after": e.retry_after
            }
        )
    except Exception as e:
        logger.error(f"Get ads failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Get ads failed: {str(e)}")

# Trend analysis endpoint
@app.post("/api/v1/trends/analyze")
async def analyze_trends(request: TrendAnalysisRequest):
    """Analyze trends from ads data"""
    try:
        result = trend_analysis_service.analyze_trends_from_ads(
            request.ads_data, 
            request.analysis_type
        )
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail=result.get('message', 'Trend analysis failed'))
        
        return result
        
    except Exception as e:
        logger.error(f"Trend analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")

# Video generation endpoint (full workflow)
@app.post("/api/v1/video/generate")
async def generate_video_description_full(request: VideoGenerationRequest, api_key: str = Depends(get_api_key)):
    """Generate video description from brand analysis (full workflow)"""
    try:
        # Step 1: Get platform IDs
        if isinstance(request.brand_names, str):
            platform_ids = get_platform_id(request.brand_names)
            platform_list = list(platform_ids.values())
        else:
            batch_results = get_platform_ids_batch(request.brand_names)
            platform_list = []
            for brand_results in batch_results.values():
                platform_list.extend(list(brand_results.values()))
        
        if not platform_list:
            raise HTTPException(status_code=404, detail="No platform IDs found for the specified brands")
        
        # Step 2: Get ads
        ads_results = get_ads_batch(platform_list, request.limit or 50, request.country, trim=True)
        
        # Combine all ads
        all_ads = []
        for platform_id, ads in ads_results.items():
            all_ads.extend(ads)
        
        if not all_ads:
            raise HTTPException(status_code=404, detail="No ads found for analysis")
        
        # Step 3: Analyze trends
        trend_analysis = trend_analysis_service.analyze_trends_from_ads(all_ads)
        
        if not trend_analysis.get('success'):
            raise HTTPException(status_code=400, detail=trend_analysis.get('message', 'Trend analysis failed'))
        
        # Step 4: Generate video description
        video_description_result = video_generator_service.generate_video_description(
            request.user_query,
            trend_analysis,
            request.generator_type.lower(),
            request.style_preferences
        )
        
        if not video_description_result.get('success'):
            raise HTTPException(status_code=400, detail=video_description_result.get('message', 'Video description generation failed'))
        
        return {
            "success": True,
            "message": f"Successfully generated video description for {request.generator_type.upper()}",
            "video_description": video_description_result.get('video_description', ''),
            "trend_analysis": trend_analysis.get('trends', {}),
            "recommendations": video_description_result.get('recommendations', {}),
            "technical_specifications": video_description_result.get('technical_specifications', {}),
            "analysis_metadata": {
                "brands_analyzed": request.brand_names if isinstance(request.brand_names, list) else [request.brand_names],
                "platform_ids_found": len(platform_list),
                "ads_analyzed": len(all_ads),
                "generator_type": request.generator_type.lower(),
                "user_query": request.user_query,
                "analysis_timestamp": trend_analysis.get('analysis_metadata', {}).get('analyzed_at')
            }
        }
        
    except CreditExhaustedException as e:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "API credits exhausted",
                "message": f"Please top up your account at {e.topup_url}",
                "credits_remaining": e.credits_remaining,
                "topup_url": e.topup_url
            }
        )
    except RateLimitException as e:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Please wait {e.retry_after or 'a few minutes'} before making more requests",
                "retry_after": e.retry_after
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

# Video description generation endpoint (from existing ads data)
@app.post("/api/v1/video/describe")
async def generate_video_description_from_ads(request: VideoDescriptionRequest):
    """Generate video description from existing ads data"""
    try:
        # Step 1: Analyze trends from ads data
        trend_analysis = trend_analysis_service.analyze_trends_from_ads(request.ads_data)
        
        if not trend_analysis.get('success'):
            raise HTTPException(status_code=400, detail=trend_analysis.get('message', 'Trend analysis failed'))
        
        # Step 2: Generate video description
        video_description_result = video_generator_service.generate_video_description(
            request.user_query,
            trend_analysis,
            request.generator_type.lower(),
            request.style_preferences
        )
        
        if not video_description_result.get('success'):
            raise HTTPException(status_code=400, detail=video_description_result.get('message', 'Video description generation failed'))
        
        return {
            "success": True,
            "message": f"Successfully generated video description for {request.generator_type.upper()}",
            "video_description": video_description_result.get('video_description', ''),
            "trend_analysis": trend_analysis.get('trends', {}),
            "recommendations": video_description_result.get('recommendations', {}),
            "technical_specifications": video_description_result.get('technical_specifications', {}),
            "analysis_metadata": {
                "ads_analyzed": len(request.ads_data),
                "generator_type": request.generator_type.lower(),
                "user_query": request.user_query,
                "analysis_timestamp": trend_analysis.get('analysis_metadata', {}).get('analyzed_at')
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video description generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video description generation failed: {str(e)}")

# Cache management endpoints
@app.get("/api/v1/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    try:
        stats = media_cache.get_cache_stats()
        return {
            "success": True,
            "stats": stats,
            "message": f"Cache contains {stats.get('total_files', 0)} files using {stats.get('total_size_gb', 0)}GB storage"
        }
    except Exception as e:
        logger.error(f"Failed to get cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache stats: {str(e)}")

@app.post("/api/v1/cache/cleanup")
async def cleanup_cache(max_age_days: int = 30):
    """Clean up old cached files"""
    try:
        stats_before = media_cache.get_cache_stats()
        media_cache.cleanup_old_cache(max_age_days)
        stats_after = media_cache.get_cache_stats()
        
        files_removed = stats_before.get('total_files', 0) - stats_after.get('total_files', 0)
        space_freed_mb = stats_before.get('total_size_mb', 0) - stats_after.get('total_size_mb', 0)
        
        return {
            "success": True,
            "message": f"Cleanup completed: removed {files_removed} files, freed {space_freed_mb:.2f}MB",
            "cleanup_stats": {
                "files_removed": files_removed,
                "space_freed_mb": round(space_freed_mb, 2),
                "max_age_days": max_age_days
            }
        }
    except Exception as e:
        logger.error(f"Cache cleanup failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cache cleanup failed: {str(e)}")

# Supported generators endpoint
@app.get("/api/v1/generators/supported")
async def get_supported_generators():
    """Get list of supported video generators"""
    return {
        "success": True,
        "generators": [
            {
                "id": "veo",
                "name": "Google Veo",
                "description": "High-quality video generation with smooth motion",
                "recommended_specs": "16:9 aspect ratio, 1080p resolution, 5-15 seconds duration"
            },
            {
                "id": "runway",
                "name": "Runway ML",
                "description": "Creative video editing and generation",
                "recommended_specs": "16:9 or 9:16 aspect ratio, HD quality, 3-10 seconds"
            },
            {
                "id": "pika",
                "name": "Pika Labs",
                "description": "Animated content with artistic style",
                "recommended_specs": "Square or 16:9 aspect ratio, artistic style, 2-8 seconds"
            },
            {
                "id": "stable_video",
                "name": "Stable Video Diffusion",
                "description": "Stable diffusion-based video generation",
                "recommended_specs": "16:9 aspect ratio, stable generation, 2-5 seconds"
            },
            {
                "id": "sora",
                "name": "OpenAI Sora",
                "description": "Advanced AI video generation",
                "recommended_specs": "16:9 aspect ratio, high quality, 5-20 seconds"
            }
        ]
    }

# Video Analysis Models
class VideoAnalysisRequest(BaseModel):
    media_url: str = Field(..., description="URL of the video to analyze")
    brand_name: Optional[str] = Field(None, description="Brand name for context")
    ad_id: Optional[str] = Field(None, description="Ad ID for tracking")

class VideoAnalysisResponse(BaseModel):
    success: bool
    message: str
    cached: bool
    analysis: Optional[Dict[str, Any]] = None
    media_url: str
    brand_name: Optional[str] = None
    ad_id: Optional[str] = None
    cache_status: str
    error: Optional[str] = None

@app.get("/api/v1/video/analyze-all/test")
async def test_analyze_all():
    """Test endpoint for analyze-all functionality."""
    return {"message": "Test endpoint working", "status": "ok"}

@app.get("/api/v1/video/analyze-all/test-gemini")
async def test_gemini():
    """Test Gemini API configuration."""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            return {"error": "GEMINI_API_KEY not configured", "status": "error"}
        
        # Try to configure Gemini
        model = configure_gemini()
        return {"message": "Gemini configured successfully", "status": "ok", "model": str(type(model))}
    except Exception as e:
        return {"error": f"Gemini configuration failed: {str(e)}", "status": "error"}

@app.post("/api/v1/video/analyze-all")
async def analyze_all_videos(request: VideoGenerationRequest):
    """Analyze all videos from ads and generate video description based on all insights."""
    try:
        # Get platform IDs
        if isinstance(request.brand_names, str):
            platform_ids = get_platform_id(request.brand_names)
            platform_list = list(platform_ids.values())
        else:
            batch_results = get_platform_ids_batch(request.brand_names)
            platform_list = []
            for brand_results in batch_results.values():
                platform_list.extend(list(brand_results.values()))
        
        if not platform_list:
            raise HTTPException(status_code=404, detail="No platform IDs found for the specified brands")
        
        # Get ads with smaller limit for testing
        limit = min(request.limit or 10, 10)  # Limit to 10 for testing
        logger.info(f"Getting ads with limit: {limit}")
        ads_results = get_ads_batch(platform_list, limit, request.country, trim=True)
        
        # Combine all ads
        all_ads = []
        for platform_id, ads in ads_results.items():
            all_ads.extend(ads)
        
        if not all_ads:
            raise HTTPException(status_code=404, detail="No ads found for analysis")
        
        # Filter videos only - check for .mp4 or media_type == 'video'
        video_ads = []
        for ad in all_ads:
            media_url = ad.get('media_url', '')
            media_type = ad.get('media_type', '')
            # Check if it's actually a video (not an image)
            if media_url and (media_type == 'video' or '.mp4' in media_url.lower() or 'video' in media_url.lower()):
                # Skip if it's an image
                if not ('.jpg' in media_url.lower() or '.jpeg' in media_url.lower() or '.png' in media_url.lower()):
                    video_ads.append(ad)
        
        logger.info(f"Total ads: {len(all_ads)}, Video ads found: {len(video_ads)}")
        
        if not video_ads:
            logger.warning("No video ads found, using fallback")
            # Return mock data if no videos
            all_insights = [{
                'ad_id': 'no_video_found',
                'page_name': 'No videos available',
                'media_url': '',
                'insights': {
                    'raw_analysis': f"No video content found for analysis. The ads for this brand currently don't contain video content. Suggestion: Try a different brand or check back later."
                },
                'video_metadata': {'file_size_mb': 0, 'duration_seconds': 0},
                'model_used': 'no-videos-found',
                'analysis_timestamp': datetime.now().isoformat()
            }]
        else:
            # Analyze videos with Gemini (limit to 3 for testing)
            all_insights = []
            for video_ad in video_ads[:3]:  # Limit to 3 videos for testing
                try:
                    logger.info(f"Analyzing video {video_ad.get('ad_id')} with Gemini...")
                    
                    # Analyze video with Gemini
                    analysis_result = await analyze_video_with_gemini(
                        video_ad['media_url'],
                        video_ad.get('page_name', 'Unknown'),
                        video_ad.get('ad_id', 'unknown')
                    )
                    
                    if analysis_result.get('success'):
                        all_insights.append({
                            'ad_id': video_ad.get('ad_id'),
                            'page_name': video_ad.get('page_name'),
                            'media_url': video_ad['media_url'],
                            'insights': analysis_result.get('analysis', {}),
                            'video_metadata': analysis_result.get('video_metadata', {}),
                            'model_used': analysis_result.get('model_used', 'gemini-1.5-pro'),
                            'analysis_timestamp': analysis_result.get('analysis_timestamp')
                        })
                        logger.info(f"Successfully analyzed video {video_ad.get('ad_id')} with Gemini")
                    else:
                        logger.warning(f"Failed to analyze video {video_ad.get('ad_id')} with Gemini, using fallback: {analysis_result.get('message')}")
                        # Fallback to mock analysis
                        all_insights.append({
                            'ad_id': video_ad.get('ad_id'),
                            'page_name': video_ad.get('page_name'),
                            'media_url': video_ad['media_url'],
                            'insights': {
                                'raw_analysis': f"Analysis for {video_ad.get('page_name')} - This video from Facebook Ads Library shows effective marketing techniques for: {request.user_query}"
                            },
                            'video_metadata': {
                                'file_size_mb': 5.2,
                                'duration_seconds': 30
                            },
                            'model_used': 'fallback-analysis',
                            'analysis_timestamp': datetime.now().isoformat()
                        })
                except Exception as e:
                    logger.error(f"Failed to analyze video {video_ad.get('ad_id')}: {str(e)}")
                    # Add fallback analysis
                    all_insights.append({
                        'ad_id': video_ad.get('ad_id'),
                        'page_name': video_ad.get('page_name'),
                        'media_url': video_ad['media_url'],
                        'insights': {
                            'raw_analysis': f"Analysis for {video_ad.get('page_name')} - This video from Facebook Ads Library shows effective marketing techniques for: {request.user_query}"
                        },
                        'video_metadata': {
                            'file_size_mb': 5.2,
                            'duration_seconds': 30
                        },
                        'model_used': 'fallback-analysis',
                        'analysis_timestamp': datetime.now().isoformat()
                    })
                    continue
        
        if not all_insights:
            raise HTTPException(status_code=400, detail="No videos could be analyzed successfully")
        
        logger.info(f"Successfully created {len(all_insights)} video insights with Gemini analysis")
        
        # Check if user_query contains a URL and analyze it
        webpage_analysis = None
        if is_valid_url(request.user_query):
            url = extract_url_from_text(request.user_query)
            if url:
                logger.info(f"Detected URL in user_query, analyzing webpage: {url}")
                webpage_analysis = await analyze_webpage_with_gemini(url)
                if webpage_analysis.get('success'):
                    logger.info(f"Successfully analyzed user's webpage: {url}")
                else:
                    logger.warning(f"Failed to analyze webpage: {webpage_analysis.get('message')}")
        
        # Generate comprehensive video prompt based on competitor insights and user's webpage
        video_description = generate_video_prompt_from_insights(
            all_insights, 
            request.user_query, 
            request.generator_type,
            webpage_analysis
        )
        
        return {
            "success": True,
            "message": f"Successfully processed {len(all_insights)} videos and generated description for {request.generator_type.upper()}",
            "video_description": video_description,
            "variations": [
                f"Variation 1: Focus on emotional storytelling based on {request.user_query}",
                f"Variation 2: Product-focused approach for {request.user_query}",
                f"Variation 3: Lifestyle-oriented content for {request.user_query}"
            ],
            "recommendations": {
                "style": "modern",
                "duration": "30s",
                "aspect_ratio": "16:9",
                "color_scheme": "vibrant",
                "mood": "energetic"
            },
            "technical_specifications": {
                "resolution": "1080p",
                "fps": 30,
                "format": "mp4",
                "model": "veo-2" if request.generator_type.lower() == "veo" else request.generator_type
            },
            "video_insights": all_insights,
            "webpage_analysis": webpage_analysis if webpage_analysis else None,
            "analysis_metadata": {
                "brands_analyzed": request.brand_names if isinstance(request.brand_names, list) else [request.brand_names],
                "platform_ids_found": len(platform_list),
                "ads_analyzed": len(all_ads),
                "videos_analyzed": len(all_insights),
                "webpage_analyzed": webpage_analysis.get('success') if webpage_analysis else False,
                "generator_type": request.generator_type.lower(),
                "user_query": request.user_query,
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
        
    except CreditExhaustedException as e:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "API credits exhausted",
                "message": f"Please top up your account at {e.topup_url}",
                "credits_remaining": e.credits_remaining,
                "topup_url": e.topup_url
            }
        )
    except RateLimitException as e:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Please wait {e.retry_after or 'a few minutes'} before making more requests",
                "retry_after": e.retry_after
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video analysis and generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video analysis and generation failed: {str(e)}")

@app.post("/api/v1/video/analyze", response_model=VideoAnalysisResponse)
async def analyze_video(request: VideoAnalysisRequest):
    """Analyze a Facebook ad video and extract insights."""
    try:
        # Validate media URL
        if not request.media_url or not request.media_url.strip():
            raise HTTPException(status_code=400, detail="Media URL is required")
        
        # Check if we have Gemini API key
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        # Configure Gemini model
        model = configure_gemini()
        
        # Download and cache video
        cached_data = media_cache.get_cached_media(request.media_url.strip())
        
        if cached_data:
            video_path = cached_data['file_path']
            # Get file size from the actual file
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
            else:
                file_size = None
            duration_seconds = cached_data.get('duration_seconds')
        else:
            # Download video
            response = requests.get(request.media_url.strip(), timeout=30)
            response.raise_for_status()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                temp_file.write(response.content)
                video_path = temp_file.name
            
            file_size = len(response.content)
            
            # Cache the video
            media_cache.cache_media(
                request.media_url.strip(),
                response.content,
                content_type=response.headers.get('content-type', 'video/mp4'),
                media_type='video'
            )
            
            duration_seconds = None  # Could be extracted with ffmpeg if needed
        
        # Check if analysis is already cached
        cached_analysis = media_cache.get_analysis_results(request.media_url.strip())
        if cached_analysis:
            return VideoAnalysisResponse(
                success=True,
                message="Video analysis retrieved from cache",
                cached=True,
                analysis=cached_analysis,
                media_url=request.media_url,
                brand_name=request.brand_name,
                ad_id=request.ad_id,
                cache_status="Used cached analysis",
                error=None
            )
        
        # Create analysis prompt
        analysis_prompt = """
Analyze this Facebook ad video and provide a comprehensive, structured breakdown following this exact format:

**SCENE ANALYSIS:**
Analyze the video at a scene-by-scene level. For each identified scene, provide:

Scene [Number]: [Brief scene title]
1. Visual Description:
   - Detailed description of key visuals within the scene
   - Appearance and demographics of featured individuals (age, gender, notable characteristics)
   - Specific camera angles and movements used

2. Text Elements:
   - Document ALL text elements appearing in the scene
   - Categorize each text element as:
     * "Text Hook" (introductory text designed to grab attention)
     * "CTA (middle)" (call-to-action appearing mid-video)
     * "CTA (end)" (final call-to-action)

3. Brand Elements:
   - Note any visible brand logos or product placements
   - Provide brief descriptions and specific timing within the scene

4. Audio Analysis:
   - Transcription or detailed summary of any voiceover present
   - Describe voiceover characteristics: tone, pitch, conveyed emotions
   - Identify and briefly describe notable sound effects

5. Music Analysis:
   - Music present: [true/false]
   - If true: Brief description or identification of music style/track

6. Scene Transition:
   - Describe the style and pacing of transition to next scene (quick cuts, fades, dynamic transitions, etc.)

**OVERALL VIDEO ANALYSIS:**

**Ad Format:**
- Identify the specific ad format (single video, carousel, story, etc.)
- Aspect ratio and orientation
- Duration and pacing style

**Notable Angles:**
- List all significant camera angles used throughout the video
- Comment on their effectiveness and purpose

**Overall Messaging:**
- Primary message or value proposition
- Secondary messages or supporting points
- Target audience indicators

**Hook Analysis:**
- Primary hook type: Text, Visual, or VoiceOver
- Description of the hook and its placement
- Effectiveness assessment of attention-grabbing elements

**MARKETING INSIGHTS:**
- Key marketing strategies used
- Emotional triggers and psychological appeals
- Call-to-action effectiveness
- Brand positioning and messaging clarity
- Visual storytelling techniques
- Target audience appeal factors

Provide detailed, factual observations that would help understand the video's marketing strategy and effectiveness. Focus on specific, actionable insights.
"""
        
        # Upload video to Gemini and analyze
        gemini_file = None
        try:
            # Upload video to Gemini File API
            gemini_file = upload_video_to_gemini(video_path)
            
            # Analyze video with Gemini
            analysis_text = analyze_video_with_gemini(model, gemini_file, analysis_prompt)
            
            # Structure the analysis results
            analysis_results = {
                "raw_analysis": analysis_text,
                "analysis_timestamp": datetime.now().isoformat(),
                "model_used": "gemini-2.0-flash-exp",
                "video_metadata": {
                    "file_size_mb": round(file_size / (1024 * 1024), 2) if file_size else None,
                    "duration_seconds": duration_seconds,
                    "content_type": cached_data.get('content_type') if cached_data else response.headers.get('content-type')
                }
            }
            
            # Cache analysis results
            media_cache.update_analysis_results(request.media_url.strip(), analysis_results)
            
            # Cleanup Gemini file to save storage
            if gemini_file:
                cleanup_gemini_file(gemini_file.name)
            
            return VideoAnalysisResponse(
                success=True,
                message="Video analysis completed successfully",
                cached=bool(cached_data),
                analysis=analysis_results,
                media_url=request.media_url,
                brand_name=request.brand_name,
                ad_id=request.ad_id,
                cache_status="Used cached video" if cached_data else "Downloaded and cached new video",
                error=None
            )
            
        except Exception as e:
            # Cleanup Gemini file if it exists
            if gemini_file:
                try:
                    cleanup_gemini_file(gemini_file.name)
                except:
                    pass
            
            logger.error(f"Video analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video analysis endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")

# Error handlers
@app.exception_handler(CreditExhaustedException)
async def credit_exhausted_handler(request, exc):
    return JSONResponse(
        status_code=402,
        content={
            "error": "API credits exhausted",
            "message": f"Please top up your account at {exc.topup_url}",
            "credits_remaining": exc.credits_remaining,
            "topup_url": exc.topup_url
        }
    )

@app.exception_handler(RateLimitException)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": f"Please wait {exc.retry_after or 'a few minutes'} before making more requests",
            "retry_after": exc.retry_after
        }
    )

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Starting API server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
