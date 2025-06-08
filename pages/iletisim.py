import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🌐 Sayfa ayarları
st.set_page_config(page_title="İletişim / Contact", page_icon="📬")

# 🌐 Dil seçimi
dil = st.selectbox("Dil / Language", ("Türkçe", "English"))

# 🌐 Metin çoklama
def metin(tr, en):
    return tr if dil == "Türkçe" else en

# ✉️ E-posta gönderme fonksiyonu
def mail_gonder(isim, eposta, telefon, mesaj):
    ALICI = "bilgintechnology@gmail.com"
    GONDEREN = "bilgintechnology@gmail.com"
    SIFRE = "hugykiklamvfzrjt"  # Buraya 16 haneli uygulama şifresini yaz

    konu = "Yeni Teklif Formu"
    icerik = f"""
    İsim: {isim}
    E-posta: {eposta}
    Telefon: {telefon}
    Mesaj: {mesaj}
    """

    # E-posta mesajını oluştur
    email_message = MIMEMultipart()
    email_message["From"] = GONDEREN
    email_message["To"] = ALICI
    email_message["Subject"] = konu
    email_message.attach(MIMEText(icerik, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GONDEREN, SIFRE)
            server.send_message(email_message)
        return metin("Mesajınız başarıyla gönderildi. Teşekkür ederiz!", "Your message has been sent successfully. Thank you!")
    except Exception as e:
        return metin(f"Hata: {e}", f"Error: {e}")

# 🎯 Başlık
st.title(metin("📬 İletişim / Teklif Al", "📬 Contact / Get a Quote"))
st.markdown(metin(
    "Aşağıdaki formu doldurarak bizimle iletişime geçebilirsiniz.",
    "Fill out the form below to contact us."
))

# 📩 Form alanları
isim = st.text_input(metin("Adınız", "Your Name"))
eposta = st.text_input("Email")
telefon = st.text_input(metin("Telefon Numarası", "Phone Number"))
mesaj = st.text_area(metin("Mesajınız", "Your Message"))

# 📨 Gönder butonu
if st.button(metin("Gönder", "Submit")):
    if isim and eposta and mesaj:
        basarili = mail_gonder(isim, eposta, telefon, mesaj)
        if basarili:
            st.success(metin("Mesajınız başarıyla gönderildi. Teşekkür ederiz!", 
                             "Your message has been sent successfully. Thank you!"))
        else:
            st.error(metin("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", 
                           "Something went wrong. Please try again later."))
    else:
        st.warning(metin("Lütfen tüm gerekli alanları doldurun.", 
                         "Please fill in all required fields."))
