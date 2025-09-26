"""
Health Metrics Models - Data structures for health monitoring
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
import json


class HealthStatus(Enum):
    """Health status enumeration"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class RiskLevel(Enum):
    """Risk level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(Enum):
    """Alert type enumeration"""
    HEALTH_MONITORING = "health_monitoring"
    EMERGENCY = "emergency"
    MEDICATION = "medication"
    APPOINTMENT = "appointment"
    SYSTEM = "system"


@dataclass
class VitalSigns:
    """Vital signs data structure"""
    heart_rate: Optional[int] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    timestamp: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "heart_rate": self.heart_rate,
            "blood_pressure_systolic": self.blood_pressure_systolic,
            "blood_pressure_diastolic": self.blood_pressure_diastolic,
            "temperature": self.temperature,
            "respiratory_rate": self.respiratory_rate,
            "oxygen_saturation": self.oxygen_saturation,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


@dataclass
class HealthMetrics:
    """Comprehensive health metrics data structure"""
    user_id: str
    vital_signs: VitalSigns
    activity_metrics: Dict[str, Any]
    sleep_metrics: Dict[str, Any]
    nutrition_metrics: Dict[str, Any]
    mood_metrics: Dict[str, Any]
    medication_metrics: Dict[str, Any]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "vital_signs": self.vital_signs.to_dict(),
            "activity_metrics": self.activity_metrics,
            "sleep_metrics": self.sleep_metrics,
            "nutrition_metrics": self.nutrition_metrics,
            "mood_metrics": self.mood_metrics,
            "medication_metrics": self.medication_metrics,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class HealthAlert:
    """Health alert data structure"""
    alert_id: str
    user_id: str
    alert_type: AlertType
    risk_level: RiskLevel
    message: str
    health_data: Dict[str, Any]
    recommended_actions: List[str]
    timestamp: datetime
    acknowledged: bool = False
    acknowledged_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "alert_id": self.alert_id,
            "user_id": self.user_id,
            "alert_type": self.alert_type.value,
            "risk_level": self.risk_level.value,
            "message": self.message,
            "health_data": self.health_data,
            "recommended_actions": self.recommended_actions,
            "timestamp": self.timestamp.isoformat(),
            "acknowledged": self.acknowledged,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None
        }


@dataclass
class HealthRecommendation:
    """Health recommendation data structure"""
    recommendation_id: str
    user_id: str
    category: str
    priority: str
    recommendations: List[str]
    goals: List[str]
    timeline: str
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "recommendation_id": self.recommendation_id,
            "user_id": self.user_id,
            "category": self.category,
            "priority": self.priority,
            "recommendations": self.recommendations,
            "goals": self.goals,
            "timeline": self.timeline,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class UserProfile:
    """User health profile data structure"""
    user_id: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    medical_conditions: List[str] = None
    medications: List[str] = None
    allergies: List[str] = None
    emergency_contacts: List[Dict[str, str]] = None
    healthcare_providers: List[Dict[str, str]] = None
    preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.medical_conditions is None:
            self.medical_conditions = []
        if self.medications is None:
            self.medications = []
        if self.allergies is None:
            self.allergies = []
        if self.emergency_contacts is None:
            self.emergency_contacts = []
        if self.healthcare_providers is None:
            self.healthcare_providers = []
        if self.preferences is None:
            self.preferences = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "age": self.age,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "medical_conditions": self.medical_conditions,
            "medications": self.medications,
            "allergies": self.allergies,
            "emergency_contacts": self.emergency_contacts,
            "healthcare_providers": self.healthcare_providers,
            "preferences": self.preferences
        }


@dataclass
class MonitoringConfig:
    """Health monitoring configuration data structure"""
    user_id: str
    vital_signs_frequency: str  # "continuous", "hourly", "daily", "weekly"
    activity_tracking: bool
    sleep_monitoring: bool
    nutrition_tracking: bool
    mood_tracking: bool
    medication_reminders: bool
    alert_thresholds: Dict[str, Any]
    notification_preferences: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "vital_signs_frequency": self.vital_signs_frequency,
            "activity_tracking": self.activity_tracking,
            "sleep_monitoring": self.sleep_monitoring,
            "nutrition_tracking": self.nutrition_tracking,
            "mood_tracking": self.mood_tracking,
            "medication_reminders": self.medication_reminders,
            "alert_thresholds": self.alert_thresholds,
            "notification_preferences": self.notification_preferences
        }
