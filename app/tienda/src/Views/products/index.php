<div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <div>
        <h2 class="text-2xl font-bold">Productos</h2>
        <p class="text-slate-400">Gestiona el catálogo de la tienda.</p>
    </div>
    <a href="/admin/products/create" class="inline-flex rounded-xl bg-gradient-to-r from-brand-1 to-brand-2 px-5 py-3 text-sm font-semibold text-white">
        + Nuevo producto
    </a>
</div>

<div class="overflow-x-auto rounded-2xl border border-white/10">
    <table class="w-full min-w-[640px] text-left text-sm">
        <thead class="border-b border-white/10 bg-slate-900/80 text-slate-400">
            <tr>
                <th class="px-4 py-3">Producto</th>
                <th class="px-4 py-3">Precio</th>
                <th class="px-4 py-3">Estado</th>
                <th class="px-4 py-3 text-right">Acciones</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-white/5">
            <?php if (empty($products)): ?>
                <tr><td colspan="4" class="px-4 py-8 text-center text-slate-500">Sin productos registrados.</td></tr>
            <?php else: ?>
                <?php foreach ($products as $product): ?>
                    <tr class="hover:bg-white/[0.02]">
                        <td class="px-4 py-3">
                            <div class="font-medium text-white"><?= e($product['name']) ?></div>
                            <div class="max-w-xs truncate text-xs text-slate-500"><?= e($product['description']) ?></div>
                        </td>
                        <td class="px-4 py-3 text-brand-4"><?= e(format_price((float) $product['price'])) ?></td>
                        <td class="px-4 py-3">
                            <?php if ($product['is_active']): ?>
                                <span class="rounded-full bg-brand-5/20 px-2 py-1 text-xs text-brand-4">Activo</span>
                            <?php else: ?>
                                <span class="rounded-full bg-slate-700 px-2 py-1 text-xs text-slate-400">Inactivo</span>
                            <?php endif; ?>
                        </td>
                        <td class="px-4 py-3 text-right">
                            <a href="/admin/products/edit?id=<?= (int) $product['id'] ?>" class="mr-3 text-brand-2 hover:underline">Editar</a>
                            <form action="/admin/products/delete" method="POST" class="inline" onsubmit="return confirm('¿Eliminar este producto?')">
                                <?= csrf_field() ?>
                                <input type="hidden" name="id" value="<?= (int) $product['id'] ?>">
                                <button type="submit" class="text-red-400 hover:underline">Eliminar</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php endif; ?>
        </tbody>
    </table>
</div>
