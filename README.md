# E-Commerce Platform – Handmade Leather Accessories

Full-stack e-commerce application built to simulate a real-world online store with product management, authentication, and order processing.

## Overview
This project was built to demonstrate a complete Angular + backend workflow, including authentication, REST APIs, and containerised deployment. It focuses on clean architecture, realistic business logic, and maintainable frontend state management.

## Tech Stack

**Frontend**
- Angular 20 (standalone components)
- TypeScript
- RxJS
- Tailwind CSS
- Angular Router, HTTP Interceptors

**Backend**
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT authentication

**Infrastructure**
- Docker
- Docker Compose

## Key Features
- Product catalog with categories
- Shopping cart with local persistence
- Secure checkout flow
- JWT-based authentication
- Order and stock management
- Protected routes and API endpoints

## Architecture & Design
- RESTful API with automatic OpenAPI documentation
- Normalised PostgreSQL schema (products, users, orders, order items)
- Angular route guards for protected pages
- HTTP interceptors for token injection
- RxJS used for reactive data flows

## Testing
- API validation via Pydantic
- Manual API testing with Postman

## Getting Started

```bash
git clone https://github.com/vtoch23/online-store-for-handmade-leather-accessories.git
cd online-store-for-handmade-leather-accessories
docker compose up --build
