# travel_budget/library

from decimal import Decimal
import boto3
from botocore.exceptions import ClientError
import requests
from django.http import JsonResponse


def calculate_user_balances(trip):
    """Calculate the balances for each user in a trip.
    Returns a dictionary mapping users to their balances."""
    balances = {user: Decimal('0') for user in trip.participants.all()}
    balances[trip.user] = Decimal('0')  # Include trip creator

    for expense in trip.expenses.all():
        payer = expense.paid_by
        balances[payer] += expense.amount

        split_amount = expense.amount / (expense.split_among.count() or 1)
        for participant in expense.split_among.all():
            if participant != payer:
                balances[participant] -= split_amount

    for payment in trip.payments.all():
        balances[payment.paid_by] += payment.amount
        balances[payment.paid_to] -= payment.amount

    return balances


def upload_to_s3(file, bucket_name, key, region='us-east-1'):
    """Upload a file to AWS S3."""
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.upload_fileobj(
            file, bucket_name, key,
            ExtraArgs={'ContentType': file.content_type}
        )
        return f"https://{bucket_name}.s3.{region}.amazonaws.com/{key}"
    except ClientError as e:
        raise Exception(f"Failed to upload to S3: {e}")


def make_api_request(url, method='GET', data=None, headers=None):
    """Make an HTTP request to an external API."""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")


def json_response(data, success=True, status=200):
    """Create a standardized JSON response."""
    return JsonResponse({
        'success': success,
        'data': data
         }, status=status)
