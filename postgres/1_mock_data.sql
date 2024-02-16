-- Insertar datos en la tabla de categorías
INSERT INTO categories (name, slug) VALUES ('Electrónica', 'electronica');
INSERT INTO categories (name, slug) VALUES ('Ropa', 'ropa');
INSERT INTO categories (name, slug) VALUES ('Alimentación', 'alimentacion');

-- Insertar datos en la tabla de estados
INSERT INTO statuses (name, slug) VALUES ('Disponible', 'disponible');
INSERT INTO statuses (name, slug) VALUES ('Agotado', 'agotado');

-- Insertar datos en la tabla de usuarios
INSERT INTO users (name, email, role, password, verified, created, updated) 
VALUES ('cristian martinez', 'crmagu@fp.insjoaquimmir.cat', 'wanner', 'insjoaquimmir', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insertar datos en la tabla de usuarios
INSERT INTO users (name, email, role, password, verified, created, updated) 
VALUES ('gerard diaz', 'gedica@fp.insjoaquimmir.cat', 'wanner', 'insjoaquimmir', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insertar datos en la tabla de productos
INSERT INTO products (title, description, photo, price, category_id, status_id, seller_id, created, updated) 
VALUES ('Smartphone', 'Teléfono inteligente de última generación', 'smartphone.jpg', 599.99, 1, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO products (title, description, photo, price, category_id, status_id, seller_id, created, updated) 
VALUES ('Camiseta', 'Camiseta de algodón de color negro', 'camiseta.jpg', 19.99, 2, 1, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insertar datos en la tabla de usuarios bloqueados
INSERT INTO blocked_users (user_id, reason) VALUES (2, 'Usuario bloqueado por comportamiento inapropiado');

-- Insertar datos en la tabla de productos baneados
INSERT INTO banned_products (product_id, reason, created) 
VALUES (1, 'Producto retirado por problemas de calidad', CURRENT_TIMESTAMP);

-- Insertar datos en la tabla de órdenes
INSERT INTO orders (product_id, buyer_id, offer, created) 
VALUES (1, 2, 549.99, CURRENT_TIMESTAMP);

-- Insertar datos en la tabla de órdenes confirmadas
INSERT INTO confirmed_orders (order_id, created) VALUES (1, CURRENT_TIMESTAMP);