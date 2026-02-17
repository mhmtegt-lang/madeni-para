import streamlit as st

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Para ve Kesirler", page_icon="🪙")

# --- CSS (Tamamen Yenilendi) ---
st.markdown("""
<style>
    /* Sayfa Arka Planı ve Genel Font */
    .main { background-color: #1a202c; color: white; }
    
    /* Kumbara Kutusu: Okunmayan beyazlık silindi, koyu ve şık bir mavi yapıldı */
    .kumbara-kutusu {
        background-color: #2d3748; /* Koyu gri/mavi */
        border: 3px dashed #63b3ed;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        color: #ebf8ff !important; /* Çok açık mavi/beyaz yazı - Koyu zeminde harika okunur */
        min-height: 300px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    .kumbara-kutusu h3, .kumbara-kutusu p {
        color: #ebf8ff !important;
        margin-bottom: 10px;
    }

    /* Madeni Paralar */
    .madeni-para {
        width: 70px; height: 70px;
        background: linear-gradient(135deg, #ecc94b, #b7791f);
        border-radius: 50%;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        font-weight: bold; color: #2d3748;
        border: 2px solid #fff;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Hata ve Başarı Mesajları */
    .hata-mesaji {
        background-color: #feb2b2; color: #9b2c2c;
        padding: 10px; border-radius: 10px; font-weight: bold;
    }
    .basari-mesaji {
        background-color: #9ae6b4; color: #22543d;
        padding: 10px; border-radius: 10px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Veri ve Hafıza ---
paralar = {"1 TL": 100, "50 Kr": 50, "25 Kr": 25, "10 Kr": 10, "5 Kr": 5, "1 Kr": 1}

if 'adet' not in st.session_state: st.session_state.adet = 0
if 'eski_para' not in st.session_state: st.session_state.eski_para = "25 Kr"

def main():
    st.title("🪙 Para Biriktirme Oyunu")
    
    # Seçim ekranı
    secim = st.selectbox("Para Türü:", list(paralar.keys()), index=2)
    deger = paralar[secim]

    # Para türü değişirse kumbarayı boşalt
    if secim != st.session_state.eski_para:
        st.session_state.adet = 0
        st.session_state.eski_para = secim
        st.rerun()

    toplam = st.session_state.adet * deger

    # Sol Panel: Kontroller | Sağ Panel: Kumbara
    col_ctrl, col_box = st.columns([1, 2])

    with col_ctrl:
        st.write("### İşlemler")
        if st.button("Kutuya At ➕", use_container_width=True):
            st.session_state.adet += 1
            st.rerun()
            
        if st.button("Son Parayı Sil ➖", use_container_width=True, type="secondary"):
            if st.session_state.adet > 0:
                st.session_state.adet -= 1
                st.rerun()
        
        st.metric("Şu anki Toplam", f"{toplam} Kr")
        st.write(f"Hedef: **100 Kr**")

    with col_box:
        # KUTU BAŞLANGICI
        st.markdown('<div class="kumbara-kutusu">', unsafe_allow_html=True)
        
        if toplam == 0:
            st.markdown("<h3>Kumbara Boş</h3><p>Para ekleyerek 1 TL yapalım!</p>", unsafe_allow_html=True)
        elif toplam == 100:
            st.markdown('<div class="basari-mesaji">🎉 TEBRİKLER! TAM 1 TL (100 Kr) OLDU!</div>', unsafe_allow_html=True)
            st.balloons()
        elif toplam > 100:
            st.markdown(f'<div class="hata-mesaji">⚠️ EYVAH! FAZLA OLDU!<br>{toplam} Kr topladın. Lütfen "Sil" butonuna bas.</div>', unsafe_allow_html=True)
        else:
            kalan = 100 - toplam
            st.markdown(f"<h3>Harika!</h3><p>1 TL için <b>{kalan} Kr</b> daha lazım.</p>", unsafe_allow_html=True)

        # Paraların Görsel Dizilimi
        para_alani = st.container()
        with para_alani:
            cols = st.columns(5)
            for i in range(st.session_state.adet):
                with cols[i % 5]:
                    st.markdown(f'<div class="madeni-para">{deger}<br>Kr</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # KUTU BİTİŞİ

    if st.session_state.adet > 0:
        if st.button("🗑️ Kumbarayı Sıfırla"):
            st.session_state.adet = 0
            st.rerun()

if __name__ == "__main__":
    main()
