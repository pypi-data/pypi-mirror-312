# aws_hotel_helpers/core.py

import boto3
from botocore.exceptions import ClientError
import logging
import json
from .exceptions import AWSHelperException
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class AWSHelper:
    def __init__(self, region_name='us-east-1', credentials=None, settings=None):
        """
        Initialize AWS Helper
        
        Args:
            region_name: AWS region
            credentials: Optional AWS credentials dict
            settings: Optional settings object for configuration
        """
        self.region_name = region_name
        self._session = None
        self.settings = settings
        self._initialize_session(credentials)
        
        # Try to load Lambda config
        try:
            with open('lambda_config.json', 'r') as f:
                self.lambda_config = json.load(f)
        except FileNotFoundError:
            logger.warning("Lambda config file not found")
            self.lambda_config = None
        
        # Set up configuration values from settings if provided
        if settings:
            self.sns_topic_arn = getattr(settings, 'AWS_SNS_TOPIC_ARN', None)
            self.sqs_queue_url = getattr(settings, 'AWS_SQS_QUEUE_URL', None)
            self.bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
        else:
            self.sns_topic_arn = None
            self.sqs_queue_url = None
            self.bucket_name = None

    def _initialize_session(self, credentials):
        """Initialize the AWS session and clients"""
        try:
            if credentials:
                self._session = boto3.Session(
                    aws_access_key_id=credentials.get('aws_access_key_id'),
                    aws_secret_access_key=credentials.get('aws_secret_access_key'),
                    aws_session_token=credentials.get('aws_session_token'),
                    region_name=self.region_name
                )
            else:
                self._session = boto3.Session(region_name=self.region_name)
            
            # Log credentials being used (masked for security)
            creds = self._session.get_credentials()
            logger.info(f"Using credentials with access key: {creds.access_key[:10]}...")
            
            # Initialize clients
            self.s3_client = self._session.client('s3')
            self.sns = self._session.client('sns')
            self.sqs = self._session.client('sqs')
            self.dynamodb = self._session.client('dynamodb')
            self.ses = self._session.client('ses')
            
        except Exception as e:
            raise AWSHelperException(f"Failed to initialize AWS session: {str(e)}")

    def upload_to_s3(self, file_obj, key, bucket_name=None, content_type=None):
        """Upload file to S3"""
        try:
            if hasattr(file_obj, 'seek'):
                file_obj.seek(0)
            
            bucket = bucket_name or self.bucket_name
            if not bucket:
                raise AWSHelperException("No bucket name provided")
            
            content_type = content_type or getattr(file_obj, 'content_type', 'image/jpeg')
            logger.info(f"Uploading to S3: {key} ({content_type})")
            
            self.s3_client.upload_fileobj(
                file_obj,
                bucket,
                key,
                ExtraArgs={'ContentType': content_type}
            )
            
            # Verify upload
            self.s3_client.head_object(Bucket=bucket, Key=key)
            
            # Generate URL
            url = self.get_presigned_url(key, bucket)
            logger.info(f"File uploaded successfully. URL: {url}")
            return url
            
        except Exception as e:
            raise AWSHelperException(f"Failed to upload to S3: {str(e)}")

    def get_presigned_url(self, key, bucket_name=None, expiration=3600):
        """Generate a presigned URL for an S3 object"""
        try:
            bucket = bucket_name or self.bucket_name
            if not bucket:
                raise AWSHelperException("No bucket name provided")
                
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket,
                    'Key': key
                },
                ExpiresIn=expiration
            )
            logger.info(f"Generated presigned URL for key: {key}")
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            return None

    def get_image_url(self, image_key, width=None, height=None):
        """Get image URL through Lambda with S3 presigned URL"""
        try:
            if not self.lambda_config or 'api_url' not in self.lambda_config:
                logger.warning("Lambda configuration not found, falling back to direct S3")
                return self.get_presigned_url(image_key)
            
            # Generate a presigned URL for Lambda to access S3
            presigned_url = self.get_presigned_url(image_key)
            if not presigned_url:
                return None
            
            # Create Lambda API URL
            base_url = f"{self.lambda_config['api_url']}?url={presigned_url}"
            if width:
                base_url += f"&width={width}"
            if height:
                base_url += f"&height={height}"
            
            logger.info(f"Generated Lambda URL for image processing: {base_url}")
            return base_url
            
        except Exception as e:
            logger.error(f"Error generating image URL: {str(e)}")
            return None

    def send_booking_confirmation(self, booking_data):
        """Send booking confirmation via SNS and email"""
        try:
            user_email = booking_data['user_email']
            logger.info(f"Sending confirmation to: {user_email}")
            
            message = f"""
            Booking Confirmation
            
            Thank you for booking with LuxStay!
            
            Booking Details:
            Hotel: {booking_data['hotel_name']}
            Room: {booking_data.get('room_type', 'Standard Room')}
            Check-in: {booking_data['check_in']}
            Check-out: {booking_data['check_out']}
            Total Price: ${booking_data['total_price']}
            
            Booking Reference: {booking_data['booking_id']}
            
            Thank you for choosing LuxStay!
            """
            
            # Publish to SNS
            if self.sns_topic_arn:
                self.sns.publish(
                    TopicArn=self.sns_topic_arn,
                    Message=message,
                    Subject='LuxStay Booking Confirmation'
                )
                logger.info("Published SNS message")
            
            # Send via SES
            self.send_email_notification(
                user_email,
                'LuxStay Booking Confirmation',
                message
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending booking confirmation: {str(e)}")
            return False

    def send_email_notification(self, email, subject, message, sender_email=None):
        """Send email via SES"""
        try:
            self.ses.send_email(
                Source=sender_email or 'noreply@yourdomain.com',
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': message}}
                }
            )
            logger.info(f"Email sent to {email}")
            return True
        except Exception as e:
            raise AWSHelperException(f"Failed to send email: {str(e)}")

    def send_to_sqs(self, queue_url, message_body):
        """Send message to SQS queue"""
        try:
            response = self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_body)
            )
            return response['MessageId']
        except Exception as e:
            raise AWSHelperException(f"Failed to send SQS message: {str(e)}")

    def receive_from_sqs(self, queue_url, max_messages=10):
        """Receive messages from SQS queue"""
        try:
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=5
            )
            return response.get('Messages', [])
        except Exception as e:
            raise AWSHelperException(f"Failed to receive SQS messages: {str(e)}")

    def save_to_dynamodb(self, table_name, item):
        """Save item to DynamoDB table"""
        try:
            self.dynamodb.put_item(
                TableName=table_name,
                Item=item
            )
            return True
        except Exception as e:
            raise AWSHelperException(f"Failed to save to DynamoDB: {str(e)}")
