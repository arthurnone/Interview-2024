
## IN YOU MARKET DB Assignment

### 1. User function including login information

The table design logic includes three main tables: `users`, `social_accounts`, `sessions` 

#### User Table

This table is used to manage basic user data such as username, account information, and passwords.

- `salt`: A unique salt value used in hashing the user's password.
- `is_active`: A boolean indicating whether the user's account is active.
- `created_at`: The timestamp when the user account was created.

**Table: `users`**

| Column       | Data Type     | Constraints                    |
|--------------|---------------|--------------------------------|
| `user_id`    | SERIAL        | PRIMARY KEY                    |
| `username`   | VARCHAR(150)  | UNIQUE, NOT NULL               |
| `email`      | VARCHAR(254)  | UNIQUE, NOT NULL               |
| `password`   | VARCHAR(128)  | NOT NULL                       |
| `salt`       | VARCHAR(32)   | NOT NULL                       |
| `is_active`  | BOOLEAN       | NOT NULL                       |
| `created_at` | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP      |

#### Social Account Table

This table stores data for users who log in using third-party services such as Google.

- `social_id`: A unique identifier for each social account.
- `user_id`: A foreign key linking to the user table.
- `provider`: The name of the third-party provider (e.g., Google).
- `provider_id`: The unique identifier provided by the third-party service.

**Table: `social_accounts`**

| Column        | Data Type     | Constraints                             |
|---------------|---------------|-----------------------------------------|
| `social_id`   | SERIAL        | PRIMARY KEY                             |
| `user_id`     | INTEGER       | FOREIGN KEY  `users`(`user_id`)         |
| `provider`    | VARCHAR(50)   | NOT NULL                                |
| `provider_id` | VARCHAR(255)  | NOT NULL                                |
| `created_at`  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP               |

#### Session Table

This table stores session data for logged-in users.

- `session_id`: A unique identifier for each session.
- `user_id`: A foreign key linking to the user table.
- `login_time`: The timestamp when the user logged in.
- `expire_date`: The timestamp when the session expires.
- `session_data`: Additional data for the session, such as tokens for third-party logins.

**Table: `sessions`**

| Column         | Data Type     | Constraints                    |
|----------------|---------------|--------------------------------|
| `session_id`   | CHAR(32)      | PRIMARY KEY                    |
| `user_id`      | INTEGER       | FOREIGN KEY `users`(`user_id`) |
| `login_time`   | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP      |
| `expire_date`  | TIMESTAMP     |                                |
| `session_data` | TEXT          |                                |

### 2. Coupon function for certain products and users

#### Coupon Table

The design logic for the Coupons table includes two types of coupons: fixed amount and percentage discount. Percentage discount coupons can have a maximum limit.

- `id`: A unique identifier for each coupon.
- `code`: A unique code for the coupon.
- `discount`: The discount amount or percentage.
- `type`: The type of coupon ('fixed' or 'percentage').
- `max_discount`: The maximum discount amount (only applicable for percentage coupons).
- `valid_from`: The start date for the coupon's validity.
- `valid_to`: The end date for the coupon's validity.
- `active`: A boolean indicating whether the coupon is active.
- `created_at`: The timestamp when the coupon was created.

**Table: `coupons`**

| Column        | Data Type     | Constraints                        |
|---------------|---------------|------------------------------------|
| `id`          | SERIAL        | PRIMARY KEY                        |
| `code`        | VARCHAR(50)   | UNIQUE, NOT NULL                   |
| `discount`    | DECIMAL(5, 2) | NOT NULL                           |
| `type`        | VARCHAR(10)   | NOT NULL                           | 
| `max_discount`| DECIMAL(10, 2)|                                    | 
| `valid_from`  | TIMESTAMP     | NOT NULL                           |
| `valid_to`    | TIMESTAMP     | NOT NULL                           |
| `active`      | BOOLEAN       | DEFAULT TRUE                       |
| `created_at`  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP          |

#### Coupon User Table
This table links coupons to users, with a status indicating whether the coupon has been used.

- `coupon_id`: A foreign key linking to the coupons table.
- `user_id`: A foreign key linking to the users table.
- `used_at`: The timestamp when the coupon was used.
- `status`: The status of the coupon (e.g., 'used' or 'unused').

**Table: `coupon_users`**

| Column       | Data Type     | Constraints                                 |
|--------------|---------------|---------------------------------------------|
| `coupon_id`  | INT           | FOREIGN KEY REFERENCES `coupons`(`id`)      |
| `user_id`    | INT           | FOREIGN KEY REFERENCES `users`(`user_id`)   |
| `used_at`    | TIMESTAMP     |                                             |
| `status`     | VARCHAR(20)   | NOT NULL DEFAULT 'unused'                   |
| PRIMARY KEY (`coupon_id`, `user_id`)                                       |

#### Coupon Products Table
This table links coupons to products.

**Table: `coupon_products`**

| Column       | Data Type     | Constraints                                |
|--------------|---------------|--------------------------------------------|
| `coupon_id`  | INT           | FOREIGN KEY REFERENCES `coupons`(`id`)     |
| `product_id` | INT           | FOREIGN KEY REFERENCES `products`(`id`)    |
| PRIMARY KEY (`coupon_id`, `product_id`)                                   |

#### Products Table
This table stores product information.

- `id`: A unique identifier for each product.
- `name`: The name of the product.
- `price`: The price of the product.
- `created_at`: The timestamp when the product was created.

**Table: `products`**

| Column       | Data Type     | Constraints                    |
|--------------|---------------|--------------------------------|
| `id`         | SERIAL        | PRIMARY KEY                    |
| `name`       | VARCHAR(100)  | NOT NULL                       |
| `price`      | DECIMAL(10, 2)| NOT NULL                       |
| `created_at` | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP      |