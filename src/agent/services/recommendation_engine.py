"""
Health Recommendation Engine - Generates personalized health recommendations
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
import json
import random

logger = logging.getLogger(__name__)


class HealthRecommendationEngine:
    """
    Service for generating personalized health recommendations
    """
    
    def __init__(self):
        self.recommendation_templates = {
            "lifestyle": self._generate_lifestyle_recommendations,
            "nutrition": self._generate_nutrition_recommendations,
            "exercise": self._generate_exercise_recommendations,
            "sleep": self._generate_sleep_recommendations,
            "stress": self._generate_stress_recommendations,
            "medication": self._generate_medication_recommendations
        }
        
    async def generate_health_recommendation(self, user_id: str, health_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized health recommendation
        """
        try:
            recommendation = {
                "recommendation_id": f"rec_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "health_analysis": health_analysis,
                "recommendation_type": "comprehensive",
                "priority": "medium",
                "recommendations": {},
                "action_plan": {},
                "follow_up": {}
            }
            
            # Analyze health data to determine recommendation focus
            focus_areas = await self._identify_focus_areas(health_analysis)
            
            # Generate recommendations for each focus area
            for area in focus_areas:
                if area in self.recommendation_templates:
                    area_recommendations = await self.recommendation_templates[area](health_analysis)
                    recommendation["recommendations"][area] = area_recommendations
            
            # Create action plan
            action_plan = await self._create_action_plan(recommendation["recommendations"])
            recommendation["action_plan"] = action_plan
            
            # Set follow-up schedule
            follow_up = await self._create_follow_up_plan(health_analysis, action_plan)
            recommendation["follow_up"] = follow_up
            
            # Determine priority
            recommendation["priority"] = await self._determine_priority(health_analysis)
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error generating health recommendation: {str(e)}")
            return {
                "error": str(e),
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _identify_focus_areas(self, health_analysis: Dict[str, Any]) -> List[str]:
        """
        Identify areas that need attention based on health analysis
        """
        focus_areas = []
        
        # Check metric analysis for areas needing attention
        metric_analysis = health_analysis.get("metric_analysis", {})
        
        # Check heart rate
        if "heart_rate" in metric_analysis:
            hr_analysis = metric_analysis["heart_rate"]
            if hr_analysis.get("hr_status") != "normal":
                focus_areas.append("exercise")
                focus_areas.append("stress")
        
        # Check blood pressure
        if "blood_pressure" in metric_analysis:
            bp_analysis = metric_analysis["blood_pressure"]
            if bp_analysis.get("risk_level") in ["high", "critical"]:
                focus_areas.append("lifestyle")
                focus_areas.append("nutrition")
                focus_areas.append("exercise")
        
        # Check activity level
        if "activity" in metric_analysis:
            activity_analysis = metric_analysis["activity"]
            if activity_analysis.get("activity_level") == "low":
                focus_areas.append("exercise")
        
        # Check sleep quality
        if "sleep" in metric_analysis:
            sleep_analysis = metric_analysis["sleep"]
            if sleep_analysis.get("sleep_quality") in ["poor", "fair"]:
                focus_areas.append("sleep")
                focus_areas.append("stress")
        
        # Check nutrition
        if "nutrition" in metric_analysis:
            nutrition_analysis = metric_analysis["nutrition"]
            if nutrition_analysis.get("nutrition_balance") == "unbalanced":
                focus_areas.append("nutrition")
        
        # Always include lifestyle recommendations
        if "lifestyle" not in focus_areas:
            focus_areas.append("lifestyle")
        
        return list(set(focus_areas))  # Remove duplicates
    
    async def _generate_lifestyle_recommendations(self, health_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate lifestyle recommendations
        """
        recommendations = {
            "category": "lifestyle",
            "priority": "high",
            "recommendations": [],
            "goals": [],
            "timeline": "ongoing"
        }
        
        # General lifestyle recommendations
        recommendations["recommendations"] = [
            "Maintain a consistent daily routine",
            "Stay hydrated by drinking 8-10 glasses of water daily",
            "Limit alcohol consumption to moderate levels",
            "Avoid smoking and secondhand smoke",
            "Practice good hygiene and handwashing",
            "Get regular health checkups and screenings"
        ]
        
        # Set lifestyle goals
        recommendations["goals"] = [
            "Establish a consistent sleep schedule",
            "Maintain a balanced diet",
            "Engage in regular physical activity",
            "Manage stress effectively",
            "Stay socially connected"
        ]
        
        return recommendations
    
    async def _generate_nutrition_recommendations(self, health_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate nutrition recommendations
        """
        recommendations = {
            "category": "nutrition",
            "priority": "medium",
            "recommendations": [],
            "goals": [],
            "timeline": "4-6 weeks"
        }
        
        recommendations["recommendations"] = [
            "Eat a variety of fruits and vegetables daily",
            "Choose whole grains over refined grains",
            "Include lean protein sources in each meal",
            "Limit processed foods and added sugars",
            "Control portion sizes",
            "Eat regular meals and snacks"
        ]
        
        recommendations["goals"] = [
            "Achieve balanced macronutrient intake",
            "Increase daily fruit and vegetable consumption",
            "Reduce processed food intake",
            "Maintain consistent meal timing"
        ]
        
        return recommendations
    
    async def _generate_exercise_recommendations(self, health_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate exercise recommendations
        """
        recommendations = {
            "category": "exercise",
            "priority": "high",
            "recommendations": [],
            "goals": [],
            "timeline": "8-12 weeks"
        }
        
        recommendations["recommendations"] = [
            "Aim for 30 minutes of moderate activity most days",
            "Include both cardio and strength training",
            "Try new activities to stay motivated",
            "Track your progress and celebrate milestones"
        ]
        
        recommendations["goals"] = [
            "Achieve 150 minutes of moderate activity per week",
            "Include strength training 2-3 times per week",
            "Increase daily step count",
            "Improve cardiovascular fitness"
        ]
        
        return recommendations
    
    async def _generate_sleep_recommendations(self, health_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate sleep recommendations
        """
        recommendations = {
            "category": "sleep",
            "priority": "high",
            "recommendations": [],
            "goals": [],
            "timeline": "2-4 weeks"
        }
        
        recommendations["recommendations"] = [
            "Maintain a consistent sleep schedule",
            "Create a relaxing bedtime routine",
            "Keep your bedroom cool, dark, and quiet",
            "Avoid screens 1 hour before bedtime",
            "Limit caffeine intake in the afternoon",
            "Avoid large meals before bedtime"
        ]
        
        recommendations["goals"] = [
            "Achieve 7-9 hours of sleep per night",
            "Improve sleep efficiency to 85% or higher",
            "Establish consistent bedtime and wake time",
            "Reduce time to fall asleep"
        ]
        
        return recommendations
    
    async def _generate_stress_recommendations(self, health_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate stress management recommendations
        """
        recommendations = {
            "category": "stress",
            "priority": "medium",
            "recommendations": [],
            "goals": [],
            "timeline": "ongoing"
        }
        
        recommendations["recommendations"] = [
            "Practice deep breathing exercises daily",
            "Try meditation or mindfulness techniques",
            "Engage in regular physical activity",
            "Maintain social connections",
            "Set realistic goals and priorities",
            "Take regular breaks throughout the day"
        ]
        
        recommendations["goals"] = [
            "Develop effective stress management techniques",
            "Improve emotional well-being",
            "Maintain work-life balance",
            "Build resilience to stress"
        ]
        
        return recommendations
    
    async def _generate_medication_recommendations(self, health_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate medication-related recommendations
        """
        recommendations = {
            "category": "medication",
            "priority": "high",
            "recommendations": [],
            "goals": [],
            "timeline": "ongoing"
        }
        
        recommendations["recommendations"] = [
            "Take medications as prescribed by your healthcare provider",
            "Keep a medication list and update it regularly",
            "Use a pill organizer to avoid missed doses",
            "Set reminders for medication times",
            "Store medications properly",
            "Report any side effects to your healthcare provider"
        ]
        
        recommendations["goals"] = [
            "Maintain medication adherence",
            "Monitor for side effects",
            "Optimize medication effectiveness",
            "Coordinate with healthcare providers"
        ]
        
        return recommendations
    
    async def _create_action_plan(self, recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a structured action plan from recommendations
        """
        action_plan = {
            "plan_id": f"plan_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "created_at": datetime.utcnow().isoformat(),
            "phases": {},
            "milestones": [],
            "resources": []
        }
        
        # Create phases based on timeline
        phases = {
            "immediate": {"duration": "1-2 weeks", "actions": []},
            "short_term": {"duration": "1-3 months", "actions": []},
            "long_term": {"duration": "3-12 months", "actions": []}
        }
        
        # Categorize recommendations by timeline
        for category, rec_data in recommendations.items():
            timeline = rec_data.get("timeline", "ongoing")
            priority = rec_data.get("priority", "medium")
            
            if timeline in ["1-2 weeks", "immediate"]:
                phases["immediate"]["actions"].extend(rec_data.get("recommendations", []))
            elif timeline in ["4-6 weeks", "2-4 weeks", "1-3 months"]:
                phases["short_term"]["actions"].extend(rec_data.get("recommendations", []))
            else:
                phases["long_term"]["actions"].extend(rec_data.get("recommendations", []))
        
        action_plan["phases"] = phases
        
        # Create milestones
        action_plan["milestones"] = [
            "Complete initial assessment and goal setting",
            "Implement immediate action items",
            "Track progress and adjust plan",
            "Achieve short-term goals",
            "Maintain long-term lifestyle changes"
        ]
        
        # Add resources
        action_plan["resources"] = [
            "Healthcare provider consultation",
            "Health monitoring apps and devices",
            "Educational materials and resources",
            "Support groups or communities",
            "Professional services (nutritionist, trainer, etc.)"
        ]
        
        return action_plan
    
    async def _create_follow_up_plan(self, health_analysis: Dict[str, Any], action_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a follow-up plan for monitoring progress
        """
        follow_up = {
            "schedule": {},
            "checkpoints": [],
            "adjustments": {},
            "success_metrics": []
        }
        
        # Create follow-up schedule
        follow_up["schedule"] = {
            "daily": ["Track daily activities and symptoms"],
            "weekly": ["Review progress and adjust goals"],
            "monthly": ["Comprehensive health assessment"],
            "quarterly": ["Healthcare provider consultation"]
        }
        
        # Create checkpoints
        follow_up["checkpoints"] = [
            {"timeframe": "1 week", "focus": "Initial implementation and adjustment"},
            {"timeframe": "1 month", "focus": "Progress assessment and goal refinement"},
            {"timeframe": "3 months", "focus": "Comprehensive evaluation and plan update"},
            {"timeframe": "6 months", "focus": "Long-term goal assessment"}
        ]
        
        # Define success metrics
        follow_up["success_metrics"] = [
            "Improved health metrics and vital signs",
            "Achievement of lifestyle goals",
            "Increased adherence to recommendations",
            "Enhanced overall well-being and quality of life"
        ]
        
        return follow_up
    
    async def _determine_priority(self, health_analysis: Dict[str, Any]) -> str:
        """
        Determine the overall priority of recommendations
        """
        risk_assessment = health_analysis.get("risk_assessment", {})
        overall_risk = risk_assessment.get("overall_risk_level", "low")
        
        if overall_risk == "critical":
            return "critical"
        elif overall_risk == "high":
            return "high"
        elif overall_risk == "medium":
            return "medium"
        else:
            return "low"
