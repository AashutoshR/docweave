export function formatMoney(amount, currency) {
  return new Intl.NumberFormat('en', { style: 'currency', currency }).format(amount / 100);
}
