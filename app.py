import streamlit as st

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Para Kumbarası", page_icon="🪙", layout="centered")

# --- CSS (Paraları Kutunun İçine Alan Tasarım) ---
st.markdown("""
<style>
    /* Ana Kumbara Kutusu */
    .kumbara-alani {
        background-color: #1e293b; /* Koyu, şık bir zemin */
        border: 4px dashed #64748b;
        border-radius: 24px;
        padding: 20px;
        min-height: 300px;
        display: flex;
        flex-wrap: wrap; /* Paraların sığmayınca alt satıra geçmesini sağlar */
        align-content: flex-start;
        justify-content: center;
        gap: 15px; /* Paralar arası boşluk */
        box-shadow: inset 0 4px 10px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    /* Kutu İçindeki Madeni Para */
    .kutu-ici-para {
        width: 65px; height: 65px;
        background: linear-gradient(135deg, #fbbf24, #d97706);
        border-radius: 50%;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        font-weight: bold; color: #1e293b;
        border: 2px solid #fff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        font-size: 14px;
        animation: dusme 0.3s ease-out; /* Para atılınca hafif düşme efekti */
    }

    @keyframes dusme {
        0% { transform: translateY(-50px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    .durum-metni {
        text-align: center; color: #f1f5f9; font-size: 1.2rem; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Hafıza Yönetimi ---
if 'para_adedi' not in st.session_state: st.session_state.para_adedi = 0
if 'secili_para' not in st.session_state: st.session_state.secili_para = "25 Kr"

# --- Veri ---
paralar = {"1 TL": 100, "50 Kr": 50, "25 Kr": 25, "10 Kr": 10, "5 Kr": 5, "1 Kr": 1}

def main():
    st.title("🪙 İnteraktif Kumbara")
    
    secim = st.sidebar.selectbox("Kutuya atılacak parayı seç:", list(paralar.keys()), index=2)
    deger = paralar[secim]

    # Para türü değişirse sıfırla
    if secim != st.session_state.secili_para:
        st.session_state.para_adedi = 0
        st.session_state.secili_para = secim
        st.rerun()

    toplam = st.session_state.para_adedi * deger

    # --- KONTROL BUTONLARI ---
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("Kutuya At ➕", use_container_width=True):
            st.session_state.para_adedi += 1
            st.rerun()
    with col2:
        if st.button("Geri Al ➖", use_container_width=True):
            if st.session_state.para_adedi > 0:
                st.session_state.para_adedi -= 1
                st.rerun()
    with col3:
        if st.button("Boşalt 🗑️", use_container_width=True):
            st.session_state.para_adedi = 0
            st.rerun()

    st.divider()

    # --- KUMBARA GÖRSELİ (İÇİNDEKİ PARALARLA) ---
    # Durum mesajları
    if toplam == 100:
        st.success("Tebrikler! Tam 1 TL yaptın!")
        st.balloons()
    elif toplam > 100:
        st.error(f"Eyvah! {toplam - 100} Kr fazla oldu. Geri almalısın.")
    else:
        st.info(f"Kutuda şu an {toplam} Kr var. 1 TL için {100 - toplam} Kr daha lazım.")

    # HTML ile Kumbarayı ve İçindeki Paraları Oluşturma
    para_htmls = "".join([f'<div class="kutu-ici-para">{deger}<br>Kr</div>' for _ in range(st.session_state.para_adedi)])
    
    st.markdown(f"""
        <div class="kumbara-alani">
            {para_htmls}
        </div>
    """, unsafe_allow_html=True)

    # Ödevdeki tabloyu hatırla (Küçük bir özet)
    st.caption(f"Özet: {st.session_state.para_adedi} tane {secim} = {toplam}/100 TL")

if __name__ == "__main__":
    main()
