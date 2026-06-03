<?php

declare(strict_types=1);

namespace App\Core;

use PDO;
use PDOException;

final class Database
{
    private static ?PDO $connection = null;

    public static function connect(array $config): PDO
    {
        if (self::$connection instanceof PDO) {
            return self::$connection;
        }

        $path = $config['sqlite'] ?? '';
        $dir = dirname($path);
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }

        try {
            self::$connection = new PDO('sqlite:' . $path, null, null, [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            ]);
            self::$connection->exec('PRAGMA foreign_keys = ON');
        } catch (PDOException $e) {
            throw new PDOException('No se pudo conectar a la base de datos: ' . $e->getMessage());
        }

        return self::$connection;
    }

    public static function pdo(): PDO
    {
        if (!self::$connection instanceof PDO) {
            $config = require dirname(__DIR__, 2) . '/config/database.php';
            return self::connect($config);
        }
        return self::$connection;
    }
}
