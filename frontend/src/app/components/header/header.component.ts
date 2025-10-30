import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CartService } from '../../services/cart.service';
import { AuthService } from '../../services/auth.service';
import { Observable } from 'rxjs';
import { UserProfile } from '../../models/auth.model';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  cartItemCount$!: Observable<number>;
  currentUser$!: Observable<UserProfile | null>;
  isProfileDropdownOpen = false;

  constructor(
    private cartService: CartService,
    public authService: AuthService
  ) {}

  ngOnInit(): void {
    this.cartItemCount$ = new Observable(observer => {
      this.cartService.cartItems$.subscribe(() => {
        observer.next(this.cartService.getItemCount());
      });
    });

    this.currentUser$ = this.authService.currentUser$;
  }

  toggleProfileDropdown(): void {
    this.isProfileDropdownOpen = !this.isProfileDropdownOpen;
  }

  closeDropdown(): void {
    this.isProfileDropdownOpen = false;
  }

  logout(): void {
    this.authService.logout();
    this.closeDropdown();
  }
}
