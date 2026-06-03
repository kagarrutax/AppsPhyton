<section class="mb-12 text-center">
    <p class="mb-2 text-sm font-medium uppercase tracking-widest text-brand-2">Catálogo en línea</p>
    <h1 class="mb-4 text-4xl font-bold sm:text-5xl">
        Descubre nuestros
        <span class="bg-gradient-to-r from-brand-1 to-brand-3 bg-clip-text text-transparent">productos</span>
    </h1>
    <p class="mx-auto max-w-2xl text-slate-400">
        Selecciona un producto y contáctanos al instante por WhatsApp para completar tu compra.
    </p>
</section>

<?php if (empty($products)): ?>
    <div class="rounded-2xl border border-dashed border-white/20 py-16 text-center text-slate-400">
        No hay productos disponibles en este momento.
    </div>
<?php else: ?>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <?php foreach ($products as $product): ?>
            <?php
                $waUrl = whatsapp_buy_url($product['name'], (float) $product['price']);
                $img = $product['image'] ? asset($product['image']) : null;
            ?>
            <article class="product-card flex flex-col overflow-hidden rounded-2xl border border-white/10 bg-slate-900/60">
                <div class="relative aspect-square bg-gradient-to-br from-slate-800 to-slate-900">
                    <?php if ($img): ?>
                        <img src="<?= e($img) ?>" alt="<?= e($product['name']) ?>" class="h-full w-full object-cover">
                    <?php else: ?>
                        <div class="flex h-full items-center justify-center gradient-brand opacity-20">
                            <svg class="h-16 w-16 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                            </svg>
                        </div>
                    <?php endif; ?>
                    <span class="absolute right-3 top-3 rounded-full bg-brand-1/90 px-3 py-1 text-xs font-semibold text-white">
                        <?= e(format_price((float) $product['price'])) ?>
                    </span>
                </div>
                <div class="flex flex-1 flex-col p-5">
                    <h2 class="mb-2 text-lg font-semibold text-white"><?= e($product['name']) ?></h2>
                    <p class="mb-4 flex-1 text-sm leading-relaxed text-slate-400 line-clamp-3">
                        <?= e($product['description']) ?>
                    </p>
                    <a
                        href="<?= e($waUrl) ?>"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="btn-whatsapp inline-flex items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-5/25 transition"
                    >
                        <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.611.611l4.458-1.495A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 01-5.006-1.372l-.357-.213-2.642.886.886-2.578-.233-.374A9.818 9.818 0 1112 21.818z"/></svg>
                        Comprar por WhatsApp
                    </a>
                </div>
            </article>
        <?php endforeach; ?>
    </div>
<?php endif; ?>
