export function formatINR(val) {
  if (val === null || val === undefined || isNaN(val)) {
    return '₹0';
  }
  const isNegative = val < 0;
  const absVal = Math.round(Math.abs(val));
  const s = absVal.toString();

  if (s.length <= 3) {
    return `${isNegative ? '-₹' : '₹'}${s}`;
  }

  let lastThree = s.substring(s.length - 3);
  let otherNumbers = s.substring(0, s.length - 3);
  if (otherNumbers !== '') {
    lastThree = ',' + lastThree;
  }
  const formattedOther = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ',');
  return `${isNegative ? '-₹' : '₹'}${formattedOther}${lastThree}`;
}
