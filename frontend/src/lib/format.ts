export function formatMoney(value: number | string) {
  return `$${Number(value).toFixed(2)}`
}

export function formatDate(value: string) {
  return new Date(value).toLocaleString('es', { dateStyle: 'medium', timeStyle: 'short' })
}
