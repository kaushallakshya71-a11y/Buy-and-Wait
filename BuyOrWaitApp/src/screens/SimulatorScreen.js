import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  Switch
} from 'react-native';
import { formatINR } from '../utils/formatters';

export default function SimulatorScreen({ onCalculate, lang }) {
  const isEn = lang === 'en';

  const [itemName, setItemName] = useState('OnePlus Smartphone');
  const [itemPrice, setItemPrice] = useState('32000');
  const [bankBalance, setBankBalance] = useState('65000');
  const [minBalance, setMinBalance] = useState('25000');
  const [salary, setSalary] = useState('50000');
  const [payday, setPayday] = useState('1');
  const [monthlyExpenses, setMonthlyExpenses] = useState('30000');
  const [emiAvailable, setEmiAvailable] = useState(true);

  const handleRun = () => {
    onCalculate({
      itemName,
      itemPrice,
      bankBalance,
      minBalance,
      salary,
      payday,
      monthlyExpenses,
      emiAvailable
    });
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Banner */}
      <View style={styles.banner}>
        <Text style={styles.bannerTitle}>
          {isEn ? '💡 3-Step Financial Reality Check' : '💡 3 चरणों में वित्तीय सुरक्षा जांच'}
        </Text>
        <Text style={styles.bannerSubtitle}>
          {isEn
            ? 'Enter your live balance and upcoming purchase. The AI simulates 90 days of cash flow to protect your emergency buffer.'
            : 'अपना बैंक बैलेंस और खर्च भरें। AI अगले 90 दिनों का सिमुलेशन करके बताएगा कि क्या यह खर्च सुरक्षित है।'}
        </Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardHeader}>
          {isEn ? '1. Planned Purchase Details' : '1. नियोजित खरीदारी का विवरण'}
        </Text>

        <Text style={styles.label}>
          {isEn ? 'Item Name (e.g. Phone, Bike, Laptop)' : 'सामान का नाम (उदा. फोन, बाइक, लैपटॉप)'}
        </Text>
        <TextInput
          style={styles.input}
          value={itemName}
          onChangeText={setItemName}
          placeholder="e.g. OnePlus Smartphone"
        />

        <Text style={styles.label}>
          {isEn ? 'Purchase Amount (₹)' : 'खरीदारी की कीमत (₹)'}
        </Text>
        <TextInput
          style={styles.input}
          value={itemPrice}
          onChangeText={setItemPrice}
          keyboardType="numeric"
          placeholder="32000"
        />

        <View style={styles.switchRow}>
          <View style={{ flex: 1 }}>
            <Text style={styles.switchLabel}>
              {isEn ? 'No-Cost EMI Available?' : 'क्या No-Cost EMI उपलब्ध है?'}
            </Text>
            <Text style={styles.helperText}>
              {isEn ? '3 or 6 month zero interest option' : '3 या 6 महीने की बिना ब्याज वाली किस्त'}
            </Text>
          </View>
          <Switch
            value={emiAvailable}
            onValueChange={setEmiAvailable}
            trackColor={{ false: '#cbd5e1', true: '#86efac' }}
            thumbColor={emiAvailable ? '#15803d' : '#94a3b8'}
          />
        </View>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardHeader}>
          {isEn ? '2. Your Financial Reality & Safety Net' : '2. आपकी वित्तीय स्थिति और सुरक्षा निधि'}
        </Text>

        <Text style={styles.label}>
          {isEn ? 'Current Available Bank Balance (₹)' : 'वर्तमान बैंक बैलेंस (₹)'}
        </Text>
        <TextInput
          style={styles.input}
          value={bankBalance}
          onChangeText={setBankBalance}
          keyboardType="numeric"
          placeholder="65000"
        />

        <Text style={styles.label}>
          {isEn ? 'Emergency Fund to Keep Untouched (₹)' : 'आपातकालीन फंड (Emergency Reserve) (₹)'}
        </Text>
        <TextInput
          style={styles.input}
          value={minBalance}
          onChangeText={setMinBalance}
          keyboardType="numeric"
          placeholder="25000"
        />
        <Text style={styles.helperText}>
          {isEn ? '🛡️ The AI will never let balance drop below this.' : '🛡️ AI कभी भी आपके बैलेंस को इससे नीचे नहीं गिरने देगा।'}
        </Text>

        <Text style={[styles.label, { marginTop: 12 }]}>
          {isEn ? 'Monthly In-Hand Salary (₹)' : 'मासिक इन-हैंड सैलरी (₹)'}
        </Text>
        <TextInput
          style={styles.input}
          value={salary}
          onChangeText={setSalary}
          keyboardType="numeric"
          placeholder="50000"
        />

        <Text style={styles.label}>
          {isEn ? 'Salary Credit Day of Month (1-31)' : 'सैलरी आने की तारीख (1-31)'}
        </Text>
        <TextInput
          style={styles.input}
          value={payday}
          onChangeText={setPayday}
          keyboardType="numeric"
          placeholder="1"
        />

        <Text style={styles.label}>
          {isEn ? 'Fixed Monthly Expenses (Rent + Ration + Bills) (₹)' : 'मासिक जरूरी खर्चे (किराया + राशन + बिल) (₹)'}
        </Text>
        <TextInput
          style={styles.input}
          value={monthlyExpenses}
          onChangeText={setMonthlyExpenses}
          keyboardType="numeric"
          placeholder="30000"
        />
      </View>

      <TouchableOpacity style={styles.button} onPress={handleRun} activeOpacity={0.85}>
        <Text style={styles.buttonText}>
          {isEn ? '⚡ Run AI Financial Reality Check' : '⚡ AI वित्तीय निर्णय चेक करें'}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8fafc' },
  content: { padding: 16, paddingBottom: 40 },
  banner: {
    backgroundColor: '#ecfdf5',
    borderWidth: 1,
    borderColor: '#a7f3d0',
    borderRadius: 12,
    padding: 14,
    marginBottom: 16
  },
  bannerTitle: { fontSize: 15, fontWeight: '700', color: '#065f46', marginBottom: 4 },
  bannerSubtitle: { fontSize: 12, color: '#047857', lineHeight: 17 },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 14,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#e2e8f0',
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 }
  },
  cardHeader: { fontSize: 16, fontWeight: '700', color: '#0f172a', marginBottom: 12 },
  label: { fontSize: 13, fontWeight: '600', color: '#334155', marginBottom: 6 },
  input: {
    backgroundColor: '#f1f5f9',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 15,
    color: '#0f172a',
    borderWidth: 1,
    borderColor: '#cbd5e1',
    marginBottom: 10
  },
  helperText: { fontSize: 11, color: '#64748b', marginTop: -6, marginBottom: 8 },
  switchRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderTopWidth: 1,
    borderTopColor: '#f1f5f9',
    marginTop: 4
  },
  switchLabel: { fontSize: 13, fontWeight: '600', color: '#334155' },
  button: {
    backgroundColor: '#047857',
    borderRadius: 12,
    paddingVertical: 15,
    alignItems: 'center',
    marginTop: 4,
    elevation: 3,
    shadowColor: '#047857',
    shadowOpacity: 0.3,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 3 }
  },
  buttonText: { color: '#ffffff', fontSize: 16, fontWeight: '700' }
});
