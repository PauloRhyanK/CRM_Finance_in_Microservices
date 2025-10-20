class Config:
    """Configuration settings for the API gateway."""
    
    # Service URLs
    AUTH_SERVICE_URL = "http://auth-service:5000"
    USER_SERVICE_URL = "http://user-service:5000"
    PRODUCT_SERVICE_URL = "http://product-service:5000"
    ORDER_SERVICE_URL = "http://order-service:5000"
    
    # Other configuration settings
    DEBUG = True
    ENV = "development"