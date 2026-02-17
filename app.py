import streamlit as st
import time

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Para ve Kesirler", page_icon="🪙")

# --- CSS (Görsellik) ---
st.markdown("""
<style>
    /* Para Stili */
    .coin {
        width: 90px; height: 90px;
        background: linear-gradient(145deg, #fbbd23, #dca00b); /* Altın efekti */
        border-radius: 50%;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        font-size: 18px; font-weight: bold; color: #2c1a05;
        border: 3px solid #fff8e1;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        margin: 5px;
        transition: transform 0.1s;
    }
    .coin:active { transform: scale(0.95); } /* Tıklama efekti */
    .coin-small { font-size: 12px; }

    /* Kutu (Kumbara) Stili */
    .container-box {
        border: 4px dashed #4f6d7a;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        background-color: #eef4f7;
        min-height: 250px;
        display: flex; flex-direction: column;
        justify-content: flex-start; align-items: center;
    }
    /* Kutu başlık ve metin rengi koyulaştırıldı */
    .container-box h4 { color: #1a3c4a; margin-bottom: 10px; }
    .container-box p { color: #2c5364; font-size: 1.1em; }
    
    /* Toplanan paraların alanı */
    .collected-coins-area {
        display: flex; flex-wrap: wrap; justify-content: center;
        margin-top: 20px; width: 100%;
    }
    
    /* Başarı Mesajı */
    .success-message {
        background-color: #d4edda; color: #155724;
        padding: 15px; border-radius: 10px;
        border: 2px solid #c3e6cb; margin-top: 20px;
        font-weight: bold; font-size: 1.2em;
    }
</style>
""", unsafe_allow_html=True)

# --- Veri ---
paralar = {
    "1 TL": 100, "50 Kuruş": 50, "25 Kuruş": 25,
    "10 Kuruş": 10, "5 Kuruş": 5, "1 Kuruş": 1
}

# --- Durum Yönetimi (Session State) ---
# Paraların kutuda toplanmasını takip etmek için hafıza kullanıyoruz.
if 'toplanan_adet' not in st.session_state:
    st.session_state.toplanan_adet = 0
if 'secilen_para_eski' not in st.session_state:
    st.session_state.secilen_para_eski = None

def main():
    st.title("🪙 İnteraktif Para ve Kesirler")
    st.write("Paraları kutuya tıklayarak gönderelim ve **1 TL (100 Kuruş)** tamamlayalım!")

    # 1. Kullanıcı Seçimi
    secilen_isim = st.selectbox("Hangi parayı biriktirelim?", list(paralar.keys()), index=2) # Varsayılan 25 Kr
    deger = paralar[secilen_isim]

    # Para değişirse sayacı sıfırla
    if secilen_isim != st.session_state.secilen_para_eski:
        st.session_state.toplanan_adet = 0
        st.session_state.secilen_para_eski = secilen_isim
        st.rerun() # Sayfayı yenile

    # 2. Hedef Hesaplama
    if deger == 0: hedef_adet = 0
    else: hedef_adet = int(100 / deger)
    
    toplanan = st.session_state.toplanan_adet
    toplam_deger = toplanan * deger
    kalan_adet = hedef_adet - toplanan

    # 3. Ekran Düzeni (Sol: Ekleme, Sağ: Kutu)
    col_sol, col_sag = st.columns([1, 2], gap="large")

    # --- SOL TARAFF: Para Ekleme Butonu ---
    with col_sol:
        st.subheader("Parayı Gönder")
        # Paranın kendisini bir buton gibi gösteriyoruz
        para_html = f"""
        <div class="coin" style="cursor: pointer; margin: 0 auto;">
            <div>{deger}</div>
            <div class="coin-small">Kuruş</div>
        </div>
        """
        # Butona tıklayınca sayaç artar
        if st.button("Kutuya At ➡️", key="para_ekle_btn", disabled=toplanan >= hedef_adet, help="Parayı kutuya atmak için tıkla"):
            st.session_state.toplanan_adet += 1
            st.rerun()
        st.markdown(para_html, unsafe_allow_html=True)

        st.markdown("---")
        st.metric("Hedef", "100 Kuruş (1 TL)")
        st.metric("Şu Anki Toplam", f"{toplam_deger} Kuruş")

    # --- SAĞ TARAF: Kumbara Kutusu ---
    with col_sag:
        st.subheader(f"Kumbara: 1 TL için {hedef_adet} tane lazım")
        
        # Kutunun başlangıcı
        st.markdown('<div class="container-box">', unsafe_allow_html=True)
        
        # Durum metni
        if toplanan == 0:
            st.markdown(f"<p>Kutu boş. Soldaki butona basarak <b>{secilen_isim}</b> eklemeye başla!</p>", unsafe_allow_html=True)
        elif toplanan < hedef_adet:
            st.markdown(f"<p>Şu ana kadar <b>{toplanan}</b> tane attın. 1 TL olması için <b>{kalan_adet}</b> tane daha lazım.</p>", unsafe_allow_html=True)
        
        # Toplanan paraları görsel olarak diz
        st.markdown('<div class="collected-coins-area">', unsafe_allow_html=True)
        cols_in_box = st.columns(4) # Kutu içinde 4 sütunlu düzen
        for i in range(toplanan):
            with cols_in_box[i % 4]:
                st.markdown(f'<div class="coin" style="width: 70px; height: 70px; font-size: 14px;">{deger}<br><span class="coin-small">Kr</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # collected-coins-area sonu

        # Başarı Durumu
        if toplanan > 0 and toplanan == hedef_adet:
            st.markdown('</div>', unsafe_allow_html=True) # container-box'ı geçici kapat
            st.markdown(f"""
            <div class="success-message">
                🎉 Harika! Tam <b>{hedef_adet}</b> tane <b>{secilen_isim}</b> bir araya geldi ve <b>1 TL</b> (100 Kuruş) oldu!
            </div>
            """, unsafe_allow_html=True)
            st.balloons() # Konfeti efekti!
            
            if st.button("Tekrar Başla 🔄"):
                st.session_state.toplanan_adet = 0
                st.rerun()
        else:
            st.markdown('</div>', unsafe_allow_html=True) # container-box sonu (başarı yoksa)

if __name__ == "__main__":
    main()
