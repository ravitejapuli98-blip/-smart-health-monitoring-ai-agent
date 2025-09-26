"""
Medical Reasoning Engine - Uses Bedrock LLM for medical analysis and reasoning
"""

import json
import asyncio
from typing import Dict, List, Optional, Any
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class MedicalReasoningEngine:
    """
    Medical reasoning engine using Amazon Bedrock for health analysis
    """
    
    def __init__(self, bedrock_client, model_id: str):
        self.bedrock_client = bedrock_client
        self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
    async def reason(self, prompt: str) -> str:
        """
        Perform medical reasoning using Bedrock LLM
        """
        try:
            # Prepare the prompt for medical reasoning
            medical_prompt = f"""
            You are a medical AI assistant with expertise in health monitoring, diagnosis, and preventive care.
            You must provide accurate, evidence-based medical insights while emphasizing that you are not a replacement for professional medical advice.
            
            {prompt}
            
            Important guidelines:
            1. Always recommend consulting healthcare professionals for serious concerns
            2. Focus on preventive care and early detection
            3. Provide evidence-based insights
            4. Consider individual health profiles and risk factors
            5. Emphasize the importance of regular medical checkups
            6. Be cautious with emergency situations and recommend immediate medical attention when appropriate
            
            Respond with a JSON object containing your analysis.
            """
            
            # Call Bedrock API
            response = await self._call_bedrock(medical_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in medical reasoning: {str(e)}")
            return json.dumps({
                "error": str(e),
                "message": "Unable to perform medical reasoning at this time"
            })
    
    async def _call_bedrock(self, prompt: str) -> str:
        """
        Call Amazon Bedrock API
        """
        try:
            # Prepare the request body for Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,  # Lower temperature for more consistent medical reasoning
                "top_p": 0.9
            }
            
            # Make the API call
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
                contentType="application/json"
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            
            # Extract the content
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                return json.dumps({
                    "error": "No response content",
                    "message": "Unable to get response from medical reasoning engine"
                })
                
        except ClientError as e:
            logger.error(f"Bedrock API error: {str(e)}")
            return json.dumps({
                "error": f"Bedrock API error: {str(e)}",
                "message": "Unable to connect to medical reasoning service"
            })
        except Exception as e:
            logger.error(f"Unexpected error in Bedrock call: {str(e)}")
            return json.dumps({
                "error": str(e),
                "message": "Unexpected error in medical reasoning"
            })
    
    async def analyze_vital_signs(self, vital_signs: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze vital signs using medical reasoning
        """
        reasoning_prompt = f"""
        Analyze these vital signs and provide a comprehensive medical assessment:
        
        Vital Signs:
        {json.dumps(vital_signs, indent=2)}
        
        User Profile:
        {json.dumps(user_profile, indent=2)}
        
        Provide analysis on:
        1. Normal vs abnormal values
        2. Potential health concerns
        3. Risk factors
        4. Recommended monitoring frequency
        5. When to seek medical attention
        
        Consider age, gender, medical history, and current medications in your analysis.
        """
        
        analysis = await self.reason(reasoning_prompt)
        return json.loads(analysis)
    
    async def assess_health_trends(self, health_history: List[Dict[str, Any]], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess health trends over time
        """
        reasoning_prompt = f"""
        Analyze these health trends over time and provide insights:
        
        Health History (last 30 days):
        {json.dumps(health_history, indent=2)}
        
        User Profile:
        {json.dumps(user_profile, indent=2)}
        
        Provide analysis on:
        1. Overall health trend direction
        2. Concerning patterns or changes
        3. Positive improvements
        4. Seasonal or cyclical patterns
        5. Recommendations for health optimization
        
        Focus on early detection of potential health issues.
        """
        
        analysis = await self.reason(reasoning_prompt)
        return json.loads(analysis)
    
    async def generate_health_recommendations(self, current_health: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized health recommendations
        """
        reasoning_prompt = f"""
        Generate personalized health recommendations based on current health status:
        
        Current Health Status:
        {json.dumps(current_health, indent=2)}
        
        User Profile:
        {json.dumps(user_profile, indent=2)}
        
        Provide recommendations on:
        1. Lifestyle modifications
        2. Dietary changes
        3. Exercise recommendations
        4. Stress management
        5. Sleep optimization
        6. Preventive care measures
        7. When to schedule medical appointments
        
        Make recommendations specific, actionable, and evidence-based.
        """
        
        recommendations = await self.reason(reasoning_prompt)
        return json.loads(recommendations)
    
    async def assess_emergency_situation(self, symptoms: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess if a situation requires emergency medical attention
        """
        reasoning_prompt = f"""
        Assess if this situation requires emergency medical attention:
        
        Current Symptoms/Data:
        {json.dumps(symptoms, indent=2)}
        
        User Profile:
        {json.dumps(user_profile, indent=2)}
        
        Provide assessment on:
        1. Emergency severity level (low/medium/high/critical)
        2. Immediate actions required
        3. Whether emergency services should be contacted
        4. Timeline for seeking medical attention
        5. Monitoring recommendations until help arrives
        
        Be conservative and prioritize safety. When in doubt, recommend seeking immediate medical attention.
        """
        
        assessment = await self.reason(reasoning_prompt)
        return json.loads(assessment)
    
    async def analyze_medication_effects(self, medication_data: Dict[str, Any], health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze potential medication effects and interactions
        """
        reasoning_prompt = f"""
        Analyze potential medication effects and interactions:
        
        Medication Information:
        {json.dumps(medication_data, indent=2)}
        
        Current Health Data:
        {json.dumps(health_data, indent=2)}
        
        Provide analysis on:
        1. Expected therapeutic effects
        2. Potential side effects to monitor
        3. Drug interactions to be aware of
        4. Timing and dosing considerations
        5. When to contact healthcare provider
        
        Always recommend consulting with healthcare providers for medication-related decisions.
        """
        
        analysis = await self.reason(reasoning_prompt)
        return json.loads(analysis)
    
    async def predict_health_risks(self, current_data: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict potential health risks based on current data
        """
        reasoning_prompt = f"""
        Predict potential health risks based on current health data:
        
        Current Health Data:
        {json.dumps(current_data, indent=2)}
        
        User Profile:
        {json.dumps(user_profile, indent=2)}
        
        Provide risk assessment on:
        1. Short-term risks (next 24-48 hours)
        2. Medium-term risks (next week to month)
        3. Long-term risks (next 3-12 months)
        4. Risk factors contributing to these risks
        5. Preventive measures to reduce risks
        6. Monitoring recommendations
        
        Focus on evidence-based risk factors and preventive strategies.
        """
        
        risk_assessment = await self.reason(reasoning_prompt)
        return json.loads(risk_assessment)
    
    async def optimize_health_plan(self, current_plan: Dict[str, Any], health_data: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize health monitoring and care plan
        """
        reasoning_prompt = f"""
        Optimize the health monitoring and care plan:
        
        Current Health Plan:
        {json.dumps(current_plan, indent=2)}
        
        Recent Health Data:
        {json.dumps(health_data, indent=2)}
        
        User Profile:
        {json.dumps(user_profile, indent=2)}
        
        Provide optimization recommendations on:
        1. Monitoring frequency adjustments
        2. Additional metrics to track
        3. Goal modifications
        4. Intervention strategies
        5. Healthcare provider coordination
        6. Technology and tool recommendations
        
        Make the plan more effective and personalized based on current health status.
        """
        
        optimization = await self.reason(reasoning_prompt)
        return json.loads(optimization)
