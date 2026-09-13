import { formatINR } from '../utils/formatters.js';

export function calculateSimulation({
  itemName,
  itemPrice,
  bankBalance,
  minBalance,
  salary,
  payday,
  monthlyExpenses,
  emiAvailable,
  lang = 'en'
}) {
  const price = parseFloat(itemPrice) || 0;
  const balance = parseFloat(bankBalance) || 0;
  const minBal = parseFloat(minBalance) || 0;
  const sal = parseFloat(salary) || 0;
  const expenses = parseFloat(monthlyExpenses) || 0;
  const pDay = parseInt(payday, 10) || 1;

  const cushion = Math.max(0, balance - minBal);
  const monthlySavings = Math.max(0, sal - expenses);

  const today = new Date();
  const currentDay = today.getDate();

  let daysToPayday = 0;
  if (pDay >= currentDay) {
    daysToPayday = pDay - currentDay;
  } else {
    daysToPayday = 30 - currentDay + pDay;
  }

  const dailySpend = expenses / 30.0;
  const commitmentsBeforePayday = dailySpend * daysToPayday;
  const safeToday = Math.max(0, Math.min(price, cushion - commitmentsBeforePayday));

  const nextPayday = new Date(today);
  nextPayday.setDate(today.getDate() + daysToPayday);
  const nextPaydayStr = nextPayday.toISOString().split('T')[0];

  const payday2 = new Date(nextPayday);
  payday2.setDate(payday2.getDate() + 30);
  const payday2Str = payday2.toISOString().split('T')[0];

  const isEn = lang === 'en';

  // 1. AFFORDABLE NOW
  if (safeToday >= price) {
    return {
      statusCode: 'affordable_now',
      statusLabel: isEn ? 'AFFORDABLE NOW (Safe Today)' : 'AFFORDABLE NOW (आज ही खरीद सकते हैं)',
      statusColor: '#15803d',
      statusBg: '#dcfce7',
      safeToday,
      cushion,
      monthlySavings,
      headline: isEn
        ? `You can safely purchase ${itemName} in full today!`
        : `आप ${itemName} को आज ही पूरा पेमेंट करके बिना किसी चिंता के खरीद सकते हैं!`,
      explanation: isEn
        ? `Your Emergency Reserve (${formatINR(minBal)}) remains 100% untouched, and your bank balance comfortably handles all bills & living expenses until your next salary credit on ${nextPaydayStr}.`
        : `आपका इमरजेंसी फंड (${formatINR(minBal)}) पूरी तरह सुरक्षित है, और अगली सैलरी (${nextPaydayStr}) आने तक के राशन व बिल निकालने के बाद भी बैलेंस पर्याप्त है।`,
      recommendedMethod: isEn ? 'Full Payment (One-Time)' : 'एकमुश्त भुगतान (Full Payment)',
      planText: isEn ? `Pay full ${formatINR(price)} today.` : `आज ही ${formatINR(price)} का भुगतान करें।`,
      waitDate: null,
      tip: isEn
        ? `Smart & safe decision! After this purchase, your safety buffer of ${formatINR(minBal)} remains completely preserved.`
        : `उत्कृष्ट निर्णय! यह खरीदारी करने के बाद भी आपकी ${formatINR(minBal)} की आपातकालीन निधि सुरक्षित रहेगी।`
    };
  }

  // 2. AFFORDABLE WITH PLAN (No-Cost EMI)
  const emi3m = price / 3.0;
  const emi6m = price / 6.0;

  if (emiAvailable && monthlySavings >= emi3m && cushion >= emi3m) {
    return {
      statusCode: 'affordable_with_plan',
      statusLabel: isEn ? 'AFFORDABLE WITH PLAN (3M No-Cost EMI)' : 'AFFORDABLE WITH PLAN (3 महीने की No-Cost EMI)',
      statusColor: '#1d4ed8',
      statusBg: '#dbeafe',
      safeToday,
      cushion,
      monthlySavings,
      headline: isEn
        ? `Recommended: 3 Months No-Cost EMI of ${formatINR(emi3m)}/month.`
        : `सलाह: 3 महीने की No-Cost EMI लें (${formatINR(emi3m)} प्रति माह)।`,
      explanation: isEn
        ? `Paying ${formatINR(price)} in full today would dip into your safety reserve. However, your monthly net surplus (${formatINR(monthlySavings)}) comfortably covers the ${formatINR(emi3m)} monthly installment.`
        : `एक साथ ${formatINR(price)} देने से आपका इमरजेंसी फंड कम हो जाएगा। लेकिन आपकी मासिक बचत (${formatINR(monthlySavings)}) से ₹${Math.round(emi3m)} की EMI आसानी से निकल जाएगी।`,
      recommendedMethod: isEn ? '3-Month No-Cost EMI' : '3 महीने की No-Cost EMI',
      planText: isEn
        ? `3 equal installments of ${formatINR(emi3m)} starting today.`
        : `आज से शुरू होकर हर माह ${formatINR(emi3m)} की 3 किस्तें।`,
      waitDate: null,
      tip: isEn
        ? `Zero-Cost EMI is safe because monthly installments are under 50% of your net monthly savings surplus.`
        : `यह EMI सुरक्षित है क्योंकि मासिक किस्त आपकी शुद्ध बचत के 50% से भी कम है।`
    };
  }

  if (emiAvailable && monthlySavings >= emi6m && cushion >= emi6m) {
    return {
      statusCode: 'affordable_with_plan',
      statusLabel: isEn ? 'AFFORDABLE WITH PLAN (6M No-Cost EMI)' : 'AFFORDABLE WITH PLAN (6 महीने की No-Cost EMI)',
      statusColor: '#1d4ed8',
      statusBg: '#dbeafe',
      safeToday,
      cushion,
      monthlySavings,
      headline: isEn
        ? `Recommended: 6 Months No-Cost EMI of ${formatINR(emi6m)}/month.`
        : `सलाह: 6 महीने की No-Cost EMI लें (${formatINR(emi6m)} प्रति माह)।`,
      explanation: isEn
        ? `Full payment would risk month-end cash flow. A 6-month installment of ${formatINR(emi6m)} fits well within your monthly savings of ${formatINR(monthlySavings)}.`
        : `एकमुश्त भुगतान से महीने के अंत में परेशानी हो सकती है। 6 माह की किस्त (${formatINR(emi6m)}) आपकी मासिक बचत (${formatINR(monthlySavings)}) में सुरक्षित फिट बैठती है।`,
      recommendedMethod: isEn ? '6-Month No-Cost EMI' : '6 महीने की No-Cost EMI',
      planText: isEn
        ? `6 installments of ${formatINR(emi6m)} monthly.`
        : `हर महीने ${formatINR(emi6m)} की 6 आसान किस्तें।`,
      waitDate: null,
      tip: isEn
        ? `Ensure you do not take any additional EMIs during these 6 months to avoid lifestyle debt.`
        : `ध्यान रखें कि इन 6 महीनों के दौरान कोई अन्य नया लोन या EMI न लें।`
    };
  }

  // 3. AFFORDABLE LATER (Wait for Payday)
  if (cushion + monthlySavings >= price) {
    return {
      statusCode: 'affordable_later',
      statusLabel: isEn ? 'AFFORDABLE LATER (Wait for Salary)' : 'AFFORDABLE LATER (सैलरी आने का इंतजार करें)',
      statusColor: '#a16207',
      statusBg: '#fef9c3',
      safeToday,
      cushion,
      monthlySavings,
      headline: isEn
        ? `Wait ${daysToPayday} days until your next salary credit on ${nextPaydayStr}.`
        : `अगली सैलरी (${nextPaydayStr}) आने तक सिर्फ ${daysToPayday} दिन रुकें।`,
      explanation: isEn
        ? `Purchasing right now risks your emergency cushion or month-end commitments. Once your salary arrives on ${nextPaydayStr}, you will have ${formatINR(cushion + monthlySavings)} safe liquidity.`
        : `अभी खरीदने से इमरजेंसी फंड या महीने के जरूरी खर्चों में रुकावट आ सकती है। ${nextPaydayStr} को सैलरी आते ही आपके पास पर्याप्त लिक्विड कैश होगा।`,
      recommendedMethod: isEn ? 'Wait for Next Salary Credit' : 'सैलरी क्रेडिट तक प्रतीक्षा (Wait)',
      planText: isEn ? `Wait until ${nextPaydayStr}, then pay in full.` : `${nextPaydayStr} तक रुकें, फिर एकमुश्त खरीदें।`,
      waitDate: nextPaydayStr,
      tip: isEn
        ? `The '30-Day Bachat Rule': Delaying an impulsive purchase by 5–15 days prevents remorse and protects month-end peace of mind.`
        : `30-दिन का बचत नियम: सैलरी से 5-10 दिन पहले बड़ा खर्च टालने से महीने के अंत का तनाव खत्म हो जाता है।`
    };
  }

  if (cushion + 2 * monthlySavings >= price) {
    return {
      statusCode: 'affordable_later',
      statusLabel: isEn ? 'AFFORDABLE LATER (Wait 2 Salary Cycles)' : 'AFFORDABLE LATER (2 महीने बचत करें)',
      statusColor: '#a16207',
      statusBg: '#fef9c3',
      safeToday,
      cushion,
      monthlySavings,
      headline: isEn
        ? `Save for 2 months until ${payday2Str}.`
        : `2 महीने रुकें और बचत पूरी होने पर ${payday2Str} को खरीदें।`,
      explanation: isEn
        ? `Accumulate 2 months of monthly savings (${formatINR(monthlySavings * 2)}) alongside your cushion to purchase safely without resorting to high-interest debt.`
        : `2 महीने की बचत (${formatINR(monthlySavings * 2)}) जमा करके बिना किसी ब्याज वाले कर्ज के सुरक्षित खरीदें।`,
      recommendedMethod: isEn ? '2-Month Savings Plan' : '2 महीने की बचत योजना',
      planText: isEn ? `Accumulate savings until ${payday2Str}.` : `${payday2Str} तक बचत करें फिर खरीदें।`,
      waitDate: payday2Str,
      tip: isEn
        ? `Patience avoids interest charges and preserves your credit score.`
        : `थोड़ा धैर्य आपको महंगे क्रेडिट कार्ड ब्याज से बचाता है।`
    };
  }

  // 4. NOT AFFORDABLE
  return {
    statusCode: 'not_affordable',
    statusLabel: isEn ? 'NOT AFFORDABLE (Not Recommended)' : 'NOT AFFORDABLE (अभी खरीदारी न करें)',
    statusColor: '#b91c1c',
    statusBg: '#fee2e2',
    safeToday: 0,
    cushion,
    monthlySavings,
    headline: isEn
      ? `Purchasing ${itemName} now is financially risky.`
      : `${itemName} अभी खरीदना आपके बजट के लिए जोखिम भरा है।`,
    explanation: isEn
      ? `This purchase of ${formatINR(price)} would immediately wipe out your emergency reserves (${formatINR(minBal)}) and cause immediate distress for fixed family obligations (rent, food, bills).`
      : `इस खरीदारी (${formatINR(price)}) से आपकी पूरी सुरक्षा निधि समाप्त हो जाएगी और घर के जरूरी खर्चों (किराया, राशन) पर असर पड़ेगा।`,
    recommendedMethod: isEn ? 'Do Not Proceed / Postpone' : 'खरीदारी रद्द करें / टालें',
    planText: isEn ? 'Postpone purchase or look for budget alternatives.' : 'अभी यह खरीदारी टालें या सस्ता विकल्प खोजें।',
    waitDate: null,
    tip: isEn
      ? `Protect your family's financial security first. Build up at least 3 months of emergency expenses before reconsidering.`
      : `परिवार की वित्तीय सुरक्षा को पहली प्राथमिकता दें। कम से कम 3 महीने का सुरक्षा फंड तैयार होने तक प्रतीक्षा करें।`
  };
}
