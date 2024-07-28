# Order API

## Summary

This project is a RESTful API developed using Ruby on Rails.

Main features:

1. Interfaces to get the product list and single product details.
2. CRUD interfaces for orders, with orders linked to products and using "test_user" as the "user_id".

## API Documentation

### Product Module

The product module only provides GET interfaces.

**Get Product List**

This interface supports pagination (`page`), limit (`limit` defaults to 10 items), and sorting (`sort` defaults to sorting by `id`).

```json
// GET http://localhost:13001/products?page=1
{
    "status": "success",
    "page": 1,
    "total": 10,
    "limit": 10,
    "products": [
        {
            "id": 1,
            "name": "Product 1",
            "price": "99.0",
            "description": "Description for product 1",
            "created_at": "2024-07-27T17:25:38.656Z",
            "updated_at": "2024-07-27T17:25:38.656Z"
        },
        ...
    ]
}
```

**Get Single Product Details**

```json
// GET http://localhost:13001/products/1
{
    "id": 1,
    "name": "Product 1",
    "price": "99.0",
    "description": "Description for product 1",
    "created_at": "2024-07-27T17:25:38.656Z",
    "updated_at": "2024-07-27T17:25:38.656Z"
}
```

### Order Module

This module provides CRUD interfaces for orders. Order IDs use UUID, and each order is linked to a product. The order status can be "Pending", "Processing", "Complete", "Closed", or "Cancelled".

#### Create Order

Create an order by selecting a product and quantity, and the total price will be automatically calculated.

**Request**

```json
// POST http://localhost:13001/orders
{
  "order": {
    "product_id": 1,
    "quantity": 2
  }
}
```

**Response**

```json
{
    "id": "d06c8cc6-2dc3-4d65-83cc-2bd6b81932a8",
    "product_id": 1,
    "quantity": 2,
    "total_price": "198.0",
    "user_id": "test_user",
    "status": "Pending",
    "created_at": "2024-07-28T12:14:43.397Z",
    "updated_at": "2024-07-28T12:14:43.397Z"
}
```

#### Get Order Data

This interface also supports pagination (`page`), limit (`limit` defaults to 10 items), and sorting (`sort` defaults to sorting by `created_at`).

**Get Order List**

```json
// GET http://localhost:13001/orders?page=1
{
    "status": "success",
    "page": 1,
    "total": 11,
    "limit": 10,
    "orders": [
        {
            "id": "5725d9bc-30e7-4a36-81f7-809e03d52401",
            "product_id": 1,
            "quantity": 2,
            "total_price": "198.0",
            "user_id": "test_user",
            "status": "Pending",
            "created_at": "2024-07-27T17:26:02.850Z",
            "updated_at": "2024-07-28T05:12:10.353Z"
        },
        ...
    ]
}
```

**Get Single Order Details**

```json
// GET http://localhost:13001/orders/5725d9bc-30e7-4a36-81f7-809e03d52401
{
    "id": "5725d9bc-30e7-4a36-81f7-809e03d52401",
    "product_id": 1,
    "quantity": 2,
    "total_price": "39.98",
    "user_id": "test_user",
    "status": "Pending",
    "created_at": "2024-07-27T17:26:02.850Z",
    "updated_at": "2024-07-28T05:12:10.353Z"
}
```

### Update Order

You can only update the `quantity` for orders with status "Pending". The total price will be recalculated based on the product price.

**Request**

```json
// PUT/PATCH http://localhost:13001/orders/5725d9bc-30e7-4a36-81f7-809e03d52401
{
    "quantity": 5
}
```

**Response**

```json
{
    "quantity": 5,
    "total_price": "495.0",
    "product_id": 1,
    "id": "5725d9bc-30e7-4a36-81f7-809e03d52401",
    "user_id": "test_user",
    "status": "Pending",
    "created_at": "2024-07-27T17:26:02.850Z",
    "updated_at": "2024-07-28T11:59:38.371Z"
}
```

### Delete Order

`DELETE http://localhost:13001/orders/d06c8cc6-2dc3-4d65-83cc-2bd6b81932a8`

## Project Setup Instructions

This project can be developed, tested, and deployed directly using Docker.

**Install Dependencies**

```sh
bash build_docker.sh
```

**Development Environment**

**Enter Docker Shell**

```sh
bash run.sh

# Initialize development database
RAILS_ENV=development bundle exec rails db:migrate
RAILS_ENV=development bundle exec rails db:seed

# Initialize production database
RAILS_ENV=production bundle exec rails db:migrate
RAILS_ENV=production bundle exec rails db:seed
```

**Unit Test**

```sh
root@77f98f68f482:/www# RAILS_ENV=test bundle exec rails test

Running 7 tests in a single process (parallelization threshold is 50)
Run options: --seed 43948

# Running:

.......

Finished in 0.226696s, 30.8783 runs/s, 57.3454 assertions/s.
7 runs, 13 assertions, 0 failures, 0 errors, 0 skips
```

**Start the Service**

```sh
docker-compose up
```

**Production Server**

```sh
docker-compose -f docker-compose.production.yml up
```
