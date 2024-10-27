# E-commerce API 🛍️

A robust REST API for e-commerce operations built with Django REST Framework. This API handles products, orders, user authentication, shipping and payments.

## 🚀 Features

- **Products Management**
  - CRUD operations for products
  - Product categories
  - Search and filter products
  - Stock management

- **Order System**
  - Create and manage orders
  - Order status tracking
  - Order history

- **Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control
  - Secure password handling

- **Payment Integration**
  - Support for multiple payment methods( FIAT and Cryptocurrency)
  - Payment status tracking
  - Transaction history

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8+
- Django 4.2+
- pip (Python package installer)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Eniiyanu/ecommerce-api.git
   cd ecommerce-api
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory and add:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/refresh/` - Refresh token

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

### Orders
- `GET /api/orders/` - List user orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details
- `PUT /api/orders/{id}/` - Update order status

## 📝 API Documentation

### Product Endpoints

#### List Products
```http
GET /api/products/
```

Query Parameters:
- `search`: Search products by name
- `category`: Filter by category
- `min_price`: Filter by minimum price
- `max_price`: Filter by maximum price

Response:
```json
{
    "count": 100,
    "next": "http://api/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Product Name",
            "description": "Product Description",
            "price": "99.99",
            "stock": 50,
            "created_at": "2024-01-20T12:00:00Z"
        }
    ]
}
```

#### Create Product
```http
POST /api/products/
```

Request Body:
```json
{
    "name": "New Product",
    "description": "Product Description",
    "price": "99.99",
    "stock": 50
}
```

### Order Endpoints

#### Create Order
```http
POST /api/orders/
```

Request Body:
```json
{
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        }
    ],
    "delivery_address": "123 Street Name, City, Country"
}
```

## 🔒 Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your-token>
```

## 💻 Development

### Running Tests
```bash
python manage.py test
```

### Code Style
This project follows PEP 8 guidelines. Run flake8 to check your code:
```bash
flake8
```

## 🚀 Deployment

### Using Docker
1. Build the image:
   ```bash
   docker build -t ecommerce-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 ecommerce-api
   ```

### Traditional Deployment
1. Set `DEBUG=False` in production
2. Configure your web server (Nginx/Apache)
3. Set up SSL certificate
4. Configure database (PostgreSQL recommended)

## 📈 Scaling Considerations

- Use caching for frequently accessed data
- Implement rate limiting for API endpoints
- Set up database indexing for frequent queries
- Consider using load balancers for high traffic

## 🛠️ Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [Django REST Framework](https://www.django-rest-framework.org/) - REST API framework
- [SQLite](https://www.sqlite.org/index.html) - Database (development)
- [PostgreSQL](https://www.postgresql.org/) - Database (production)


## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## 👥 Authors

- Your Name - Initial work - [Eniiyanu](https://github.com/Eniiyanu)

## 🙏 Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc

## 📞 Support

For support, email your-email@example.com or join our Slack channel.
