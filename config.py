"""
Configuration file for Automata Compiler API

This file contains configuration settings for different environments.
"""

import os
from pathlib import Path


class Config:
    """Base configuration class."""
    
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'automata-compiler-secret-key-2024'
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024  # 16KB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Compilation configuration
    MAX_SOURCE_LENGTH = 10000  # 10KB source code limit
    COMPILATION_TIMEOUT = 30   # 30 seconds compilation timeout
    
    # API configuration
    API_TITLE = "Automata Compiler API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "REST API for compiling Automata Language (.af) code"
    
    # Paths
    BASE_DIR = Path(__file__).parent
    SRC_DIR = BASE_DIR / 'src'
    EXAMPLES_DIR = BASE_DIR / 'examples'
    TEMP_DIR = BASE_DIR / 'temp'


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    FLASK_ENV = 'development'
    
    # Enable detailed error messages in development
    EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Security headers
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year cache for static files
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'automata_compiler.log'


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    DEBUG = True
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default']) 