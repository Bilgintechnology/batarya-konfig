import streamlit as st

# ⛳ Sayfa ayarları – EN ÜSTE ALINDI!
st.set_page_config(page_title="İletişim / Contact", page_icon="📬")

# 🌐 Dil seçimi
dil = st.selectbox("Dil / Language", ("Türkçe", "English"))

# 🌐 Metin çoklama fonksiyonu
def metin(turkce, ingilizce):
    return turkce if dil == "Türkçe" else ingilizce

# Başlık
st.title(metin("📬 İletişim / Teklif Al", "📬 Contact / Get a Quote"))

st.markdown(metin(
    "Aşağıdaki formu doldurarak bizimle iletişime geçebilir veya özel teklif alabilirsiniz.",
    "Fill out the form below to contact us or request a custom quote."
))

# 📩 Form alanları
isim = st.text_input(metin("Adınız", "Your Name"))
eposta = st.text_input("Email")
telefon = st.text_input(metin("Telefon Numarası", "Phone Number"))
mesaj = st.text_area(metin("Mesajınız", "Your Message"))

# Gönder butonu
if st.button(metin("Gönder", "Submit")):
    if isim and eposta and mesaj:
        st.success(metin("Mesajınız başarıyla gönderildi. Teşekkür ederiz!", 
                         "Your message has been sent successfully. Thank you!"))
        
        # 📌 Gelecekte burada mesajı e-posta, Google Sheet veya veritabanına kaydedebilirsin.
        
    else:
        st.error(metin("Lütfen zorunlu alanları doldurun.", 
                       "Please fill out all required fields."))
