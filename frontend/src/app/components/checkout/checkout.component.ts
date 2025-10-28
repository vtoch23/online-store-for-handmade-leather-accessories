import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { CartService } from '../../services/cart.service';
import { CartItem } from '../../models/cart.model';
import { OrderCreate, OrderItemCreate } from '../../models/order.model';

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss']
})
export class CheckoutComponent implements OnInit {
  checkoutForm!: FormGroup;
  cartItems: CartItem[] = [];
  total = 0;
  submitting = false;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private cartService: CartService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cartService.cartItems$.subscribe(items => {
      this.cartItems = items;
      this.total = this.cartService.getTotal();

      if (items.length === 0) {
        this.router.navigate(['/']);
      }
    });

    this.checkoutForm = this.fb.group({
      fullName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      address: ['', Validators.required],
      city: ['', Validators.required],
      postalCode: ['', Validators.required],
      country: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.checkoutForm.valid && !this.submitting) {
      this.submitting = true;
      this.error = null;

      const formValue = this.checkoutForm.value;
      const shippingAddress = `${formValue.address}, ${formValue.city}, ${formValue.postalCode}, ${formValue.country}`;

      const orderItems: OrderItemCreate[] = this.cartItems.map(item => ({
        product_id: item.product.id,
        quantity: item.quantity
      }));

      const order: OrderCreate = {
        shipping_address: shippingAddress,
        items: orderItems
      };

      // The backend will get the user from the JWT token
      this.apiService.createOrder(order).subscribe({
        next: (createdOrder) => {
          this.cartService.clearCart();
          this.router.navigate(['/'], {
            queryParams: { orderSuccess: createdOrder.id }
          });
        },
        error: (err) => {
          console.error('Error creating order:', err);
          this.error = err.error?.detail || 'Failed to create order. Please try again.';
          this.submitting = false;
        }
      });
    }
  }
}
