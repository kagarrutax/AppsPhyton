<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/src/bootstrap.php';

use App\Core\Database;

$passed = 0;
$failed = 0;

function assert_true(bool $condition, string $message): void
{
    global $passed, $failed;
    if ($condition) {
        echo "  OK: {$message}\n";
        $passed++;
    } else {
        echo "  FAIL: {$message}\n";
        $failed++;
    }
}

echo "=== Smoke tests Tienda ===\n\n";

$dbPath = dirname(__DIR__) . '/database/tienda.sqlite';
if (!is_file($dbPath)) {
    echo "Inicializando base de datos...\n";
    passthru('php ' . escapeshellarg(dirname(__DIR__) . '/database/init.php'));
}

$config = require dirname(__DIR__) . '/config/database.php';
$pdo = Database::connect($config);

echo "Database:\n";
assert_true($pdo instanceof PDO, 'Conexión PDO SQLite');

$count = (int) $pdo->query('SELECT COUNT(*) FROM products')->fetchColumn();
assert_true($count >= 1, 'Hay productos seed (' . $count . ')');

$admin = $pdo->query("SELECT * FROM users WHERE email = 'admin@tienda.com'")->fetch();
assert_true($admin !== false && $admin['role'] === 'admin', 'Usuario admin existe');
assert_true(password_verify('admin123', $admin['password']), 'Password admin123 válido');

echo "\nHelpers:\n";
$url = whatsapp_buy_url('Test Product', 99.9);
assert_true(str_contains($url, 'wa.me'), 'URL WhatsApp contiene wa.me');
assert_true(str_contains($url, 'Test'), 'URL WhatsApp contiene nombre producto');

assert_true(format_price(10.5) === 'S/ 10.50', 'format_price funciona');
assert_true(e('<script>') === '&lt;script&gt;', 'escape HTML funciona');

echo "\n=== Resultado: {$passed} passed, {$failed} failed ===\n";
exit($failed > 0 ? 1 : 0);
