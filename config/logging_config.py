# config/logging_config.py
import logging
import os
from datetime import datetime

def setup_logging():
    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Create log filename with timestamp
    log_filename = f'logs/tiktok_scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)