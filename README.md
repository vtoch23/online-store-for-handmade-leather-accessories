# Handmade Leather Accessories Online Store

A full-stack e-commerce application for selling handmade leather accessories, built with FastAPI (Python), PostgreSQL, and Angular.

## Features

- **Product Catalog** - Browse handmade leather products by category
- **Shopping Cart** - Add, remove, and manage items in cart (stored in localStorage)
- **User Authentication** - Register, login, and secure JWT-based authentication
- **Secure Checkout** - Protected checkout process requiring authentication
- **Order Management** - Create and view orders with automatic stock management
- **Email Notifications** - Automatic order confirmation emails
- **Responsive Design** - Beautiful UI styled with Tailwind CSS
- **RESTful API** - Well-documented FastAPI backend with automatic OpenAPI docs
- **PostgreSQL Database** - Robust data storage with SQLAlchemy ORM
- **Docker Support** - Complete containerization for easy deployment

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **Angular 20** - Modern frontend framework with standalone components
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework for styling
- **RxJS** - Reactive programming for state management

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration and database
│   │   ├── models/       # Database models
│   │   └── schemas/      # Pydantic schemas
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/  # Angular components
│   │   │   ├── models/      # TypeScript interfaces
│   │   │   └── services/    # API and business logic services
│   │   └── environments/
│   └── Dockerfile
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Docker and Docker Compose (for containerized deployment)

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd online-store-for-handmade-leather-accessories
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Make sure PostgreSQL is running and create the database
# psql -U postgres
# CREATE DATABASE leather_store_db;
# CREATE USER leather_store WITH PASSWORD 'leather_store_password';
# GRANT ALL PRIVILEGES ON DATABASE leather_store_db TO leather_store;

# Seed the database with sample data
python seed_data.py

# Run the backend server on port 8001 (to avoid conflict with CryptoTracker)
uvicorn app.main:app --reload --port 8001
```

The backend will be available at [http://localhost:8001](http://localhost:8001)
- API documentation: [http://localhost:8001/docs](http://localhost:8001/docs)
- Alternative docs: [http://localhost:8001/redoc](http://localhost:8001/redoc)

#### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Run the development server
npm start
```

The frontend will be available at [http://localhost:4200](http://localhost:4200)

### Running with Docker

For a complete containerized setup:

```bash
# From project root
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5434
- Backend API on port 8001
- Frontend on port 8080

Access the application at [http://localhost](http://localhost)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive JWT token
- `GET /api/auth/me` - Get current user profile (requires auth)
- `POST /api/auth/logout` - Logout endpoint

### Products
- `GET /api/products` - Get all products (with optional category filter)
- `GET /api/products/{id}` - Get product by ID
- `POST /api/products` - Create a new product (admin only)
- `PUT /api/products/{id}` - Update a product (admin only)
- `DELETE /api/products/{id}` - Soft delete a product (admin only)

### Categories
- `GET /api/categories` - Get all categories
- `GET /api/categories/{id}` - Get category by ID
- `POST /api/categories` - Create a new category (admin only)

### Orders (Authentication Required)
- `GET /api/orders` - Get user's orders (or all if admin)
- `GET /api/orders/{id}` - Get order by ID (own orders only)
- `POST /api/orders` - Create a new order (sends email confirmation)

## Database Schema

### Tables
- **categories** - Product categories
- **products** - Product information
- **users** - Customer accounts
- **orders** - Customer orders
- **order_items** - Items in each order

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend Development

```bash
cd frontend
npm start
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:4200"]
ENVIRONMENT=development
```

## Sample Data

The database can be seeded with sample data using:

```bash
cd backend
python seed_data.py
```

This creates:
- 4 product categories (Wallets, Bags, Belts, Accessories)
- 8 sample products with realistic pricing and stock levels
- 1 demo user (email: demo@example.com, password: demo123)

Note: The password for the demo user is hashed using bcrypt.

## Deployment

### Production Considerations

1. **Environment Variables**: Update all secrets and passwords
2. **CORS**: Configure appropriate CORS origins
3. **Database**: Use a managed PostgreSQL service
4. **Static Files**: Configure proper static file serving
5. **HTTPS**: Set up SSL certificates
6. **Monitoring**: Add logging and monitoring tools

### Docker Production Build

```bash
docker-compose -f docker-compose.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

## Key Features Implemented

### Authentication & Security
- JWT-based authentication with secure password hashing (bcrypt)
- Protected routes with Angular route guards
- HTTP interceptor for automatic token injection
- User registration with email validation
- Secure login with proper error handling

### Email Notifications
- Order confirmation emails sent automatically after checkout
- Beautiful HTML email templates
- Development mode logs emails to console
- Production-ready SMTP configuration support

### Shopping Experience
- Real-time cart updates with localStorage persistence
- Category-based product filtering
- Stock management and validation
- Responsive design with Tailwind CSS
- User-friendly error messages

## Roadmap

- [x] User authentication and authorization
- [x] Email notifications for orders
- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Product reviews and ratings
- [ ] Admin dashboard for managing products
- [ ] Advanced inventory management
- [ ] Order status tracking and updates
- [ ] Wishlist functionality
- [ ] Product search and advanced filtering
- [ ] User profile management
