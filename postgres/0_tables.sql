CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT NOT NULL
);

CREATE TABLE statuses (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    password TEXT NOT NULL,
    verified INTEGER NOT NULL,
    email_token TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    token TEXT UNIQUE,
    token_expiration TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    photo TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (status_id) REFERENCES statuses(id),
    FOREIGN KEY (seller_id) REFERENCES users(id)
);

CREATE TABLE blocked_users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE,
    reason TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE banned_products (
    product_id INTEGER PRIMARY KEY,
    reason TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    offer NUMERIC(10, 2) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (buyer_id) REFERENCES users(id)
);

CREATE TABLE confirmed_orders (
    order_id INTEGER PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);