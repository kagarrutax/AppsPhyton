import { ORDER_STATUS_LABELS, PAYMENT_STATUS_LABELS } from '../../constants/orderStatus'

export function StatusBadge({ status, type = 'order' }: { status: string; type?: 'order' | 'payment' }) {
  const map = type === 'payment' ? PAYMENT_STATUS_LABELS : ORDER_STATUS_LABELS
  const st = map[status] || { label: status, color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200' }
  return (
    <span className={`text-xs font-semibold px-3 py-1 rounded-full ${st.color}`}>
      {st.label}
    </span>
  )
}
