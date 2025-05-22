import streamlit as st

# 🔤 Dil seçimi
dil = st.selectbox("Dil / Language", ("Türkçe", "English"))

# 🌐 Metinleri dile göre gösteren fonksiyon
def metin(turkce, ingilizce):
    return turkce if dil == "Türkçe" else ingilizce

# 🧪 Batarya türleri ve hücre voltajı önerileri
batarya_turleri = {
    "Li-ion (3.7V)": 3.7,
    "LiFePO4 (3.2V)": 3.2,
    "Kurşun Asit (2V)": 2.0,
    "Özel / Manuel": None
}

st.title(metin("🔋 Batarya Konfigürasyon Hesaplayıcı", "🔋 Battery Configuration Calculator"))

# 🔌 Batarya türü seçimi
tur = st.selectbox(metin("Batarya Türünü Seçin", "Select Battery Type"), list(batarya_turleri.keys()))

if batarya_turleri[tur] is not None:
    cell_voltage = batarya_turleri[tur]
    st.info(metin(f"Otomatik hücre voltajı: {cell_voltage} V", f"Auto cell voltage: {cell_voltage} V"))
else:
    cell_voltage = st.number_input(metin("Hücre Voltajı (V)", "Cell Voltage (V)"), value=3.7)

# 🧾 Hücre bilgileri
cell_capacity = st.number_input(metin("Hücre Kapasitesi (Ah)", "Cell Capacity (Ah)"), value=2.5)
series_count = st.number_input(metin("Seri Sayısı (S)", "Series Count (S)"), value=10, step=1)
parallel_count = st.number_input(metin("Paralel Sayısı (P)", "Parallel Count (P)"), value=4, step=1)

# ⚙️ Opsiyonel girişler
motor_watt = st.number_input(metin("Motor Gücü (W)", "Motor Power (W)"), value=500)
bms_voltage = st.number_input(metin("BMS Voltajı (V)", "BMS Voltage (V)"), value=36.0)
bms_current = st.number_input(metin("BMS Akımı (A)", "BMS Current (A)"), value=20.0)
charge_current = st.number_input(metin("Şarj Akımı (A)", "Charging Current (A)"), value=2.0)


# ⚡ Hesapla
if st.button(metin("Hesapla", "Calculate")):
    total_voltage = series_count * cell_voltage
    total_capacity = parallel_count * cell_capacity
    energy = total_voltage * total_capacity  # Wh
    runtime = energy / motor_watt if motor_watt > 0 else 0
    charge_time = total_capacity / charge_current if charge_current > 0 else 0


    st.markdown(metin("## 📊 Sonuçlar", "## 📊 Results"))
    st.write(f"🔹 {metin('Toplam Voltaj', 'Total Voltage')}: **{total_voltage:.2f} V**")
    st.write(f"🔹 {metin('Toplam Kapasite', 'Total Capacity')}: **{total_capacity:.2f} Ah**")
    st.write(f"🔹 {metin('Enerji', 'Energy')}: **{energy:.2f} Wh**")
    st.write(f"🔹 {metin('Tahmini Kullanım Süresi', 'Estimated Runtime')}: **{runtime:.2f} {metin('saat', 'hours')}**")
    st.write(f"🔹 {metin('Tahmini Şarj Süresi', 'Estimated Charging Time')}: **{charge_time:.2f} {metin('saat', 'hours')}**")


    st.markdown(metin("## 🔍 BMS Uyum Kontrolü", "## 🔍 BMS Compatibility Check"))
    bms_ok = abs(total_voltage - bms_voltage) <= 2
    current_ok = bms_current >= (motor_watt / total_voltage)

    if bms_ok and current_ok:
        st.success(metin("✅ BMS uyumlu görünüyor.", "✅ BMS appears compatible."))
    else:
        st.error(metin("⚠️ BMS uyumsuz olabilir. Değerleri kontrol edin.", "⚠️ BMS may be incompatible. Check values."))

    # 📋 Kopyalanabilir sonuç
    st.markdown(metin("## 📋 Sonuçları Kopyala", "## 📋 Copyable Results"))
    result_text = f"""
🔋 {metin('Batarya Konfigürasyon Sonuçları', 'Battery Configuration Results')}

🔹 {metin('Toplam Voltaj', 'Total Voltage')}: {total_voltage:.2f} V
🔹 {metin('Toplam Kapasite', 'Total Capacity')}: {total_capacity:.2f} Ah
🔹 {metin('Enerji', 'Energy')}: {energy:.2f} Wh
🔹 {metin('Tahmini Kullanım Süresi', 'Estimated Runtime')}: {runtime:.2f} {metin('saat', 'hours')}
🔹 {metin('Tahmini Şarj Süresi', 'Estimated Charging Time')}: {charge_time:.2f} {metin('saat', 'hours')}


🔍 {metin('BMS Uyumu', 'BMS Compatibility')}:
- {metin('Voltaj Uygunluğu', 'Voltage Match')}: {'Evet' if bms_ok else 'Hayır'}
- {metin('Akım Uygunluğu', 'Current Match')}: {'Evet' if current_ok else 'Hayır'}
"""
    st.text_area(metin("Sonuçlar (Kopyalanabilir)", "Results (Copyable)"), result_text, height=220)
