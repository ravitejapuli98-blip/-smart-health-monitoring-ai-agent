"""
Health Analyzer Service - Analyzes health data and patterns
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
import statistics
import math
import numpy as np

logger = logging.getLogger(__name__)


class HealthAnalyzer:
    """
    Service for analyzing health data and identifying patterns
    """
    
    def __init__(self):
        self.analysis_cache = {}
        self.baseline_metrics = {}
        
    async def analyze_health_metrics(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive analysis of health metrics
        """
        try:
            analysis = {
                "data_id": health_data.get("id", "unknown"),
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "metric_analysis": {},
                "pattern_analysis": {},
                "risk_assessment": {},
                "recommendations": {}
            }
            
            # Analyze individual metrics
            metric_analysis = await self._analyze_individual_metrics(health_data)
            analysis["metric_analysis"] = metric_analysis
            
            # Analyze patterns
            pattern_analysis = await self._analyze_health_patterns(health_data)
            analysis["pattern_analysis"] = pattern_analysis
            
            # Assess risks
            risk_assessment = await self._assess_health_risks(health_data, metric_analysis)
            analysis["risk_assessment"] = risk_assessment
            
            # Generate recommendations
            recommendations = await self._generate_analysis_recommendations(health_data, metric_analysis, risk_assessment)
            analysis["recommendations"] = recommendations
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing health metrics: {str(e)}")
            return {
                "data_id": health_data.get("id", "unknown"),
                "error": str(e),
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
    
    async def _analyze_individual_metrics(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze individual health metrics
        """
        metric_analysis = {}
        data = health_data.get("data", {})
        
        # Heart rate analysis
        if "current_hr" in data:
            hr_analysis = self._analyze_heart_rate(data)
            metric_analysis["heart_rate"] = hr_analysis
        
        # Blood pressure analysis
        if "systolic" in data and "diastolic" in data:
            bp_analysis = self._analyze_blood_pressure(data)
            metric_analysis["blood_pressure"] = bp_analysis
        
        # Temperature analysis
        if "body_temp" in data:
            temp_analysis = self._analyze_temperature(data)
            metric_analysis["temperature"] = temp_analysis
        
        # Activity analysis
        if "steps" in data:
            activity_analysis = self._analyze_activity(data)
            metric_analysis["activity"] = activity_analysis
        
        # Sleep analysis
        if "sleep_duration" in data:
            sleep_analysis = self._analyze_sleep(data)
            metric_analysis["sleep"] = sleep_analysis
        
        # Nutrition analysis
        if "calories_consumed" in data:
            nutrition_analysis = self._analyze_nutrition(data)
            metric_analysis["nutrition"] = nutrition_analysis
        
        return metric_analysis
    
    def _analyze_heart_rate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze heart rate data
        """
        current_hr = data.get("current_hr", 0)
        resting_hr = data.get("resting_hr", 0)
        max_hr = data.get("max_hr", 0)
        
        analysis = {
            "current_hr": current_hr,
            "resting_hr": resting_hr,
            "max_hr": max_hr,
            "hr_status": "normal",
            "hr_zone": "unknown",
            "concerns": [],
            "recommendations": []
        }
        
        # Determine heart rate status
        if current_hr < 60:
            analysis["hr_status"] = "bradycardia"
            analysis["concerns"].append("Heart rate below normal range")
        elif current_hr > 100:
            analysis["hr_status"] = "tachycardia"
            analysis["concerns"].append("Heart rate above normal range")
        else:
            analysis["hr_status"] = "normal"
        
        # Determine heart rate zone
        if max_hr > 0:
            hr_percentage = (current_hr / max_hr) * 100
            if hr_percentage < 50:
                analysis["hr_zone"] = "recovery"
            elif hr_percentage < 60:
                analysis["hr_zone"] = "fat_burn"
            elif hr_percentage < 70:
                analysis["hr_zone"] = "aerobic"
            elif hr_percentage < 80:
                analysis["hr_zone"] = "anaerobic"
            else:
                analysis["hr_zone"] = "neuromuscular"
        
        # Generate recommendations
        if analysis["hr_status"] == "bradycardia":
            analysis["recommendations"].append("Consider consulting a healthcare provider")
        elif analysis["hr_status"] == "tachycardia":
            analysis["recommendations"].append("Monitor for symptoms and consider medical evaluation")
        
        return analysis
    
    def _analyze_blood_pressure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze blood pressure data
        """
        systolic = data.get("systolic", 0)
        diastolic = data.get("diastolic", 0)
        
        analysis = {
            "systolic": systolic,
            "diastolic": diastolic,
            "bp_category": "unknown",
            "risk_level": "unknown",
            "concerns": [],
            "recommendations": []
        }
        
        # Determine blood pressure category
        if systolic < 120 and diastolic < 80:
            analysis["bp_category"] = "normal"
            analysis["risk_level"] = "low"
        elif systolic < 130 and diastolic < 80:
            analysis["bp_category"] = "elevated"
            analysis["risk_level"] = "low"
        elif systolic < 140 or diastolic < 90:
            analysis["bp_category"] = "stage_1_hypertension"
            analysis["risk_level"] = "medium"
        elif systolic < 180 or diastolic < 120:
            analysis["bp_category"] = "stage_2_hypertension"
            analysis["risk_level"] = "high"
        else:
            analysis["bp_category"] = "hypertensive_crisis"
            analysis["risk_level"] = "critical"
        
        # Add concerns and recommendations
        if analysis["risk_level"] in ["high", "critical"]:
            analysis["concerns"].append("High blood pressure detected")
            analysis["recommendations"].append("Seek immediate medical attention")
        elif analysis["risk_level"] == "medium":
            analysis["concerns"].append("Elevated blood pressure")
            analysis["recommendations"].append("Monitor regularly and consider lifestyle changes")
        
        return analysis
    
    def _analyze_temperature(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze body temperature data
        """
        body_temp = data.get("body_temp", 0)
        
        analysis = {
            "body_temp": body_temp,
            "temp_status": "normal",
            "concerns": [],
            "recommendations": []
        }
        
        # Determine temperature status
        if body_temp < 97.0:
            analysis["temp_status"] = "hypothermia"
            analysis["concerns"].append("Body temperature below normal")
        elif body_temp > 100.4:
            analysis["temp_status"] = "fever"
            analysis["concerns"].append("Elevated body temperature")
        else:
            analysis["temp_status"] = "normal"
        
        # Add recommendations
        if analysis["temp_status"] == "fever":
            analysis["recommendations"].append("Monitor symptoms and consider medical evaluation")
        elif analysis["temp_status"] == "hypothermia":
            analysis["recommendations"].append("Seek immediate medical attention")
        
        return analysis
    
    def _analyze_activity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze physical activity data
        """
        steps = data.get("steps", 0)
        calories_burned = data.get("calories_burned", 0)
        active_minutes = data.get("active_minutes", 0)
        
        analysis = {
            "steps": steps,
            "calories_burned": calories_burned,
            "active_minutes": active_minutes,
            "activity_level": "unknown",
            "goals_met": {},
            "recommendations": []
        }
        
        # Determine activity level
        if steps >= 10000:
            analysis["activity_level"] = "excellent"
        elif steps >= 7500:
            analysis["activity_level"] = "good"
        elif steps >= 5000:
            analysis["activity_level"] = "moderate"
        else:
            analysis["activity_level"] = "low"
        
        # Check goals
        analysis["goals_met"] = {
            "steps_goal": steps >= 10000,
            "active_minutes_goal": active_minutes >= 30,
            "calories_goal": calories_burned >= 300
        }
        
        # Add recommendations
        if analysis["activity_level"] == "low":
            analysis["recommendations"].append("Increase daily physical activity")
        elif analysis["activity_level"] == "excellent":
            analysis["recommendations"].append("Maintain current activity level")
        
        return analysis
    
    def _analyze_sleep(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze sleep data
        """
        sleep_duration = data.get("sleep_duration", 0)
        sleep_efficiency = data.get("sleep_efficiency", 0)
        deep_sleep = data.get("deep_sleep", 0)
        rem_sleep = data.get("rem_sleep", 0)
        
        analysis = {
            "sleep_duration": sleep_duration,
            "sleep_efficiency": sleep_efficiency,
            "deep_sleep": deep_sleep,
            "rem_sleep": rem_sleep,
            "sleep_quality": "unknown",
            "concerns": [],
            "recommendations": []
        }
        
        # Determine sleep quality
        if sleep_duration >= 7 and sleep_duration <= 9 and sleep_efficiency >= 85:
            analysis["sleep_quality"] = "excellent"
        elif sleep_duration >= 6 and sleep_duration <= 10 and sleep_efficiency >= 75:
            analysis["sleep_quality"] = "good"
        elif sleep_duration >= 5 and sleep_efficiency >= 65:
            analysis["sleep_quality"] = "fair"
        else:
            analysis["sleep_quality"] = "poor"
        
        # Add concerns and recommendations
        if sleep_duration < 6:
            analysis["concerns"].append("Insufficient sleep duration")
            analysis["recommendations"].append("Aim for 7-9 hours of sleep per night")
        
        if sleep_efficiency < 75:
            analysis["concerns"].append("Low sleep efficiency")
            analysis["recommendations"].append("Improve sleep hygiene and environment")
        
        return analysis
    
    def _analyze_nutrition(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze nutrition data
        """
        calories = data.get("calories_consumed", 0)
        protein = data.get("protein", 0)
        carbs = data.get("carbs", 0)
        fat = data.get("fat", 0)
        water = data.get("water_intake", 0)
        
        analysis = {
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "water_intake": water,
            "nutrition_balance": "unknown",
            "concerns": [],
            "recommendations": []
        }
        
        # Analyze macronutrient balance
        if protein >= 60 and protein <= 120:
            protein_status = "adequate"
        else:
            protein_status = "inadequate"
            analysis["concerns"].append("Protein intake outside recommended range")
        
        if carbs >= 150 and carbs <= 300:
            carbs_status = "adequate"
        else:
            carbs_status = "inadequate"
            analysis["concerns"].append("Carbohydrate intake outside recommended range")
        
        if fat >= 50 and fat <= 100:
            fat_status = "adequate"
        else:
            fat_status = "inadequate"
            analysis["concerns"].append("Fat intake outside recommended range")
        
        # Determine overall nutrition balance
        if all(status == "adequate" for status in [protein_status, carbs_status, fat_status]):
            analysis["nutrition_balance"] = "balanced"
        else:
            analysis["nutrition_balance"] = "unbalanced"
        
        # Water intake analysis
        if water < 8:
            analysis["concerns"].append("Insufficient water intake")
            analysis["recommendations"].append("Increase daily water consumption")
        
        return analysis
    
    async def _analyze_health_patterns(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze health patterns and trends
        """
        pattern_analysis = {
            "trends": {},
            "anomalies": [],
            "correlations": {},
            "seasonal_patterns": {}
        }
        
        # This would typically analyze historical data
        # For now, we'll provide a basic structure
        
        return pattern_analysis
    
    async def _assess_health_risks(self, health_data: Dict[str, Any], metric_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess overall health risks
        """
        risk_assessment = {
            "overall_risk_level": "low",
            "risk_factors": [],
            "risk_score": 0,
            "immediate_concerns": [],
            "long_term_risks": []
        }
        
        # Calculate risk score based on metric analysis
        risk_score = 0
        
        for metric, analysis in metric_analysis.items():
            if "risk_level" in analysis:
                if analysis["risk_level"] == "critical":
                    risk_score += 10
                elif analysis["risk_level"] == "high":
                    risk_score += 7
                elif analysis["risk_level"] == "medium":
                    risk_score += 4
                elif analysis["risk_level"] == "low":
                    risk_score += 1
            
            if "concerns" in analysis:
                risk_assessment["risk_factors"].extend(analysis["concerns"])
        
        risk_assessment["risk_score"] = risk_score
        
        # Determine overall risk level
        if risk_score >= 20:
            risk_assessment["overall_risk_level"] = "critical"
        elif risk_score >= 15:
            risk_assessment["overall_risk_level"] = "high"
        elif risk_score >= 10:
            risk_assessment["overall_risk_level"] = "medium"
        else:
            risk_assessment["overall_risk_level"] = "low"
        
        return risk_assessment
    
    async def _generate_analysis_recommendations(self, health_data: Dict[str, Any], 
                                               metric_analysis: Dict[str, Any], 
                                               risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate recommendations based on analysis
        """
        recommendations = {
            "immediate_actions": [],
            "lifestyle_changes": [],
            "monitoring_recommendations": [],
            "healthcare_referrals": []
        }
        
        # Collect recommendations from metric analysis
        for metric, analysis in metric_analysis.items():
            if "recommendations" in analysis:
                recommendations["lifestyle_changes"].extend(analysis["recommendations"])
        
        # Add risk-based recommendations
        if risk_assessment["overall_risk_level"] in ["high", "critical"]:
            recommendations["immediate_actions"].append("Schedule medical consultation")
            recommendations["healthcare_referrals"].append("Primary care physician")
        
        if risk_assessment["overall_risk_level"] == "critical":
            recommendations["immediate_actions"].append("Consider emergency medical evaluation")
        
        # Add monitoring recommendations
        recommendations["monitoring_recommendations"].append("Continue regular health monitoring")
        
        return recommendations
    
    async def compare_with_baseline(self, user_id: str, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare current data with user's baseline
        """
        if user_id not in self.baseline_metrics:
            # Create baseline from current data if none exists
            self.baseline_metrics[user_id] = current_data
            return {
                "status": "baseline_created",
                "message": "Baseline metrics established from current data"
            }
        
        baseline = self.baseline_metrics[user_id]
        comparison = {
            "user_id": user_id,
            "comparison_timestamp": datetime.utcnow().isoformat(),
            "changes": {},
            "trends": {},
            "alerts": []
        }
        
        # Compare metrics
        for metric, current_value in current_data.items():
            if metric in baseline:
                baseline_value = baseline[metric]
                change = current_value - baseline_value
                change_percentage = (change / baseline_value) * 100 if baseline_value != 0 else 0
                
                comparison["changes"][metric] = {
                    "baseline": baseline_value,
                    "current": current_value,
                    "change": change,
                    "change_percentage": change_percentage
                }
                
                # Check for significant changes
                if abs(change_percentage) > 20:  # 20% change threshold
                    comparison["alerts"].append(f"Significant change in {metric}: {change_percentage:.1f}%")
        
        return comparison
