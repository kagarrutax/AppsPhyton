CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    image TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_products_active ON products(is_active);

-- Admin demo: admin@tienda.com / admin123 (hash se actualiza en init.php)
INSERT OR IGNORE INTO users (id, name, email, password, role)
VALUES (
    1,
    'Administrador',
    'admin@tienda.com',
    '$2y$10$placeholderplaceholderplaceholderplaceholde',
    'admin'
);

INSERT OR IGNORE INTO products (id, name, description, price, image, is_active) VALUES
(1, 'Auriculares Pro', 'Sonido envolvente con cancelación de ruido activa.', 149.90, NULL, 1),
(2, 'Smartwatch Fit', 'Monitorea pasos, sueño y notificaciones en tu muñeca.', 89.50, NULL, 1),
(3, 'Mochila Urbana', 'Resistente al agua, compartimento para laptop 15".', 59.00, NULL, 1),
(4, 'Lámpara LED', 'Luz cálida regulable, ideal para escritorio.', 34.99, NULL, 1);
