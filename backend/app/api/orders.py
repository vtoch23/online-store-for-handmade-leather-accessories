from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_user, get_optional_current_user
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import Order as OrderSchema, OrderCreate
from app.services.email import send_order_confirmation_email

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=List[OrderSchema])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all orders for the current user (or all if admin)."""
    query = db.query(Order)

    # Regular users can only see their own orders
    if not current_user.is_admin:
        query = query.filter(Order.user_id == current_user.id)

    orders = query.offset(skip).limit(limit).all()

    # Enrich order items with product details
    for order in orders:
        for item in order.items:
            if item.product:
                item.product_name = item.product.name
                item.product_image_url = item.product.image_url

    return orders


@router.get("/{order_id}", response_model=OrderSchema)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Regular users can only see their own orders
    if not current_user.is_admin and order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )

    return order


@router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new order."""
    # Calculate total and validate products
    total_amount = 0
    order_items = []

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found"
            )

        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )

        item_total = product.price * item.quantity
        total_amount += item_total

        order_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price_at_purchase": product.price
        })

        # Update stock
        product.stock_quantity -= item.quantity

    # Create order
    db_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        shipping_address=order.shipping_address
    )
    db.add(db_order)
    db.flush()  # Get the order ID

    # Create order items
    for item_data in order_items:
        db_item = OrderItem(order_id=db_order.id, **item_data)
        db.add(db_item)

    db.commit()
    db.refresh(db_order)

    # Send order confirmation email in background
    background_tasks.add_task(
        send_order_confirmation_email,
        email=current_user.email,
        order_id=db_order.id,
        total_amount=total_amount,
        customer_name=current_user.full_name or current_user.email
    )

    return db_order
