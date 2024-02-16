CREATE TABLE `users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` TEXT COLLATE utf8mb4_unicode_ci,
  `email` TEXT COLLATE utf8mb4_unicode_ci,
  `role` TEXT COLLATE utf8mb4_unicode_ci,
  `password` TEXT COLLATE utf8mb4_unicode_ci,
  `email_token` TEXT COLLATE utf8mb4_unicode_ci,
  `verified` INT DEFAULT NULL,
  `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `token` TEXT COLLATE utf8mb4_unicode_ci,
  `token_expiration` TEXT COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `categories` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `slug` VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `statuses` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `slug` VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `products` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `photo` VARCHAR(255) NOT NULL,
  `price` NUMERIC(10, 2) NOT NULL,
  `category_id` INT,
  `status_id` INT,
  `seller_id` INT,
  `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`),
  FOREIGN KEY (`status_id`) REFERENCES `statuses`(`id`),
  FOREIGN KEY (`seller_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `blocked_users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT,
  `reason` VARCHAR(255) DEFAULT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `banned_products` (
  `product_id` INT PRIMARY KEY AUTO_INCREMENT,
  `reason` VARCHAR(255) NOT NULL,
  `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `orders` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `product_id` INT NOT NULL,
  `buyer_id` INT NOT NULL,
  `offer` NUMERIC(10, 2) NOT NULL,
  `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `uc_product_buyer` (`product_id`, `buyer_id`),
  FOREIGN KEY (`product_id`) REFERENCES `products`(`id`),
  FOREIGN KEY (`buyer_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `confirmed_orders` (
  `order_id` INT PRIMARY KEY AUTO_INCREMENT,
  `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;