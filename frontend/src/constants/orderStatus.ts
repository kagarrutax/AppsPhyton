export const ORDER_STATUS_LABELS: Record<string, { label: string; color: string }> = {
  pendiente: { label: 'Pendiente', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300' },
  pagado: { label: 'Pagado', color: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300' },
  verificado: { label: 'Verificado', color: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/40 dark:text-indigo-300' },
  preparando: { label: 'Preparando', color: 'bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300' },
  listo: { label: 'Listo', color: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300' },
  entregado: { label: 'Entregado', color: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' },
  cancelado: { label: 'Cancelado', color: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300' },
}

export const PAYMENT_STATUS_LABELS: Record<string, { label: string; color: string }> = {
  pendiente: { label: 'Pendiente', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300' },
  aprobado: { label: 'Aprobado', color: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300' },
  rechazado: { label: 'Rechazado', color: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300' },
}

export const ORDER_STATUSES = [
  'pendiente',
  'pagado',
  'verificado',
  'preparando',
  'listo',
  'entregado',
  'cancelado',
] as const
