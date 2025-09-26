"""
Deployment script for Smart Health Monitoring AI Agent
"""

import boto3
import json
import zipfile
import os
import time
from typing import Dict, Any

def create_deployment_package():
    """
    Create deployment package for Lambda function
    """
    print("Creating deployment package...")
    
    # Create zip file
    with zipfile.ZipFile('health_agent_deployment.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add main lambda function
        zipf.write('lambda_function.py')
        
        # Add requirements
        zipf.write('requirements.txt')
        
        # Add source code
        for root, dirs, files in os.walk('src'):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path)
        
        # Add README
        zipf.write('README.md')
    
    print("Deployment package created: health_agent_deployment.zip")
    return 'health_agent_deployment.zip'


def deploy_lambda_function(package_path: str, function_name: str = 'smart-health-monitoring-agent'):
    """
    Deploy Lambda function
    """
    print(f"Deploying Lambda function: {function_name}")
    
    lambda_client = boto3.client('lambda')
    
    try:
        # Read the deployment package
        with open(package_path, 'rb') as f:
            zip_content = f.read()
        
        # Create or update the function
        try:
            # Try to update existing function
            response = lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )
            print(f"Updated existing function: {response['FunctionName']}")
        except lambda_client.exceptions.ResourceNotFoundException:
            # Create new function
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.9',
                Role='arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role',  # Update with your role
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_content},
                Description='Smart Health Monitoring AI Agent',
                Timeout=300,
                MemorySize=512,
                Environment={
                    'Variables': {
                        'AWS_REGION': 'us-east-1'
                    }
                }
            )
            print(f"Created new function: {response['FunctionName']}")
        
        return response['FunctionArn']
    
    except Exception as e:
        print(f"Error deploying Lambda function: {str(e)}")
        return None


def create_api_gateway(api_name: str = 'health-monitoring-api'):
    """
    Create API Gateway for the health monitoring agent
    """
    print(f"Creating API Gateway: {api_name}")
    
    api_client = boto3.client('apigateway')
    
    try:
        # Create REST API
        response = api_client.create_rest_api(
            name=api_name,
            description='API for Smart Health Monitoring AI Agent',
            endpointConfiguration={
                'types': ['REGIONAL']
            }
        )
        
        api_id = response['id']
        print(f"Created API Gateway: {api_id}")
        
        # Get root resource
        resources = api_client.get_resources(restApiId=api_id)
        root_resource_id = resources['items'][0]['id']
        
        # Create resources and methods
        create_api_resources(api_client, api_id, root_resource_id)
        
        return api_id
    
    except Exception as e:
        print(f"Error creating API Gateway: {str(e)}")
        return None


def create_api_resources(api_client, api_id: str, root_resource_id: str):
    """
    Create API Gateway resources and methods
    """
    # Create /monitor resource
    monitor_resource = api_client.create_resource(
        restApiId=api_id,
        parentId=root_resource_id,
        pathPart='monitor'
    )
    
    # Create POST method for /monitor
    api_client.put_method(
        restApiId=api_id,
        resourceId=monitor_resource['id'],
        httpMethod='POST',
        authorizationType='NONE'
    )
    
    # Create /status/{user_id} resource
    status_resource = api_client.create_resource(
        restApiId=api_id,
        parentId=root_resource_id,
        pathPart='status'
    )
    
    user_id_resource = api_client.create_resource(
        restApiId=api_id,
        parentId=status_resource['id'],
        pathPart='{user_id}'
    )
    
    # Create GET method for /status/{user_id}
    api_client.put_method(
        restApiId=api_id,
        resourceId=user_id_resource['id'],
        httpMethod='GET',
        authorizationType='NONE'
    )
    
    # Create /emergency resource
    emergency_resource = api_client.create_resource(
        restApiId=api_id,
        parentId=root_resource_id,
        pathPart='emergency'
    )
    
    # Create POST method for /emergency
    api_client.put_method(
        restApiId=api_id,
        resourceId=emergency_resource['id'],
        httpMethod='POST',
        authorizationType='NONE'
    )
    
    print("API Gateway resources created successfully")


def create_s3_bucket(bucket_name: str = 'health-monitoring-data-bucket'):
    """
    Create S3 bucket for health data storage
    """
    print(f"Creating S3 bucket: {bucket_name}")
    
    s3_client = boto3.client('s3')
    
    try:
        # Create bucket
        s3_client.create_bucket(Bucket=bucket_name)
        
        # Enable versioning
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        
        # Enable encryption
        s3_client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    }
                ]
            }
        )
        
        print(f"S3 bucket created: {bucket_name}")
        return bucket_name
    
    except Exception as e:
        print(f"Error creating S3 bucket: {str(e)}")
        return None


def create_iam_role(role_name: str = 'health-monitoring-lambda-role'):
    """
    Create IAM role for Lambda function
    """
    print(f"Creating IAM role: {role_name}")
    
    iam_client = boto3.client('iam')
    
    # Trust policy for Lambda
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    # Permissions policy
    permissions_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject"
                ],
                "Resource": "arn:aws:s3:::health-monitoring-data-bucket/*"
            }
        ]
    }
    
    try:
        # Create role
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for Smart Health Monitoring AI Agent Lambda function'
        )
        
        # Attach permissions policy
        iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName='HealthMonitoringPermissions',
            PolicyDocument=json.dumps(permissions_policy)
        )
        
        print(f"IAM role created: {role_name}")
        return response['Role']['Arn']
    
    except Exception as e:
        print(f"Error creating IAM role: {str(e)}")
        return None


def main():
    """
    Main deployment function
    """
    print("Starting deployment of Smart Health Monitoring AI Agent...")
    
    # Create deployment package
    package_path = create_deployment_package()
    
    # Create IAM role
    role_arn = create_iam_role()
    
    # Create S3 bucket
    bucket_name = create_s3_bucket()
    
    # Deploy Lambda function
    function_arn = deploy_lambda_function(package_path)
    
    # Create API Gateway
    api_id = create_api_gateway()
    
    print("\nDeployment completed!")
    print(f"Lambda Function ARN: {function_arn}")
    print(f"API Gateway ID: {api_id}")
    print(f"S3 Bucket: {bucket_name}")
    print(f"IAM Role ARN: {role_arn}")
    
    # Clean up deployment package
    if os.path.exists(package_path):
        os.remove(package_path)
        print(f"Cleaned up deployment package: {package_path}")


if __name__ == "__main__":
    main()
