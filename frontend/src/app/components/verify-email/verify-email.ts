import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-verify-email',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './verify-email.html',
  styleUrls: ['./verify-email.scss']
})
export class VerifyEmailComponent implements OnInit {
  verifying = true;
  success = false;
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit() {
    // Get token from query params
    this.route.queryParams.subscribe(params => {
      const token = params['token'];

      if (token) {
        this.verifyEmail(token);
      } else {
        this.verifying = false;
        this.errorMessage = 'Invalid verification link. No token provided.';
      }
    });
  }

  verifyEmail(token: string) {
    this.authService.verifyEmail(token).subscribe({
      next: (response) => {
        this.verifying = false;
        this.success = true;

        // Redirect to login after 3 seconds
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 3000);
      },
      error: (error) => {
        this.verifying = false;
        this.success = false;
        this.errorMessage = error.error?.detail || 'Email verification failed. Please try again.';
      }
    });
  }

  goToLogin() {
    this.router.navigate(['/login']);
  }
}
