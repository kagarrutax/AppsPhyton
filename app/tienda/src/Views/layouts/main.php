<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= e($title ?? 'Tienda') ?> | <?= e(app_config('name')) ?></title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            1: '#cf26d9',
                            2: '#d65c9f',
                            3: '#d98c90',
                            4: '#3bcc33',
                            5: '#1fad5f',
                        }
                    }
                }
            }
        }
    </script>
    <link rel="stylesheet" href="<?= asset('css/palette.css') ?>">
</head>
<body class="min-h-screen bg-slate-950 text-slate-100 antialiased hero-pattern">
    <header class="sticky top-0 z-50 border-b border-white/10 bg-slate-950/80 backdrop-blur-md">
        <nav class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
            <a href="/" class="text-xl font-bold tracking-tight">
                <span class="bg-gradient-to-r from-brand-1 via-brand-2 to-brand-3 bg-clip-text text-transparent">
                    <?= e(app_config('name')) ?>
                </span>
            </a>
            <div class="flex items-center gap-3 text-sm">
                <?php if (\App\Core\Auth::isAdmin()): ?>
                    <a href="/dashboard" class="rounded-lg px-3 py-2 text-slate-300 hover:bg-white/5 hover:text-white">Dashboard</a>
                    <a href="/admin/products" class="rounded-lg px-3 py-2 text-slate-300 hover:bg-white/5 hover:text-white">Productos</a>
                <?php endif; ?>
                <?php if (\App\Core\Auth::check()): ?>
                    <span class="hidden text-slate-400 sm:inline"><?= e(\App\Core\Auth::user()['name'] ?? '') ?></span>
                    <form action="/logout" method="POST" class="inline">
                        <?= csrf_field() ?>
                        <button type="submit" class="rounded-lg border border-white/10 px-3 py-2 text-slate-300 hover:bg-white/5">Salir</button>
                    </form>
                <?php else: ?>
                    <a href="/login" class="rounded-lg px-3 py-2 text-slate-300 hover:bg-white/5">Login</a>
                    <a href="/register" class="rounded-lg bg-gradient-to-r from-brand-1 to-brand-2 px-4 py-2 font-medium text-white shadow-lg shadow-brand-1/20">Registro</a>
                <?php endif; ?>
            </div>
        </nav>
    </header>

    <main class="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        <?php if ($msg = flash('success')): ?>
            <div class="mb-6 rounded-xl border border-brand-5/30 bg-brand-5/10 px-4 py-3 text-brand-4"><?= e($msg) ?></div>
        <?php endif; ?>
        <?php if ($msg = flash('error')): ?>
            <div class="mb-6 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-red-300"><?= e($msg) ?></div>
        <?php endif; ?>
        <?= $content ?>
    </main>

    <footer class="mt-16 border-t border-white/10 py-8 text-center text-sm text-slate-500">
        &copy; <?= date('Y') ?> <?= e(app_config('name')) ?> — Compra segura vía WhatsApp
    </footer>
</body>
</html>
