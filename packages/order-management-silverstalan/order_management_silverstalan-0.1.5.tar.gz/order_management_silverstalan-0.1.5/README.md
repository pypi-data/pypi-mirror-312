

A comprehensive, object-oriented order management system using AWS services (DynamoDB, S3, and SNS).
The main controller that orchestrates all operations, handling the complete order lifecycle from creation to deletion.
Manages all database operations through an abstract interface, providing CRUD operations for orders in DynamoDB.
Abstract base class defining the contract for storage operations, enabling easy extension for different storage solutions.
Handles document storage and retrieval in AWS S3, maintaining order documents in JSON format.
Manages event notifications through AWS SNS, keeping all relevant parties informed about order status changes.
Object-oriented design with clear separation of concerns
- Order CRUD operations with DynamoDB storage
- Document storage in S3
- Event notifications via SNS
- Decimal and JSON encoding utilities
- Type hints and proper error handling
pip install order-management-silverstalan
Requirements

Python 3.8+
boto3
AWS credentials configured
AWS resources:

DynamoDB table
S3 bucket
SNS topic



Author
silverstalan
