<?php

declare(strict_types=1);

namespace App\Controllers;

use App\Core\Auth;
use App\Core\Controller;
use App\Models\Product;
use App\Models\User;

final class DashboardController extends Controller
{
    public function index(): void
    {
        Auth::requireAdmin();
        $this->view('dashboard/index', [
            'title' => 'Dashboard',
            'stats' => [
                'products' => Product::countAll(),
                'active_products' => Product::countActive(),
                'users' => User::countAll(),
            ],
        ], 'admin');
    }
}
