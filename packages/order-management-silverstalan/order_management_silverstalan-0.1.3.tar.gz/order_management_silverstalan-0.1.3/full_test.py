from order_management_pkg.processor import OrderProcessor
from decimal import Decimal

def test_order_management():
    # Initialize with actual resource names
    processor = OrderProcessor(
        table_name='orders-table',
        bucket_name='order-docs-bucket-silverstalan',  # Update with your bucket name
        topic_arn='arn:aws:sns:us-east-1:975050073542:order-notifications'  # Will replace this with actual ARN
    )

    # Test 1: Create an order
    print("\n1. Testing Order Creation...")
    test_order = {
        'order_id': 'TEST001',
        'customer_id': 'CUST001',
        'total_amount': Decimal('99.99'),
        'status': 'PENDING'
    }
    
    try:
        result = processor.create_order(test_order)
        print("✓ Order created successfully")
        print(f"Order details: {result}")
    except Exception as e:
        print(f"✗ Error creating order: {str(e)}")

    # Test 2: Get the order
    print("\n2. Testing Order Retrieval...")
    try:
        order = processor.get_order('TEST001')
        print("✓ Order retrieved successfully")
        print(f"Retrieved order: {order}")
    except Exception as e:
        print(f"✗ Error retrieving order: {str(e)}")

    # Test 3: Update order status
    print("\n3. Testing Order Status Update...")
    try:
        updated_order = processor.update_status('TEST001', 'PROCESSING')
        print("✓ Order status updated successfully")
        print(f"Updated order: {updated_order}")
    except Exception as e:
        print(f"✗ Error updating order status: {str(e)}")

    # Test 4: List all orders
    print("\n4. Testing Order Listing...")
    try:
        orders = processor.list_orders()
        print("✓ Orders listed successfully")
        print(f"Total orders: {len(orders)}")
    except Exception as e:
        print(f"✗ Error listing orders: {str(e)}")

    # Test 5: Delete the order
    print("\n5. Testing Order Deletion...")
    try:
        processor.delete_order('TEST001')
        print("✓ Order deleted successfully")
    except Exception as e:
        print(f"✗ Error deleting order: {str(e)}")

if __name__ == "__main__":
    print("Starting Order Management System Tests...")
    test_order_management()
    print("\nTests completed!")
