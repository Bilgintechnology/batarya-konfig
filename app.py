import streamlit as st

st.title("🔋 Batarya Konfigürasyon Hesaplayıcı")

st.subheader("🔧 Hücre Bilgileri")
cell_voltage = st.number_input("Hücre Voltajı (V)", value=3.7)
cell_capacity = st.number_input("Hücre Kapasitesi (Ah)", value=2.5)
series_count = st.number_input("Seri Sayısı (S)", value=10, step=1)
parallel_count = st.number_input("Paralel Sayısı (P)", value=4, step=1)

st.subheader("⚙️ Opsiyonel Girişler")
motor_watt = st.number_input("Motor Gücü (W)", value=500)
bms_voltage = st.number_input("BMS Voltajı (V)", value=36.0)
bms_current = st.number_input("BMS Akımı (A)", value=20.0)

if st.button("Hesapla"):
    total_voltage = series_count * cell_voltage
    total_capacity = parallel_count * cell_capacity
    energy = total_voltage * total_capacity  # Wh
    runtime = energy / motor_watt if motor_watt > 0 else 0

    st.markdown("## 📊 Sonuçlar")
    st.write(f"🔹 Toplam Voltaj: **{total_voltage:.2f} V**")
    st.write(f"🔹 Toplam Kapasite: **{total_capacity:.2f} Ah**")
    st.write(f"🔹 Enerji (Wh): **{energy:.2f} Wh**")
    st.write(f"🔹 Tahmini Kullanım Süresi: **{runtime:.2f} saat**")

    st.markdown("## 🔍 BMS Uyum Kontrolü")
    bms_ok = abs(total_voltage - bms_voltage) <= 2
    current_ok = bms_current >= (motor_watt / total_voltage)

    if bms_ok and current_ok:
        st.success("✅ BMS uyumlu görünüyor.")
    else:
        st.error("⚠️ BMS uyumsuz olabilir. Değerleri kontrol edin.")
    st.markdown("## 📋 Sonuçları Kopyala")

    result_text = f"""
🔋 Batarya Konfigürasyon Sonuçları

🔹 Toplam Voltaj: {total_voltage:.2f} V
🔹 Toplam Kapasite: {total_capacity:.2f} Ah
🔹 Enerji: {energy:.2f} Wh
🔹 Tahmini Kullanım Süresi: {runtime:.2f} saat

🔍 BMS Uyumu:
- Voltaj Uygunluğu: {'Evet' if bms_ok else 'Hayır'}
- Akım Uygunluğu: {'Evet' if current_ok else 'Hayır'}
"""

    st.text_area("Sonuçlar (Kopyalanabilir)", result_text, height=200)
