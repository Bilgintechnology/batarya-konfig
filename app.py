import os

import streamlit as st

st.markdown("""
    <style>
    body {
        background-color: #F5F5F5;
        font-family: 'Segoe UI', sans-serif;
    }

    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }

    h1, h2, h3 {
        color: #0A2647;
    }

    .stButton>button {
        background-color: #FFB200;
        color: white;
        font-weight: bold;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        border: none;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #e69c00;
        transform: scale(1.03);
    }

    .stTextInput>div>input, .stTextArea>div>textarea {
        border: 2px solid #2C74B3;
        border-radius: 6px;
        padding: 8px;
        font-size: 16px;
    }

    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

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

logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

if os.path.exists(logo_path):
    st.image(logo_path, width=150)
else:
    st.warning("Logo bulunamadı.")

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
    st.session_state.result_text = f"""
 {metin('Batarya Konfigürasyon Sonuçları', 'Battery Configuration Results')}

 {metin('Toplam Voltaj', 'Total Voltage')}: {total_voltage:.2f} V
 {metin('Toplam Kapasite', 'Total Capacity')}: {total_capacity:.2f} Ah
 {metin('Enerji', 'Energy')}: {energy:.2f} Wh
 {metin('Tahmini Kullanım Süresi', 'Estimated Runtime')}: {runtime:.2f} {metin('saat', 'hours')}
 {metin('Tahmini Şarj Süresi', 'Estimated Charging Time')}: {charge_time:.2f} {metin('saat', 'hours')}


 {metin('BMS Uyumu', 'BMS Compatibility')}:
- {metin('Voltaj Uygunluğu', 'Voltage Match')}: {'Evet' if bms_ok else 'Hayır'}
- {metin('Akım Uygunluğu', 'Current Match')}: {'Evet' if current_ok else 'Hayır'}
"""
    st.text_area(metin("Sonuçlar (Kopyalanabilir)", "Results (Copyable)"), st.session_state.result_text, height=220)


st.markdown("---")

st.markdown(f"### {metin('Bizimle çalışmak ister misiniz?', 'Want to work with us?')}")

if st.button(metin("📬 Teklif Al", "📬 Get a Quote")):
    st.switch_page("pages/iletisim.py")

if "result_text" not in st.session_state:
    st.session_state.result_text = ""


from utils.pdf_olustur import pdf_olustur


st.markdown("---")
st.subheader("📄 PDF Çıktısı")

col1, col2 = st.columns([3, 1])
with col2:
    pdf_erisim_kodu = st.text_input("🔐 Kod girin:", type="password")

if pdf_erisim_kodu == "2024PDF":
    st.success("✅ Kod doğru! PDF çıktısı alabilirsiniz.")

    if "result_text" in st.session_state and st.session_state.result_text.strip() != "":
        if st.button("📥 PDF Oluştur ve İndir"):
            pdf_path = pdf_olustur(st.session_state.result_text)
            with open(pdf_path, "rb") as f:
                st.download_button("📄 PDF İndir", data=f, file_name="batarya_raporu.pdf")
    else:
        st.info("ℹ️ Lütfen önce hesaplama yapın.")

else:
    st.warning("⚠️ PDF çıktısı almak için geçerli bir kod girin.")

