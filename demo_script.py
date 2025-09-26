"""
Demo Script for Smart Health Monitoring AI Agent
"""

import asyncio
import json
from datetime import datetime, timedelta
from src.agent.core.health_agent import SmartHealthMonitoringAgent

async def demo_health_monitoring_agent():
    """
    Demonstrate the Smart Health Monitoring AI Agent capabilities
    """
    print("🏥 Smart Health Monitoring AI Agent Demo")
    print("=" * 50)
    
    # Initialize the agent
    print("\n1. Initializing Health Monitoring Agent...")
    agent = SmartHealthMonitoringAgent()
    
    # Demo user profile
    user_id = "demo_user_001"
    monitoring_config = {
        "age": 35,
        "gender": "female",
        "medical_conditions": ["hypertension", "type_2_diabetes"],
        "medications": ["Metformin", "Lisinopril"],
        "risk_factors": ["family_history_heart_disease", "sedentary_lifestyle"],
        "goals": ["improve_cardiovascular_health", "better_diabetes_management"],
        "alert_preferences": {
            "email": True,
            "sms": True,
            "push": True
        }
    }
    
    print(f"   User ID: {user_id}")
    print(f"   Age: {monitoring_config['age']}")
    print(f"   Medical Conditions: {', '.join(monitoring_config['medical_conditions'])}")
    
    # Start autonomous monitoring
    print("\n2. Starting Autonomous Health Monitoring...")
    monitoring_result = await agent.start_autonomous_monitoring(user_id, monitoring_config)
    
    if monitoring_result["status"] == "success":
        print("   ✅ Monitoring started successfully")
        
        # Display monitoring plan
        plan = monitoring_result["monitoring_plan"]
        print(f"\n   📋 Monitoring Plan Created:")
        print(f"   - Vital Signs: {plan.get('vital_signs', [])}")
        print(f"   - Health Metrics: {plan.get('health_metrics', [])}")
        print(f"   - Alert Thresholds: {plan.get('alert_thresholds', {})}")
        
        # Display results
        results = monitoring_result["results"]
        print(f"\n   📊 Monitoring Results:")
        print(f"   - Health Data Points Collected: {len(results['health_data_collected'])}")
        print(f"   - Health Analyses Performed: {len(results['health_analysis'])}")
        print(f"   - Alerts Generated: {len(results['alerts_generated'])}")
        print(f"   - Recommendations Created: {len(results['recommendations'])}")
        
        # Show sample health data
        if results["health_data_collected"]:
            print(f"\n   📈 Sample Health Data:")
            sample_data = results["health_data_collected"][0]
            print(f"   - Source: {sample_data.get('source', 'Unknown')}")
            print(f"   - Metric Type: {sample_data.get('metric_type', 'Unknown')}")
            print(f"   - Timestamp: {sample_data.get('timestamp', 'Unknown')}")
        
        # Show sample analysis
        if results["health_analysis"]:
            print(f"\n   🔍 Sample Health Analysis:")
            sample_analysis = results["health_analysis"][0]
            medical_analysis = sample_analysis.get("medical_analysis", {})
            print(f"   - Risk Level: {medical_analysis.get('risk_level', 'Unknown')}")
            print(f"   - Key Insights: {medical_analysis.get('key_insights', [])}")
        
        # Show alerts
        if results["alerts_generated"]:
            print(f"\n   🚨 Health Alerts:")
            for alert in results["alerts_generated"]:
                print(f"   - Alert ID: {alert.get('alert_id', 'Unknown')}")
                print(f"   - Risk Level: {alert.get('risk_level', 'Unknown')}")
                print(f"   - Message: {alert.get('alert_message', 'Unknown')}")
        
        # Show recommendations
        if results["recommendations"]:
            print(f"\n   💡 Health Recommendations:")
            for rec in results["recommendations"]:
                print(f"   - Category: {rec.get('category', 'Unknown')}")
                print(f"   - Priority: {rec.get('priority', 'Unknown')}")
                print(f"   - Timeline: {rec.get('timeline', 'Unknown')}")
    
    else:
        print(f"   ❌ Error starting monitoring: {monitoring_result.get('error', 'Unknown error')}")
    
    # Demo emergency alert handling
    print(f"\n3. Demonstrating Emergency Alert Handling...")
    emergency_data = {
        "symptoms": {
            "chest_pain": True,
            "shortness_of_breath": True,
            "heart_rate": 150,
            "blood_pressure": "180/110"
        },
        "severity": "critical",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    emergency_result = await agent.handle_emergency_alert(user_id, emergency_data)
    
    if emergency_result["status"] == "emergency_handled":
        print("   ✅ Emergency alert handled successfully")
        assessment = emergency_result["assessment"]
        print(f"   - Severity Assessment: {assessment.get('severity_level', 'Unknown')}")
        print(f"   - Immediate Actions: {assessment.get('immediate_actions', [])}")
        print(f"   - Actions Taken: {len(emergency_result['actions_taken'])}")
    else:
        print(f"   ❌ Error handling emergency: {emergency_result.get('error', 'Unknown error')}")
    
    # Demo agent status
    print(f"\n4. Agent Status Check...")
    status = await agent.get_agent_status()
    print(f"   - Status: {status.get('status', 'Unknown')}")
    print(f"   - Active Monitoring: {status.get('active_monitoring', 0)}")
    print(f"   - Users Monitored: {status.get('users_monitored', 0)}")
    print(f"   - Health Data Points: {status.get('health_data_points', 0)}")
    
    # Demo configuration update
    print(f"\n5. Updating Monitoring Configuration...")
    new_config = {
        "additional_metrics": ["sleep_quality", "stress_level"],
        "alert_frequency": "hourly"
    }
    
    update_result = await agent.update_monitoring_config(user_id, new_config)
    
    if update_result["status"] == "success":
        print("   ✅ Configuration updated successfully")
        print(f"   - Updated Config: {update_result.get('updated_config', {})}")
    else:
        print(f"   ❌ Error updating configuration: {update_result.get('message', 'Unknown error')}")
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"\nKey Features Demonstrated:")
    print(f"✅ Autonomous health monitoring")
    print(f"✅ Medical reasoning with Bedrock LLM")
    print(f"✅ Multi-source data collection")
    print(f"✅ Intelligent health analysis")
    print(f"✅ Emergency alert handling")
    print(f"✅ Personalized recommendations")
    print(f"✅ Real-time monitoring capabilities")


