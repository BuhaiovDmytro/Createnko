import logging
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

class VideoGeneratorService:
    """Service for generating video descriptions for Veo and other video generators."""
    
    def __init__(self):
        self.logger = logger
        self.supported_generators = ['veo', 'runway', 'pika', 'stable_video', 'sora']
    
    def generate_video_description_from_insights(self, user_query: str, video_insights: List[Dict[str, Any]], 
                                               generator_type: str = 'veo', 
                                               style_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate video description based on analyzed video insights from Gemini.
        
        Args:
            user_query: User's original request/query
            video_insights: List of video insights from Gemini analysis
            generator_type: Type of video generator ('veo', 'runway', 'pika', etc.)
            style_preferences: Optional style preferences from user
            
        Returns:
            Dictionary with generated video description and recommendations
        """
        try:
            if not user_query or not video_insights:
                return {
                    "success": False,
                    "message": "User query and video insights are required",
                    "video_description": "",
                    "error": "Missing required parameters"
                }
            
            self.logger.info(f"Generating video description for {len(video_insights)} insights")
            self.logger.info(f"Generator type: {generator_type}, type: {type(generator_type)}")
            
            # Validate generator type
            if generator_type.lower() not in self.supported_generators:
                generator_type = 'veo'  # Default to Veo
            
            self.logger.info("Extracting combined insights...")
            # Extract insights from all videos
            combined_insights = self._extract_combined_insights(video_insights)
            self.logger.info("Combined insights extracted successfully")
            
            # Generate main video description
            video_description = self._create_video_description_from_insights(
                user_query, combined_insights, generator_type, style_preferences
            )
            
            # Generate variations
            variations = self._create_video_variations(
                user_query, combined_insights, generator_type, style_preferences
            )
            
            # Generate recommendations
            recommendations = self._create_recommendations_from_insights(
                combined_insights, generator_type
            )
            
            # Generate technical specifications
            technical_specs = self._create_technical_specifications(
                generator_type, combined_insights
            )
            
            return {
                "success": True,
                "message": f"Successfully generated video description for {generator_type.upper()} based on {len(video_insights)} video insights",
                "video_description": video_description,
                "variations": variations,
                "recommendations": recommendations,
                "technical_specifications": technical_specs,
                "generated_at": datetime.now().isoformat(),
                "generator_type": generator_type.lower(),
                "insights_analyzed": len(video_insights)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating video description from insights: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to generate video description: {str(e)}",
                "video_description": "",
                "error": str(e)
            }

    def generate_video_description(self, user_query: str, trends_data: Dict[str, Any], 
                                 generator_type: str = 'veo', 
                                 style_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate video description for video generators based on user query and trends.
        
        Args:
            user_query: User's original request/query
            trends_data: Trend analysis data from Facebook Ads Library
            generator_type: Type of video generator ('veo', 'runway', 'pika', etc.)
            style_preferences: Optional style preferences from user
            
        Returns:
            Dictionary with generated video description and recommendations
        """
        try:
            if not user_query or not trends_data:
                return {
                    "success": False,
                    "message": "User query and trends data are required",
                    "video_description": "",
                    "error": "Missing required parameters"
                }
            
            # Validate generator type
            if generator_type.lower() not in self.supported_generators:
                generator_type = 'veo'  # Default to Veo
            
            # Extract key insights from trends
            trend_insights = self._extract_trend_insights(trends_data)
            
            # Generate main video description
            video_description = self._create_video_description(
                user_query, trend_insights, generator_type, style_preferences
            )
            
            # Generate unique variations
            variations = self._create_unique_variations(
                video_description, trend_insights, generator_type
            )
            
            # Generate additional recommendations
            recommendations = self._generate_recommendations(
                user_query, trend_insights, generator_type
            )
            
            # Create technical specifications
            technical_specs = self._generate_technical_specs(
                trend_insights, generator_type
            )
            
            return {
                "success": True,
                "message": f"Generated unique video descriptions for {generator_type.upper()}",
                "video_description": video_description,
                "variations": variations,
                "recommendations": recommendations,
                "technical_specifications": technical_specs,
                "trend_insights_used": trend_insights,
                "generator_type": generator_type,
                "generated_at": datetime.now().isoformat(),
                "error": None
            }
            
        except Exception as e:
            self.logger.error(f"Video description generation failed: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to generate video description: {str(e)}",
                "video_description": "",
                "error": str(e)
            }
    
    def _extract_trend_insights(self, trends_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key insights from trends data."""
        insights = {
            "content_trends": {},
            "visual_trends": {},
            "messaging_trends": {},
            "format_trends": {},
            "recommendations": {}
        }
        
        try:
            trends = trends_data.get('trends', {})
            
            # Extract content trends
            content_trends = trends.get('content_trends', {})
            insights["content_trends"] = {
                "common_words": content_trends.get('word_frequency', {}),
                "common_phrases": content_trends.get('phrase_patterns', {}),
                "themes": content_trends.get('common_themes', []),
                "text_length_stats": content_trends.get('text_length_stats', {})
            }
            
            # Extract visual trends
            visual_trends = trends.get('visual_trends', {})
            insights["visual_trends"] = {
                "image_count": visual_trends.get('image_count', 0),
                "visual_style_indicators": visual_trends.get('visual_style_indicators', {})
            }
            
            # Extract video trends
            video_trends = trends.get('video_trends', {})
            insights["video_trends"] = {
                "video_count": video_trends.get('video_count', 0),
                "video_format_indicators": video_trends.get('video_format_indicators', {})
            }
            
            # Extract messaging trends
            messaging_trends = trends.get('messaging_trends', {})
            insights["messaging_trends"] = {
                "emotional_tone": messaging_trends.get('emotional_tone', {}),
                "cta_patterns": messaging_trends.get('cta_patterns', {}),
                "value_propositions": messaging_trends.get('value_propositions', {}),
                "messaging_strategies": messaging_trends.get('messaging_strategies', [])
            }
            
            # Extract format trends
            format_trends = trends.get('format_trends', {})
            insights["format_trends"] = {
                "format_distribution": format_trends.get('format_distribution', {}),
                "format_preferences": format_trends.get('format_preferences', {})
            }
            
            # Extract recommendations
            recommendations = trends.get('recommendations', {})
            insights["recommendations"] = recommendations
            
        except Exception as e:
            self.logger.warning(f"Failed to extract some trend insights: {str(e)}")
        
        return insights
    
    def _analyze_user_query(self, user_query: str) -> Dict[str, Any]:
        """Analyze user query to understand intent, context, and requirements."""
        analysis = {
            "intent": "general",
            "video_type": "promotional",
            "target_audience": "general",
            "emotional_tone": "positive",
            "content_focus": "product_showcase",
            "urgency_level": "normal",
            "style_preferences": [],
            "key_elements": [],
            "call_to_action": "learn_more",
            "complexity": "medium"
        }
        
        query_lower = user_query.lower()
        
        # Analyze intent
        if any(word in query_lower for word in ['реклама', 'рекламне', 'рекламний', 'advertisement', 'ad', 'promo']):
            analysis["intent"] = "advertising"
            analysis["video_type"] = "commercial"
        elif any(word in query_lower for word in ['туторіал', 'навчання', 'як', 'tutorial', 'how to', 'learn']):
            analysis["intent"] = "educational"
            analysis["video_type"] = "tutorial"
        elif any(word in query_lower for word in ['презентація', 'демонстрація', 'показати', 'presentation', 'demo', 'show']):
            analysis["intent"] = "demonstration"
            analysis["video_type"] = "product_demo"
        elif any(word in query_lower for word in ['історія', 'story', 'narrative', 'розповідь']):
            analysis["intent"] = "storytelling"
            analysis["video_type"] = "narrative"
        
        # Analyze target audience
        if any(word in query_lower for word in ['молодь', 'підлітки', 'teen', 'youth', 'young']):
            analysis["target_audience"] = "youth"
        elif any(word in query_lower for word in ['дорослі', 'бізнес', 'adult', 'business', 'professional']):
            analysis["target_audience"] = "adults"
        elif any(word in query_lower for word in ['сім\'я', 'family', 'parents']):
            analysis["target_audience"] = "families"
        
        # Analyze emotional tone
        if any(word in query_lower for word in ['веселий', 'радісний', 'fun', 'happy', 'joyful']):
            analysis["emotional_tone"] = "joyful"
        elif any(word in query_lower for word in ['серйозний', 'серйозно', 'serious', 'professional']):
            analysis["emotional_tone"] = "serious"
        elif any(word in query_lower for word in ['надихаючий', 'мотивуючий', 'inspiring', 'motivational']):
            analysis["emotional_tone"] = "inspiring"
        elif any(word in query_lower for word in ['терміново', 'швидко', 'urgent', 'quick', 'fast']):
            analysis["emotional_tone"] = "urgent"
            analysis["urgency_level"] = "high"
        
        # Analyze content focus
        if any(word in query_lower for word in ['продукт', 'товар', 'product', 'item']):
            analysis["content_focus"] = "product_showcase"
        elif any(word in query_lower for word in ['послуга', 'service', 'сервіс']):
            analysis["content_focus"] = "service_demonstration"
        elif any(word in query_lower for word in ['бренд', 'компанія', 'brand', 'company']):
            analysis["content_focus"] = "brand_story"
        elif any(word in query_lower for word in ['функції', 'можливості', 'features', 'capabilities']):
            analysis["content_focus"] = "feature_highlight"
        
        # Analyze style preferences
        if any(word in query_lower for word in ['мінімалістичний', 'простий', 'minimalist', 'simple', 'clean']):
            analysis["style_preferences"].append("minimalist")
        elif any(word in query_lower for word in ['яскравий', 'кольоровий', 'bright', 'colorful', 'vibrant']):
            analysis["style_preferences"].append("colorful")
        elif any(word in query_lower for word in ['елегантний', 'розкішний', 'elegant', 'luxury', 'premium']):
            analysis["style_preferences"].append("elegant")
        elif any(word in query_lower for word in ['сучасний', 'модний', 'modern', 'trendy', 'contemporary']):
            analysis["style_preferences"].append("modern")
        
        # Analyze key elements
        if any(word in query_lower for word in ['анімація', 'рух', 'animation', 'motion']):
            analysis["key_elements"].append("animation")
        if any(word in query_lower for word in ['текст', 'надписи', 'text', 'typography']):
            analysis["key_elements"].append("text_overlay")
        if any(word in query_lower for word in ['музика', 'звук', 'music', 'audio']):
            analysis["key_elements"].append("audio")
        if any(word in query_lower for word in ['переходи', 'transitions', 'effects']):
            analysis["key_elements"].append("transitions")
        
        # Analyze call to action
        if any(word in query_lower for word in ['купити', 'замовити', 'buy', 'order', 'purchase']):
            analysis["call_to_action"] = "purchase"
        elif any(word in query_lower for word in ['завантажити', 'download', 'install']):
            analysis["call_to_action"] = "download"
        elif any(word in query_lower for word in ['підписатися', 'subscribe', 'follow']):
            analysis["call_to_action"] = "subscribe"
        elif any(word in query_lower for word in ['дізнатися', 'learn more', 'find out']):
            analysis["call_to_action"] = "learn_more"
        
        # Analyze complexity
        if len(user_query.split()) > 20 or any(word in query_lower for word in ['складний', 'детальний', 'complex', 'detailed']):
            analysis["complexity"] = "high"
        elif len(user_query.split()) < 5:
            analysis["complexity"] = "low"
        
        return analysis
    
    def _create_video_description(self, user_query: str, trend_insights: Dict[str, Any], 
                                 generator_type: str, style_preferences: Optional[Dict[str, Any]]) -> str:
        """Create a highly detailed and unique video description."""
        
        # Analyze user query for intent and context
        query_analysis = self._analyze_user_query(user_query)
        
        # Extract specific competitive insights
        competitive_insights = self._extract_competitive_insights(trend_insights)
        
        # Create a narrative-driven description
        description_parts = []
        
        # 1. Opening Hook (based on trending emotional triggers and user intent)
        opening_hook = self._create_opening_hook(trend_insights, query_analysis)
        description_parts.append(opening_hook)
        
        # 2. Visual Storytelling (based on successful competitor patterns and user needs)
        visual_story = self._create_visual_story(trend_insights, competitive_insights, query_analysis)
        description_parts.append(visual_story)
        
        # 3. Specific Scene Descriptions (based on trending content and user intent)
        scene_descriptions = self._create_scene_descriptions(trend_insights, query_analysis)
        description_parts.extend(scene_descriptions)
        
        # 4. Technical Execution (generator-specific and user-optimized)
        technical_execution = self._create_technical_execution(trend_insights, generator_type, query_analysis)
        description_parts.append(technical_execution)
        
        # 5. Emotional Arc (based on messaging trends and user psychology)
        emotional_arc = self._create_emotional_arc(trend_insights, query_analysis)
        description_parts.append(emotional_arc)
        
        # 6. Call-to-Action Integration (based on successful CTAs and user intent)
        cta_integration = self._create_cta_integration(trend_insights, query_analysis)
        description_parts.append(cta_integration)
        
        return " ".join(description_parts)
    
    def _extract_competitive_insights(self, trend_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Extract specific competitive insights for personalized prompts."""
        insights = {
            "dominant_visual_style": "",
            "successful_messaging_patterns": [],
            "trending_content_themes": [],
            "effective_cta_patterns": [],
            "emotional_triggers": [],
            "visual_composition_trends": []
        }
        
        # Analyze visual trends
        visual_trends = trend_insights.get('visual_trends', {})
        video_trends = trend_insights.get('video_trends', {})
        
        if video_trends.get('video_count', 0) > visual_trends.get('image_count', 0):
            insights["dominant_visual_style"] = "dynamic_video_focused"
        else:
            insights["dominant_visual_style"] = "static_image_focused"
        
        # Analyze messaging patterns
        messaging_trends = trend_insights.get('messaging_trends', {})
        emotional_tone = messaging_trends.get('emotional_tone', {})
        
        for tone, count in emotional_tone.items():
            if count > 0:
                insights["emotional_triggers"].append(tone)
        
        # Analyze content themes
        content_trends = trend_insights.get('content_trends', {})
        themes = content_trends.get('themes', [])
        insights["trending_content_themes"] = themes[:3]
        
        # Analyze CTA patterns
        cta_patterns = messaging_trends.get('cta_patterns', {})
        insights["effective_cta_patterns"] = list(cta_patterns.keys())[:3]
        
        return insights
    
    def _create_opening_hook(self, trend_insights: Dict[str, Any], query_analysis: Dict[str, Any]) -> str:
        """Create an attention-grabbing opening hook based on trends and user intent."""
        messaging_trends = trend_insights.get('messaging_trends', {})
        emotional_tone = messaging_trends.get('emotional_tone', {})
        
        # Determine the most effective emotional trigger from both trends and user analysis
        user_tone = query_analysis.get('emotional_tone', 'positive')
        trend_tone = max(emotional_tone.items(), key=lambda x: x[1])[0] if emotional_tone else 'positive'
        
        # Combine user intent with trending emotional triggers
        video_type = query_analysis.get('video_type', 'promotional')
        target_audience = query_analysis.get('target_audience', 'general')
        urgency_level = query_analysis.get('urgency_level', 'normal')
        
        # Create context-aware opening hooks
        if video_type == 'tutorial':
            return f"Open with a clear, relatable problem that your target audience faces. Show the frustration or challenge in a way that immediately connects with {target_audience}, using authentic expressions and real-world scenarios."
        elif video_type == 'commercial':
            if urgency_level == 'high':
                return f"Start with a dramatic, time-sensitive moment that immediately captures attention. Show a problem or challenge that needs immediate resolution, with intense lighting and quick cuts to build urgency."
            else:
                return f"Begin with an engaging moment that showcases the value proposition. Use compelling visuals that speak directly to {target_audience} needs and desires."
        elif video_type == 'narrative':
            return f"Open with a compelling character or situation that draws viewers into the story. Create emotional connection through authentic moments that resonate with {target_audience}."
        elif video_type == 'product_demo':
            return f"Start with a clear demonstration of the problem your product solves. Show the 'before' state in a way that {target_audience} can immediately relate to and understand."
        
        # Fallback to emotional tone-based hooks
        hook_templates = {
            'urgent': f"Open with a dramatic, time-sensitive moment that immediately captures attention. Show a problem or challenge that needs immediate resolution, with intense lighting and quick cuts.",
            'positive': f"Begin with an uplifting, inspiring moment that showcases transformation and possibility. Use warm, bright lighting and smooth camera movements to create an optimistic atmosphere.",
            'serious': f"Start with a professional, authoritative moment that establishes credibility and expertise. Use clean, focused lighting and steady camera work.",
            'inspiring': f"Open with a motivational moment that sparks ambition and possibility. Use dynamic lighting and inspiring visuals that energize the viewer.",
            'joyful': f"Begin with a fun, energetic moment that immediately brings a smile. Use bright colors, playful movements, and positive energy."
        }
        
        return hook_templates.get(user_tone, f"Create an engaging opening that immediately draws viewers in and establishes the video's purpose.")
    
    def _create_visual_story(self, trend_insights: Dict[str, Any], competitive_insights: Dict[str, Any], query_analysis: Dict[str, Any]) -> str:
        """Create detailed visual storytelling based on successful patterns and user intent."""
        visual_style = competitive_insights.get('dominant_visual_style', 'dynamic_video_focused')
        themes = competitive_insights.get('trending_content_themes', [])
        
        # Get user preferences
        style_preferences = query_analysis.get('style_preferences', [])
        content_focus = query_analysis.get('content_focus', 'product_showcase')
        complexity = query_analysis.get('complexity', 'medium')
        
        # Create style-specific visual story
        if 'minimalist' in style_preferences:
            story_base = "Create a clean, minimalist visual narrative with plenty of white space, simple compositions, and focused elements."
        elif 'colorful' in style_preferences:
            story_base = "Develop a vibrant, colorful visual story with bold color palettes, dynamic contrasts, and energetic compositions."
        elif 'elegant' in style_preferences:
            story_base = "Craft an elegant, sophisticated visual narrative with refined aesthetics, premium materials, and luxury elements."
        elif 'modern' in style_preferences:
            story_base = "Create a contemporary, modern visual story with sleek designs, innovative layouts, and cutting-edge aesthetics."
        else:
            story_base = "Develop a compelling visual narrative that effectively communicates your message."
        
        # Add content focus
        if content_focus == 'product_showcase':
            story_base += " Focus on highlighting product features, benefits, and unique selling points through clear, detailed visuals."
        elif content_focus == 'service_demonstration':
            story_base += " Emphasize the service delivery process, customer experience, and value creation through step-by-step visual storytelling."
        elif content_focus == 'brand_story':
            story_base += " Tell the brand story through authentic moments, company values, and emotional connections."
        elif content_focus == 'feature_highlight':
            story_base += " Showcase specific features and capabilities through detailed demonstrations and clear explanations."
        
        # Add complexity considerations
        if complexity == 'high':
            story_base += " Include multiple visual layers, complex compositions, and detailed elements that require careful attention."
        elif complexity == 'low':
            story_base += " Keep visuals simple, clear, and easy to understand with minimal distractions."
        
        # Add trending themes
        if themes:
            story_base += f" Incorporate trending themes like {', '.join(themes[:2])} to stay relevant and engaging."
        
        return story_base
    
    def _create_scene_descriptions(self, trend_insights: Dict[str, Any], query_analysis: Dict[str, Any]) -> List[str]:
        """Create specific scene descriptions based on trending content and user intent."""
        scenes = []
        
        # Get user analysis data
        video_type = query_analysis.get('video_type', 'promotional')
        content_focus = query_analysis.get('content_focus', 'product_showcase')
        target_audience = query_analysis.get('target_audience', 'general')
        emotional_tone = query_analysis.get('emotional_tone', 'positive')
        key_elements = query_analysis.get('key_elements', [])
        
        # Create context-aware scenes based on video type
        if video_type == 'tutorial':
            scenes.append(f"Scene 1: Establish the learning objective clearly. Show the current state or problem that needs to be solved, using relatable scenarios that {target_audience} can identify with.")
            scenes.append(f"Scene 2: Demonstrate the step-by-step process. Use clear, detailed shots that show each action clearly, with helpful visual cues and explanations.")
            scenes.append(f"Scene 3: Show the successful outcome and reinforce key learning points. Highlight the benefits and practical applications.")
            
        elif video_type == 'commercial':
            # Scene 1: Problem/Challenge
            messaging_trends = trend_insights.get('messaging_trends', {})
            strategies = messaging_trends.get('messaging_strategies', [])
            
            if 'problem-solution' in strategies:
                scenes.append(f"Scene 1: Show a relatable problem or challenge that your product addresses. Use close-up shots of frustrated expressions, cluttered environments, or obstacles that create empathy and connection with {target_audience}.")
            
            # Scene 2: Solution Introduction
            value_props = messaging_trends.get('value_propositions', {})
            dominant_value = max(value_props.items(), key=lambda x: x[1])[0] if value_props else 'quality'
            
            value_scenes = {
                'price': f"Scene 2: Reveal your product as an affordable solution with money-saving visuals, price comparisons, and budget-friendly aesthetics that appeal to {target_audience}.",
                'quality': f"Scene 2: Showcase your product with premium quality indicators, detailed craftsmanship, and high-end visual elements that demonstrate superior value.",
                'convenience': f"Scene 2: Demonstrate your product's ease of use with simple, effortless actions, streamlined processes, and user-friendly interfaces.",
                'results': f"Scene 2: Highlight your product's benefits with before/after comparisons, measurable outcomes, and clear value demonstration."
            }
            
            scenes.append(value_scenes.get(dominant_value, f"Scene 2: Introduce your product as the solution with clear, compelling visual evidence that speaks to {target_audience}."))
            
            # Scene 3: Transformation/Outcome
            if emotional_tone in ['positive', 'joyful', 'inspiring']:
                scenes.append(f"Scene 3: Show the positive transformation and outcomes of using your product. Use bright, uplifting visuals, satisfied expressions, and successful results that inspire {target_audience}.")
                
        elif video_type == 'narrative':
            scenes.append(f"Scene 1: Introduce the main character or situation. Create emotional connection through authentic moments that resonate with {target_audience}.")
            scenes.append(f"Scene 2: Develop the story with conflict or challenge. Show character growth, obstacles overcome, or meaningful moments.")
            scenes.append(f"Scene 3: Resolve the story with a satisfying conclusion. Show transformation, learning, or emotional payoff.")
            
        elif video_type == 'product_demo':
            scenes.append(f"Scene 1: Show the problem or need that your product addresses. Demonstrate the current pain points or limitations that {target_audience} experiences.")
            scenes.append(f"Scene 2: Demonstrate your product in action. Show key features, functionality, and benefits through clear, detailed demonstrations.")
            scenes.append(f"Scene 3: Highlight the results and benefits. Show the positive outcomes, improvements, and value that your product delivers.")
        
        # Add key elements if specified
        if 'animation' in key_elements:
            scenes.append("Include smooth animations and dynamic motion throughout the scenes to enhance visual appeal and engagement.")
        if 'text_overlay' in key_elements:
            scenes.append("Incorporate clear, readable text overlays that reinforce key messages and provide additional context.")
        if 'transitions' in key_elements:
            scenes.append("Use creative transitions between scenes that maintain visual flow and enhance the storytelling.")
        
        return scenes
    
    def _create_technical_execution(self, trend_insights: Dict[str, Any], generator_type: str, query_analysis: Dict[str, Any]) -> str:
        """Create technical execution details for the specific generator and user needs."""
        complexity = query_analysis.get('complexity', 'medium')
        key_elements = query_analysis.get('key_elements', [])
        video_type = query_analysis.get('video_type', 'promotional')
        
        # Base technical specs
        technical_specs = {
            'veo': "Execute with Veo's cinematic capabilities: use smooth camera movements, realistic lighting, and natural motion. Focus on 16:9 aspect ratio with 1080p quality, 5-15 second duration. Emphasize photorealistic rendering and fluid transitions.",
            'runway': "Leverage Runway's creative tools: use artistic style consistency, creative editing features, and expressive motion. Optimize for 16:9 or 9:16 formats with HD quality, 3-10 second duration. Focus on creative expression and artistic flair.",
            'pika': "Utilize Pika's artistic capabilities: emphasize creative animations, visual appeal, and artistic style. Use square or 16:9 aspect ratios with 2-8 second duration. Focus on creative visual storytelling and artistic expression.",
            'stable_video': "Apply Stable Video's generation: keep prompts clear and simple, ensure stable generation, maintain consistent style. Use 16:9 aspect ratio with 2-5 second duration. Focus on reliable, consistent output.",
            'sora': "Harness Sora's advanced features: use detailed descriptions, focus on realism, leverage high-quality generation. Use 16:9 aspect ratio with 5-20 second duration. Emphasize photorealistic quality and complex scenes."
        }
        
        base_spec = technical_specs.get(generator_type.lower(), "Execute with standard video generation parameters and high-quality output.")
        
        # Add complexity considerations
        if complexity == 'high':
            base_spec += " Include detailed technical specifications, complex scene compositions, and sophisticated visual elements."
        elif complexity == 'low':
            base_spec += " Keep technical requirements simple and straightforward for easy execution."
        
        # Add key elements considerations
        if 'animation' in key_elements:
            base_spec += " Prioritize smooth animations and dynamic motion throughout the video."
        if 'text_overlay' in key_elements:
            base_spec += " Ensure clear, readable text overlays with proper contrast and positioning."
        if 'transitions' in key_elements:
            base_spec += " Use creative transitions and effects to enhance visual flow."
        
        # Add video type considerations
        if video_type == 'tutorial':
            base_spec += " Focus on clear, educational visuals with step-by-step clarity and instructional design."
        elif video_type == 'commercial':
            base_spec += " Optimize for commercial appeal with attention-grabbing visuals and persuasive elements."
        elif video_type == 'narrative':
            base_spec += " Emphasize storytelling elements with character development and emotional pacing."
        
        return base_spec
    
    def _create_emotional_arc(self, trend_insights: Dict[str, Any], query_analysis: Dict[str, Any]) -> str:
        """Create emotional arc based on messaging trends and user intent."""
        messaging_trends = trend_insights.get('messaging_trends', {})
        emotional_tone = messaging_trends.get('emotional_tone', {})
        
        # Get user analysis
        user_tone = query_analysis.get('emotional_tone', 'positive')
        video_type = query_analysis.get('video_type', 'promotional')
        target_audience = query_analysis.get('target_audience', 'general')
        
        # Create emotional progression based on user intent
        arc_parts = []
        
        # Video type specific emotional arcs
        if video_type == 'tutorial':
            arc_parts.append("Start with curiosity and engagement, build confidence through learning, and end with empowerment and achievement")
        elif video_type == 'commercial':
            if user_tone == 'urgent':
                arc_parts.append("Build tension and urgency in the first half, then provide relief and satisfaction")
            elif user_tone == 'inspiring':
                arc_parts.append("Begin with aspiration, show transformation possibilities, and end with motivation and action")
            else:
                arc_parts.append("Start with relatability, build desire and interest, and conclude with satisfaction and action")
        elif video_type == 'narrative':
            arc_parts.append("Establish emotional connection, develop conflict or challenge, and resolve with meaningful payoff")
        elif video_type == 'product_demo':
            arc_parts.append("Begin with problem recognition, build understanding and interest, and end with confidence and desire")
        
        # Add trend-based emotional elements
        if emotional_tone.get('urgent', 0) > 0:
            arc_parts.append("incorporate urgency and time-sensitivity")
        
        if emotional_tone.get('positive', 0) > 0:
            arc_parts.append("maintain uplifting and optimistic tone")
        
        if emotional_tone.get('exclusive', 0) > 0:
            arc_parts.append("convey premium, exclusive feeling")
        
        if emotional_tone.get('social', 0) > 0:
            arc_parts.append("emphasize connection and community")
        
        if arc_parts:
            return f"Create an emotional arc that {', '.join(arc_parts)} to maximize engagement with {target_audience} and drive desired action."
        else:
            return f"Develop a compelling emotional journey that resonates with {target_audience} and creates meaningful connection."
    
    def _create_cta_integration(self, trend_insights: Dict[str, Any], query_analysis: Dict[str, Any]) -> str:
        """Create call-to-action integration based on successful patterns and user intent."""
        messaging_trends = trend_insights.get('messaging_trends', {})
        cta_patterns = messaging_trends.get('cta_patterns', {})
        
        # Get user analysis
        user_cta = query_analysis.get('call_to_action', 'learn_more')
        video_type = query_analysis.get('video_type', 'promotional')
        target_audience = query_analysis.get('target_audience', 'general')
        urgency_level = query_analysis.get('urgency_level', 'normal')
        
        # Create context-aware CTA based on user intent
        if user_cta == 'purchase':
            if urgency_level == 'high':
                return f"Integrate a compelling 'Buy Now' moment with urgency-inducing visuals, countdown elements, and clear purchase indicators that appeal to {target_audience}."
            else:
                return f"Create an engaging 'Shop Now' sequence with product showcases, easy navigation visuals, and shopping-focused aesthetics that guide {target_audience} to purchase."
        elif user_cta == 'download':
            return f"Create a compelling 'Download' sequence with app store visuals, installation process, and digital convenience indicators that make it easy for {target_audience} to get started."
        elif user_cta == 'subscribe':
            return f"Develop an inviting 'Subscribe' moment with community benefits, exclusive content previews, and membership-focused aesthetics that appeal to {target_audience}."
        elif user_cta == 'learn_more':
            return f"Design an informative 'Learn More' section with educational visuals, detailed explanations, and knowledge-focused presentation that satisfies {target_audience}'s curiosity."
        
        # Fallback to trend-based CTA
        if cta_patterns:
            # Get the most effective CTA pattern from trends
            top_cta = max(cta_patterns.items(), key=lambda x: x[1])[0]
            
            cta_integrations = {
                'buy now': f"Integrate a compelling 'Buy Now' moment with urgency-inducing visuals, countdown elements, and clear purchase indicators that resonate with {target_audience}.",
                'shop now': f"Create an engaging 'Shop Now' sequence with product showcases, easy navigation visuals, and shopping-focused aesthetics that guide {target_audience}.",
                'learn more': f"Design an informative 'Learn More' section with educational visuals, detailed explanations, and knowledge-focused presentation for {target_audience}.",
                'sign up': f"Develop an inviting 'Sign Up' moment with registration visuals, community benefits, and membership-focused aesthetics that appeal to {target_audience}.",
                'download': f"Create a compelling 'Download' sequence with app store visuals, installation process, and digital convenience indicators for {target_audience}."
            }
            
            return cta_integrations.get(top_cta, f"Integrate a clear, compelling call-to-action that drives {target_audience} engagement and conversion.")
        else:
            return f"Include a strong, clear call-to-action that motivates {target_audience} to take the desired action."
    
    def _create_unique_variations(self, base_description: str, trend_insights: Dict[str, Any], 
                                generator_type: str) -> List[str]:
        """Create multiple unique variations of the video description."""
        variations = []
        
        # Variation 1: Focus on emotional storytelling
        emotional_variation = self._create_emotional_variation(base_description, trend_insights)
        variations.append(emotional_variation)
        
        # Variation 2: Focus on technical excellence
        technical_variation = self._create_technical_variation(base_description, generator_type)
        variations.append(technical_variation)
        
        # Variation 3: Focus on competitive differentiation
        competitive_variation = self._create_competitive_variation(base_description, trend_insights)
        variations.append(competitive_variation)
        
        return variations
    
    def _create_emotional_variation(self, base_description: str, trend_insights: Dict[str, Any]) -> str:
        """Create an emotionally-focused variation."""
        messaging_trends = trend_insights.get('messaging_trends', {})
        emotional_tone = messaging_trends.get('emotional_tone', {})
        
        # Extract the most dominant emotional tone
        dominant_tone = max(emotional_tone.items(), key=lambda x: x[1])[0] if emotional_tone else 'positive'
        
        emotional_prefixes = {
            'urgent': "Create an emotionally charged video that builds tension and urgency. ",
            'positive': "Develop an uplifting, inspiring narrative that creates emotional connection. ",
            'exclusive': "Craft a sophisticated, premium experience that conveys exclusivity. ",
            'social': "Build a relatable, community-focused story that emphasizes human connection. "
        }
        
        return emotional_prefixes.get(dominant_tone, "Create an emotionally engaging video that resonates deeply with viewers. ") + base_description
    
    def _create_technical_variation(self, base_description: str, generator_type: str) -> str:
        """Create a technically-focused variation."""
        technical_prefixes = {
            'veo': "Optimize for Veo's cinematic capabilities with photorealistic rendering. ",
            'runway': "Leverage Runway's creative tools for artistic expression. ",
            'pika': "Utilize Pika's artistic capabilities for creative storytelling. ",
            'stable_video': "Apply Stable Video's reliable generation for consistent output. ",
            'sora': "Harness Sora's advanced features for high-quality realism. "
        }
        
        return technical_prefixes.get(generator_type.lower(), "Focus on technical excellence and high-quality output. ") + base_description
    
    def _create_competitive_variation(self, base_description: str, trend_insights: Dict[str, Any]) -> str:
        """Create a competitive differentiation variation."""
        content_trends = trend_insights.get('content_trends', {})
        themes = content_trends.get('themes', [])
        
        if themes:
            theme_focus = f"Differentiate by emphasizing {', '.join(themes[:2])} themes that competitors are missing. "
        else:
            theme_focus = "Stand out from competitors with unique positioning and messaging. "
        
        return theme_focus + base_description
    
    def _get_visual_style_recommendations(self, trend_insights: Dict[str, Any]) -> str:
        """Get visual style recommendations from trends."""
        recommendations = []
        
        # Analyze visual trends
        visual_trends = trend_insights.get('visual_trends', {})
        video_trends = trend_insights.get('video_trends', {})
        
        # Check if video content is trending
        video_count = video_trends.get('video_count', 0)
        image_count = visual_trends.get('image_count', 0)
        
        if video_count > image_count:
            recommendations.append("dynamic video content with smooth transitions")
        else:
            recommendations.append("high-quality visual content with clear composition")
        
        # Add messaging-based visual recommendations
        messaging_trends = trend_insights.get('messaging_trends', {})
        emotional_tone = messaging_trends.get('emotional_tone', {})
        
        if emotional_tone.get('positive', 0) > 0:
            recommendations.append("bright, uplifting visual tone")
        
        if emotional_tone.get('urgent', 0) > 0:
            recommendations.append("attention-grabbing visuals with bold elements")
        
        return ", ".join(recommendations) if recommendations else "professional, engaging visuals"
    
    def _get_messaging_recommendations(self, trend_insights: Dict[str, Any]) -> str:
        """Get messaging recommendations from trends."""
        recommendations = []
        
        messaging_trends = trend_insights.get('messaging_trends', {})
        
        # Analyze emotional tone
        emotional_tone = messaging_trends.get('emotional_tone', {})
        if emotional_tone:
            dominant_tone = max(emotional_tone.items(), key=lambda x: x[1])[0] if emotional_tone else None
            if dominant_tone:
                tone_mapping = {
                    'positive': 'positive and uplifting messaging',
                    'urgent': 'urgent and action-oriented messaging',
                    'exclusive': 'exclusive and premium messaging',
                    'social': 'social and community-focused messaging'
                }
                recommendations.append(tone_mapping.get(dominant_tone, 'engaging messaging'))
        
        # Analyze messaging strategies
        strategies = messaging_trends.get('messaging_strategies', [])
        if strategies:
            strategy_mapping = {
                'storytelling': 'narrative storytelling approach',
                'problem-solution': 'problem-solution format',
                'before-after': 'transformation showcase',
                'social_proof': 'social proof and testimonials',
                'scarcity': 'limited-time offers'
            }
            for strategy in strategies[:2]:  # Top 2 strategies
                if strategy in strategy_mapping:
                    recommendations.append(strategy_mapping[strategy])
        
        # Analyze value propositions
        value_props = messaging_trends.get('value_propositions', {})
        if value_props:
            dominant_value = max(value_props.items(), key=lambda x: x[1])[0] if value_props else None
            if dominant_value:
                value_mapping = {
                    'price': 'cost-effective value proposition',
                    'quality': 'premium quality focus',
                    'convenience': 'ease of use and convenience',
                    'results': 'clear benefits and outcomes',
                    'guarantee': 'risk-free guarantee'
                }
                recommendations.append(value_mapping.get(dominant_value, 'strong value proposition'))
        
        return ", ".join(recommendations) if recommendations else "clear and compelling messaging"
    
    def _get_format_recommendations(self, trend_insights: Dict[str, Any], generator_type: str) -> str:
        """Get format recommendations from trends."""
        recommendations = []
        
        format_trends = trend_insights.get('format_trends', {})
        format_distribution = format_trends.get('format_distribution', {})
        
        # Analyze preferred formats
        if format_distribution.get('VIDEO', 0) > format_distribution.get('IMAGE', 0):
            recommendations.append("video format")
        else:
            recommendations.append("visual content format")
        
        # Add generator-specific recommendations
        generator_specs = {
            'veo': 'high-quality video generation with smooth motion',
            'runway': 'creative video editing and generation',
            'pika': 'animated content with artistic style',
            'stable_video': 'stable diffusion-based video generation',
            'sora': 'advanced AI video generation'
        }
        
        if generator_type.lower() in generator_specs:
            recommendations.append(generator_specs[generator_type.lower()])
        
        return ", ".join(recommendations) if recommendations else "standard video format"
    
    def _get_technical_recommendations(self, generator_type: str) -> str:
        """Get technical recommendations for specific generator."""
        technical_specs = {
            'veo': '16:9 aspect ratio, 1080p resolution, 5-15 seconds duration',
            'runway': '16:9 or 9:16 aspect ratio, HD quality, 3-10 seconds',
            'pika': 'square or 16:9 aspect ratio, artistic style, 2-8 seconds',
            'stable_video': '16:9 aspect ratio, stable generation, 2-5 seconds',
            'sora': '16:9 aspect ratio, high quality, 5-20 seconds'
        }
        
        return technical_specs.get(generator_type.lower(), 'standard video specifications')
    
    def _format_style_preferences(self, style_preferences: Dict[str, Any]) -> str:
        """Format style preferences into text."""
        preferences = []
        
        if style_preferences.get('color_scheme'):
            preferences.append(f"color scheme: {style_preferences['color_scheme']}")
        
        if style_preferences.get('mood'):
            preferences.append(f"mood: {style_preferences['mood']}")
        
        if style_preferences.get('style'):
            preferences.append(f"style: {style_preferences['style']}")
        
        if style_preferences.get('duration'):
            preferences.append(f"duration: {style_preferences['duration']}")
        
        return ", ".join(preferences)
    
    def _generate_recommendations(self, user_query: str, trend_insights: Dict[str, Any], 
                                generator_type: str) -> Dict[str, List[str]]:
        """Generate comprehensive recommendations."""
        recommendations = {
            "content_recommendations": [],
            "visual_recommendations": [],
            "technical_recommendations": [],
            "optimization_recommendations": []
        }
        
        # Content recommendations
        content_trends = trend_insights.get('content_trends', {})
        common_words = content_trends.get('common_words', {})
        themes = content_trends.get('themes', [])
        
        if common_words:
            top_words = list(common_words.keys())[:3]
            recommendations["content_recommendations"].append(
                f"Incorporate trending keywords: {', '.join(top_words)}"
            )
        
        if themes:
            recommendations["content_recommendations"].append(
                f"Focus on trending themes: {', '.join(themes[:3])}"
            )
        
        # Visual recommendations
        visual_trends = trend_insights.get('visual_trends', {})
        video_trends = trend_insights.get('video_trends', {})
        
        if video_trends.get('video_count', 0) > visual_trends.get('image_count', 0):
            recommendations["visual_recommendations"].append("Prioritize video content over static images")
        
        recommendations["visual_recommendations"].append("Ensure high visual quality and clear composition")
        recommendations["visual_recommendations"].append("Use attention-grabbing visuals in the first 3 seconds")
        
        # Technical recommendations
        recommendations["technical_recommendations"].append(
            f"Optimize for {generator_type.upper()} capabilities and limitations"
        )
        recommendations["technical_recommendations"].append("Test different aspect ratios for platform optimization")
        recommendations["technical_recommendations"].append("Consider mobile-first design for social media")
        
        # Optimization recommendations
        recommendations["optimization_recommendations"].append("A/B test different versions")
        recommendations["optimization_recommendations"].append("Monitor performance metrics")
        recommendations["optimization_recommendations"].append("Iterate based on engagement data")
        
        return recommendations
    
    def _generate_technical_specs(self, trend_insights: Dict[str, Any], generator_type: str) -> Dict[str, Any]:
        """Generate technical specifications."""
        specs = {
            "generator_type": generator_type,
            "recommended_aspect_ratio": "16:9",
            "recommended_resolution": "1080p",
            "recommended_duration": "5-15 seconds",
            "optimization_tips": []
        }
        
        # Adjust specs based on trends
        format_trends = trend_insights.get('format_trends', {})
        format_distribution = format_trends.get('format_distribution', {})
        
        if format_distribution.get('VIDEO', 0) > 0:
            specs["optimization_tips"].append("Video content is trending - prioritize motion and transitions")
        
        # Generator-specific optimizations
        generator_optimizations = {
            'veo': ["Use clear, descriptive prompts", "Focus on smooth motion", "Avoid complex scenes"],
            'runway': ["Leverage creative editing features", "Use style consistency", "Optimize for artistic expression"],
            'pika': ["Emphasize artistic style", "Use creative animations", "Focus on visual appeal"],
            'stable_video': ["Keep prompts simple", "Ensure stable generation", "Use consistent style"],
            'sora': ["Leverage advanced capabilities", "Use detailed descriptions", "Focus on realism"]
        }
        
        specs["optimization_tips"].extend(
            generator_optimizations.get(generator_type.lower(), [])
        )
        
        return specs
    
    def _extract_combined_insights(self, video_insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract and combine insights from all analyzed videos."""
        combined = {
            "total_videos": len(video_insights),
            "common_themes": [],
            "visual_patterns": [],
            "messaging_strategies": [],
            "technical_insights": [],
            "brand_patterns": {},
            "duration_insights": [],
            "style_insights": []
        }
        
        # Extract insights from each video
        for insight in video_insights:
            video_data = insight.get('insights', {})
            raw_analysis = video_data.get('raw_analysis', '')
            
            # Extract themes and patterns from raw analysis
            if raw_analysis:
                # Simple keyword extraction (can be enhanced with NLP)
                themes = self._extract_themes_from_text(raw_analysis)
                combined["common_themes"].extend(themes)
                
                # Extract visual patterns
                visual_patterns = self._extract_visual_patterns(raw_analysis)
                combined["visual_patterns"].extend(visual_patterns)
                
                # Extract messaging strategies
                messaging = self._extract_messaging_strategies(raw_analysis)
                combined["messaging_strategies"].extend(messaging)
            
            # Technical insights
            metadata = insight.get('video_metadata', {})
            if metadata:
                combined["technical_insights"].append({
                    "duration": metadata.get('duration_seconds'),
                    "file_size": metadata.get('file_size_mb'),
                    "brand": insight.get('page_name', 'Unknown')
                })
            
            # Brand patterns
            brand = insight.get('page_name', 'Unknown')
            if brand not in combined["brand_patterns"]:
                combined["brand_patterns"][brand] = 0
            combined["brand_patterns"][brand] += 1
        
        # Remove duplicates and get top patterns
        combined["common_themes"] = list(set(combined["common_themes"]))[:10]
        combined["visual_patterns"] = list(set(combined["visual_patterns"]))[:10]
        combined["messaging_strategies"] = list(set(combined["messaging_strategies"]))[:10]
        
        return combined
    
    def _extract_themes_from_text(self, text: str) -> List[str]:
        """Extract common themes from analysis text."""
        # Simple keyword extraction - can be enhanced with NLP
        themes = []
        text_lower = text.lower()
        
        theme_keywords = [
            'product', 'service', 'quality', 'price', 'value', 'benefit',
            'feature', 'advantage', 'solution', 'problem', 'need',
            'lifestyle', 'emotion', 'story', 'testimonial', 'review',
            'comparison', 'competition', 'unique', 'special', 'exclusive'
        ]
        
        for keyword in theme_keywords:
            if keyword in text_lower:
                themes.append(keyword.title())
        
        return themes
    
    def _extract_visual_patterns(self, text: str) -> List[str]:
        """Extract visual patterns from analysis text."""
        patterns = []
        text_lower = text.lower()
        
        visual_keywords = [
            'color', 'bright', 'dark', 'contrast', 'animation', 'motion',
            'close-up', 'wide shot', 'text overlay', 'logo', 'brand',
            'people', 'faces', 'hands', 'product shot', 'lifestyle',
            'background', 'foreground', 'lighting', 'shadow'
        ]
        
        for keyword in visual_keywords:
            if keyword in text_lower:
                patterns.append(keyword.title())
        
        return patterns
    
    def _extract_messaging_strategies(self, text: str) -> List[str]:
        """Extract messaging strategies from analysis text."""
        strategies = []
        text_lower = text.lower()
        
        messaging_keywords = [
            'call to action', 'cta', 'buy now', 'learn more', 'discover',
            'limited time', 'offer', 'discount', 'sale', 'free',
            'testimonial', 'review', 'rating', 'star', 'recommendation',
            'social proof', 'trust', 'credibility', 'authority'
        ]
        
        for keyword in messaging_keywords:
            if keyword in text_lower:
                strategies.append(keyword.title())
        
        return strategies
    
    def _create_video_description_from_insights(self, user_query: str, combined_insights: Dict[str, Any], 
                                              generator_type: str, style_preferences: Optional[Dict[str, Any]]) -> str:
        """Create video description based on combined insights."""
        
        # Base description
        description_parts = [
            f"Create a {generator_type.upper()} video based on the user request: '{user_query}'"
        ]
        
        # Add insights from analyzed videos
        if combined_insights.get('common_themes'):
            themes = ', '.join(combined_insights['common_themes'][:5])
            description_parts.append(f"Incorporate these key themes from successful ads: {themes}")
        
        if combined_insights.get('visual_patterns'):
            patterns = ', '.join(combined_insights['visual_patterns'][:5])
            description_parts.append(f"Use these visual elements: {patterns}")
        
        if combined_insights.get('messaging_strategies'):
            strategies = ', '.join(combined_insights['messaging_strategies'][:3])
            description_parts.append(f"Apply these messaging strategies: {strategies}")
        
        # Add technical recommendations
        description_parts.append(f"Optimize for {generator_type.upper()} video generation")
        description_parts.append("Ensure high visual quality and engaging content")
        
        # Add style preferences if provided
        if style_preferences:
            if style_preferences.get('mood'):
                description_parts.append(f"Maintain a {style_preferences['mood']} mood throughout")
            if style_preferences.get('tone'):
                description_parts.append(f"Use a {style_preferences['tone']} tone")
        
        return " | ".join(description_parts)
    
    def _create_video_variations(self, user_query: str, combined_insights: Dict[str, Any], 
                               generator_type: str, style_preferences: Optional[Dict[str, Any]]) -> List[str]:
        """Create video description variations."""
        variations = []
        
        # Emotional focus variation
        emotional_parts = [
            f"Create an emotionally engaging {generator_type.upper()} video for: '{user_query}'",
            "Focus on emotional connection and storytelling",
            "Use warm colors and intimate camera angles"
        ]
        if combined_insights.get('common_themes'):
            emotional_parts.append(f"Emphasize themes: {', '.join(combined_insights['common_themes'][:3])}")
        variations.append(" | ".join(emotional_parts))
        
        # Technical focus variation
        technical_parts = [
            f"Create a technically impressive {generator_type.upper()} video for: '{user_query}'",
            "Focus on product features and technical specifications",
            "Use clean, professional visuals and clear messaging"
        ]
        if combined_insights.get('visual_patterns'):
            technical_parts.append(f"Apply visual patterns: {', '.join(combined_insights['visual_patterns'][:3])}")
        variations.append(" | ".join(technical_parts))
        
        # Competitive differentiation variation
        competitive_parts = [
            f"Create a competitive {generator_type.upper()} video for: '{user_query}'",
            "Highlight unique selling points and competitive advantages",
            "Use bold visuals and confident messaging"
        ]
        if combined_insights.get('messaging_strategies'):
            competitive_parts.append(f"Apply strategies: {', '.join(combined_insights['messaging_strategies'][:3])}")
        variations.append(" | ".join(competitive_parts))
        
        return variations
    
    def _create_recommendations_from_insights(self, combined_insights: Dict[str, Any], generator_type: str) -> Dict[str, List[str]]:
        """Create recommendations based on video insights."""
        recommendations = {
            "content_recommendations": [],
            "visual_recommendations": [],
            "technical_recommendations": [],
            "optimization_recommendations": []
        }
        
        # Content recommendations based on themes
        if combined_insights.get('common_themes'):
            recommendations["content_recommendations"].append(
                f"Focus on these successful themes: {', '.join(combined_insights['common_themes'][:5])}"
            )
        
        # Visual recommendations based on patterns
        if combined_insights.get('visual_patterns'):
            recommendations["visual_recommendations"].append(
                f"Incorporate these visual elements: {', '.join(combined_insights['visual_patterns'][:5])}"
            )
        
        # Messaging recommendations
        if combined_insights.get('messaging_strategies'):
            recommendations["content_recommendations"].append(
                f"Use these messaging approaches: {', '.join(combined_insights['messaging_strategies'][:3])}"
            )
        
        # Technical recommendations
        recommendations["technical_recommendations"].append(f"Optimize for {generator_type.upper()}")
        recommendations["technical_recommendations"].append("Ensure high production quality")
        
        # Optimization recommendations
        recommendations["optimization_recommendations"].append("Test different variations")
        recommendations["optimization_recommendations"].append("Monitor engagement metrics")
        
        return recommendations
    
    def generate_batch_descriptions(self, queries: List[str], trends_data: Dict[str, Any], 
                                   generator_type: str = 'veo') -> Dict[str, Any]:
        """Generate multiple video descriptions for batch processing."""
        try:
            descriptions = []
            
            for query in queries:
                result = self.generate_video_description(query, trends_data, generator_type)
                descriptions.append({
                    "query": query,
                    "description": result.get('video_description', ''),
                    "success": result.get('success', False)
                })
            
            successful_count = sum(1 for desc in descriptions if desc['success'])
            
            return {
                "success": True,
                "message": f"Generated {successful_count}/{len(queries)} video descriptions",
                "descriptions": descriptions,
                "batch_info": {
                    "total_queries": len(queries),
                    "successful": successful_count,
                    "failed": len(queries) - successful_count
                },
                "error": None
            }
            
        except Exception as e:
            self.logger.error(f"Batch description generation failed: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to generate batch descriptions: {str(e)}",
                "descriptions": [],
                "error": str(e)
            }

    def _create_technical_specifications(self, generator_type: str, combined_insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create technical specifications for video generation.
        
        Args:
            generator_type: Type of video generator
            combined_insights: Combined insights from all videos
            
        Returns:
            Dictionary with technical specifications
        """
        try:
            # Base specifications
            specs = {
                "resolution": "1080p",
                "aspect_ratio": "16:9",
                "fps": 30,
                "duration": "30s",
                "format": "mp4",
                "quality": "high"
            }
            
            # Generator-specific specifications
            if generator_type.lower() == 'veo':
                specs.update({
                    "model": "veo-2",
                    "style": "cinematic",
                    "motion": "smooth",
                    "lighting": "natural"
                })
            elif generator_type.lower() == 'runway':
                specs.update({
                    "model": "gen-3",
                    "style": "realistic",
                    "motion": "dynamic",
                    "lighting": "dramatic"
                })
            elif generator_type.lower() == 'pika':
                specs.update({
                    "model": "pika-1.0",
                    "style": "artistic",
                    "motion": "fluid",
                    "lighting": "creative"
                })
            elif generator_type.lower() == 'stable_video':
                specs.update({
                    "model": "svd",
                    "style": "stable",
                    "motion": "controlled",
                    "lighting": "balanced"
                })
            elif generator_type.lower() == 'sora':
                specs.update({
                    "model": "sora-1.0",
                    "style": "photorealistic",
                    "motion": "natural",
                    "lighting": "realistic"
                })
            
            # Add insights-based specifications
            if combined_insights.get('common_duration'):
                specs["duration"] = combined_insights['common_duration']
            
            if combined_insights.get('common_aspect_ratio'):
                specs["aspect_ratio"] = combined_insights['common_aspect_ratio']
            
            if combined_insights.get('common_style'):
                specs["style"] = combined_insights['common_style']
            
            return specs
            
        except Exception as e:
            self.logger.error(f"Error creating technical specifications: {str(e)}")
            return {
                "resolution": "1080p",
                "aspect_ratio": "16:9",
                "fps": 30,
                "duration": "30s",
                "format": "mp4",
                "quality": "high"
            }


# Global instance
video_generator_service = VideoGeneratorService()
