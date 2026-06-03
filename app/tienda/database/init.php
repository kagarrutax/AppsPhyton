<?php

declare(strict_types=1);

$base = dirname(__DIR__);
require_once $base . '/src/bootstrap.php';

use App\Core\Database;

$config = require $base . '/config/database.php';
$pdo = Database::connect($config);

$schema = file_get_contents($base . '/database/schema.sql');
$pdo->exec($schema);

$hash = password_hash('admin123', PASSWORD_DEFAULT);
$stmt = $pdo->prepare('UPDATE users SET password = ? WHERE email = ?');
$stmt->execute([$hash, 'admin@tienda.com']);

$uploadDir = $base . '/public/uploads/products';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}

echo "Base de datos inicializada en: {$config['sqlite']}\n";
echo "Admin: admin@tienda.com / admin123\n";
