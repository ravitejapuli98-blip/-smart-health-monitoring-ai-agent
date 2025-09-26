"""
Health Data Collector Service - Collects health data from multiple sources
"""

import asyncio
import aiohttp
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
import json
import random

logger = logging.getLogger(__name__)


class HealthDataCollector:
    """
    Service for collecting health data from multiple sources
    """
    
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.data_sources = {
            "wearable_devices": self.collect_wearable_data,
            "health_apps": self.collect_health_app_data,
            "external_apis": self.collect_external_health_data,
            "manual_input": self.collect_manual_health_data
        }
        
    async def collect_wearable_data(self, user_id: str, metric_type: str) -> Dict[str, Any]:
        """
        Collect data from wearable devices (Apple Watch, Fitbit, etc.)
        """
        try:
            # Simulate wearable device data collection
            # In production, this would integrate with actual wearable APIs
            
            wearable_data = {
                "user_id": user_id,
                "source": "wearable_device",
                "metric_type": metric_type,
                "timestamp": datetime.utcnow().isoformat(),
                "data": {}
            }
            
            if metric_type == "heart_rate":
                wearable_data["data"] = {
                    "current_hr": random.randint(60, 100),
                    "resting_hr": random.randint(50, 70),
                    "max_hr": random.randint(180, 200),
                    "hr_variability": random.uniform(20, 50),
                    "hr_zones": {
                        "fat_burn": random.randint(20, 30),
                        "cardio": random.randint(30, 40),
                        "peak": random.randint(10, 20)
                    }
                }
            elif metric_type == "blood_pressure":
                wearable_data["data"] = {
                    "systolic": random.randint(110, 140),
                    "diastolic": random.randint(70, 90),
                    "pulse_pressure": random.randint(30, 50),
                    "measurement_time": datetime.utcnow().isoformat()
                }
            elif metric_type == "temperature":
                wearable_data["data"] = {
                    "body_temp": round(random.uniform(97.0, 99.5), 1),
                    "ambient_temp": round(random.uniform(68.0, 75.0), 1),
                    "measurement_location": "wrist"
                }
            elif metric_type == "activity":
                wearable_data["data"] = {
                    "steps": random.randint(5000, 15000),
                    "calories_burned": random.randint(200, 800),
                    "active_minutes": random.randint(30, 120),
                    "distance": round(random.uniform(2.0, 8.0), 2),
                    "floors_climbed": random.randint(5, 25)
                }
            elif metric_type == "sleep":
                wearable_data["data"] = {
                    "sleep_duration": random.randint(6, 9),
                    "deep_sleep": random.randint(1, 3),
                    "rem_sleep": random.randint(1, 2),
                    "light_sleep": random.randint(3, 5),
                    "sleep_efficiency": round(random.uniform(75, 95), 1),
                    "bedtime": (datetime.utcnow() - timedelta(hours=8)).isoformat(),
                    "wake_time": datetime.utcnow().isoformat()
                }
            
            return wearable_data
            
        except Exception as e:
            logger.error(f"Error collecting wearable data: {str(e)}")
            return {"error": str(e), "user_id": user_id, "metric_type": metric_type}
    
    async def collect_health_app_data(self, user_id: str, metric_type: str) -> Dict[str, Any]:
        """
        Collect data from health apps (MyFitnessPal, Strava, etc.)
        """
        try:
            app_data = {
                "user_id": user_id,
                "source": "health_app",
                "metric_type": metric_type,
                "timestamp": datetime.utcnow().isoformat(),
                "data": {}
            }
            
            if metric_type == "nutrition":
                app_data["data"] = {
                    "calories_consumed": random.randint(1500, 2500),
                    "protein": random.randint(60, 120),
                    "carbs": random.randint(150, 300),
                    "fat": random.randint(50, 100),
                    "fiber": random.randint(20, 40),
                    "sugar": random.randint(30, 80),
                    "sodium": random.randint(1500, 3000),
                    "water_intake": random.randint(6, 12)
                }
            elif metric_type == "exercise":
                app_data["data"] = {
                    "workout_type": random.choice(["cardio", "strength", "yoga", "running"]),
                    "duration": random.randint(20, 90),
                    "intensity": random.choice(["low", "moderate", "high"]),
                    "calories_burned": random.randint(150, 600),
                    "heart_rate_avg": random.randint(120, 160),
                    "heart_rate_max": random.randint(160, 190)
                }
            elif metric_type == "mood":
                app_data["data"] = {
                    "mood_score": random.randint(1, 10),
                    "stress_level": random.randint(1, 10),
                    "energy_level": random.randint(1, 10),
                    "anxiety_level": random.randint(1, 10),
                    "notes": "Feeling good today"
                }
            elif metric_type == "medication":
                app_data["data"] = {
                    "medications_taken": [
                        {"name": "Vitamin D", "dose": "1000 IU", "time": "08:00"},
                        {"name": "Omega-3", "dose": "1000mg", "time": "12:00"}
                    ],
                    "medications_missed": [],
                    "side_effects": []
                }
            
            return app_data
            
        except Exception as e:
            logger.error(f"Error collecting health app data: {str(e)}")
            return {"error": str(e), "user_id": user_id, "metric_type": metric_type}
    
    async def collect_external_health_data(self, user_id: str) -> Dict[str, Any]:
        """
        Collect data from external health APIs and services
        """
        try:
            external_data = {
                "user_id": user_id,
                "source": "external_api",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {}
            }
            
            # Simulate external health data collection
            # In production, this would integrate with APIs like:
            # - Electronic Health Records (EHR) systems
            # - Laboratory result APIs
            # - Pharmacy APIs
            # - Insurance health data APIs
            
            external_data["data"] = {
                "lab_results": {
                    "cholesterol": {
                        "total": random.randint(150, 250),
                        "hdl": random.randint(40, 80),
                        "ldl": random.randint(70, 160),
                        "triglycerides": random.randint(50, 200),
                        "date": (datetime.utcnow() - timedelta(days=30)).isoformat()
                    },
                    "blood_glucose": {
                        "fasting": random.randint(70, 110),
                        "hba1c": round(random.uniform(5.0, 7.0), 1),
                        "date": (datetime.utcnow() - timedelta(days=30)).isoformat()
                    },
                    "complete_blood_count": {
                        "hemoglobin": round(random.uniform(12.0, 16.0), 1),
                        "hematocrit": round(random.uniform(36.0, 46.0), 1),
                        "white_blood_cells": round(random.uniform(4.0, 11.0), 1),
                        "platelets": random.randint(150, 450),
                        "date": (datetime.utcnow() - timedelta(days=30)).isoformat()
                    }
                },
                "medical_history": {
                    "conditions": ["hypertension", "type_2_diabetes"],
                    "allergies": ["penicillin"],
                    "surgeries": ["appendectomy_2015"],
                    "last_physical": (datetime.utcnow() - timedelta(days=90)).isoformat()
                },
                "medication_history": {
                    "current_medications": [
                        {"name": "Metformin", "dose": "500mg", "frequency": "twice_daily"},
                        {"name": "Lisinopril", "dose": "10mg", "frequency": "once_daily"}
                    ],
                    "recent_changes": []
                }
            }
            
            return external_data
            
        except Exception as e:
            logger.error(f"Error collecting external health data: {str(e)}")
            return {"error": str(e), "user_id": user_id}
    
    async def collect_manual_health_data(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect manually entered health data
        """
        try:
            manual_data = {
                "user_id": user_id,
                "source": "manual_input",
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            
            return manual_data
            
        except Exception as e:
            logger.error(f"Error collecting manual health data: {str(e)}")
            return {"error": str(e), "user_id": user_id}
    
    async def collect_comprehensive_health_data(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Collect comprehensive health data from all sources
        """
        all_data = []
        
        # Define metrics to collect
        wearable_metrics = ["heart_rate", "blood_pressure", "temperature", "activity", "sleep"]
        app_metrics = ["nutrition", "exercise", "mood", "medication"]
        
        # Create collection tasks
        tasks = []
        
        # Collect wearable data
        for metric in wearable_metrics:
            task = self.collect_wearable_data(user_id, metric)
            tasks.append(task)
        
        # Collect health app data
        for metric in app_metrics:
            task = self.collect_health_app_data(user_id, metric)
            tasks.append(task)
        
        # Collect external data
        task = self.collect_external_health_data(user_id)
        tasks.append(task)
        
        # Execute all collection tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, dict) and "error" not in result:
                all_data.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Data collection error: {str(result)}")
        
        return all_data
    
    async def validate_health_data(self, health_data: Dict[str, Any]) -> bool:
        """
        Validate health data for completeness and accuracy
        """
        try:
            # Check required fields
            required_fields = ["user_id", "source", "timestamp", "data"]
            for field in required_fields:
                if field not in health_data:
                    return False
            
            # Validate timestamp
            try:
                datetime.fromisoformat(health_data["timestamp"])
            except ValueError:
                return False
            
            # Validate data structure
            if not isinstance(health_data["data"], dict):
                return False
            
            # Source-specific validation
            source = health_data["source"]
            if source == "wearable_device":
                return self._validate_wearable_data(health_data["data"])
            elif source == "health_app":
                return self._validate_health_app_data(health_data["data"])
            elif source == "external_api":
                return self._validate_external_data(health_data["data"])
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating health data: {str(e)}")
            return False
    
    def _validate_wearable_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate wearable device data
        """
        # Check for reasonable value ranges
        if "heart_rate" in data:
            hr = data["heart_rate"]
            if not (30 <= hr <= 220):
                return False
        
        if "temperature" in data:
            temp = data["temperature"]
            if not (95.0 <= temp <= 105.0):
                return False
        
        return True
    
    def _validate_health_app_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate health app data
        """
        # Check for reasonable value ranges
        if "calories_consumed" in data:
            calories = data["calories_consumed"]
            if not (0 <= calories <= 5000):
                return False
        
        return True
    
    def _validate_external_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate external API data
        """
        # Check for required structure
        if "lab_results" not in data:
            return False
        
        return True
    
    async def get_health_data_history(self, user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get historical health data for a user
        """
        try:
            # Simulate retrieving historical data
            # In production, this would query a database
            
            history = []
            for i in range(days):
                date = datetime.utcnow() - timedelta(days=i)
                
                # Generate mock historical data
                historical_data = {
                    "user_id": user_id,
                    "date": date.isoformat(),
                    "heart_rate_avg": random.randint(60, 100),
                    "steps": random.randint(5000, 15000),
                    "sleep_hours": round(random.uniform(6, 9), 1),
                    "calories_burned": random.randint(200, 800),
                    "mood_score": random.randint(1, 10)
                }
                
                history.append(historical_data)
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting health data history: {str(e)}")
            return []
    
    async def close(self):
        """
        Close the session
        """
        await self.session.close()
