INSERT INTO categories (name, slug) VALUES ('Electrónica', 'electronica');
INSERT INTO categories (name, slug) VALUES ('Ropa', 'ropa');
INSERT INTO categories (name, slug) VALUES ('Alimentación', 'alimentacion');

INSERT INTO statuses (name, slug) VALUES ('Disponible', 'disponible');
INSERT INTO statuses (name, slug) VALUES ('Agotado', 'agotado');

INSERT INTO users (name, email, role, password, verified, created, updated) 
VALUES ('Juan Pérez', 'juan@example.com', 'admin', 'hashed_password', 1, NOW(), NOW());

INSERT INTO users (name, email, role, password, verified, created, updated) 
VALUES ('María López', 'maria@example.com', 'editor', 'hashed_password', 1, NOW(), NOW());

INSERT INTO products (title, description, photo, price, category_id, status_id, seller_id, created, updated) 
VALUES ('Smartphone', 'Teléfono inteligente de última generación', 'smartphone.jpg', 599.99, 1, 1, 1, NOW(), NOW());

INSERT INTO products (title, description, photo, price, category_id, status_id, seller_id, created, updated) 
VALUES ('Camiseta', 'Camiseta de algodón de color negro', 'camiseta.jpg', 19.99, 2, 1, 2, NOW(), NOW());

INSERT INTO blocked_users (user_id, reason) VALUES (2, 'Usuario bloqueado por comportamiento inapropiado');

INSERT INTO banned_products (product_id, reason, created) 
VALUES (1, 'Producto retirado por problemas de calidad', NOW());

INSERT INTO orders (product_id, buyer_id, offer, created) 
VALUES (1, 2, 549.99, NOW());

INSERT INTO confirmed_orders (order_id, created) VALUES (1, NOW());