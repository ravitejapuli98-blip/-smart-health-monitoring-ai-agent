"""
Create deployment package for AWS Lambda
Includes all necessary files and dependencies
"""

import zipfile
import os
import shutil
from pathlib import Path

def create_deployment_package():
    """
    Create a clean deployment package for AWS Lambda
    """
    print("Creating deployment package...")
    
    # Create temporary directory for packaging
    temp_dir = "deployment_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Copy main lambda function
        shutil.copy2("lambda_function.py", temp_dir)
        
        # Copy source code
        shutil.copytree("src", os.path.join(temp_dir, "src"))
        
        # Copy requirements
        shutil.copy2("requirements.txt", temp_dir)
        
        # Create zip file
        zip_filename = "health_monitoring_agent_deployment.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"Deployment package created: {zip_filename}")
        
        # Get file size
        file_size = os.path.getsize(zip_filename)
        print(f"Package size: {file_size / 1024 / 1024:.2f} MB")
        
        return zip_filename
        
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print("Cleaned up temporary files")

if __name__ == "__main__":
    create_deployment_package()
