"""
AWS Lambda function for Smart Health Monitoring AI Agent
"""

import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

# Import our agent components
from src.agent.core.health_agent import SmartHealthMonitoringAgent

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the health agent
health_agent = SmartHealthMonitoringAgent()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for health monitoring agent
    """
    try:
        # Parse the event
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        body = event.get('body', '{}')
        
        # Parse body if it's a string
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                body = {}
        
        # Route the request
        if http_method == 'POST' and path == '/monitor':
            return asyncio.run(handle_start_monitoring(body))
        elif http_method == 'GET' and path.startswith('/status/'):
            user_id = path.split('/')[-1]
            return asyncio.run(handle_get_status(user_id))
        elif http_method == 'POST' and path == '/emergency':
            return asyncio.run(handle_emergency_alert(body))
        elif http_method == 'GET' and path == '/agent/status':
            return asyncio.run(handle_agent_status())
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                },
                'body': json.dumps({'error': 'Endpoint not found'})
            }
    
    except Exception as e:
        logger.error(f"Error in lambda handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }


async def handle_start_monitoring(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle start monitoring request
    """
    try:
        user_id = body.get('user_id')
        monitoring_config = body.get('monitoring_config', {})
        
        if not user_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'user_id is required'})
            }
        
        # Start autonomous monitoring
        result = await health_agent.start_autonomous_monitoring(user_id, monitoring_config)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
    
    except Exception as e:
        logger.error(f"Error in start monitoring: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }


async def handle_get_status(user_id: str) -> Dict[str, Any]:
    """
    Handle get status request
    """
    try:
        # Get user's monitoring status
        # This would typically query a database for user status
        status = {
            'user_id': user_id,
            'monitoring_active': True,
            'last_check': datetime.utcnow().isoformat(),
            'health_status': 'stable',
            'active_alerts': 0
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(status)
        }
    
    except Exception as e:
        logger.error(f"Error in get status: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }


async def handle_emergency_alert(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle emergency alert request
    """
    try:
        user_id = body.get('user_id')
        alert_data = body.get('alert_data', {})
        
        if not user_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'user_id is required'})
            }
        
        # Handle emergency alert
        result = await health_agent.handle_emergency_alert(user_id, alert_data)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
    
    except Exception as e:
        logger.error(f"Error in emergency alert: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }


async def handle_agent_status() -> Dict[str, Any]:
    """
    Handle agent status request
    """
    try:
        status = await health_agent.get_agent_status()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(status)
        }
    
    except Exception as e:
        logger.error(f"Error in agent status: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
