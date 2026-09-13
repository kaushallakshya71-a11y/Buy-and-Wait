import React, { useState } from 'react';
import {
  SafeAreaView,
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  StatusBar
} from 'react-native';
import SimulatorScreen from './src/screens/SimulatorScreen';
import ResultScreen from './src/screens/ResultScreen';
import GuideScreen from './src/screens/GuideScreen';
import FAQScreen from './src/screens/FAQScreen';
import { calculateSimulation } from './src/engine/affordabilityEngine';

export default function App() {
  const [lang, setLang] = useState('en'); // 'en' or 'hi'
  const [activeTab, setActiveTab] = useState('simulator'); // 'simulator' | 'guide' | 'faq'
  const [simulationResult, setSimulationResult] = useState(null);

  const isEn = lang === 'en';

  const handleCalculate = (formData) => {
    const res = calculateSimulation({ ...formData, lang });
    setSimulationResult(res);
  };

  const handleBackToSimulator = () => {
    setSimulationResult(null);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#047857" />

      {/* Header Banner */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <Text style={styles.title}>
            {isEn ? 'Buy or Wait?' : 'खरीदें या रुकें?'}
          </Text>
          <Text style={styles.subtitle}>
            {isEn
              ? 'AI Financial Affordability Advisor'
              : 'AI वित्तीय निर्णय एवं बचत सलाहकार'}
          </Text>
        </View>

        {/* Language Switcher */}
        <TouchableOpacity
          style={styles.langButton}
          onPress={() => setLang(lang === 'en' ? 'hi' : 'en')}
          activeOpacity={0.8}
        >
          <Text style={styles.langButtonText}>
            {lang === 'en' ? 'हिंदी 🇮🇳' : 'English 🇬🇧'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Main Body */}
      <View style={styles.body}>
        {simulationResult ? (
          <ResultScreen
            result={simulationResult}
            onBack={handleBackToSimulator}
            lang={lang}
          />
        ) : (
          <>
            {activeTab === 'simulator' && (
              <SimulatorScreen onCalculate={handleCalculate} lang={lang} />
            )}
            {activeTab === 'guide' && <GuideScreen lang={lang} />}
            {activeTab === 'faq' && <FAQScreen lang={lang} />}
          </>
        )}
      </View>

      {/* Bottom Tab Bar (hidden when viewing result to maximize screen space) */}
      {!simulationResult && (
        <View style={styles.bottomNav}>
          <TouchableOpacity
            style={[
              styles.navItem,
              activeTab === 'simulator' && styles.navItemActive
            ]}
            onPress={() => setActiveTab('simulator')}
          >
            <Text style={styles.navIcon}>⚡</Text>
            <Text
              style={[
                styles.navLabel,
                activeTab === 'simulator' && styles.navLabelActive
              ]}
            >
              {isEn ? 'Simulator' : 'सिमुलेटर'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.navItem, activeTab === 'guide' && styles.navItemActive]}
            onPress={() => setActiveTab('guide')}
          >
            <Text style={styles.navIcon}>📖</Text>
            <Text
              style={[
                styles.navLabel,
                activeTab === 'guide' && styles.navLabelActive
              ]}
            >
              {isEn ? 'Rules' : 'नियम'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.navItem, activeTab === 'faq' && styles.navItemActive]}
            onPress={() => setActiveTab('faq')}
          >
            <Text style={styles.navIcon}>❓</Text>
            <Text
              style={[
                styles.navLabel,
                activeTab === 'faq' && styles.navLabelActive
              ]}
            >
              {isEn ? 'FAQs' : 'सवाल'}
            </Text>
          </TouchableOpacity>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#047857'
  },
  header: {
    backgroundColor: '#047857',
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 14,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    elevation: 4
  },
  headerLeft: {
    flex: 1
  },
  title: {
    fontSize: 20,
    fontWeight: '800',
    color: '#ffffff'
  },
  subtitle: {
    fontSize: 11,
    color: '#d1fae5',
    marginTop: 2
  },
  langButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.4)'
  },
  langButtonText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '700'
  },
  body: {
    flex: 1,
    backgroundColor: '#f8fafc'
  },
  bottomNav: {
    flexDirection: 'row',
    backgroundColor: '#ffffff',
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0',
    paddingVertical: 8,
    elevation: 8
  },
  navItem: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 4
  },
  navItemActive: {
    borderTopWidth: 2,
    borderTopColor: '#047857'
  },
  navIcon: {
    fontSize: 18,
    marginBottom: 2
  },
  navLabel: {
    fontSize: 11,
    fontWeight: '600',
    color: '#64748b'
  },
  navLabelActive: {
    color: '#047857',
    fontWeight: '800'
  }
});
