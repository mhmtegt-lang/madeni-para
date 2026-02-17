import streamlit as st

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Para ve Kesirler", page_icon="🪙")

# --- CSS (Görsellik ve Renk Ayarları) ---
st.markdown("""
<style>
    /* Para Stili */
    .coin {
        width: 80px; height: 80px;
        background: linear-gradient(145deg, #ffd700, #e6ac00); /* Daha canlı altın */
        border-radius: 50%;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        font-size: 16px; font-weight: bold; color: #4a3b00;
        border: 4px solid #fff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin: 8px;
        transition: transform 0.1s;
    }
    .coin:active { transform: scale(0.90); }
    .coin-small { font-size: 10px; opacity: 0.8; }

    /* Kumbara Kutusu Stili */
    .container-box {
        border: 3px dashed #a0aec0; /* Gri kesikli çizgi */
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        /* ÖNEMLİ: Arka planı hafif gri, yazıyı KESİN SİYAH yapıyoruz */
        background-color: #f7fafc; 
        color: #1a202c !important; 
        min-height: 250px;
        display: flex; flex-direction: column;
        align-items: center;
    }
    
    /* Kutu içindeki başlıkların rengini zorla siyah yap */
    .container-box h4, .container-box p {
        color: #1a202c !important;
    }

    /* Toplanan paraların alanı */
    .collected-coins-area {
        display: flex; flex-wrap: wrap; justify-content: center;
        margin-top: 15px; width: 100%;
        background-color: rgba(0,0,0,0.05); /* Paraların olduğu yer hafif koyu */
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Uyarı Mesajları */
    .success-msg { color: #2f855a; font-weight: bold; font-size: 1.2em; margin-top: 10px;}
    .error-msg { color: #c53030; font-weight: bold; margin-top: 10px;}

</style>
""", unsafe_allow_html=True)

# --- Veri ---
paralar = {
    "1 TL": 100, "50 Kuruş": 50, "25 Kuruş": 25,
    "10 Kuruş": 10, "5 Kuruş": 5, "1 Kuruş": 1
}

# --- Hafıza (Session State) ---
if 'toplanan_adet' not in st.session_state:
    st.session_state.toplanan_adet = 0
if 'secilen_para_eski' not in st.session_state:
    st.session_state.secilen_para_eski = None

def main():
    st.title("🪙 İnteraktif Para Kumbarası")
    st.markdown("Hedefimiz kutuyu tam **100 Kuruş (1 TL)** yapmak!")

    # 1. Seçim
    secilen_isim = st.selectbox("Hangi parayı kullanacağız?", list(paralar.keys()), index=2)
    deger = paralar[secilen_isim]

    # Para değişirse sıfırla
    if secilen_isim != st.session_state.secilen_para_eski:
        st.session_state.toplanan_adet = 0
        st.session_state.secilen_para_eski = secilen_isim
        st.rerun()

    # Hesaplamalar
    hedef_adet = int(100 / deger) if deger > 0 else 0
    toplanan = st.session_state.toplanan_adet
    toplam_deger = toplanan * deger
    
    # Ekran Düzeni
    col_kontrol, col_kutu = st.columns([1, 2], gap="medium")

    # --- SOL: Kontrol Paneli ---
    with col_kontrol:
        st.subheader("İşlemler")
        
        # Para Görseli (Buton gibi duran)
        st.markdown(f"""
        <div class="coin" style="margin: 0 auto 20px auto;">
            <div>{deger}</div><div class="coin-small">Kr</div>
        </div>
        """, unsafe_allow_html=True)

        # BUTONLAR (Yan Yana)
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            # Ekleme Butonu
            # Hedef geçildiyse pasif yapmıyoruz ki "fazla oldu" hatasını görebilsinler (pedagojik)
            # Ama 100'ü çok geçince durduralım.
            if st.button("Ekle ➕", use_container_width=True):
                st.session_state.toplanan_adet += 1
                st.rerun()

        with btn_col2:
            # Silme Butonu
            if st.button("Sil ➖", use_container_width=True):
                if toplanan > 0:
                    st.session_state.toplanan_adet -= 1
                    st.rerun()

        st.divider()
        st.metric("Hedef", "100 Kuruş")
        
        # Toplam değer renklendirmesi
        delta_color = "normal"
        if toplam_deger == 100: delta_color = "normal" # Streamlit bug'ı olmasın diye normal
        elif toplam_deger > 100: delta_color = "inverse"
        
        st.metric("Kutudaki Tutar", f"{toplam_deger} Kuruş", delta=None)

    # --- SAĞ: Kutu (Kumbara) ---
    with col_kutu:
        st.subheader("Kumbara")
        
        # Kutuyu aç
        st.markdown('<div class="container-box">', unsafe_allow_html=True)
        
        # Durum Mesajları
        if toplanan == 0:
            st.markdown(f"<h4>Kutu Boş</h4><p>Soldaki <b>Ekle</b> butonuna basarak {secilen_isim} ekle.</p>", unsafe_allow_html=True)
        elif toplam_deger < 100:
            kalan = hedef_adet - toplanan
            st.markdown(f"<h4>Devam Et...</h4><p>1 TL olması için <b>{kalan}</b> tane daha lazım.</p>", unsafe_allow_html=True)
        elif toplam_deger == 100:
            st.markdown(f"<div class='success-msg'>🎉 TEBRİKLER! TAM 1 TL OLDU! 🎉</div>", unsafe_allow_html=True)
            st.balloons()
        else:
            # Fazla para durumu
            fazla_miktar = toplam_deger - 100
            st.markdown(f"<div class='error-msg'>⚠️ DİKKAT: FAZLA OLDU!<br>{fazla_miktar} kuruş fazlan var. 'Sil' butonuyla geri al.</div>", unsafe_allow_html=True)

        # Paraları Göster
        if toplanan > 0:
            st.markdown('<div class="collected-coins-area">', unsafe_allow_html=True)
            
            # Grid sistemi
            cols = st.columns(4)
            for i in range(toplanan):
                with cols[i % 4]:
                    # CSS içindeki .coin sınıfını kullanıyoruz
                    st.markdown(f"""
                    <div class="coin" style="width:60px; height:60px; font-size:12px;">
                        {deger}<br>Kr
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Kutuyu kapat
        st.markdown('</div>', unsafe_allow_html=True)

        # Sıfırlama butonu (Sadece işlem yapıldıysa görünür)
        if toplanan > 0:
            if st.button("🗑️ Kutuyu Tamamen Boşalt"):
                st.session_state.toplanan_adet = 0
                st.rerun()

if __name__ == "__main__":
    main()
