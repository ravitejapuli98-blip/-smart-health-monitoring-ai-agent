"""
Demo Recording Guide for Smart Health Monitoring AI Agent
This script helps create a professional demo video for the hackathon
"""

import time
import os
import sys

def print_banner(text, char="=", width=60):
    """Print a formatted banner"""
    print(f"\n{char * width}")
    print(f"{text:^{width}}")
    print(f"{char * width}\n")

def demo_intro():
    """Introduction section"""
    print_banner("SMART HEALTH MONITORING AI AGENT", "=")
    print("Welcome to the Smart Health Monitoring AI Agent!")
    print("An innovative solution for autonomous health monitoring")
    print("Built for AWS AI Agent Global Hackathon")
    print("\nKey Features:")
    print("• Autonomous health monitoring")
    print("• AI-powered medical reasoning")
    print("• Real-time health analysis")
    print("• Emergency response system")
    print("• Personalized recommendations")

def demo_architecture():
    """Show architecture"""
    print_banner("SYSTEM ARCHITECTURE", "-")
    print("AWS Services Used:")
    print("┌─────────────────────────────────────────────────┐")
    print("│  Amazon Bedrock (Claude 3.5 Sonnet)            │")
    print("│  ├── Medical reasoning & decision-making       │")
    print("│  └── Health pattern analysis                   │")
    print("├─────────────────────────────────────────────────┤")
    print("│  AWS Lambda                                    │")
    print("│  ├── Serverless health data processing         │")
    print("│  └── Autonomous monitoring engine              │")
    print("├─────────────────────────────────────────────────┤")
    print("│  Amazon API Gateway                            │")
    print("│  ├── RESTful health monitoring API             │")
    print("│  └── Secure endpoint management                │")
    print("├─────────────────────────────────────────────────┤")
    print("│  Amazon S3                                     │")
    print("│  ├── Encrypted health data storage             │")
    print("│  └── Historical health records                 │")
    print("└─────────────────────────────────────────────────┘")

def demo_live_monitoring():
    """Simulate live health monitoring"""
    print_banner("LIVE HEALTH MONITORING DEMO", "-")
    
    # Simulate health data collection
    health_data = {
        "user_id": "demo_user_001",
        "timestamp": "2024-01-15T10:30:00Z",
        "vital_signs": {
            "heart_rate": 72,
            "blood_pressure": "120/80",
            "temperature": 98.6,
            "oxygen_saturation": 98
        },
        "activity": {
            "steps": 8542,
            "calories_burned": 420,
            "active_minutes": 45
        },
        "sleep": {
            "duration_hours": 7.5,
            "quality_score": 85,
            "deep_sleep_percentage": 25
        }
    }
    
    print("Collecting health data from multiple sources...")
    time.sleep(1)
    
    print(f"✓ Wearable device data: {health_data['vital_signs']['heart_rate']} BPM")
    print(f"✓ Blood pressure: {health_data['vital_signs']['blood_pressure']} mmHg")
    print(f"✓ Activity tracking: {health_data['activity']['steps']} steps")
    print(f"✓ Sleep analysis: {health_data['sleep']['duration_hours']} hours")
    
    time.sleep(1)
    print("\nAnalyzing health patterns with AI...")
    time.sleep(1)
    
    # Simulate AI analysis
    print("✓ Health status: NORMAL")
    print("✓ Risk assessment: LOW")
    print("✓ Trend analysis: IMPROVING")
    
    return health_data

