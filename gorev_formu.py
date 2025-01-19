import streamlit as st
import locale
from datetime import datetime, time, timedelta
import re


def validate_time_format(time_str):
    """
    Saat formatının DD:SS şeklinde olup olmadığını kontrol eder
    """
    pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, time_str))

def time_to_minutes(t):
    """
    time nesnesini dakikaya çevirir
    """
    return t.hour * 60 + t.minute

# State başlatma
if 'last_departure' not in st.session_state:
    st.session_state.last_departure = time(8, 0)  # Varsayılan başlangıç saati
if 'last_return' not in st.session_state:
    st.session_state.last_return = time(17, 0)    # Varsayılan dönüş saati
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
if "selected_items" not in st.session_state:
    st.session_state.selected_items = []

# Bolu ili ilçe ve belde belediyeleri listesi
ilceler = [
    "Merkez", "Mengen", "Gerede", "Göynük", "Kıbrıscık",
    "Mudurnu", "Seben", "Dörtdivan", "Yeniçağa"
]

# Personel listesi
personel = [
    "Aç", "Açıklama Ekle", "Açıklamayı Sil", "Baskı Önizle ve Yazdır",
    "Biçim Boyacısı", "Birden Çok Sayfa Görüntüle", "Bul",
    "Değişikliklerle İzle", "Dikey Metin Kutusu Çiz", "Dipnot",
    "Dokunma/Fare Modu", "Düzeltmeyi Kabul Et", "Düzeltmeyi Reddet",
    "E-posta ile Gönder", "Farklı Kaydet", "Geri Al", "Hızlı Yazdır",
    "Kaydet", "Kes", "Kopyala", "Köprü Ekle", "Liste Düzeyini Değiştir",
    "Madde İşaretleri"
]

def toggle_form():
    st.session_state.show_form = not st.session_state.show_form

# Sayfa başlığı
st.title("Seyahat Bilgileri")

# İlk satır - 4 kolon
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

with row1_col1:
    selected_date = st.date_input("Tarih", format="DD.MM.YYYY")

with row1_col2:
    vehicle_type = st.selectbox("Araç Türü", options=["Resmi Araç", "Özel Araç"], index=0)

with row1_col3:
    departure_time = st.time_input(
        "Gidiş Saati",
        value=st.session_state.last_departure,
        step=timedelta(minutes=15)
    )
    st.session_state.last_departure = departure_time

with row1_col4:
    return_time = st.time_input(
        "Dönüş Saati",
        value=st.session_state.last_return,
        step=timedelta(minutes=15)
    )
    st.session_state.last_return = return_time

# Zaman kontrolleri
departure_minutes = time_to_minutes(departure_time)
return_minutes = time_to_minutes(return_time)

if return_minutes <= departure_minutes:
    st.error("Dönüş saati, gidiş saatinden sonra olmalıdır!")

# İkinci satır - 4 kolon
row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)

with row2_col1:
    selected_district = st.selectbox("İlçe", options=ilceler, index=0)

with row2_col2:
    neighborhood = st.text_input("Köy/Mahalle", placeholder="Köy veya mahalle adını giriniz")

with row2_col3:
    inspection_duty = st.checkbox("Denetim Kontrol Görevi", value=False)

with row2_col4:
    outside_adjacent = st.checkbox("Mücavir Alan Dışı", value=False)

# Personel Seçim Bölümü
st.markdown("---")  # Ayırıcı çizgi

# Personel Ekle butonu
col1, col2 = st.columns([1, 5])
with col1:
    st.button("Gizle" if st.session_state.show_form else "Personel Ekle", on_click=toggle_form)

# Personel form görünümü
if st.session_state.show_form:
    col_left, col_right = st.columns(2)

    # Sol kolon - Personel listesi
    with col_left:
        st.markdown("### Personel Listesi")
        selected_person = st.selectbox("Personel seçin:", personel, key="person_select")
        if st.button("Ekle >>"):
            if selected_person not in st.session_state.selected_items:
                st.session_state.selected_items.append(selected_person)

    # Sağ kolon - Seçili personel
    with col_right:
        st.markdown("### Seçili Personel")
        for item in st.session_state.selected_items:
            col_item, col_remove = st.columns([3, 1])
            with col_item:
                st.write(item)
            with col_remove:
                if st.button("Kaldır", key=f"remove_{item}"):
                    st.session_state.selected_items.remove(item)
                    st.rerun()

        # İşlem butonları
        if st.session_state.selected_items:
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Kaydet"):
                    st.success("Personel seçimleri kaydedildi!")
            with col2:
                if st.button("Tüm Kayıtları Sil"):
                    st.session_state.selected_items = []
                    st.rerun()
            with col3:
                if st.button("İptal"):
                    st.session_state.show_form = False
                    st.rerun()
