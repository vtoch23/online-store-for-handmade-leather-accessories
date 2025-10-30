import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { CartItem } from '../models/cart.model';
import { Product } from '../models/product.model';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private cartItems = new BehaviorSubject<CartItem[]>([]);
  public cartItems$ = this.cartItems.asObservable();
  private currentUserEmail: string | null = null;

  constructor(private authService: AuthService) {
    // Load guest cart initially
    this.loadCart();

    // Subscribe to current user changes
    this.authService.currentUser$.subscribe(user => {
      const newUserEmail = user?.email || null;

      // If user just logged in (was guest, now has email)
      if (newUserEmail && !this.currentUserEmail) {
        this.mergeGuestCartWithUserCart(newUserEmail);
      }
      // If user logged out (had email, now null)
      else if (!newUserEmail && this.currentUserEmail) {
        this.currentUserEmail = null;
        this.loadCart();
      }
      // If user changed (different email)
      else if (newUserEmail !== this.currentUserEmail) {
        this.currentUserEmail = newUserEmail;
        this.loadCart();
      }
    });
  }

  addToCart(product: Product, quantity: number = 1): void {
    const currentCart = this.cartItems.value;
    const existingItem = currentCart.find(item => item.product.id === product.id);

    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      currentCart.push({ product, quantity });
    }

    this.updateCart(currentCart);
  }

  removeFromCart(productId: number): void {
    const currentCart = this.cartItems.value.filter(
      item => item.product.id !== productId
    );
    this.updateCart(currentCart);
  }

  updateQuantity(productId: number, quantity: number): void {
    const currentCart = this.cartItems.value;
    const item = currentCart.find(item => item.product.id === productId);

    if (item) {
      if (quantity <= 0) {
        this.removeFromCart(productId);
      } else {
        item.quantity = quantity;
        this.updateCart(currentCart);
      }
    }
  }

  clearCart(): void {
    this.updateCart([]);
  }

  getTotal(): number {
    return this.cartItems.value.reduce(
      (total, item) => total + item.product.price * item.quantity,
      0
    );
  }

  getItemCount(): number {
    return this.cartItems.value.reduce(
      (count, item) => count + item.quantity,
      0
    );
  }

  private updateCart(cart: CartItem[]): void {
    this.cartItems.next(cart);
    const cartKey = this.getCartKey();
    localStorage.setItem(cartKey, JSON.stringify(cart));
  }

  private loadCart(): void {
    const cartKey = this.getCartKey();
    const savedCart = localStorage.getItem(cartKey);
    if (savedCart) {
      this.cartItems.next(JSON.parse(savedCart));
    } else {
      this.cartItems.next([]);
    }
  }

  private getCartKey(): string {
    // If user is logged in, use their email as part of the key
    // Otherwise use a guest cart key
    return this.currentUserEmail ? `cart_${this.currentUserEmail}` : 'cart_guest';
  }

  private mergeGuestCartWithUserCart(userEmail: string): void {
    // Get guest cart
    const guestCart = localStorage.getItem('cart_guest');
    const guestItems: CartItem[] = guestCart ? JSON.parse(guestCart) : [];

    // Get user's existing cart
    const userCartKey = `cart_${userEmail}`;
    const userCart = localStorage.getItem(userCartKey);
    const userItems: CartItem[] = userCart ? JSON.parse(userCart) : [];

    // Merge: add guest items to user cart, combining quantities for duplicates
    const mergedCart = [...userItems];

    guestItems.forEach(guestItem => {
      const existingItem = mergedCart.find(item => item.product.id === guestItem.product.id);
      if (existingItem) {
        // Product already in user cart, add quantities
        existingItem.quantity += guestItem.quantity;
      } else {
        // New product, add to merged cart
        mergedCart.push(guestItem);
      }
    });

    // Update current user email and save merged cart
    this.currentUserEmail = userEmail;
    this.updateCart(mergedCart);

    // Clear guest cart
    localStorage.removeItem('cart_guest');
  }
}
