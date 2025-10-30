import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { OrderService, Order as ApiOrder } from '../../services/order.service';

interface Order {
  id: number;
  order_number: string;
  date: string;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  total: number;
  items: OrderItem[];
}

interface OrderItem {
  product_name: string;
  quantity: number;
  price: number;
  image_url?: string;
}

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './orders.html',
  styleUrl: './orders.scss',
})
export class OrdersComponent implements OnInit {
  orders: Order[] = [];
  loading = true;
  selectedOrder: Order | null = null;

  constructor(private orderService: OrderService) {}

  ngOnInit(): void {
    this.loadOrders();
  }

  loadOrders(): void {
    this.loading = true;
    this.orderService.getOrders().subscribe({
      next: (apiOrders: ApiOrder[]) => {
        // Transform API orders to component format
        this.orders = apiOrders.map(apiOrder => ({
          id: apiOrder.id,
          order_number: `ORD-${apiOrder.id.toString().padStart(6, '0')}`,
          date: apiOrder.created_at,
          status: apiOrder.status as 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled',
          total: apiOrder.total_amount,
          items: apiOrder.items.map(item => ({
            product_name: item.product_name,
            quantity: item.quantity,
            price: item.price_at_purchase,
            image_url: item.product_image_url || '/assets/placeholder.jpg'
          }))
        }));
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading orders:', error);
        this.loading = false;
      }
    });
  }

  getStatusColor(status: string): string {
    const colors: { [key: string]: string } = {
      'pending': 'bg-yellow-100 text-yellow-800',
      'processing': 'bg-blue-100 text-blue-800',
      'shipped': 'bg-purple-100 text-purple-800',
      'delivered': 'bg-green-100 text-green-800',
      'cancelled': 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-stone-100 text-stone-800';
  }

  getStatusText(status: string): string {
    return status.charAt(0).toUpperCase() + status.slice(1);
  }

  viewOrderDetails(order: Order): void {
    this.selectedOrder = order;
  }

  closeOrderDetails(): void {
    this.selectedOrder = null;
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  }
}
