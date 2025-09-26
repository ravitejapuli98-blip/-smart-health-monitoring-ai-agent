"""
Architecture Diagram Generator for Smart Health Monitoring AI Agent
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway
from diagrams.aws.ai import Bedrock
from diagrams.aws.integration import SNS
from diagrams.aws.security import IAM
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.client import Users
from diagrams.onprem.mobile import Mobile
from diagrams.onprem.analytics import Grafana
from diagrams.generic.blank import Blank

def create_architecture_diagram():
    """
    Create architecture diagram for the Smart Health Monitoring AI Agent
    """
    
    with Diagram("Smart Health Monitoring AI Agent Architecture", 
                 filename="architecture_diagram", 
                 show=False, 
                 direction="TB"):
        
        # External data sources
        with Cluster("External Data Sources"):
            wearable_devices = Mobile("Wearable Devices\n(Apple Watch, Fitbit)")
            health_apps = Mobile("Health Apps\n(MyFitnessPal, Strava)")
            external_apis = Prometheus("External Health APIs\n(EHR, Lab Results)")
        
        # Users
        users = Users("Users\n(Patients, Healthcare Providers)")
        
        # API Gateway
        api_gateway = APIGateway("API Gateway\nHealth Monitoring API")
        
        # Core AI Agent
        with Cluster("AI Agent Core"):
            lambda_function = Lambda("Smart Health\nMonitoring Agent\n(Lambda Function)")
            bedrock_llm = Bedrock("Amazon Bedrock\nClaude 3.5 Sonnet\n(Medical Reasoning)")
        
        # Services
        with Cluster("Agent Services"):
            data_collector = Lambda("Health Data\nCollector")
            health_analyzer = Lambda("Health\nAnalyzer")
            alert_system = Lambda("Alert\nSystem")
            recommendation_engine = Lambda("Recommendation\nEngine")
        
        # Storage
        with Cluster("Data Storage"):
            s3_bucket = S3("Health Data\nStorage (S3)")
            rds_database = RDS("User Profiles\n& History (RDS)")
        
        # Notifications
        with Cluster("Notification System"):
            sns_service = SNS("Amazon SNS\n(Notifications)")
            email_notifications = Blank("Email\nNotifications")
            sms_notifications = Blank("SMS\nNotifications")
            push_notifications = Blank("Push\nNotifications")
        
        # Monitoring
        with Cluster("Monitoring & Analytics"):
            cloudwatch = Prometheus("CloudWatch\nLogs & Metrics")
            grafana_dashboard = Grafana("Health Dashboard\n(Grafana)")
        
        # Security
        iam_role = IAM("IAM Role\n(Permissions)")
        
        # Connections
        users >> api_gateway
        api_gateway >> lambda_function
        
        lambda_function >> bedrock_llm
        lambda_function >> data_collector
        lambda_function >> health_analyzer
        lambda_function >> alert_system
        lambda_function >> recommendation_engine
        
        data_collector >> wearable_devices
        data_collector >> health_apps
        data_collector >> external_apis
        
        health_analyzer >> s3_bucket
        alert_system >> sns_service
        recommendation_engine >> rds_database
        
        sns_service >> email_notifications
        sns_service >> sms_notifications
        sns_service >> push_notifications
        
        lambda_function >> cloudwatch
        cloudwatch >> grafana_dashboard
        
        lambda_function >> iam_role
        
        # Data flow annotations
        wearable_devices - Edge(label="Health Data", style="dashed") - data_collector
        health_apps - Edge(label="Activity Data", style="dashed") - data_collector
        external_apis - Edge(label="Medical Records", style="dashed") - data_collector
        
        bedrock_llm - Edge(label="Medical Reasoning", style="dashed") - health_analyzer
        health_analyzer - Edge(label="Analysis Results", style="dashed") - alert_system
        alert_system - Edge(label="Health Alerts", style="dashed") - sns_service


def create_data_flow_diagram():
    """
    Create data flow diagram for the health monitoring process
    """
    
    with Diagram("Health Monitoring Data Flow", 
                 filename="data_flow_diagram", 
                 show=False, 
                 direction="LR"):
        
        # Data Collection Phase
        with Cluster("Data Collection"):
            wearable_data = Mobile("Wearable\nData")
            app_data = Mobile("Health App\nData")
            external_data = Prometheus("External\nHealth APIs")
        
        # Processing Phase
        with Cluster("AI Processing"):
            data_collector = Lambda("Data\nCollector")
            health_analyzer = Lambda("Health\nAnalyzer")
            bedrock_reasoning = Bedrock("Medical\nReasoning")
        
        # Analysis Phase
        with Cluster("Analysis & Insights"):
            pattern_analysis = Lambda("Pattern\nAnalysis")
            risk_assessment = Lambda("Risk\nAssessment")
            recommendation_gen = Lambda("Recommendation\nGeneration")
        
        # Action Phase
        with Cluster("Actions & Notifications"):
            alert_generation = Lambda("Alert\nGeneration")
            notification_system = SNS("Notification\nSystem")
            health_dashboard = Grafana("Health\nDashboard")
        
        # Storage
        data_storage = S3("Health Data\nStorage")
        
        # Flow connections
        wearable_data >> data_collector
        app_data >> data_collector
        external_data >> data_collector
        
        data_collector >> health_analyzer
        health_analyzer >> bedrock_reasoning
        bedrock_reasoning >> pattern_analysis
        
        pattern_analysis >> risk_assessment
        risk_assessment >> recommendation_gen
        
        risk_assessment >> alert_generation
        alert_generation >> notification_system
        recommendation_gen >> health_dashboard
        
        data_collector >> data_storage
        health_analyzer >> data_storage


if __name__ == "__main__":
    print("Generating architecture diagrams...")
    create_architecture_diagram()
    create_data_flow_diagram()
    print("Architecture diagrams generated successfully!")
    print("Files created:")
    print("- architecture_diagram.png")
    print("- data_flow_diagram.png")
