# aws_hotel_helpers/exceptions.py

class AWSHelperException(Exception):
    """Base exception for AWS Helper errors"""
    pass

class CredentialsError(AWSHelperException):
    """Raised when there are issues with AWS credentials"""
    pass

class S3Error(AWSHelperException):
    """Raised when S3 operations fail"""
    pass

class SNSError(AWSHelperException):
    """Raised when SNS operations fail"""
    pass

class SQSError(AWSHelperException):
    """Raised when SQS operations fail"""
    pass