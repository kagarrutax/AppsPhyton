<?php

declare(strict_types=1);

return [
    'name' => 'TiendaCatálogo',
    'url' => 'http://localhost:8080',
    'whatsapp' => [
        'country_code' => '51',
        'phone' => '999888777',
        'seller_name' => 'Vendedor',
    ],
    'upload' => [
        'max_size' => 2 * 1024 * 1024,
        'allowed_mimes' => ['image/jpeg', 'image/png', 'image/webp'],
        'path' => dirname(__DIR__) . '/public/uploads/products',
    ],
];
