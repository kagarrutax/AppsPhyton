<?php

declare(strict_types=1);

namespace App\Models;

use App\Core\Database;
use PDO;

final class Product
{
    public static function activeCatalog(): array
    {
        $stmt = Database::pdo()->query(
            'SELECT * FROM products WHERE is_active = 1 ORDER BY created_at DESC'
        );
        return $stmt->fetchAll();
    }

    public static function all(): array
    {
        $stmt = Database::pdo()->query('SELECT * FROM products ORDER BY created_at DESC');
        return $stmt->fetchAll();
    }

    public static function find(int $id): ?array
    {
        $stmt = Database::pdo()->prepare('SELECT * FROM products WHERE id = :id');
        $stmt->execute(['id' => $id]);
        $row = $stmt->fetch();
        return $row ?: null;
    }

    public static function create(array $data): bool
    {
        $stmt = Database::pdo()->prepare(
            'INSERT INTO products (name, description, price, image, is_active)
             VALUES (:name, :description, :price, :image, :is_active)'
        );
        return $stmt->execute([
            'name' => $data['name'],
            'description' => $data['description'],
            'price' => $data['price'],
            'image' => $data['image'] ?? null,
            'is_active' => $data['is_active'] ?? 1,
        ]);
    }

    public static function update(int $id, array $data): bool
    {
        $stmt = Database::pdo()->prepare(
            'UPDATE products SET
                name = :name,
                description = :description,
                price = :price,
                image = :image,
                is_active = :is_active,
                updated_at = datetime(\'now\')
             WHERE id = :id'
        );
        return $stmt->execute([
            'id' => $id,
            'name' => $data['name'],
            'description' => $data['description'],
            'price' => $data['price'],
            'image' => $data['image'] ?? null,
            'is_active' => $data['is_active'] ?? 1,
        ]);
    }

    public static function delete(int $id): bool
    {
        $stmt = Database::pdo()->prepare('DELETE FROM products WHERE id = :id');
        return $stmt->execute(['id' => $id]);
    }

    public static function countAll(): int
    {
        return (int) Database::pdo()->query('SELECT COUNT(*) FROM products')->fetchColumn();
    }

    public static function countActive(): int
    {
        return (int) Database::pdo()->query('SELECT COUNT(*) FROM products WHERE is_active = 1')->fetchColumn();
    }
}
