from order_management_pkg.processor import OrderProcessor

# Initialize the processor
processor = OrderProcessor('test-table', 'test-bucket', 'test-topic')

# Test creating an order
test_order = {
    'order_id': 'TEST001',
    'customer_id': 'CUST001',
    'total_amount': 99.99,
    'status': 'PENDING'
}

try:
    print("Testing Order Management Library...")
    print("Initializing OrderProcessor...")
    print(f"Processor initialized successfully with table: test-table")
    
except Exception as e:
    print(f"Error: {str(e)}")
