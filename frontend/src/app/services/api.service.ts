import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Product } from '../models/product.model';
import { Category } from '../models/category.model';
import { Order, OrderCreate } from '../models/order.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Product endpoints
  getProducts(categoryId?: number, skip = 0, limit = 100): Observable<Product[]> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    if (categoryId) {
      params = params.set('category_id', categoryId.toString());
    }

    return this.http.get<Product[]>(`${this.baseUrl}/products`, { params });
  }

  getProduct(id: number): Observable<Product> {
    return this.http.get<Product>(`${this.baseUrl}/products/${id}`);
  }

  // Category endpoints
  getCategories(skip = 0, limit = 100): Observable<Category[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    return this.http.get<Category[]>(`${this.baseUrl}/categories`, { params });
  }

  getCategory(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.baseUrl}/categories/${id}`);
  }

  // Order endpoints
  createOrder(order: OrderCreate): Observable<Order> {
    return this.http.post<Order>(`${this.baseUrl}/orders`, order);
  }

  getOrders(userId?: number, skip = 0, limit = 100): Observable<Order[]> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    if (userId) {
      params = params.set('user_id', userId.toString());
    }

    return this.http.get<Order[]>(`${this.baseUrl}/orders`, { params });
  }

  getOrder(id: number): Observable<Order> {
    return this.http.get<Order>(`${this.baseUrl}/orders/${id}`);
  }
}
