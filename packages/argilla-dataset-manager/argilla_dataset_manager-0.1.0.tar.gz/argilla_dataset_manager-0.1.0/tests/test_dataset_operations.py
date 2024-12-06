"""
Test script for dataset management operations.
"""

import sys
from pathlib import Path
import logging
import json
from datetime import datetime
import argilla as rg

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils import DatasetManager, get_argilla_client
from my_datasets import SettingsManager, create_qa_dataset_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use an existing workspace for testing
TEST_WORKSPACE = "qa_workspace"  # This workspace exists in your Argilla instance

def test_connection():
    """Test Argilla connection."""
    try:
        client = get_argilla_client()
        logger.info("✓ Successfully connected to Argilla")
        return client
    except Exception as e:
        logger.error(f"✗ Failed to connect to Argilla: {str(e)}")
        raise

def test_dataset_creation(client):
    """Test dataset creation with settings."""
    try:
        # Initialize managers
        dataset_manager = DatasetManager(client)
        
        # Create test settings
        test_name = f"test_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Basic settings for text classification
        settings = {
            'guidelines': 'Test dataset for QA classification',
            'labels': ['question', 'answer', 'other']
        }
        
        # Create dataset
        dataset = dataset_manager.create_dataset(
            workspace=TEST_WORKSPACE,
            dataset=test_name,
            settings=settings
        )
        
        logger.info(f"✓ Successfully created test dataset: {test_name}")
        return dataset
        
    except Exception as e:
        logger.error(f"✗ Failed to create dataset: {str(e)}")
        raise

def test_record_creation(dataset):
    """Test adding records to a dataset."""
    try:
        # Create a test record
        record = rg.Record(
            fields={
                "text": "What is Argilla?"
            }
        )
        
        # Add record to dataset
        dataset.records.log([record])
        logger.info("✓ Successfully added test record")
        
    except Exception as e:
        logger.error(f"✗ Failed to add record: {str(e)}")
        raise

def main():
    """Run all tests."""
    try:
        logger.info("Starting dataset operation tests...")
        
        # Test 1: Connection
        client = test_connection()
        
        # Test 2: Dataset Creation
        dataset = test_dataset_creation(client)
        
        # Test 3: Record Creation
        test_record_creation(dataset)
        
        logger.info("All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Tests failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 