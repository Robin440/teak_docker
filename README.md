# Teakwood Factory

Teakwood Factory is a backend application designed to manage and support the operations of a teakwood product manufacturing and sales business. The application is built using Django and Django REST Framework, providing a robust API and admin interface for managing products, categories, subcategories, banners, and other supporting data models.

## Features

- **Product Management:** Create, update, and manage teakwood products.
- **Category & Subcategory Management:** Organize products into categories and subcategories.
- **Banner Management:** Manage promotional banners for the website or marketing purposes.
- **Support Models:** Additional models to support product information and business logic.
- **Admin Interface:** Easy-to-use Django admin interface for managing all models.
- **API Integration:** RESTful API endpoints for CRUD operations using Django REST Framework.
- **Data Generation:** Generate sample data using the Faker package.

## Tools and Technologies Used

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework (DRF)**: A powerful and flexible toolkit for building Web APIs.
- **Docker**: A platform for developing, shipping, and running applications in containers. This project uses Docker to manage the development and deployment environment.
- **Faker Package**: A Python package used to generate fake data for testing and development purposes.

## Models

The application consists of several models to represent different entities:

1. **Product**: Represents a teakwood product with attributes like name, description, price, and category.
2. **Category**: Represents the main category of products.
3. **Subcategory**: Represents subcategories under each main category.
4. **Banner**: Represents promotional banners with attributes like image, title, and link.
5. **Support Models**: Additional models to support product-related operations, such as product reviews, tags, and inventory management.

## Getting Started

To get started with the Teakwood Factory application, follow these steps:

### Prerequisites

- Docker installed on your machine
- Basic knowledge of Django and Docker

### Installation

1. **Clone the Repository**

   ```bash
   https://github.com/Robin440/teak_docker.git
   cd teakwood-factory
   ```

### Build and Run the Docker Containers
   ```bash
   docker-compose up --build
   ```
   This command will build the Docker containers and start the application.

### Run Migrations

   Inside the Docker container, run the following command to apply database migrations:
   ```bash
   docker compose exec -it tdango bash
   python manage.py migrate
   ```
### Create a Superuser

### Create an admin user to access the Django admin interface:

   ```bash
   docker-compose exec -it tdango bash
   python manage.py createsuperuser
   ```

### Access the Admin Interface

   Open your web browser and go to  ```http://localhost:8009/admin``` to access the Django admin interface. Use the superuser credentials you created to log in.


### API Endpoints
   The application provides several API endpoints to interact with the models. The endpoints are designed using Django REST Framework and are available for CRUD operations on products, categories, subcategories, and banners.

   Refer to the API Documentation for detailed information on available endpoints and usage examples.

### Contributing
   If you want to contribute to the development of Teakwood Factory, please follow these steps:

   - **Fork the repository.**
   - **Create a new branch: git checkout -b feature/YourFeatureName.***
   - **Make your changes and commit them: git commit -m 'Add some feature'.**
   - **Push to the branch: git push origin feature/YourFeatureName.**
   - **Submit a pull request.**

### License
   This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgements
   - **Django**
   - **Django REST Framework**
   - **Docker**
   - **Faker**

Thank you for using Teakwood Factory! We hope this application helps you manage your teakwood business efficiently.

Feel free to adjust this `README.md` according to the specific details and requirements of your project.




