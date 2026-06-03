<div class="mb-8">
    <h2 class="text-2xl font-bold">Panel administrativo</h2>
    <p class="text-slate-400">Resumen general de la tienda.</p>
</div>

<div class="grid gap-4 sm:grid-cols-3">
    <div class="rounded-2xl border border-white/10 bg-slate-900/60 p-6">
        <p class="text-sm text-slate-400">Total productos</p>
        <p class="mt-2 text-3xl font-bold text-brand-1"><?= (int) $stats['products'] ?></p>
    </div>
    <div class="rounded-2xl border border-white/10 bg-slate-900/60 p-6">
        <p class="text-sm text-slate-400">Productos activos</p>
        <p class="mt-2 text-3xl font-bold text-brand-4"><?= (int) $stats['active_products'] ?></p>
    </div>
    <div class="rounded-2xl border border-white/10 bg-slate-900/60 p-6">
        <p class="text-sm text-slate-400">Usuarios registrados</p>
        <p class="mt-2 text-3xl font-bold text-brand-2"><?= (int) $stats['users'] ?></p>
    </div>
</div>

<div class="mt-8 flex flex-wrap gap-3">
    <a href="/admin/products" class="rounded-xl bg-gradient-to-r from-brand-1 to-brand-2 px-5 py-3 text-sm font-semibold text-white">
        Gestionar productos
    </a>
    <a href="/" class="rounded-xl border border-white/10 px-5 py-3 text-sm text-slate-300 hover:bg-white/5">
        Ver catálogo público
    </a>
</div>

<div class="mt-8 rounded-2xl border border-brand-5/20 bg-brand-5/5 p-5 text-sm text-slate-300">
    <strong class="text-brand-4">WhatsApp del vendedor:</strong>
    +<?= e(app_config('whatsapp.country_code') . app_config('whatsapp.phone')) ?>
    — Edita <code class="text-brand-2">config/app.php</code> para cambiar el número.
</div>
