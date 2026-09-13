import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';

export default function FAQScreen({ lang }) {
  const isEn = lang === 'en';
  const [expanded, setExpanded] = useState({ 0: true });

  const toggle = (idx) => {
    setExpanded((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const faqs = [
    {
      q: isEn
        ? 'Why was my purchase rejected even though my bank balance is higher than the price?'
        : 'बैंक बैलेंस होने के बाद भी AI ने खरीदारी को सुरक्षित क्यों नहीं माना?',
      a: isEn
        ? 'Because your Emergency Reserve and fixed debits (rent, groceries, bills) before your next payday are deducted first. If your balance is ₹50,000 and the phone is ₹40,000, but your emergency reserve is ₹25,000, your spendable cushion is only ₹25,000. The AI strictly protects your emergency cushion.'
        : 'क्योंकि आपके बैलेंस में से इमरजेंसी फंड और अगली सैलरी तक के जरूरी खर्च (किराया, राशन, बिल) पहले घटाए जाते हैं। यदि बैलेंस ₹50,000 है और फोन ₹40,000 का है लेकिन सुरक्षा निधि ₹25,000 है, तो खर्च योग्य बचत केवल ₹25,000 है।'
    },
    {
      q: isEn
        ? 'When does the AI recommend a No-Cost EMI instead of full payment?'
        : 'एकमुश्त भुगतान के बजाय No-Cost EMI कब सुझाई जाती है?',
      a: isEn
        ? 'When paying in full would drain your emergency reserve below the safety threshold, but your monthly surplus savings (Salary minus Fixed Expenses) can comfortably cover the monthly installment without any stress.'
        : 'जब पूरा पैसा एक साथ देने से इमरजेंसी फंड खत्म हो रहा हो, लेकिन आपकी हर महीने की बचत (सैलरी में से खर्चे घटाकर) आसानी से मासिक किस्त भर सकती हो।'
    },
    {
      q: isEn
        ? 'What is the "30-Day Bachat Rule" behind the Wait recommendation?'
        : 'Wait (इंतजार करें) सलाह के पीछे "30-दिन का बचत नियम" क्या है?',
      a: isEn
        ? 'When a purchase is deferred until your next salary date, it protects your month-end liquidity and prevents impulse spending. If you still desire the item after payday, you can purchase it safely.'
        : 'जब किसी बड़े खर्च को अगली सैलरी तक टाल दिया जाता है, तो जल्दबाजी में की गई खरीदारी से बचाव होता है और महीने के आखिरी दिनों में नकदी का संकट नहीं होता।'
    },
    {
      q: isEn
        ? 'Is my personal financial data secure and private?'
        : 'क्या मेरा वित्तीय डेटा सुरक्षित और निजी है?',
      a: isEn
        ? 'Yes, 100%. All calculations and simulations execute entirely locally on your mobile device. Zero financial data is sent to external servers or cloud APIs.'
        : 'हाँ, 100% सुरक्षित। सारा सिमुलेशन आपके फोन पर स्थानीय रूप से चलता है। कोई भी डेटा किसी सर्वर पर नहीं भेजा जाता।'
    }
  ];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.heading}>
        {isEn ? 'User Guide & Frequently Asked Questions' : 'उपयोगकर्ता गाइड और सामान्य प्रश्न'}
      </Text>
      <Text style={styles.subheading}>
        {isEn
          ? 'Answers to common questions regarding financial simulations, EMIs, and emergency reserves.'
          : 'वित्तीय सिमुलेशन, नो-कॉस्ट ईएमआई और आपातकालीन फंड से जुड़े अक्सर पूछे जाने वाले सवाल।'}
      </Text>

      {faqs.map((item, idx) => {
        const isOpen = !!expanded[idx];
        return (
          <View key={idx} style={styles.faqCard}>
            <TouchableOpacity
              style={styles.questionRow}
              onPress={() => toggle(idx)}
              activeOpacity={0.7}
            >
              <Text style={styles.questionText}>{item.q}</Text>
              <Text style={styles.arrow}>{isOpen ? '▲' : '▼'}</Text>
            </TouchableOpacity>

            {isOpen ? (
              <View style={styles.answerContainer}>
                <Text style={styles.answerText}>{item.a}</Text>
              </View>
            ) : null}
          </View>
        );
      })}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8fafc' },
  content: { padding: 16, paddingBottom: 40 },
  heading: { fontSize: 18, fontWeight: '800', color: '#0f172a', marginBottom: 6 },
  subheading: { fontSize: 13, color: '#64748b', marginBottom: 18, lineHeight: 18 },
  faqCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#e2e8f0',
    overflow: 'hidden'
  },
  questionRow: {
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#ffffff'
  },
  questionText: { fontSize: 14, fontWeight: '700', color: '#0f172a', flex: 1, paddingRight: 10 },
  arrow: { fontSize: 12, color: '#047857', fontWeight: 'bold' },
  answerContainer: {
    paddingHorizontal: 16,
    paddingBottom: 16,
    paddingTop: 4,
    borderTopWidth: 1,
    borderTopColor: '#f1f5f9'
  },
  answerText: { fontSize: 13, color: '#475569', lineHeight: 20 }
});
