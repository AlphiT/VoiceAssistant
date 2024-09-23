import google.generativeai as genai
import gem_api_key
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

# API anahtarınızı yapılandırın
genai.configure(api_key=gem_api_key.api_Key)

# Modeli seçin
model = genai.GenerativeModel('gemini-pro')

# Sesli komutları dinlemek için tanıyıcı ayarla
recognizer = sr.Recognizer()


def sesli_cevap_oku(metin):
    """Google Text-to-Speech kullanarak metni sese çevirir ve playsound ile oynatır"""
    tts = gTTS(text=metin, lang='tr')
    tts.save("cevap.mp3")
    # playsound kullanarak MP3 dosyasını oynat
    playsound("cevap.mp3")


def dinle_ve_sor():
    # Mikrofondan gelen sesi tanı ve metne çevir
    with sr.Microphone() as source:
        print("Sizi dinliyorum...")
        recognizer.adjust_for_ambient_noise(source)  # Arka plan gürültüsüne göre ayar yap
        ses = recognizer.listen(source)  # Sesi dinle

        try:
            # Sesi Google'ın ses tanıma servisi ile metne dönüştür
            soru = recognizer.recognize_google(ses, language="tr-TR")
            print(f"Siz: {soru}")
            return soru
        except sr.UnknownValueError:
            print("Ne dediğinizi anlayamadım.")
            return None
        except sr.RequestError:
            print("Google ses tanıma servisine ulaşılamıyor.")
            return None


while True:
    # Sesli komutu dinle ve soruyu al
    soru = dinle_ve_sor()

    # Eğer soru alındıysa işleme devam et
    if soru:
        if soru.lower() == 'çıkış':  # Çıkmak için komut verildiğinde dur
            print("Çıkış yapılıyor.")
            break

        # Modelden cevabı al
        response = model.generate_content(soru)

        # Cevabı yazdır
        print(f"Cevap: {response.text}")

        # Sesli yanıtı gTTS ile ver ve playsound ile oynat
        sesli_cevap_oku(response.text)

# Dosya tamamlandıktan sonra silin
os.remove("cevap.mp3")
