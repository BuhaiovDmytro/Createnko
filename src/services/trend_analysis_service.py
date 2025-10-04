import logging
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import re

logger = logging.getLogger(__name__)

class TrendAnalysisService:
    """Service for analyzing trends from Facebook Ads Library data."""
    
    def __init__(self):
        self.logger = logger
    
    def analyze_trends_from_ads(self, ads_data: List[Dict[str, Any]], 
                              analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze trends from Facebook ads data.
        
        Args:
            ads_data: List of ad objects from Facebook Ads Library
            analysis_type: Type of analysis ("comprehensive", "visual", "text", "video")
            
        Returns:
            Dictionary with trend analysis results
        """
        try:
            if not ads_data:
                return {
                    "success": False,
                    "message": "No ads data provided for analysis",
                    "trends": {},
                    "error": "Empty ads data"
                }
            
            # Filter and categorize ads
            image_ads = [ad for ad in ads_data if ad.get('media_type') == 'IMAGE']
            video_ads = [ad for ad in ads_data if ad.get('media_type') == 'VIDEO']
            
            # Extract video details
            analyzed_videos = self._extract_video_details(video_ads)
            
            trends = {
                "overview": self._analyze_overview_trends(ads_data),
                "content_trends": self._analyze_content_trends(ads_data),
                "visual_trends": self._analyze_visual_trends(image_ads) if image_ads else {},
                "video_trends": self._analyze_video_trends(video_ads) if video_ads else {},
                "messaging_trends": self._analyze_messaging_trends(ads_data),
                "format_trends": self._analyze_format_trends(ads_data),
                "recommendations": self._generate_recommendations(ads_data),
                "analyzed_videos": analyzed_videos,
                "reasoning": self._generate_reasoning(ads_data, image_ads, video_ads)
            }
            
            return {
                "success": True,
                "message": f"Successfully analyzed trends from {len(ads_data)} ads",
                "trends": trends,
                "analysis_metadata": {
                    "total_ads": len(ads_data),
                    "image_ads": len(image_ads),
                    "video_ads": len(video_ads),
                    "analysis_type": analysis_type,
                    "analyzed_at": datetime.now().isoformat()
                },
                "error": None
            }
            
        except Exception as e:
            self.logger.error(f"Trend analysis failed: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to analyze trends: {str(e)}",
                "trends": {},
                "error": str(e)
            }
    
    def _analyze_overview_trends(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze overall trends and patterns."""
        total_ads = len(ads_data)
        
        # Media type distribution
        media_types = Counter(ad.get('media_type', 'UNKNOWN') for ad in ads_data)
        
        # Date analysis
        date_patterns = self._analyze_date_patterns(ads_data)
        
        # Brand analysis
        brands = Counter(ad.get('page_name', 'Unknown') for ad in ads_data)
        
        return {
            "total_ads_analyzed": total_ads,
            "media_type_distribution": dict(media_types),
            "date_patterns": date_patterns,
            "top_brands": dict(brands.most_common(10)),
            "analysis_period": self._get_analysis_period(ads_data)
        }
    
    def _analyze_content_trends(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content-related trends."""
        # Extract text content
        all_text = []
        for ad in ads_data:
            body_text = ad.get('body', '')
            if body_text:
                all_text.append(body_text)
        
        # Analyze common words and phrases
        word_frequency = self._analyze_word_frequency(all_text)
        phrase_patterns = self._analyze_phrase_patterns(all_text)
        
        # Analyze text length patterns
        text_lengths = [len(text) for text in all_text if text]
        avg_text_length = sum(text_lengths) / len(text_lengths) if text_lengths else 0
        
        return {
            "word_frequency": word_frequency,
            "phrase_patterns": phrase_patterns,
            "text_length_stats": {
                "average_length": round(avg_text_length, 2),
                "min_length": min(text_lengths) if text_lengths else 0,
                "max_length": max(text_lengths) if text_lengths else 0,
                "total_text_samples": len(text_lengths)
            },
            "common_themes": self._extract_themes(all_text)
        }
    
    def _analyze_visual_trends(self, image_ads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze visual trends from image ads."""
        if not image_ads:
            return {}
        
        # Analyze image URLs for patterns
        image_patterns = self._analyze_image_patterns(image_ads)
        
        return {
            "image_count": len(image_ads),
            "image_patterns": image_patterns,
            "visual_style_indicators": self._extract_visual_style_indicators(image_ads)
        }
    
    def _analyze_video_trends(self, video_ads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze video trends from video ads."""
        if not video_ads:
            return {}
        
        # Analyze video URLs for patterns
        video_patterns = self._analyze_video_patterns(video_ads)
        
        return {
            "video_count": len(video_ads),
            "video_patterns": video_patterns,
            "video_format_indicators": self._extract_video_format_indicators(video_ads)
        }
    
    def _analyze_messaging_trends(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze messaging and communication trends."""
        all_text = [ad.get('body', '') for ad in ads_data if ad.get('body')]
        
        # Analyze emotional tone
        emotional_indicators = self._analyze_emotional_tone(all_text)
        
        # Analyze call-to-action patterns
        cta_patterns = self._analyze_cta_patterns(all_text)
        
        # Analyze value propositions
        value_props = self._analyze_value_propositions(all_text)
        
        return {
            "emotional_tone": emotional_indicators,
            "cta_patterns": cta_patterns,
            "value_propositions": value_props,
            "messaging_strategies": self._identify_messaging_strategies(all_text)
        }
    
    def _analyze_format_trends(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze format and structure trends."""
        formats = Counter(ad.get('media_type', 'UNKNOWN') for ad in ads_data)
        
        return {
            "format_distribution": dict(formats),
            "format_preferences": self._analyze_format_preferences(ads_data),
            "structure_patterns": self._analyze_structure_patterns(ads_data)
        }
    
    def _generate_recommendations(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate recommendations based on trend analysis."""
        recommendations = {
            "content_recommendations": self._generate_content_recommendations(ads_data),
            "visual_recommendations": self._generate_visual_recommendations(ads_data),
            "format_recommendations": self._generate_format_recommendations(ads_data),
            "messaging_recommendations": self._generate_messaging_recommendations(ads_data)
        }
        
        return recommendations
    
    def _analyze_date_patterns(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze date patterns in ads."""
        dates = []
        for ad in ads_data:
            start_date = ad.get('start_date')
            if start_date:
                try:
                    # Handle both offset-aware and offset-naive datetime strings
                    if start_date.endswith('Z'):
                        dates.append(datetime.fromisoformat(start_date.replace('Z', '+00:00')))
                    else:
                        dates.append(datetime.fromisoformat(start_date))
                except:
                    continue
        
        if not dates:
            return {"pattern": "No date data available"}
        
        # Analyze recency
        now = datetime.now()
        # Make all dates timezone-aware for comparison
        recent_ads = []
        for d in dates:
            try:
                # Convert to naive datetime for comparison
                if d.tzinfo is not None:
                    d_naive = d.replace(tzinfo=None)
                else:
                    d_naive = d
                if (now - d_naive).days <= 30:
                    recent_ads.append(d)
            except Exception as e:
                self.logger.warning(f"Error comparing dates: {e}")
                continue
        
        return {
            "total_with_dates": len(dates),
            "recent_ads_30_days": len(recent_ads),
            "date_range": {
                "earliest": min(dates).isoformat() if dates else None,
                "latest": max(dates).isoformat() if dates else None
            }
        }
    
    def _analyze_word_frequency(self, texts: List[str]) -> Dict[str, int]:
        """Analyze word frequency in texts."""
        word_count = Counter()
        
        for text in texts:
            # Simple word extraction (can be improved with NLP)
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            word_count.update(words)
        
        # Filter out common stop words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'man', 'oil', 'sit', 'try', 'use', 'she', 'put', 'end', 'why', 'let', 'big', 'few', 'got', 'run', 'yes', 'any', 'ask', 'came', 'give', 'help', 'just', 'know', 'like', 'look', 'make', 'most', 'over', 'some', 'take', 'than', 'them', 'very', 'what', 'when', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'been', 'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well', 'were'}
        
        filtered_words = {word: count for word, count in word_count.items() 
                         if word not in stop_words and len(word) > 3}
        
        return dict(Counter(filtered_words).most_common(20))
    
    def _analyze_phrase_patterns(self, texts: List[str]) -> Dict[str, int]:
        """Analyze common phrase patterns."""
        phrases = Counter()
        
        for text in texts:
            # Extract 2-3 word phrases
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                phrases[phrase] += 1
        
        return dict(phrases.most_common(15))
    
    def _extract_themes(self, texts: List[str]) -> List[str]:
        """Extract common themes from texts."""
        # Simple theme extraction based on keywords
        theme_keywords = {
            'discount': ['sale', 'discount', 'off', 'deal', 'save', 'cheap'],
            'new_product': ['new', 'latest', 'fresh', 'innovative', 'breakthrough'],
            'quality': ['premium', 'quality', 'best', 'top', 'excellent', 'superior'],
            'convenience': ['easy', 'simple', 'quick', 'fast', 'convenient'],
            'social_proof': ['popular', 'trending', 'loved', 'recommended', 'trusted'],
            'urgency': ['limited', 'hurry', 'act now', 'don\'t miss', 'expires'],
            'lifestyle': ['lifestyle', 'life', 'daily', 'everyday', 'routine']
        }
        
        themes = defaultdict(int)
        for text in texts:
            text_lower = text.lower()
            for theme, keywords in theme_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        themes[theme] += 1
        
        return [theme for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    def _analyze_image_patterns(self, image_ads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in image ads."""
        return {
            "total_images": len(image_ads),
            "image_url_patterns": self._extract_url_patterns([ad.get('media_url') for ad in image_ads])
        }
    
    def _analyze_video_patterns(self, video_ads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in video ads."""
        return {
            "total_videos": len(video_ads),
            "video_url_patterns": self._extract_url_patterns([ad.get('media_url') for ad in video_ads])
        }
    
    def _extract_url_patterns(self, urls: List[str]) -> Dict[str, Any]:
        """Extract patterns from URLs."""
        if not urls:
            return {}
        
        # Analyze URL structure
        domains = Counter()
        extensions = Counter()
        
        for url in urls:
            if url:
                try:
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    domains[parsed.netloc] += 1
                    
                    # Extract file extension
                    path = parsed.path
                    if '.' in path:
                        ext = path.split('.')[-1].lower()
                        extensions[ext] += 1
                except:
                    continue
        
        return {
            "domains": dict(domains.most_common(5)),
            "file_extensions": dict(extensions.most_common(5))
        }
    
    def _extract_visual_style_indicators(self, image_ads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract visual style indicators from image ads."""
        return {
            "image_count": len(image_ads),
            "style_indicators": "Requires image analysis for detailed visual trends"
        }
    
    def _extract_video_format_indicators(self, video_ads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract video format indicators from video ads."""
        return {
            "video_count": len(video_ads),
            "format_indicators": "Requires video analysis for detailed format trends"
        }
    
    def _analyze_emotional_tone(self, texts: List[str]) -> Dict[str, int]:
        """Analyze emotional tone indicators."""
        emotional_keywords = {
            'positive': ['amazing', 'awesome', 'fantastic', 'great', 'wonderful', 'excellent', 'perfect', 'love', 'best', 'incredible'],
            'urgent': ['hurry', 'limited', 'expires', 'act now', 'don\'t miss', 'last chance', 'quickly', 'immediately'],
            'exclusive': ['exclusive', 'limited', 'special', 'unique', 'only', 'rare', 'premium', 'vip'],
            'social': ['share', 'follow', 'join', 'community', 'friends', 'family', 'together', 'connect']
        }
        
        tone_counts = defaultdict(int)
        for text in texts:
            text_lower = text.lower()
            for tone, keywords in emotional_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        tone_counts[tone] += 1
        
        return dict(tone_counts)
    
    def _analyze_cta_patterns(self, texts: List[str]) -> Dict[str, int]:
        """Analyze call-to-action patterns."""
        cta_patterns = [
            'buy now', 'shop now', 'get it', 'order now', 'click here', 'learn more',
            'sign up', 'join now', 'start now', 'try now', 'download', 'subscribe',
            'book now', 'reserve', 'claim', 'grab', 'snag', 'score'
        ]
        
        cta_counts = Counter()
        for text in texts:
            text_lower = text.lower()
            for cta in cta_patterns:
                if cta in text_lower:
                    cta_counts[cta] += 1
        
        return dict(cta_counts.most_common(10))
    
    def _analyze_value_propositions(self, texts: List[str]) -> Dict[str, int]:
        """Analyze value proposition patterns."""
        value_keywords = {
            'price': ['free', 'cheap', 'affordable', 'budget', 'low cost', 'discount', 'save'],
            'quality': ['premium', 'quality', 'best', 'top', 'excellent', 'superior', 'high-end'],
            'convenience': ['easy', 'simple', 'quick', 'fast', 'convenient', 'effortless'],
            'results': ['results', 'outcomes', 'benefits', 'improve', 'enhance', 'boost'],
            'guarantee': ['guarantee', 'warranty', 'promise', 'assurance', 'risk-free']
        }
        
        value_counts = defaultdict(int)
        for text in texts:
            text_lower = text.lower()
            for value_type, keywords in value_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        value_counts[value_type] += 1
        
        return dict(value_counts)
    
    def _identify_messaging_strategies(self, texts: List[str]) -> List[str]:
        """Identify common messaging strategies."""
        strategies = []
        
        # Analyze for different strategies
        all_text = ' '.join(texts).lower()
        
        if any(word in all_text for word in ['story', 'journey', 'experience']):
            strategies.append('storytelling')
        
        if any(word in all_text for word in ['problem', 'solution', 'fix', 'solve']):
            strategies.append('problem-solution')
        
        if any(word in all_text for word in ['before', 'after', 'transformation', 'change']):
            strategies.append('before-after')
        
        if any(word in all_text for word in ['testimonial', 'review', 'customer', 'user']):
            strategies.append('social_proof')
        
        if any(word in all_text for word in ['exclusive', 'limited', 'special', 'only']):
            strategies.append('scarcity')
        
        return strategies
    
    def _analyze_format_preferences(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze format preferences."""
        formats = Counter(ad.get('media_type', 'UNKNOWN') for ad in ads_data)
        
        return {
            "format_distribution": dict(formats),
            "preferred_format": formats.most_common(1)[0][0] if formats else "Unknown"
        }
    
    def _analyze_structure_patterns(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze structural patterns in ads."""
        return {
            "average_text_length": sum(len(ad.get('body', '')) for ad in ads_data) / len(ads_data) if ads_data else 0,
            "text_length_distribution": self._analyze_text_length_distribution(ads_data)
        }
    
    def _analyze_text_length_distribution(self, ads_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze text length distribution."""
        lengths = [len(ad.get('body', '')) for ad in ads_data if ad.get('body')]
        
        if not lengths:
            return {}
        
        # Categorize by length
        categories = {
            'short (0-50)': len([l for l in lengths if l <= 50]),
            'medium (51-150)': len([l for l in lengths if 51 <= l <= 150]),
            'long (151+)': len([l for l in lengths if l > 150])
        }
        
        return categories
    
    def _generate_content_recommendations(self, ads_data: List[Dict[str, Any]]) -> List[str]:
        """Generate content recommendations."""
        recommendations = []
        
        # Analyze text length trends
        text_lengths = [len(ad.get('body', '')) for ad in ads_data if ad.get('body')]
        if text_lengths:
            avg_length = sum(text_lengths) / len(text_lengths)
            if avg_length < 50:
                recommendations.append("Consider longer, more descriptive content for better engagement")
            elif avg_length > 200:
                recommendations.append("Consider shorter, more concise messaging for better readability")
        
        # Analyze word frequency for content suggestions
        all_text = ' '.join([ad.get('body', '') for ad in ads_data if ad.get('body')])
        if 'free' in all_text.lower():
            recommendations.append("'Free' is a popular keyword - consider incorporating free offers")
        
        if 'new' in all_text.lower():
            recommendations.append("'New' products/features are trending - highlight novelty")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _generate_visual_recommendations(self, ads_data: List[Dict[str, Any]]) -> List[str]:
        """Generate visual recommendations."""
        recommendations = []
        
        media_types = Counter(ad.get('media_type', 'UNKNOWN') for ad in ads_data)
        
        if media_types.get('VIDEO', 0) > media_types.get('IMAGE', 0):
            recommendations.append("Video content is trending - prioritize video creation")
        else:
            recommendations.append("Image content is popular - ensure high-quality visuals")
        
        recommendations.append("Focus on eye-catching visuals that align with brand identity")
        recommendations.append("Consider A/B testing different visual styles")
        
        return recommendations
    
    def _generate_format_recommendations(self, ads_data: List[Dict[str, Any]]) -> List[str]:
        """Generate format recommendations."""
        recommendations = []
        
        # Analyze format distribution
        formats = Counter(ad.get('media_type', 'UNKNOWN') for ad in ads_data)
        
        if formats.get('VIDEO', 0) > 0:
            recommendations.append("Video ads are effective - create engaging video content")
        
        if formats.get('IMAGE', 0) > 0:
            recommendations.append("Image ads work well - focus on compelling visuals")
        
        recommendations.append("Test different ad formats to find what works best")
        recommendations.append("Consider carousel ads for showcasing multiple products")
        
        return recommendations
    
    def _generate_messaging_recommendations(self, ads_data: List[Dict[str, Any]]) -> List[str]:
        """Generate messaging recommendations."""
        recommendations = []
        
        # Analyze emotional tone
        all_text = ' '.join([ad.get('body', '') for ad in ads_data if ad.get('body')]).lower()
        
        if 'urgent' in all_text or 'limited' in all_text:
            recommendations.append("Urgency messaging is effective - create time-sensitive offers")
        
        if 'free' in all_text:
            recommendations.append("Free offers are popular - consider free trials or samples")
        
        recommendations.append("Focus on clear value propositions")
        recommendations.append("Use emotional triggers that resonate with your audience")
        recommendations.append("Include strong call-to-action statements")
        
        return recommendations
    
    def _get_analysis_period(self, ads_data: List[Dict[str, Any]]) -> Dict[str, str]:
        """Get the analysis period from ads data."""
        dates = []
        for ad in ads_data:
            start_date = ad.get('start_date')
            if start_date:
                try:
                    # Handle both offset-aware and offset-naive datetime strings
                    if start_date.endswith('Z'):
                        dates.append(datetime.fromisoformat(start_date.replace('Z', '+00:00')))
                    else:
                        dates.append(datetime.fromisoformat(start_date))
                except:
                    continue
        
        if dates:
            # Convert all dates to naive for comparison
            naive_dates = []
            for d in dates:
                if d.tzinfo is not None:
                    naive_dates.append(d.replace(tzinfo=None))
                else:
                    naive_dates.append(d)
            
            return {
                "earliest": min(naive_dates).isoformat(),
                "latest": max(naive_dates).isoformat(),
                "period_days": (max(naive_dates) - min(naive_dates)).days
            }
        else:
            return {"period": "No date information available"}
    
    def _extract_video_details(self, video_ads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract detailed information about video ads for display."""
        video_details = []
        
        for ad in video_ads:
            video_info = {
                "id": ad.get('id', ''),
                "ad_id": ad.get('id', ''),  # Add ad_id field for video analysis
                "page_name": ad.get('page_name', 'Unknown'),
                "media_url": ad.get('media_url', ''),
                "body": ad.get('body', ''),
                "start_date": ad.get('start_date', ''),
                "end_date": ad.get('end_date', ''),
                "ad_creative_bodies": ad.get('ad_creative_bodies', []),
                "ad_creative_link_captions": ad.get('ad_creative_link_captions', []),
                "ad_creative_link_descriptions": ad.get('ad_creative_link_descriptions', []),
                "ad_creative_link_titles": ad.get('ad_creative_link_titles', []),
                "currency": ad.get('currency', ''),
                "estimated_audience_size": ad.get('estimated_audience_size', {}),
                "languages": ad.get('languages', []),
                "publisher_platforms": ad.get('publisher_platforms', []),
                "region_distribution": ad.get('region_distribution', {}),
                "video_thumbnail": self._extract_video_thumbnail(ad.get('media_url', '')),
                "video_duration": self._estimate_video_duration(ad),
                "engagement_indicators": self._extract_engagement_indicators(ad)
            }
            video_details.append(video_info)
        
        return video_details
    
    def _extract_video_thumbnail(self, media_url: str) -> str:
        """Extract or generate video thumbnail URL."""
        if not media_url:
            return ""
        
        # For Facebook videos, we can try to extract thumbnail
        # This is a simplified approach - in production, you might want to use video processing
        if 'video' in media_url.lower() or media_url.endswith(('.mp4', '.mov', '.avi')):
            # Return the same URL as thumbnail for now
            # In production, you'd generate actual thumbnails
            return media_url
        
        return media_url
    
    def _estimate_video_duration(self, ad: Dict[str, Any]) -> str:
        """Estimate video duration based on ad data."""
        # This is a placeholder - in production, you'd analyze the actual video
        # For now, we'll return a default duration
        return "15-30 seconds"  # Typical ad duration
    
    def _extract_engagement_indicators(self, ad: Dict[str, Any]) -> Dict[str, Any]:
        """Extract engagement indicators from ad data."""
        return {
            "has_call_to_action": bool(ad.get('ad_creative_link_titles')),
            "has_link_description": bool(ad.get('ad_creative_link_descriptions')),
            "has_captions": bool(ad.get('ad_creative_link_captions')),
            "multiple_languages": len(ad.get('languages', [])) > 1,
            "multiple_platforms": len(ad.get('publisher_platforms', [])) > 1,
            "estimated_reach": ad.get('estimated_audience_size', {}).get('lower_bound', 0)
        }
    
    def _generate_reasoning(self, ads_data: List[Dict[str, Any]], 
                          image_ads: List[Dict[str, Any]], 
                          video_ads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate detailed reasoning for the analysis."""
        
        total_ads = len(ads_data)
        video_count = len(video_ads)
        image_count = len(image_ads)
        
        reasoning = {
            "analysis_summary": f"Проаналізовано {total_ads} оголошень з Facebook Ads Library",
            "data_breakdown": {
                "total_ads": total_ads,
                "video_ads": video_count,
                "image_ads": image_count,
                "video_percentage": round((video_count / total_ads) * 100, 1) if total_ads > 0 else 0,
                "image_percentage": round((image_count / total_ads) * 100, 1) if total_ads > 0 else 0
            },
            "key_findings": self._generate_key_findings(ads_data, image_ads, video_ads),
            "trend_insights": self._generate_trend_insights(ads_data),
            "competitive_analysis": self._generate_competitive_analysis(ads_data),
            "recommendation_rationale": self._generate_recommendation_rationale(ads_data)
        }
        
        return reasoning
    
    def _generate_key_findings(self, ads_data: List[Dict[str, Any]], 
                             image_ads: List[Dict[str, Any]], 
                             video_ads: List[Dict[str, Any]]) -> List[str]:
        """Generate key findings from the analysis."""
        findings = []
        
        # Media type analysis
        if len(video_ads) > len(image_ads):
            findings.append(f"Відео контент домінує ({len(video_ads)} відео vs {len(image_ads)} зображень) - це вказує на тренд до динамічного контенту")
        elif len(image_ads) > len(video_ads):
            findings.append(f"Статичний контент популярніший ({len(image_ads)} зображень vs {len(video_ads)} відео) - можливо через простоту створення")
        
        # Text analysis
        all_text = [ad.get('body', '') for ad in ads_data if ad.get('body')]
        if all_text:
            avg_length = sum(len(text) for text in all_text) / len(all_text)
            if avg_length < 50:
                findings.append("Короткі повідомлення домінують - аудиторія віддає перевагу лаконічному контенту")
            elif avg_length > 150:
                findings.append("Довгі описи популярні - аудиторія готова читати детальну інформацію")
        
        # Brand analysis
        brands = Counter(ad.get('page_name', 'Unknown') for ad in ads_data)
        if brands:
            top_brand = brands.most_common(1)[0]
            findings.append(f"Найактивніший бренд: {top_brand[0]} ({top_brand[1]} оголошень)")
        
        # Emotional tone analysis
        all_text_combined = ' '.join(all_text).lower()
        if 'free' in all_text_combined:
            findings.append("Ключове слово 'безкоштовно' часто використовується - безкоштовні пропозиції ефективні")
        
        if 'new' in all_text_combined:
            findings.append("Акцент на новизні продуктів - інновації привабливі для аудиторії")
        
        return findings[:5]  # Limit to top 5 findings
    
    def _generate_trend_insights(self, ads_data: List[Dict[str, Any]]) -> List[str]:
        """Generate trend insights."""
        insights = []
        
        # Analyze recent activity
        recent_ads = [ad for ad in ads_data if ad.get('start_date')]
        if recent_ads:
            insights.append(f"Активність: {len(recent_ads)} оголошень з датами запуску")
        
        # Analyze platform distribution
        platforms = Counter()
        for ad in ads_data:
            platforms.update(ad.get('publisher_platforms', []))
        
        if platforms:
            top_platform = platforms.most_common(1)[0]
            insights.append(f"Найпопулярніша платформа: {top_platform[0]} ({top_platform[1]} оголошень)")
        
        # Analyze language diversity
        languages = set()
        for ad in ads_data:
            languages.update(ad.get('languages', []))
        
        if len(languages) > 1:
            insights.append(f"Мультимовність: {len(languages)} мов - глобальний підхід до маркетингу")
        
        return insights
    
    def _generate_competitive_analysis(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate competitive analysis."""
        brands = Counter(ad.get('page_name', 'Unknown') for ad in ads_data)
        
        analysis = {
            "total_competitors": len(brands),
            "top_competitors": dict(brands.most_common(5)),
            "market_concentration": self._calculate_market_concentration(brands),
            "competitive_intensity": "High" if len(brands) > 10 else "Medium" if len(brands) > 5 else "Low"
        }
        
        return analysis
    
    def _calculate_market_concentration(self, brands: Counter) -> str:
        """Calculate market concentration."""
        total_ads = sum(brands.values())
        if total_ads == 0:
            return "Unknown"
        
        # Calculate Herfindahl-Hirschman Index (simplified)
        hhi = sum((count / total_ads) ** 2 for count in brands.values())
        
        if hhi > 0.25:
            return "High concentration (few dominant players)"
        elif hhi > 0.15:
            return "Medium concentration"
        else:
            return "Low concentration (fragmented market)"
    
    def _generate_recommendation_rationale(self, ads_data: List[Dict[str, Any]]) -> List[str]:
        """Generate rationale for recommendations."""
        rationale = []
        
        # Video vs Image rationale
        video_ads = [ad for ad in ads_data if ad.get('media_type') == 'VIDEO']
        image_ads = [ad for ad in ads_data if ad.get('media_type') == 'IMAGE']
        
        if len(video_ads) > len(image_ads):
            rationale.append("Відео контент переважає серед конкурентів - рекомендуємо інвестувати в відео для конкурентоспроможності")
        else:
            rationale.append("Статичний контент популярний - можна досягти успіху з якісними зображеннями")
        
        # Text length rationale
        all_text = [ad.get('body', '') for ad in ads_data if ad.get('body')]
        if all_text:
            avg_length = sum(len(text) for text in all_text) / len(all_text)
            if avg_length < 100:
                rationale.append("Короткі повідомлення ефективні - аудиторія має обмежений час на читання")
            else:
                rationale.append("Детальні описи працюють - аудиторія цінує інформативність")
        
        # Emotional triggers rationale
        all_text_combined = ' '.join(all_text).lower()
        if 'urgent' in all_text_combined or 'limited' in all_text_combined:
            rationale.append("Терміновість працює - створюйте обмежені за часом пропозиції")
        
        return rationale


# Global instance
trend_analysis_service = TrendAnalysisService()
