"""
Alert System Service - Handles health alerts and notifications
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)


class AlertSystem:
    """
    Service for managing health alerts and notifications
    """
    
    def __init__(self):
        self.alert_history = {}
        self.notification_channels = {
            "email": self._send_email_notification,
            "sms": self._send_sms_notification,
            "push": self._send_push_notification,
            "webhook": self._send_webhook_notification
        }
        
    async def generate_health_alert(self, user_id: str, health_analysis: Dict[str, Any], risk_level: str) -> Dict[str, Any]:
        """
        Generate a health alert based on analysis
        """
        try:
            alert = {
                "alert_id": f"alert_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "user_id": user_id,
                "risk_level": risk_level,
                "alert_type": "health_monitoring",
                "timestamp": datetime.utcnow().isoformat(),
                "health_data": health_analysis,
                "alert_message": "",
                "recommended_actions": [],
                "notification_sent": False
            }
            
            # Generate alert message based on risk level
            if risk_level == "critical":
                alert["alert_message"] = "CRITICAL: Immediate medical attention may be required"
                alert["recommended_actions"] = [
                    "Seek immediate medical attention",
                    "Contact emergency services if symptoms worsen",
                    "Notify healthcare provider"
                ]
            elif risk_level == "high":
                alert["alert_message"] = "HIGH PRIORITY: Health concern detected - medical consultation recommended"
                alert["recommended_actions"] = [
                    "Schedule medical consultation within 24 hours",
                    "Monitor symptoms closely",
                    "Contact healthcare provider"
                ]
            elif risk_level == "medium":
                alert["alert_message"] = "MEDIUM PRIORITY: Health monitoring alert - consider medical evaluation"
                alert["recommended_actions"] = [
                    "Schedule medical consultation within 1 week",
                    "Continue monitoring",
                    "Consider lifestyle modifications"
                ]
            else:
                alert["alert_message"] = "LOW PRIORITY: Health monitoring notice"
                alert["recommended_actions"] = [
                    "Continue regular monitoring",
                    "Maintain healthy lifestyle"
                ]
            
            # Store alert in history
            if user_id not in self.alert_history:
                self.alert_history[user_id] = []
            self.alert_history[user_id].append(alert)
            
            # Send notifications
            await self._send_alert_notifications(alert)
            
            return alert
            
        except Exception as e:
            logger.error(f"Error generating health alert: {str(e)}")
            return {
                "error": str(e),
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _send_alert_notifications(self, alert: Dict[str, Any]) -> None:
        """
        Send alert notifications through multiple channels
        """
        user_id = alert["user_id"]
        risk_level = alert["risk_level"]
        
        # Determine notification channels based on risk level
        if risk_level == "critical":
            channels = ["email", "sms", "push", "webhook"]
        elif risk_level == "high":
            channels = ["email", "push", "webhook"]
        elif risk_level == "medium":
            channels = ["email", "push"]
        else:
            channels = ["push"]
        
        # Send notifications through each channel
        for channel in channels:
            try:
                await self.notification_channels[channel](alert)
            except Exception as e:
                logger.error(f"Error sending {channel} notification: {str(e)}")
        
        alert["notification_sent"] = True
    
    async def _send_email_notification(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send email notification
        """
        # Simulate email sending
        # In production, this would integrate with AWS SES or similar service
        
        email_data = {
            "to": f"user_{alert['user_id']}@example.com",
            "subject": f"Health Alert: {alert['alert_message']}",
            "body": self._generate_email_body(alert),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Email notification sent: {email_data['subject']}")
        return email_data
    
    async def _send_sms_notification(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send SMS notification
        """
        # Simulate SMS sending
        # In production, this would integrate with AWS SNS or similar service
        
        sms_data = {
            "to": f"+1234567890",  # User's phone number
            "message": f"Health Alert: {alert['alert_message']}",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"SMS notification sent: {sms_data['message']}")
        return sms_data
    
    async def _send_push_notification(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send push notification
        """
        # Simulate push notification
        # In production, this would integrate with AWS SNS or Firebase
        
        push_data = {
            "device_token": f"device_token_{alert['user_id']}",
            "title": "Health Alert",
            "body": alert["alert_message"],
            "data": {
                "alert_id": alert["alert_id"],
                "risk_level": alert["risk_level"],
                "timestamp": alert["timestamp"]
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Push notification sent: {push_data['title']}")
        return push_data
    
    async def _send_webhook_notification(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send webhook notification
        """
        # Simulate webhook sending
        # In production, this would send to healthcare provider systems
        
        webhook_data = {
            "url": "https://healthcare-provider.com/webhook/alerts",
            "payload": {
                "alert_id": alert["alert_id"],
                "user_id": alert["user_id"],
                "risk_level": alert["risk_level"],
                "alert_message": alert["alert_message"],
                "health_data": alert["health_data"],
                "recommended_actions": alert["recommended_actions"],
                "timestamp": alert["timestamp"]
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Webhook notification sent to: {webhook_data['url']}")
        return webhook_data
    
    def _generate_email_body(self, alert: Dict[str, Any]) -> str:
        """
        Generate email body for health alert
        """
        body = f"""
        Health Alert Notification
        
        Alert ID: {alert['alert_id']}
        Risk Level: {alert['risk_level'].upper()}
        Timestamp: {alert['timestamp']}
        
        Message: {alert['alert_message']}
        
        Recommended Actions:
        """
        
        for i, action in enumerate(alert['recommended_actions'], 1):
            body += f"\n{i}. {action}"
        
        body += f"""
        
        Health Data Summary:
        {json.dumps(alert['health_data'], indent=2)}
        
        This is an automated health monitoring alert. Please consult with your healthcare provider for medical advice.
        
        Best regards,
        Smart Health Monitoring AI Agent
        """
        
        return body
    
    async def notify_emergency_services(self, user_id: str, emergency_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Notify emergency services for critical situations
        """
        try:
            emergency_notification = {
                "notification_id": f"emergency_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "user_id": user_id,
                "emergency_type": "health_critical",
                "severity": emergency_assessment.get("severity_level", "unknown"),
                "timestamp": datetime.utcnow().isoformat(),
                "assessment": emergency_assessment,
                "location": "User's registered address",  # In production, get from user profile
                "contact_info": f"Emergency contact for user {user_id}",
                "status": "sent"
            }
            
            # Simulate emergency services notification
            # In production, this would integrate with emergency services APIs
            
            logger.info(f"Emergency services notified for user {user_id}")
            return emergency_notification
            
        except Exception as e:
            logger.error(f"Error notifying emergency services: {str(e)}")
            return {
                "error": str(e),
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def notify_healthcare_provider(self, user_id: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Notify healthcare provider about health concerns
        """
        try:
            provider_notification = {
                "notification_id": f"provider_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "user_id": user_id,
                "provider_id": f"provider_{user_id}",  # In production, get from user profile
                "notification_type": "health_concern",
                "timestamp": datetime.utcnow().isoformat(),
                "health_data": health_data,
                "priority": health_data.get("risk_level", "medium"),
                "status": "sent"
            }
            
            # Simulate healthcare provider notification
            # In production, this would integrate with healthcare provider systems
            
            logger.info(f"Healthcare provider notified for user {user_id}")
            return provider_notification
            
        except Exception as e:
            logger.error(f"Error notifying healthcare provider: {str(e)}")
            return {
                "error": str(e),
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def notify_user_contacts(self, user_id: str, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Notify user's emergency contacts
        """
        try:
            # Simulate getting emergency contacts
            emergency_contacts = [
                {"name": "Emergency Contact 1", "phone": "+1234567890", "email": "contact1@example.com"},
                {"name": "Emergency Contact 2", "phone": "+0987654321", "email": "contact2@example.com"}
            ]
            
            contact_notifications = []
            
            for contact in emergency_contacts:
                notification = {
                    "contact_name": contact["name"],
                    "contact_phone": contact["phone"],
                    "contact_email": contact["email"],
                    "message": f"Health alert for {user_id}: {alert_data.get('alert_message', 'Health concern detected')}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "sent"
                }
                
                contact_notifications.append(notification)
            
            logger.info(f"Emergency contacts notified for user {user_id}")
            return {
                "user_id": user_id,
                "contacts_notified": contact_notifications,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error notifying user contacts: {str(e)}")
            return {
                "error": str(e),
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_alert_history(self, user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get alert history for a user
        """
        if user_id not in self.alert_history:
            return []
        
        # Filter alerts from the last N days
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        recent_alerts = [
            alert for alert in self.alert_history[user_id]
            if datetime.fromisoformat(alert["timestamp"]) > cutoff_date
        ]
        
        return recent_alerts
    
    async def acknowledge_alert(self, alert_id: str, user_id: str) -> Dict[str, Any]:
        """
        Acknowledge an alert
        """
        if user_id in self.alert_history:
            for alert in self.alert_history[user_id]:
                if alert["alert_id"] == alert_id:
                    alert["acknowledged"] = True
                    alert["acknowledged_at"] = datetime.utcnow().isoformat()
                    
                    return {
                        "status": "acknowledged",
                        "alert_id": alert_id,
                        "user_id": user_id,
                        "acknowledged_at": alert["acknowledged_at"]
                    }
        
        return {
            "status": "error",
            "message": f"Alert {alert_id} not found for user {user_id}"
        }
    
    async def create_alert_rule(self, user_id: str, rule_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a custom alert rule for a user
        """
        rule = {
            "rule_id": f"rule_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "user_id": user_id,
            "rule_config": rule_config,
            "created_at": datetime.utcnow().isoformat(),
            "active": True
        }
        
        # Store rule (in production, this would be stored in a database)
        if user_id not in self.alert_history:
            self.alert_history[user_id] = []
        
        return rule
    
    async def test_alert_system(self, user_id: str) -> Dict[str, Any]:
        """
        Test the alert system
        """
        test_alert = {
            "alert_id": f"test_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "user_id": user_id,
            "risk_level": "low",
            "alert_type": "system_test",
            "timestamp": datetime.utcnow().isoformat(),
            "alert_message": "This is a test alert to verify the notification system",
            "recommended_actions": ["Verify you received this test alert"],
            "notification_sent": True
        }
        
        # Send test notifications
        await self._send_alert_notifications(test_alert)
        
        return test_alert