def demo_ai_reasoning():
    """Show AI reasoning capabilities"""
    print_banner("AI MEDICAL REASONING", "-")
    
    print("Amazon Bedrock Claude 3.5 Sonnet Analysis:")
    print("┌─────────────────────────────────────────────────┐")
    print("│  Medical Pattern Recognition:                  │")
    print("│  • Heart rate within normal range (60-100)     │")
    print("│  • Blood pressure optimal (120/80)             │")
    print("│  • Sleep quality improving trend                │")
    print("│  • Activity level adequate                      │")
    print("├─────────────────────────────────────────────────┤")
    print("│  Risk Assessment:                              │")
    print("│  • Cardiovascular risk: LOW                    │")
    print("│  • Sleep disorder risk: LOW                    │")
    print("│  • Overall health score: 85/100                │")
    print("├─────────────────────────────────────────────────┤")
    print("│  Personalized Recommendations:                 │")
    print("│  • Continue current exercise routine           │")
    print("│  • Maintain sleep schedule                     │")
    print("│  • Consider adding meditation for stress       │")
    print("└─────────────────────────────────────────────────┘")

def demo_emergency_scenario():
    """Show emergency response"""
    print_banner("EMERGENCY RESPONSE SYSTEM", "-")
    
    print("Simulating critical health event...")
    time.sleep(1)
    
    print("⚠️  ALERT: Abnormal heart rate detected!")
    print("   Heart rate: 150 BPM (CRITICAL)")
    print("   Blood pressure: 180/110 (HIGH)")
    print("   Time: 2024-01-15T14:25:00Z")
    
    time.sleep(1)
    print("\nAI Agent Response:")
    print("✓ Immediate alert generated")
    print("✓ Healthcare provider notified")
    print("✓ Emergency contact called")
    print("✓ Medical history retrieved")
    print("✓ Ambulance dispatched")
    
    print("\nAutomated Actions:")
    print("• SNS notification sent to doctor")
    print("• SMS alert sent to emergency contact")
    print("• Health data prepared for medical team")
    print("• Location shared with emergency services")

def demo_impact():
    """Show real-world impact"""
    print_banner("REAL-WORLD IMPACT", "-")
    
    print("Healthcare Transformation:")
    print("• Proactive vs Reactive Care")
    print("• Early Detection of Health Issues")
    print("• Reduced Emergency Room Visits")
    print("• Improved Patient Outcomes")
    print("• Cost-effective Healthcare Delivery")
    
    print("\nTechnical Innovation:")
    print("• Serverless Architecture")
    print("• Real-time AI Processing")
    print("• Multi-source Data Integration")
    print("• Autonomous Decision Making")
    print("• Scalable Cloud Infrastructure")

def demo_conclusion():
    """Demo conclusion"""
    print_banner("HACKATHON COMPLIANCE", "-")
    
    print("✅ LLM on AWS: Amazon Bedrock Claude 3.5 Sonnet")
    print("✅ Reasoning: Advanced medical analysis & decision-making")
    print("✅ Autonomous: Monitors health without human intervention")
    print("✅ External Integration: Wearables, health apps, medical APIs")
    print("✅ AWS Services: Bedrock, Lambda, API Gateway, S3, SNS")
    print("✅ Real Impact: Addresses critical healthcare challenges")
    
    print_banner("THANK YOU", "=")
    print("Smart Health Monitoring AI Agent")
    print("AWS AI Agent Global Hackathon 2024")
    print("Repository: github.com/ravitejapuli98-blip/smart-health-monitoring-ai-agent")

def main():
    """Main demo function"""
    print("Starting Smart Health Monitoring AI Agent Demo...")
    print("This demo will run for approximately 3 minutes")
    print("Press Ctrl+C to stop at any time\n")
    
    try:
        # Demo sections with timing
        demo_intro()
        time.sleep(2)
        
        demo_architecture()
        time.sleep(2)
        
        health_data = demo_live_monitoring()
        time.sleep(2)
        
        demo_ai_reasoning()
        time.sleep(2)
        
        demo_emergency_scenario()
        time.sleep(2)
        
        demo_impact()
        time.sleep(2)
        
        demo_conclusion()
        
    except KeyboardInterrupt:
        print("\n\nDemo stopped by user")
        print("Thank you for watching!")

if __name__ == "__main__":
    main()
