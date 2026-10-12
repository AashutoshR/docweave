/**
 * Cart maths shared by the checkout page.
 */

import { formatMoney } from './money';

/**
 * Sum the line items of a cart.
 * @param {Array<{price: number, qty: number}>} items - Line items.
 * @returns {number} Total in minor units.
 */
export function total(items, taxRate = 0) {
  const net = items.reduce((sum, item) => sum + item.price * item.qty, 0);
  return Math.round(net * (1 + taxRate));
}

/**
 * Render the cart total for display.
 * @param {Array} items - Line items.
 * @param {string} currency - ISO currency code.
 * @returns {string} Formatted total.
 */
export const renderTotal = (items, currency) => formatMoney(total(items), currency);
