"""
Smart Health Monitoring AI Agent - Core Agent Implementation
Uses Amazon Bedrock for medical reasoning and autonomous health monitoring
"""

import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError
import logging

from ..services.health_data_collector import HealthDataCollector
from ..services.health_analyzer import HealthAnalyzer
from ..services.alert_system import AlertSystem
from ..services.recommendation_engine import HealthRecommendationEngine
from ..models.health_metrics import HealthMetrics, VitalSigns, HealthAlert
from ..utils.medical_reasoning import MedicalReasoningEngine

logger = logging.getLogger(__name__)


class SmartHealthMonitoringAgent:
    """
    Main AI Agent for autonomous health monitoring and analysis
    """
    
    def __init__(self, region_name: str = "us-east-1"):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name=region_name)
        self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        # Initialize services
        self.health_data_collector = HealthDataCollector()
        self.health_analyzer = HealthAnalyzer()
        self.alert_system = AlertSystem()
        self.recommendation_engine = HealthRecommendationEngine()
        self.medical_reasoning = MedicalReasoningEngine(self.bedrock_client, self.model_id)
        
        # Agent state
        self.active_monitoring = {}
        self.health_history = []
        self.user_profiles = {}
        self.alert_thresholds = {}
        
    async def start_autonomous_monitoring(self, user_id: str, monitoring_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start autonomous health monitoring for a user
        """
        try:
            logger.info(f"Starting autonomous health monitoring for user {user_id}")
            
            # Initialize user profile
            self.user_profiles[user_id] = {
                "monitoring_config": monitoring_config,
                "health_history": [],
                "alert_preferences": monitoring_config.get("alert_preferences", {}),
                "last_check": datetime.utcnow().isoformat()
            }
            
            # Create monitoring plan using medical reasoning
            monitoring_plan = await self._create_monitoring_plan(user_id, monitoring_config)
            
            # Start autonomous monitoring tasks
            monitoring_results = await self._execute_autonomous_monitoring(user_id, monitoring_plan)
            
            return {
                "status": "success",
                "user_id": user_id,
                "monitoring_plan": monitoring_plan,
                "results": monitoring_results,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in autonomous monitoring: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _create_monitoring_plan(self, user_id: str, monitoring_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use medical reasoning to create a personalized monitoring plan
        """
        reasoning_prompt = f"""
        You are a medical AI agent specialized in health monitoring. Based on the user's health profile and monitoring configuration,
        create a comprehensive autonomous monitoring plan.
        
        User Profile:
        - Age: {monitoring_config.get('age', 'Not specified')}
        - Medical Conditions: {monitoring_config.get('medical_conditions', [])}
        - Current Medications: {monitoring_config.get('medications', [])}
        - Risk Factors: {monitoring_config.get('risk_factors', [])}
        - Monitoring Goals: {monitoring_config.get('goals', [])}
        
        Create a monitoring plan that includes:
        1. Vital signs to monitor and frequency
        2. Health metrics to track
        3. Alert thresholds for each metric
        4. Recommended health checks
        5. Emergency response protocols
        
        Focus on preventive care and early detection of potential health issues.
        Respond with a JSON plan.
        """
        
        plan = await self.medical_reasoning.reason(reasoning_prompt)
        return json.loads(plan)
    
    async def _execute_autonomous_monitoring(self, user_id: str, monitoring_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute autonomous health monitoring tasks
        """
        results = {
            "health_data_collected": [],
            "health_analysis": [],
            "alerts_generated": [],
            "recommendations": [],
            "monitoring_summary": {}
        }
        
        # Task 1: Collect health data from multiple sources
        logger.info("Collecting health data from multiple sources")
        health_data = await self._collect_health_data_autonomously(user_id, monitoring_plan)
        results["health_data_collected"] = health_data
        
        # Task 2: Analyze health data using medical reasoning
        logger.info("Analyzing health data with medical reasoning")
        health_analysis = await self._analyze_health_data_autonomously(user_id, health_data)
        results["health_analysis"] = health_analysis
        
        # Task 3: Generate alerts for concerning patterns
        logger.info("Generating health alerts")
        alerts = await self._generate_health_alerts_autonomously(user_id, health_analysis)
        results["alerts_generated"] = alerts
        
        # Task 4: Generate personalized health recommendations
        logger.info("Generating health recommendations")
        recommendations = await self._generate_health_recommendations_autonomously(user_id, health_analysis)
        results["recommendations"] = recommendations
        
        # Task 5: Update monitoring summary
        results["monitoring_summary"] = await self._create_monitoring_summary(user_id, health_data, health_analysis)
        
        return results
    
    async def _collect_health_data_autonomously(self, user_id: str, monitoring_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Autonomously collect health data from multiple sources
        """
        collected_data = []
        
        # Get monitoring targets from plan
        vital_signs = monitoring_plan.get("vital_signs", ["heart_rate", "blood_pressure", "temperature"])
        health_metrics = monitoring_plan.get("health_metrics", ["sleep_quality", "activity_level", "stress_level"])
        
        # Collect data from multiple sources concurrently
        tasks = []
        
        # Collect wearable device data
        for vital_sign in vital_signs:
            task = self.health_data_collector.collect_wearable_data(user_id, vital_sign)
            tasks.append(task)
        
        # Collect health app data
        for metric in health_metrics:
            task = self.health_data_collector.collect_health_app_data(user_id, metric)
            tasks.append(task)
        
        # Collect external health API data
        task = self.health_data_collector.collect_external_health_data(user_id)
        tasks.append(task)
        
        # Execute all collection tasks concurrently
        collection_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in collection_results:
            if isinstance(result, list):
                collected_data.extend(result)
            elif isinstance(result, dict):
                collected_data.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Data collection error: {str(result)}")
        
        return collected_data
    
    async def _analyze_health_data_autonomously(self, user_id: str, health_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Autonomously analyze health data using medical reasoning
        """
        analyzed_data = []
        
        for data_point in health_data:
            try:
                # Use medical reasoning to analyze health data
                medical_analysis = await self._reason_about_health_data(data_point, user_id)
                
                # Perform statistical analysis
                statistical_analysis = await self.health_analyzer.analyze_health_metrics(data_point)
                
                # Combine analysis results
                analyzed_data_point = {
                    **data_point,
                    "medical_analysis": medical_analysis,
                    "statistical_analysis": statistical_analysis,
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
                
                analyzed_data.append(analyzed_data_point)
                
            except Exception as e:
                logger.error(f"Error analyzing health data: {str(e)}")
        
        return analyzed_data
    
    async def _reason_about_health_data(self, health_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Use medical reasoning to analyze health data
        """
        user_profile = self.user_profiles.get(user_id, {})
        
        reasoning_prompt = f"""
        Analyze this health data point and provide a comprehensive medical assessment:
        
        Health Data:
        {json.dumps(health_data, indent=2)}
        
        User Profile:
        {json.dumps(user_profile, indent=2)}
        
        Provide medical analysis on:
        1. Health status assessment
        2. Potential concerns or anomalies
        3. Risk factors identified
        4. Comparison with normal ranges
        5. Recommended actions
        
        Focus on early detection of potential health issues and preventive care.
        Respond with a JSON analysis.
        """
        
        analysis = await self.medical_reasoning.reason(reasoning_prompt)
        return json.loads(analysis)
    
    async def _generate_health_alerts_autonomously(self, user_id: str, health_analysis: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate health alerts based on analysis
        """
        alerts = []
        
        for analysis in health_analysis:
            try:
                medical_analysis = analysis.get("medical_analysis", {})
                risk_level = medical_analysis.get("risk_level", "low")
                
                if risk_level in ["high", "critical"]:
                    alert = await self.alert_system.generate_health_alert(
                        user_id, analysis, risk_level
                    )
                    alerts.append(alert)
                    
            except Exception as e:
                logger.error(f"Error generating alert: {str(e)}")
        
        return alerts
    
    async def _generate_health_recommendations_autonomously(self, user_id: str, health_analysis: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate personalized health recommendations
        """
        recommendations = []
        
        for analysis in health_analysis:
            try:
                recommendation = await self.recommendation_engine.generate_health_recommendation(
                    user_id, analysis
                )
                recommendations.append(recommendation)
                
            except Exception as e:
                logger.error(f"Error generating recommendation: {str(e)}")
        
        return recommendations
    
    async def _create_monitoring_summary(self, user_id: str, health_data: List[Dict[str, Any]], 
                                       health_analysis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a comprehensive monitoring summary
        """
        summary = {
            "user_id": user_id,
            "monitoring_period": "24_hours",
            "data_points_collected": len(health_data),
            "analyses_performed": len(health_analysis),
            "overall_health_status": "unknown",
            "key_insights": [],
            "action_items": [],
            "next_monitoring_schedule": (datetime.utcnow() + timedelta(hours=6)).isoformat()
        }
        
        # Analyze overall health status
        risk_levels = [analysis.get("medical_analysis", {}).get("risk_level", "low") for analysis in health_analysis]
        
        if "critical" in risk_levels:
            summary["overall_health_status"] = "critical_attention_needed"
        elif "high" in risk_levels:
            summary["overall_health_status"] = "monitoring_required"
        elif "medium" in risk_levels:
            summary["overall_health_status"] = "stable_with_concerns"
        else:
            summary["overall_health_status"] = "stable"
        
        # Extract key insights
        for analysis in health_analysis:
            insights = analysis.get("medical_analysis", {}).get("key_insights", [])
            summary["key_insights"].extend(insights)
        
        # Extract action items
        for analysis in health_analysis:
            actions = analysis.get("medical_analysis", {}).get("recommended_actions", [])
            summary["action_items"].extend(actions)
        
        return summary
    
    async def handle_emergency_alert(self, user_id: str, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle emergency health alerts autonomously
        """
        try:
            logger.info(f"Handling emergency alert for user {user_id}")
            
            # Use medical reasoning to assess emergency severity
            emergency_assessment = await self._assess_emergency_severity(alert_data)
            
            # Take appropriate emergency actions
            emergency_actions = await self._execute_emergency_actions(user_id, emergency_assessment)
            
            return {
                "status": "emergency_handled",
                "user_id": user_id,
                "assessment": emergency_assessment,
                "actions_taken": emergency_actions,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error handling emergency alert: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _assess_emergency_severity(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess emergency severity using medical reasoning
        """
        reasoning_prompt = f"""
        Assess the severity of this health emergency and determine appropriate response:
        
        Alert Data:
        {json.dumps(alert_data, indent=2)}
        
        Provide assessment on:
        1. Emergency severity level (low/medium/high/critical)
        2. Immediate actions required
        3. Healthcare provider notification needed
        4. Emergency services required
        5. Monitoring recommendations
        
        Respond with a JSON assessment.
        """
        
        assessment = await self.medical_reasoning.reason(reasoning_prompt)
        return json.loads(assessment)
    
    async def _execute_emergency_actions(self, user_id: str, emergency_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute emergency actions based on assessment
        """
        actions_taken = []
        
        severity = emergency_assessment.get("severity_level", "low")
        
        if severity == "critical":
            # Notify emergency services
            emergency_notification = await self.alert_system.notify_emergency_services(user_id, emergency_assessment)
            actions_taken.append(emergency_notification)
        
        if severity in ["high", "critical"]:
            # Notify healthcare provider
            provider_notification = await self.alert_system.notify_healthcare_provider(user_id, emergency_assessment)
            actions_taken.append(provider_notification)
        
        # Notify user/emergency contacts
        user_notification = await self.alert_system.notify_user_contacts(user_id, emergency_assessment)
        actions_taken.append(user_notification)
        
        return actions_taken
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """
        Get current agent status and metrics
        """
        return {
            "status": "active",
            "active_monitoring": len(self.active_monitoring),
            "users_monitored": len(self.user_profiles),
            "health_data_points": sum(len(profile.get("health_history", [])) for profile in self.user_profiles.values()),
            "last_activity": datetime.utcnow().isoformat()
        }
    
    async def update_monitoring_config(self, user_id: str, new_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update monitoring configuration for a user
        """
        if user_id in self.user_profiles:
            self.user_profiles[user_id]["monitoring_config"].update(new_config)
            
            # Recreate monitoring plan with new configuration
            new_plan = await self._create_monitoring_plan(user_id, self.user_profiles[user_id]["monitoring_config"])
            
            return {
                "status": "success",
                "user_id": user_id,
                "updated_config": self.user_profiles[user_id]["monitoring_config"],
                "new_monitoring_plan": new_plan
            }
        
        return {
            "status": "error",
            "message": f"User {user_id} not found"
        }
