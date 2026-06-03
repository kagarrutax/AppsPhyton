<?php

declare(strict_types=1);

namespace App\Core;

abstract class Controller
{
    protected function view(string $template, array $data = [], string $layout = 'main'): void
    {
        extract($data, EXTR_SKIP);
        $viewsPath = dirname(__DIR__) . '/Views';
        $contentFile = $viewsPath . '/' . $template . '.php';
        $layoutFile = $viewsPath . '/layouts/' . $layout . '.php';

        if (!is_file($contentFile)) {
            throw new \RuntimeException("Vista no encontrada: {$template}");
        }

        ob_start();
        require $contentFile;
        $content = ob_get_clean();

        require $layoutFile;
    }

    protected function requirePost(): void
    {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            http_response_code(405);
            exit('Método no permitido');
        }
        if (!verify_csrf()) {
            http_response_code(419);
            exit('Token CSRF inválido');
        }
    }
}
