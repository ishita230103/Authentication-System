import { Component } from '@angular/core';
import { AuthService } from './auth.service';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
})
export class AuthComponent {
  username: string = '';
  password: string = '';
  message: string = '';

  constructor(private authService: AuthService) {}

  register() {
    this.authService.register(this.username, this.password).subscribe(
      (response) => {
        this.message = 'Registration successful!';
      },
      (error) => {
        this.message = 'Registration failed!';
      }
    );
  }

  login() {
    this.authService.login(this.username, this.password).subscribe(
      (response) => {
        this.message = 'Login successful!';
      },
      (error) => {
        this.message = 'Login failed!';
      }
    );
  }
}
