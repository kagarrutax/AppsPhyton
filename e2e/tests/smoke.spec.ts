import { test, expect } from '@playwright/test'

test.describe('Tienda pública', () => {
  test('carga la página principal con productos', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/FastFood/)
    await expect(page.getByRole('button', { name: 'Menú' })).toBeVisible()
  })

  test('navega al login', async ({ page }) => {
    await page.goto('/')
    await page.getByRole('button', { name: 'Ingresar' }).click()
    await expect(page).toHaveURL(/\/login/)
    await expect(page.getByRole('heading', { name: /Bienvenido/i })).toBeVisible()
  })
})

test.describe('Flujo admin', () => {
  test('login admin redirige al panel', async ({ page }) => {
    await page.goto('/login')
    await page.locator('input[type="email"]').fill('admin@admin.com')
    await page.locator('input[type="password"]').fill('Admin123*')
    await page.getByRole('button', { name: 'Ingresar' }).click()
    await expect(page).toHaveURL(/\/admin/)
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
  })

  test('dashboard muestra KPIs', async ({ page }) => {
    await page.goto('/login')
    await page.locator('input[type="email"]').fill('admin@admin.com')
    await page.locator('input[type="password"]').fill('Admin123*')
    await page.getByRole('button', { name: 'Ingresar' }).click()
    await expect(page.getByText('Ventas totales')).toBeVisible()
    await expect(page.getByText('Pedidos').first()).toBeVisible()
  })
})

test.describe('Flujo cliente', () => {
  test('registro y acceso al carrito', async ({ page }) => {
    const email = `cliente_${Date.now()}@test.com`

    await page.goto('/register')
    await page.locator('form .grid input').first().fill('Cliente')
    await page.locator('form .grid input').nth(1).fill('E2E')
    await page.locator('input[type="email"]').fill(email)
    await page.locator('input[type="password"]').fill('Cliente123*')
    await page.getByRole('button', { name: 'Registrarse' }).click()

    await expect(page).toHaveURL('/')
    await page.goto('/cart')
    await expect(page.getByRole('heading', { name: /Tu carrito/i })).toBeVisible()
  })
})
