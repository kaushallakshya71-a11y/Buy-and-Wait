# Buy or Wait? — React Native Android Mobile App

Autonomous AI Financial Affordability & Cash-Flow Advisor for Android.

---

## 📱 Features

1. **⚡ New User Financial Simulator**:
   - Live Bank Balance, Emergency Reserve (Suraksha Nidhi), In-hand Salary, Payday date, Fixed Monthly Expenses.
   - Test any planned purchase (OnePlus phone, Bike downpayment, Laptop).
   - Instant AI Affordability Check:
     - 🟢 **Affordable Now** (Safe to buy today in full)
     - 🔵 **Affordable with Plan** (Safe with 3M/6M Zero-Cost EMI)
     - 🟡 **Affordable Later** (Wait for next salary credit)
     - 🔴 **Not Affordable** (Would deplete emergency fund)
2. **📖 Indian Household Financial Principles**:
   - 4 Desi Financial ground rules (Emergency Nidhi, Roti-Kirana-Bills protection, Month-end crunch, Debt trap prevention).
3. **❓ User Guide & FAQs**:
   - Interactive expandable Q&A on Emergency Fund vs Bank Balance, EMI mechanics, and offline privacy.
4. **🌐 100% Bilingual**:
   - One-tap switch between **English 🇬🇧** and **हिंदी 🇮🇳**.
5. **🔒 100% Offline & Private**:
   - Zero API calls, zero server telemetry, instant calculation on device.

---

## 🚀 How to Run & Build APK

### Option A: Test Instantly on Android Phone (Using Expo Go)
1. Install **Expo Go** from Google Play Store on your Android phone.
2. In terminal, navigate to `BuyOrWaitApp`:
   ```bash
   cd BuyOrWaitApp
   npm start
   ```
3. Scan the QR code displayed in the terminal using the Expo Go app. The app will launch instantly on your device!

---

### Option B: Build Standalone Installable Android `.apk` (Via EAS Cloud Build)
This builds a direct `.apk` file that you can download and install on any Android phone without needing Android Studio locally.

1. Create a free account at [https://expo.dev/signup](https://expo.dev/signup) (if not already created).
2. Log in to your Expo account in terminal:
   ```bash
   cd BuyOrWaitApp
   npx eas login
   ```
3. Start the cloud APK build:
   ```bash
   npx eas build --platform android --profile preview
   ```
4. EAS Cloud will compile your Android APK. When finished, it will print a direct download link and QR code in the terminal.
5. Download the `.apk` file, transfer/download it to your Android device, and tap **Install**!
