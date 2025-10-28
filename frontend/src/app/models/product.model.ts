export interface Product {
  id: number;
  name: string;
  description: string | null;
  price: number;
  stock_quantity: number;
  image_url: string | null;
  is_active: boolean;
  category_id: number | null;
  sku: string;
  created_at: string;
  updated_at: string | null;
}

export interface ProductCreate {
  name: string;
  description?: string;
  price: number;
  stock_quantity: number;
  image_url?: string;
  is_active: boolean;
  category_id?: number;
  sku: string;
}
