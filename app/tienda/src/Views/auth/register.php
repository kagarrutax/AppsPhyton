<div class="mx-auto max-w-md">
    <div class="rounded-2xl border border-white/10 bg-slate-900/60 p-8 shadow-xl">
        <h1 class="mb-2 text-2xl font-bold">Crear cuenta</h1>
        <p class="mb-6 text-sm text-slate-400">Regístrate para acceder a la tienda.</p>
        <form action="/register" method="POST" class="space-y-4">
            <?= csrf_field() ?>
            <div>
                <label for="name" class="mb-1 block text-sm text-slate-300">Nombre</label>
                <input type="text" id="name" name="name" required
                    class="w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3 text-white outline-none focus:border-brand-1">
            </div>
            <div>
                <label for="email" class="mb-1 block text-sm text-slate-300">Email</label>
                <input type="email" id="email" name="email" required
                    class="w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3 text-white outline-none focus:border-brand-1">
            </div>
            <div>
                <label for="password" class="mb-1 block text-sm text-slate-300">Contraseña</label>
                <input type="password" id="password" name="password" required minlength="6"
                    class="w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3 text-white outline-none focus:border-brand-1">
            </div>
            <div>
                <label for="password_confirmation" class="mb-1 block text-sm text-slate-300">Confirmar contraseña</label>
                <input type="password" id="password_confirmation" name="password_confirmation" required minlength="6"
                    class="w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3 text-white outline-none focus:border-brand-1">
            </div>
            <button type="submit" class="w-full rounded-xl bg-gradient-to-r from-brand-4 to-brand-5 py-3 font-semibold text-white">
                Registrarme
            </button>
        </form>
        <p class="mt-6 text-center text-sm text-slate-400">
            ¿Ya tienes cuenta?
            <a href="/login" class="text-brand-2 hover:underline">Inicia sesión</a>
        </p>
    </div>
</div>
