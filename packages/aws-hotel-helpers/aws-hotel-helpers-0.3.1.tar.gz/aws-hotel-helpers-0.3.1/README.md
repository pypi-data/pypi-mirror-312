# AWS Hotel Helpers

A Python library that simplifies AWS operations for hotel management systems. This package provides easy-to-use helpers for S3 file storage, SNS notifications, and other AWS services commonly used in hotel management applications.

## Installation

Install the package using pip:

```bash
pip install aws-hotel-helpers
```

## Quick Start

Here's a simple example of how to use the package:

```python
from aws_hotel_helpers import AWSHelper

# Initialize the helper
aws_helper = AWSHelper(region_name='us-east-1')

# Upload an image to S3
try:
    image_url = aws_helper.upload_image(
        image_file,
        bucket_name='my-hotel-images'
    )
    print(f"Image uploaded successfully: {image_url}")
except Exception as e:
    print(f"Error uploading image: {str(e)}")

# Send a booking notification
booking_data = {
    'booking_id': '12345',
    'user_email': 'guest@example.com',
    'hotel_name': 'Luxury Hotel',
    'check_in': '2024-04-01',
    'check_out': '2024-04-05',
    'total_price': '500.00'
}

aws_helper.send_booking_notification(
    'arn:aws:sns:us-east-1:123456789012:BookingNotifications',
    booking_data
)
```

## Features

- Simple S3 file upload with automatic content type detection
- SNS notification sending for booking confirmations
- Automatic credential management
- Comprehensive error handling

## Documentation

For more detailed documentation and examples, visit our [GitHub repository](https://github.com/yourusername/aws-hotel-helpers).

## License

This project is licensed under the MIT License - see the LICENSE file for details.