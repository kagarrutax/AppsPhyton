<?php

declare(strict_types=1);

namespace App\Controllers;

use App\Core\Controller;
use App\Models\Product;

final class HomeController extends Controller
{
    public function index(): void
    {
        $products = Product::activeCatalog();
        $this->view('home/index', [
            'title' => 'Catálogo',
            'products' => $products,
        ]);
    }
}
