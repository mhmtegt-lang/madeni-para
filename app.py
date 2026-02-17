import streamlit as st

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Para ve Kesirler", page_icon="🪙")

# --- CSS (Görsellik için basit stil) ---
# Burası paraların yuvarlak görünmesini sağlar
st.markdown("""
<style>
    .coin {
        width: 100px;
        height: 100px;
        background-color: #fca311; /* Altın sarısı */
        border-radius: 50%; /* Yuvarlak yap */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        color: white;
        margin: 10px auto;
        border: 4px solid #e5e5e5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .container-box {
        border: 2px dashed #14213d;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# --- Veri (Paralarımız) ---
# Sadece basit bir sözlük yapısı kullanıyoruz
paralar = {
    "1 TL": 100,
    "50 Kuruş": 50,
    "25 Kuruş": 25,
    "10 Kuruş": 10,
    "5 Kuruş": 5,
    "1 Kuruş": 1
}

def main():
    st.title("🪙 Paralar ve Kesirler")
    st.write("Bir para seçelim ve **1 TL (100 Kuruş)** olması için kaç tane gerektiğini görelim.")

    # 1. Kullanıcıdan Seçim Al
    secilen_isim = st.selectbox("İncelemek istediğin parayı seç:", list(paralar.keys()))
    
    # Seçilen paranın kuruş değeri
    deger = paralar[secilen_isim]
    
    # 2. Hesaplamalar
    if deger == 0:
        adet = 0
    else:
        adet = int(100 / deger) # 100'ü paranın değerine bölüyoruz

    # 3. Ekranı İkiye Böl (Sol: Bilgi, Sağ: Görsel)
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Bilgiler")
        st.info(f"Seçilen: **{secilen_isim}**")
        
        # Kesir Gösterimi (Ödevdeki gibi)
        st.metric(label="Kesir Olarak", value=f"1/{adet}" if adet > 0 else "0")
        st.metric(label="Paydası 100 Olarak", value=f"{deger}/100")

    with col2:
        st.subheader("Görsel Anlatım")
        
        # Olayın koptuğu yer: Görselleştirme
        if adet > 0:
            st.markdown(f"""
            <div class="container-box">
                <h4>Bu kutu 1 TL (100 Kuruş) eder</h4>
                <p>İçinde tam <b>{adet}</b> tane <b>{secilen_isim}</b> var.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Paraları yan yana/alt alta dizmek için kolonlar
            # Her satırda en fazla 4 tane olsun ki güzel görünsün
            sutun_sayisi = 4 
            
            # Dinamik olarak paraları çiziyoruz
            ozel_konteyner = st.container()
            with ozel_konteyner:
                cols = st.columns(sutun_sayisi)
                for i in range(adet):
                    # Sırayla kolonlara yerleştir
                    with cols[i % sutun_sayisi]:
                        st.markdown(f'<div class="coin">{deger}<br>Kr</div>', unsafe_allow_html=True)
            
            # Matematiksel Toplama İşlemi
            if adet > 1:
                st.write("---")
                toplama_islemi = " + ".join([f"**1/{adet}**"] * adet)
                st.write("Matematiksel olarak:")
                st.write(f"{toplama_islemi} = **1 TAM (1 TL)**")

if __name__ == "__main__":
    main()
