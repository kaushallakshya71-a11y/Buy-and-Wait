import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';
import { formatINR } from '../utils/formatters';

export default function ResultScreen({ result, onBack, lang }) {
  if (!result) return null;
  const isEn = lang === 'en';

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Back Button */}
      <TouchableOpacity style={styles.backButton} onPress={onBack}>
        <Text style={styles.backButtonText}>
          {isEn ? '← Back to Simulator' : '← वापस सिमुलेटर पर जाएं'}
        </Text>
      </TouchableOpacity>

      {/* Status Badge */}
      <View style={[styles.statusBadge, { backgroundColor: result.statusBg, borderColor: result.statusColor }]}>
        <Text style={[styles.statusBadgeText, { color: result.statusColor }]}>
          {result.statusLabel}
        </Text>
      </View>

      {/* Main Headline */}
      <View style={styles.card}>
        <Text style={styles.headline}>{result.headline}</Text>
        <Text style={styles.explanation}>{result.explanation}</Text>
      </View>

      {/* 3 Metric Cards */}
      <View style={styles.metricsRow}>
        <View style={styles.metricCard}>
          <Text style={styles.metricTitle}>
            {isEn ? 'SAFE TODAY' : 'आज सुरक्षित'}
          </Text>
          <Text style={[styles.metricValue, { color: '#047857' }]}>
            {formatINR(result.safeToday)}
          </Text>
        </View>

        <View style={styles.metricCard}>
          <Text style={styles.metricTitle}>
            {isEn ? 'SAFE CUSHION' : 'अतिरिक्त सुरक्षा'}
          </Text>
          <Text style={styles.metricValue}>
            {formatINR(result.cushion)}
          </Text>
        </View>

        <View style={styles.metricCard}>
          <Text style={styles.metricTitle}>
            {isEn ? 'NET SAVINGS' : 'मासिक बचत'}
          </Text>
          <Text style={styles.metricValue}>
            {formatINR(result.monthlySavings)}
          </Text>
        </View>
      </View>

      {/* Recommended Action */}
      <View style={styles.card}>
        <Text style={styles.cardHeader}>
          {isEn ? 'Recommended Action Plan' : 'सिफारिश की गई कार्य योजना'}
        </Text>
        <View style={styles.actionRow}>
          <Text style={styles.actionLabel}>{isEn ? 'Method:' : 'तरीका:'}</Text>
          <Text style={styles.actionValue}>{result.recommendedMethod}</Text>
        </View>
        <View style={styles.actionRow}>
          <Text style={styles.actionLabel}>{isEn ? 'Plan:' : 'प्लान:'}</Text>
          <Text style={styles.actionValue}>{result.planText}</Text>
        </View>
        {result.waitDate ? (
          <View style={styles.actionRow}>
            <Text style={styles.actionLabel}>{isEn ? 'Earliest Safe Date:' : 'सबसे सुरक्षित तारीख:'}</Text>
            <Text style={[styles.actionValue, { color: '#b45309', fontWeight: '700' }]}>{result.waitDate}</Text>
          </View>
        ) : null}
      </View>

      {/* Insight Tip Box */}
      <View style={styles.tipBox}>
        <Text style={styles.tipTitle}>
          {isEn ? '💡 Financial Prudence Insight' : '💡 समझदारी भरी वित्तीय सीख'}
        </Text>
        <Text style={styles.tipText}>{result.tip}</Text>
      </View>

      <TouchableOpacity style={styles.recalculateButton} onPress={onBack} activeOpacity={0.85}>
        <Text style={styles.recalculateButtonText}>
          {isEn ? 'Test Another Purchase' : 'किसी अन्य सामान के लिए जांचें'}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8fafc' },
  content: { padding: 16, paddingBottom: 40 },
  backButton: { marginBottom: 12, paddingVertical: 4 },
  backButtonText: { color: '#047857', fontWeight: '700', fontSize: 14 },
  statusBadge: {
    borderWidth: 1.5,
    borderRadius: 30,
    paddingVertical: 10,
    paddingHorizontal: 16,
    alignItems: 'center',
    marginBottom: 16
  },
  statusBadgeText: { fontWeight: '800', fontSize: 14, letterSpacing: 0.5 },
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
  headline: { fontSize: 17, fontWeight: '800', color: '#0f172a', marginBottom: 8, lineHeight: 23 },
  explanation: { fontSize: 13, color: '#475569', lineHeight: 19 },
  metricsRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 16, gap: 8 },
  metricCard: {
    flex: 1,
    backgroundColor: '#ffffff',
    borderRadius: 10,
    padding: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#e2e8f0'
  },
  metricTitle: { fontSize: 10, fontWeight: '700', color: '#64748b', marginBottom: 4, letterSpacing: 0.5 },
  metricValue: { fontSize: 15, fontWeight: '800', color: '#0f172a' },
  cardHeader: { fontSize: 15, fontWeight: '700', color: '#0f172a', marginBottom: 12 },
  actionRow: { flexDirection: 'row', marginBottom: 8, flexWrap: 'wrap' },
  actionLabel: { fontSize: 13, fontWeight: '600', color: '#64748b', width: 130 },
  actionValue: { fontSize: 13, fontWeight: '600', color: '#0f172a', flex: 1 },
  tipBox: {
    backgroundColor: '#f0fdf4',
    borderLeftWidth: 4,
    borderLeftColor: '#22c55e',
    borderRadius: 10,
    padding: 14,
    marginBottom: 20
  },
  tipTitle: { fontSize: 13, fontWeight: '700', color: '#15803d', marginBottom: 4 },
  tipText: { fontSize: 12, color: '#166534', lineHeight: 18 },
  recalculateButton: {
    backgroundColor: '#0f172a',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center'
  },
  recalculateButtonText: { color: '#ffffff', fontSize: 15, fontWeight: '700' }
});
