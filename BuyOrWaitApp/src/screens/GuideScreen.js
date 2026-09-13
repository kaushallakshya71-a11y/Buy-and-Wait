import React from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';

export default function GuideScreen({ lang }) {
  const isEn = lang === 'en';

  const rules = [
    {
      title: isEn ? '1. Emergency Nidhi (Safety Reserve)' : '1. सुरक्षा कवच (इमरजेंसी निधि)',
      desc: isEn
        ? 'Households require 3 to 6 months of living expenses for health crises, job shifts, or unforeseen events. The AI agent strictly enforces that this minimum balance is never breached.'
        : 'हर परिवार को 3 से 6 महीने का खर्च आपात स्थिति के लिए रखना आवश्यक है। AI सुनिश्चित करता है कि यह न्यूनतम बैलेंस किसी भी खरीदारी के लिए कभी खर्च न हो।',
      border: '#15803d'
    },
    {
      title: isEn ? '2. Roti, Kirana & Family Support' : '2. रोटी, राशन और परिवार सहायता',
      desc: isEn
        ? 'Rent, electricity bills, school fees, and allowances sent to parents are non-negotiable protected commitments. Zero cuts are permitted from these essential categories.'
        : 'किराया, बिजली का बिल, बच्चों की फीस और माता-पिता को भेजे जाने वाले पैसे सुरक्षित श्रेणियां हैं। इनमें ₹1 की भी कटौती की अनुमति नहीं है।',
      border: '#1d4ed8'
    },
    {
      title: isEn ? '3. Month-End Salary Crunch' : '3. महीने का अंतिम हफ्ता व सैलरी चक्र',
      desc: isEn
        ? 'When purchases occur late in the monthly salary cycle (25th–30th), the AI recommends waiting a few days for salary settlement to prevent month-end cash flow stress.'
        : 'यदि खरीदारी महीने के अंत में हो रही है, तो AI 5-10 दिन रुककर अगली सैलरी का इंतजार करने की सलाह देता है ताकि कैश की कमी न हो।',
      border: '#a16207'
    },
    {
      title: isEn ? '4. Zero-Cost EMI vs Debt Trap' : '4. No-Cost EMI बनाम कर्ज का जाल',
      desc: isEn
        ? 'Installments are recommended only when monthly commitments are comfortably covered by net surplus savings, ensuring you never fall into credit card rollover debt.'
        : 'किस्त (EMI) तभी सुझाई जाती है जब आपकी मासिक बचत उस किस्त को आसानी से वहन कर सके, ताकि आप क्रेडिट कार्ड के ब्याज के जाल में न फंसें।',
      border: '#b91c1c'
    }
  ];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.heading}>
        {isEn ? 'Indian Household Financial Ground Rules' : 'भारतीय परिवारों के लिए वित्तीय नियम'}
      </Text>
      <Text style={styles.subheading}>
        {isEn
          ? 'Core principles designed for middle-class and salaried households to build wealth without taking uncalculated debt.'
          : 'मध्यमवर्गीय और नौकरीपेशा परिवारों को बिना किसी अनावश्यक कर्ज के सुरक्षित रखने वाले मार्गदर्शक सिद्धांत।'}
      </Text>

      {rules.map((rule, idx) => (
        <View key={idx} style={[styles.ruleCard, { borderLeftColor: rule.border }]}>
          <Text style={[styles.ruleTitle, { color: rule.border }]}>{rule.title}</Text>
          <Text style={styles.ruleDesc}>{rule.desc}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8fafc' },
  content: { padding: 16, paddingBottom: 40 },
  heading: { fontSize: 18, fontWeight: '800', color: '#0f172a', marginBottom: 6 },
  subheading: { fontSize: 13, color: '#64748b', marginBottom: 18, lineHeight: 18 },
  ruleCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 14,
    borderLeftWidth: 5,
    borderWidth: 1,
    borderColor: '#e2e8f0',
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 5,
    shadowOffset: { width: 0, height: 2 }
  },
  ruleTitle: { fontSize: 15, fontWeight: '700', marginBottom: 6 },
  ruleDesc: { fontSize: 13, color: '#334155', lineHeight: 19 }
});
