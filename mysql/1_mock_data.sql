-- Mock data para la tabla 'categories'
INSERT INTO categories (id, name, slug) VALUES
(1, 'Electronics', 'electronics'),
(2, 'Clothing', 'clothing'),
(3, 'Home and Garden', 'home-garden');

-- Mock data para la tabla 'statuses'
INSERT INTO statuses (id, name, slug) VALUES
('Active', 'active'),
('Inactive', 'inactive'),
('Pending', 'pending');

-- Mock data para la tabla 'users'
INSERT INTO users (id, name, email, role, password, verified) VALUES
('John Doe', 'john.doe@example.com', 'seller', 'hashed_password', 1, NULL),
('Jane Smith', 'jane.smith@example.com', 'buyer', 'hashed_password', 1, NULL);

-- Mock data para la tabla 'products'
INSERT INTO products (id, title, description, photo, price, category_id, status_id, seller_id) VALUES
('Smartphone', 'High-end smartphone with advanced features.', 'smartphone.jpg', 699.99, 1, 1, 1),
('Laptop', 'Powerful laptop for professional use.', 'laptop.jpg', 1299.99, 1, 1, 1),
('T-shirt', 'Comfortable cotton T-shirt in various colors.', 'tshirt.jpg', 19.99, 2, 1, 2);

-- Mock data para la tabla 'orders'
INSERT INTO orders (id, product_id, buyer_id, offer) VALUES
(1, 2, 650.00),
(3, 1, 18.00);

-- Mock data para la tabla 'confirmed_orders'
INSERT INTO confirmed_orders (order_id) VALUES
(1);