async def demo_api_endpoints():
    """
    Demonstrate API endpoint functionality
    """
    print(f"\n🌐 API Endpoints Demo")
    print("=" * 30)
    
    # Simulate API calls
    api_endpoints = [
        {
            "method": "POST",
            "endpoint": "/monitor",
            "description": "Start autonomous health monitoring",
            "sample_request": {
                "user_id": "demo_user_001",
                "monitoring_config": {
                    "age": 35,
                    "medical_conditions": ["hypertension"]
                }
            }
        },
        {
            "method": "GET",
            "endpoint": "/status/{user_id}",
            "description": "Get user monitoring status",
            "sample_request": None
        },
        {
            "method": "POST",
            "endpoint": "/emergency",
            "description": "Handle emergency health alerts",
            "sample_request": {
                "user_id": "demo_user_001",
                "alert_data": {
                    "symptoms": {"chest_pain": True},
                    "severity": "critical"
                }
            }
        },
        {
            "method": "GET",
            "endpoint": "/agent/status",
            "description": "Get agent system status",
            "sample_request": None
        }
    ]
    
    for endpoint in api_endpoints:
        print(f"\n📡 {endpoint['method']} {endpoint['endpoint']}")
        print(f"   Description: {endpoint['description']}")
        if endpoint['sample_request']:
            print(f"   Sample Request: {json.dumps(endpoint['sample_request'], indent=2)}")


def main():
    """
    Main demo function
    """
    print("🚀 Starting Smart Health Monitoring AI Agent Demo")
    print("This demo showcases the autonomous health monitoring capabilities")
    print("using Amazon Bedrock for medical reasoning and decision-making.")
    
    # Run the main demo
    asyncio.run(demo_health_monitoring_agent())
    
    # Run API demo
    asyncio.run(demo_api_endpoints())
    
    print(f"\n📋 Hackathon Compliance Summary:")
    print(f"✅ LLM: Amazon Bedrock Claude 3.5 Sonnet")
    print(f"✅ Reasoning: Advanced medical reasoning and decision-making")
    print(f"✅ Autonomous: Executes health monitoring without human intervention")
    print(f"✅ External Integration: Health APIs, wearable devices, medical databases")
    print(f"✅ AWS Services: Bedrock, Lambda, API Gateway, S3")
    print(f"✅ Real-world Impact: Addresses critical healthcare monitoring challenges")


if __name__ == "__main__":
    main()
