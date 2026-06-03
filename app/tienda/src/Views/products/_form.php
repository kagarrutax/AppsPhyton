<?php
$formAction = $formAction ?? '/admin/products';
$submitLabel = $submitLabel ?? 'Crear producto';
$product = $product ?? ['name' => '', 'description' => '', 'price' => '', 'is_active' => 1, 'image' => null];
?>
<div class="mx-auto max-w-2xl">
    <a href="/admin/products" class="mb-4 inline-block text-sm text-slate-400 hover:text-white">&larr; Volver</a>
    <div class="rounded-2xl border border-white/10 bg-slate-900/60 p-6 sm:p-8">
        <h2 class="mb-6 text-xl font-bold"><?= e($title ?? 'Producto') ?></h2>
        <form action="<?= e($formAction) ?>" method="POST" enctype="multipart/form-data" class="space-y-5">
            <?= csrf_field() ?>
            <?php if (!empty($product['id'])): ?>
                <input type="hidden" name="id" value="<?= (int) $product['id'] ?>">
            <?php endif; ?>
            <div>
                <label class="mb-1 block text-sm text-slate-300">Nombre</label>
                <input type="text" name="name" required value="<?= e($product['name']) ?>"
                    class="w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3 outline-none focus:border-brand-1">
            </div>
            <div>
                <label class="mb-1 block text-sm text-slate-300">Descripción</label>
                <textarea name="description" required rows="4"
                    class="w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3 outline-none focus:border-brand-1"><?= e($product['description']) ?></textarea>
            </div>
            <div>
                <label class="mb-1 block text-sm text-slate-300">Precio (S/)</label>
                <input type="number" name="price" required min="0" step="0.01" value="<?= e((string) $product['price']) ?>"
                    class="w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3 outline-none focus:border-brand-1">
            </div>
            <div>
                <label class="mb-1 block text-sm text-slate-300">Imagen (JPG, PNG, WebP — máx. 2 MB)</label>
                <input type="file" name="image" accept="image/jpeg,image/png,image/webp"
                    class="w-full text-sm text-slate-400 file:mr-4 file:rounded-lg file:border-0 file:bg-brand-1/20 file:px-4 file:py-2 file:text-brand-1">
                <?php if (!empty($product['image'])): ?>
                    <p class="mt-2 text-xs text-slate-500">Imagen actual: <?= e($product['image']) ?></p>
                <?php endif; ?>
            </div>
            <label class="flex items-center gap-2 text-sm text-slate-300">
                <input type="checkbox" name="is_active" value="1" <?= !empty($product['is_active']) ? 'checked' : '' ?>
                    class="rounded border-white/20 bg-slate-950 text-brand-1 focus:ring-brand-1">
                Producto visible en catálogo
            </label>
            <button type="submit" class="rounded-xl bg-gradient-to-r from-brand-4 to-brand-5 px-6 py-3 font-semibold text-white">
                <?= e($submitLabel) ?>
            </button>
        </form>
    </div>
</div>
