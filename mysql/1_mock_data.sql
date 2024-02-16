-- Mock data para la tabla 'categories'
INSERT INTO categories (id, name, slug) VALUES
(1, 'Electronics', 'electronics'),
(2, 'Clothing', 'clothing'),
(3, 'Home and Garden', 'home-garden');

-- Mock data para la tabla 'statuses'
INSERT INTO statuses (id, name, slug) VALUES
(1, 'Active', 'active'),
(2, 'Inactive', 'inactive'),
(3, 'Pending', 'pending');

-- Mock data para la tabla 'users'
INSERT INTO users (id, name, email, role, password, verified, email_token, created, updated, token, token_expiration) VALUES
(1, 'John Doe', 'john.doe@example.com', 'seller', 'hashed_password', 1, NULL, '2022-01-01 12:00:00', '2022-01-01 12:00:00', 'token_123', '2023-01-01 12:00:00'),
(2, 'Jane Smith', 'jane.smith@example.com', 'buyer', 'hashed_password', 1, NULL, '2022-01-02 12:00:00', '2022-01-02 12:00:00', 'token_456', '2023-02-01 12:00:00');

-- Mock data para la tabla 'products'
INSERT INTO products (id, title, description, photo, price, category_id, status_id, seller_id, created, updated) VALUES
(1, 'Smartphone', 'High-end smartphone with advanced features.', 'smartphone.jpg', 699.99, 1, 1, 1, '2022-01-03 12:00:00', '2022-01-03 12:00:00'),
(2, 'Laptop', 'Powerful laptop for professional use.', 'laptop.jpg', 1299.99, 1, 1, 1, '2022-01-04 12:00:00', '2022-01-04 12:00:00'),
(3, 'T-shirt', 'Comfortable cotton T-shirt in various colors.', 'tshirt.jpg', 19.99, 2, 1, 2, '2022-01-05 12:00:00', '2022-01-05 12:00:00');

-- Mock data para la tabla 'blocked_users'
INSERT INTO blocked_users (id, user_id, reason) VALUES
(1, 2, 'Violated terms of service');

-- Mock data para la tabla 'banned_products'
INSERT INTO banned_products (product_id, reason, created) VALUES
(2, 'Product no longer available', '2022-01-06 12:00:00');

-- Mock data para la tabla 'orders'
INSERT INTO orders (id, product_id, buyer_id, offer, created) VALUES
(1, 1, 2, 650.00, '2022-01-07 12:00:00'),
(2, 3, 1, 18.00, '2022-01-08 12:00:00');

-- Mock data para la tabla 'confirmed_orders'
INSERT INTO confirmed_orders (order_id, created) VALUES
(1, '2022-01-09 12:00:00');
