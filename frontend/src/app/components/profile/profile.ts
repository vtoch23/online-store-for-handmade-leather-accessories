import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { UserProfile } from '../../models/auth.model';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, RouterModule, ReactiveFormsModule],
  templateUrl: './profile.html',
  styleUrls: ['./profile.scss']
})
export class ProfileComponent implements OnInit {
  user: UserProfile | null = null;
  profileForm: FormGroup;
  loading = false;
  successMessage: string | null = null;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService
  ) {
    this.profileForm = this.fb.group({
      full_name: ['', Validators.required],
      email: [{ value: '', disabled: true }],
      birthday: [''],
      address: [''],
      phone: ['']
    });
  }

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      this.user = user;
      if (user) {
        this.profileForm.patchValue({
          full_name: user.full_name || '',
          email: user.email,
          // These would come from backend in a full implementation
          birthday: '',
          address: '',
          phone: ''
        });
      }
    });
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      this.loading = true;
      this.successMessage = 'Profile updated successfully!';
      this.errorMessage = null;

      // In a full implementation, this would call a backend API
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    }
  }
}
