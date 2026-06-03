<?php

declare(strict_types=1);

namespace App\Controllers;

use App\Core\Auth;
use App\Core\Controller;
use App\Models\Product;

final class ProductController extends Controller
{
    public function index(): void
    {
        Auth::requireAdmin();
        $this->view('products/index', [
            'title' => 'Productos',
            'products' => Product::all(),
        ], 'admin');
    }

    public function create(): void
    {
        Auth::requireAdmin();
        $this->view('products/create', ['title' => 'Nuevo producto'], 'admin');
    }

    public function store(): void
    {
        Auth::requireAdmin();
        $this->requirePost();
        $data = $this->validatedProductData();
        if ($data === null) {
            redirect('/admin/products/create');
        }

        $image = $this->handleUpload();
        if ($image === false) {
            redirect('/admin/products/create');
        }
        $data['image'] = $image;

        if (!Product::create($data)) {
            flash('error', 'No se pudo guardar el producto.');
            redirect('/admin/products/create');
        }

        flash('success', 'Producto creado correctamente.');
        redirect('/admin/products');
    }

    public function edit(): void
    {
        Auth::requireAdmin();
        $product = $this->findProductOrRedirect();
        $this->view('products/edit', [
            'title' => 'Editar producto',
            'product' => $product,
        ], 'admin');
    }

    public function update(): void
    {
        Auth::requireAdmin();
        $this->requirePost();
        $_GET['id'] = (int) ($_POST['id'] ?? 0);
        $product = $this->findProductOrRedirect();
        $data = $this->validatedProductData();
        if ($data === null) {
            redirect('/admin/products/' . $product['id'] . '/edit');
        }

        $data['image'] = $product['image'];
        $upload = $this->handleUpload();
        if ($upload === false) {
            redirect('/admin/products/' . $product['id'] . '/edit');
        }
        if ($upload !== null) {
            $this->deleteImageFile($product['image']);
            $data['image'] = $upload;
        }

        if (!Product::update((int) $product['id'], $data)) {
            flash('error', 'No se pudo actualizar el producto.');
            redirect('/admin/products/' . $product['id'] . '/edit');
        }

        flash('success', 'Producto actualizado.');
        redirect('/admin/products');
    }

    public function destroy(): void
    {
        Auth::requireAdmin();
        $this->requirePost();
        $_GET['id'] = (int) ($_POST['id'] ?? 0);
        $product = $this->findProductOrRedirect();

        if (!Product::delete((int) $product['id'])) {
            flash('error', 'No se pudo eliminar el producto.');
            redirect('/admin/products');
        }

        $this->deleteImageFile($product['image']);
        flash('success', 'Producto eliminado.');
        redirect('/admin/products');
    }

    private function findProductOrRedirect(): array
    {
        $id = (int) ($_GET['id'] ?? 0);
        $product = Product::find($id);
        if (!$product) {
            flash('error', 'Producto no encontrado.');
            redirect('/admin/products');
        }
        return $product;
    }

    /** @return array<string, mixed>|null */
    private function validatedProductData(): ?array
    {
        $name = trim($_POST['name'] ?? '');
        $description = trim($_POST['description'] ?? '');
        $price = (float) str_replace(',', '.', $_POST['price'] ?? '0');
        $isActive = isset($_POST['is_active']) ? 1 : 0;

        if ($name === '' || $description === '') {
            flash('error', 'Nombre y descripción son obligatorios.');
            return null;
        }
        if ($price < 0) {
            flash('error', 'El precio no puede ser negativo.');
            return null;
        }

        return [
            'name' => $name,
            'description' => $description,
            'price' => $price,
            'is_active' => $isActive,
        ];
    }

    /** @return string|null|false null = sin archivo, string = ruta, false = error */
    private function handleUpload(): string|null|false
    {
        if (!isset($_FILES['image']) || $_FILES['image']['error'] === UPLOAD_ERR_NO_FILE) {
            return null;
        }

        $file = $_FILES['image'];
        if ($file['error'] !== UPLOAD_ERR_OK) {
            flash('error', 'Error al subir la imagen.');
            return false;
        }

        $maxSize = (int) app_config('upload.max_size', 2097152);
        if ($file['size'] > $maxSize) {
            flash('error', 'La imagen supera el tamaño máximo permitido (2 MB).');
            return false;
        }

        $finfo = new \finfo(FILEINFO_MIME_TYPE);
        $mime = $finfo->file($file['tmp_name']);
        $allowed = app_config('upload.allowed_mimes', []);
        if (!in_array($mime, $allowed, true)) {
            flash('error', 'Formato de imagen no permitido. Usa JPG, PNG o WebP.');
            return false;
        }

        $ext = match ($mime) {
            'image/jpeg' => 'jpg',
            'image/png' => 'png',
            'image/webp' => 'webp',
            default => null,
        };
        if ($ext === null) {
            flash('error', 'Formato de imagen no válido.');
            return false;
        }

        $dir = app_config('upload.path');
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }

        $filename = bin2hex(random_bytes(16)) . '.' . $ext;
        $destination = $dir . DIRECTORY_SEPARATOR . $filename;
        if (!move_uploaded_file($file['tmp_name'], $destination)) {
            flash('error', 'No se pudo guardar la imagen.');
            return false;
        }

        return 'uploads/products/' . $filename;
    }

    private function deleteImageFile(?string $path): void
    {
        if ($path === null || $path === '') {
            return;
        }
        $full = dirname(__DIR__, 2) . '/public/' . ltrim($path, '/');
        if (is_file($full)) {
            unlink($full);
        }
    }
}
