import boto3
import uuid
from exception import AWSDDBException


def put_item(coin_type, compare_type, diff, start, end):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('Platform.Price.Diff')
    try:
        response = table.put_item(
            Item = {
                'ID': str(uuid.uuid4()),
                'CoinType': coin_type,
                'CompareType': compare_type,
                'DifferencePercentage': diff,
                'StartTime': start,
                'EndTime': end
            }
        )
    except:
        raise AWSDDBException("Failed to put item into ddb table")

