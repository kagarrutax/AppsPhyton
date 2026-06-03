<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= e($title ?? 'Admin') ?> | Admin</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: { 1: '#cf26d9', 2: '#d65c9f', 3: '#d98c90', 4: '#3bcc33', 5: '#1fad5f' }
                    }
                }
            }
        }
    </script>
    <link rel="stylesheet" href="<?= asset('css/palette.css') ?>">
</head>
<body class="min-h-screen bg-slate-950 text-slate-100">
    <div class="flex min-h-screen">
        <aside class="hidden w-64 flex-shrink-0 border-r border-white/10 bg-slate-900/50 p-6 lg:block">
            <a href="/" class="mb-8 block text-lg font-bold text-brand-1"><?= e(app_config('name')) ?></a>
            <nav class="space-y-1 text-sm">
                <a href="/dashboard" class="block rounded-lg px-3 py-2 hover:bg-white/5">Dashboard</a>
                <a href="/admin/products" class="block rounded-lg px-3 py-2 hover:bg-white/5">Productos</a>
                <a href="/" class="block rounded-lg px-3 py-2 text-slate-400 hover:bg-white/5">Ver catálogo</a>
            </nav>
        </aside>
        <div class="flex flex-1 flex-col">
            <header class="flex items-center justify-between border-b border-white/10 px-4 py-4 sm:px-8">
                <h1 class="text-lg font-semibold"><?= e($title ?? 'Admin') ?></h1>
                <form action="/logout" method="POST">
                    <?= csrf_field() ?>
                    <button type="submit" class="text-sm text-slate-400 hover:text-white">Cerrar sesión</button>
                </form>
            </header>
            <main class="flex-1 p-4 sm:p-8">
                <?php if ($msg = flash('success')): ?>
                    <div class="mb-6 rounded-xl border border-brand-5/30 bg-brand-5/10 px-4 py-3 text-brand-4"><?= e($msg) ?></div>
                <?php endif; ?>
                <?php if ($msg = flash('error')): ?>
                    <div class="mb-6 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-red-300"><?= e($msg) ?></div>
                <?php endif; ?>
                <?= $content ?>
            </main>
        </div>
    </div>
</body>
</html>
