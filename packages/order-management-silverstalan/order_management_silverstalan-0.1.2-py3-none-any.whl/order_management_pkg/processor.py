# functions/order-service/order_management/processor.py

import json
import boto3
import os
from decimal import Decimal
from datetime import datetime
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

class OrderError(Exception):
    """Base class for Order exceptions"""
    pass

class OrderNotFoundError(OrderError):
    """Raised when order is not found"""
    pass

class DocumentNotFoundError(OrderError):
    """Raised when document is not found"""
    pass

class BaseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(str(obj))  # Convert Decimal to float
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(BaseEncoder, self).default(obj)

class DecimalEncoder:
    @staticmethod
    def encode(obj):
        if isinstance(obj, Decimal):
            return float(str(obj))
        if isinstance(obj, dict):
            return {k: DecimalEncoder.encode(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [DecimalEncoder.encode(v) for v in obj]
        return obj

class StorageHandler(ABC):
    """Abstract base class for storage operations"""
    
    @abstractmethod
    def save(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get(self, id: str) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def update(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def delete(self, id: str) -> None:
        pass
    
    @abstractmethod
    def list_all(self) -> List[Dict[str, Any]]:
        pass

class DynamoDBHandler(StorageHandler):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        print(f"Initialized DynamoDB handler for table: {table_name}")
    
    def save(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Saving item to DynamoDB: {data['order_id']}")
        self.table.put_item(Item=data)
        return DecimalEncoder.encode(data)
    
    def get(self, id: str) -> Optional[Dict[str, Any]]:
        print(f"Getting item from DynamoDB: {id}")
        response = self.table.get_item(Key={'order_id': id})
        item = response.get('Item')
        return DecimalEncoder.encode(item) if item else None
    
    def update(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Updating item in DynamoDB: {id}")
        update_expression = "SET #status = :status, updated_at = :time"
        expression_values = {
            ':status': data['status'],
            ':time': datetime.utcnow().isoformat()
        }
        attr_names = {'#status': 'status'}
        
        response = self.table.update_item(
            Key={'order_id': id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=attr_names,
            ReturnValues='ALL_NEW'
        )
        return DecimalEncoder.encode(response['Attributes'])
    
    def delete(self, id: str) -> None:
        print(f"Deleting item from DynamoDB: {id}")
        self.table.delete_item(Key={'order_id': id})
    
    def list_all(self) -> List[Dict[str, Any]]:
        print("Scanning all items from DynamoDB")
        response = self.table.scan()
        items = response.get('Items', [])
        return [DecimalEncoder.encode(item) for item in items]

class S3DocumentHandler:
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client('s3')
        self.bucket = bucket_name
        print(f"Initialized S3 document handler for bucket: {bucket_name}")
    
    def store_document(self, order_id: str, document: Dict[str, Any]) -> str:
        key = f"orders/{order_id}/order.json"
        try:
            print(f"Storing document in S3: {key}")
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=json.dumps(document, cls=BaseEncoder),
                ContentType='application/json'
            )
            print(f"Successfully stored document in S3: {key}")
            return key
        except Exception as e:
            print(f"Error storing document in S3: {str(e)}")
            raise
    
    def get_document(self, order_id: str) -> Dict[str, Any]:
        key = f"orders/{order_id}/order.json"
        try:
            print(f"Getting document from S3: {key}")
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
            return json.loads(response['Body'].read())
        except self.s3.exceptions.NoSuchKey:
            print(f"Document not found in S3: {key}")
            raise DocumentNotFoundError(f"Document not found for order {order_id}")
        except Exception as e:
            print(f"Error getting document from S3: {str(e)}")
            raise

    def delete_document(self, order_id: str) -> None:
        """Delete order document from S3"""
        key = f"orders/{order_id}/order.json"
        try:
            print(f"Attempting to delete document from S3: {key}")
            self.s3.delete_object(
                Bucket=self.bucket,
                Key=key
            )
            # Verify deletion
            try:
                self.s3.head_object(Bucket=self.bucket, Key=key)
                raise Exception(f"Document still exists after deletion: {key}")
            except self.s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == '404':
                    print(f"Successfully deleted document from S3: {key}")
                else:
                    raise
        except Exception as e:
            print(f"Error deleting document from S3: {str(e)}")
            raise

class NotificationService:
    def __init__(self, topic_arn: str):
        self.sns = boto3.client('sns')
        self.topic_arn = topic_arn
        print(f"Initialized SNS notification service for topic: {topic_arn}")
    
    def send_notification(self, event_type: str, data: Dict[str, Any]) -> None:
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            
            message = f"""
Order Event: {event_type}
Time: {timestamp}
Order ID: {data.get('order_id')}
Status: {data.get('status', 'N/A')}
------------------------
Details: {json.dumps(data, indent=2)}
"""
            
            print(f"Sending SNS notification for event: {event_type}")
            response = self.sns.publish(
                TopicArn=self.topic_arn,
                Message=message,
                Subject=f"Order System Notification: {event_type}",
                MessageAttributes={
                    'event_type': {
                        'DataType': 'String',
                        'StringValue': event_type
                    }
                }
            )
            print(f"Successfully sent notification: {event_type}, MessageId: {response.get('MessageId')}")
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            raise

class OrderProcessor:
    def __init__(self, table_name: str, bucket_name: str, topic_arn: str):
        print(f"Initializing OrderProcessor with table: {table_name}, bucket: {bucket_name}, topic: {topic_arn}")
        self.db_handler = DynamoDBHandler(table_name)
        self.doc_handler = S3DocumentHandler(bucket_name)
        self.notification_service = NotificationService(topic_arn)
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new order"""
        try:
            print(f"Creating new order: {order_data['order_id']}")
            
            # Save to DynamoDB
            saved_order = self.db_handler.save(order_data)
            
            # Store document in S3
            document_key = self.doc_handler.store_document(order_data['order_id'], saved_order)
            
            # Send notification
            self.notification_service.send_notification('ORDER_CREATED', {
                'order_id': order_data['order_id'],
                'document_key': document_key,
                'status': 'PENDING',
                'customer_id': order_data['customer_id'],
                'total_amount': str(order_data['total_amount'])
            })
            
            print(f"Successfully created order: {order_data['order_id']}")
            return saved_order
            
        except Exception as e:
            print(f"Error in create_order: {str(e)}")
            raise
    
    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get order by ID"""
        try:
            print(f"Getting order: {order_id}")
            return self.db_handler.get(order_id)
        except Exception as e:
            print(f"Error getting order: {str(e)}")
            raise
    
    def update_status(self, order_id: str, status: str) -> Dict[str, Any]:
        """Update order status"""
        try:
            print(f"Updating order status: {order_id} to {status}")
            order = self.db_handler.get(order_id)
            if not order:
                raise OrderNotFoundError(f"Order {order_id} not found")
            
            updated_order = self.db_handler.update(order_id, {'status': status})
            
            # Update document in S3
            document_key = self.doc_handler.store_document(order_id, updated_order)
            
            # Send notification
            self.notification_service.send_notification('STATUS_UPDATED', {
                'order_id': order_id,
                'status': status,
                'document_key': document_key,
                'customer_id': updated_order['customer_id'],
                'previous_status': order['status']
            })
            
            print(f"Successfully updated order status: {order_id} to {status}")
            return updated_order
            
        except OrderNotFoundError:
            raise
        except Exception as e:
            print(f"Error updating status: {str(e)}")
            raise
    
    def delete_order(self, order_id: str) -> None:
        """Delete order and associated documents"""
        try:
            print(f"Starting deletion process for order: {order_id}")
            
            # Get order details before deletion
            order = self.db_handler.get(order_id)
            if not order:
                raise OrderNotFoundError(f"Order {order_id} not found")
            
            # Delete from S3 first
            print(f"Deleting S3 document for order: {order_id}")
            self.doc_handler.delete_document(order_id)
            
            # Delete from DynamoDB
            print(f"Deleting from DynamoDB: {order_id}")
            self.db_handler.delete(order_id)
            
            # Send notification
            self.notification_service.send_notification('ORDER_DELETED', {
                'order_id': order_id,
                'customer_id': order['customer_id'],
                'status': 'DELETED',
                'previous_status': order['status']
            })
            
            print(f"Successfully deleted order: {order_id}")
            
        except OrderNotFoundError:
            raise
        except Exception as e:
            print(f"Error deleting order: {str(e)}")
            raise
    
    def list_orders(self) -> List[Dict[str, Any]]:
        """List all orders"""
        try:
            print("Retrieving all orders")
            orders = self.db_handler.list_all()
            print(f"Successfully retrieved {len(orders)} orders")
            return orders
        except Exception as e:
            print(f"Error listing orders: {str(e)}")
            raise