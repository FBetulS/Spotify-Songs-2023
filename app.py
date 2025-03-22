import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# Veri yükleme ve ön işleme
@st.cache_data
def load_data():
    df = pd.read_csv("spotify-2023.csv", encoding='latin1')
    # Veri temizleme işlemleri
    df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
    df['in_deezer_playlists'] = pd.to_numeric(df['in_deezer_playlists'], errors='coerce')
    df['in_shazam_charts'] = pd.to_numeric(df['in_shazam_charts'], errors='coerce')
    df['in_shazam_charts'] = df['in_shazam_charts'].fillna(df['in_apple_charts'])
    df['key'] = df['key'].fillna(' ')
    df['toplam_listelerde'] = df['in_spotify_playlists'] + df['in_apple_playlists'] + df['in_deezer_playlists']
    df = pd.get_dummies(df, columns=['key', 'mode'])
    return df

df = load_data()

# Benzerlik matrisini önceden hesapla
# app.py'deki prepare_similarity fonksiyonunu şu şekilde güncelleyin:
@st.cache_data
def prepare_similarity():
    features = [
        'bpm', 'danceability_%', 'valence_%', 'energy_%', 
        'acousticness_%', 'instrumentalness_%', 'liveness_%', 
        'speechiness_%', 'key_A', 'key_A#', 'key_B', 'key_C#', 
        'key_D', 'key_D#', 'key_E', 'key_F', 'key_F#', 'key_G', 
        'key_G#', 'mode_Major', 'mode_Minor', 'streams', 
        'toplam_listelerde'
    ]
    
    df_features = df[features].copy()
    
    # Eksik değerleri doldur
    df_features = df_features.fillna(df_features.mean())
    
    # StandardScaler ile ölçeklendirme
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_features)
    
    # Cosine Similarity matrisini oluştur
    similarity_matrix = cosine_similarity(scaled_features)
    
    return pd.DataFrame(similarity_matrix, index=df['track_name'], columns=df['track_name'])

similarity_df = prepare_similarity()

# Streamlit arayüzü
st.title('Spotify Şarkı Öneri Sistemi')
st.write("Toplam şarkı sayısı:", df.shape[0])

# Sidebar
st.sidebar.header("Filtreler")
selected_year = st.sidebar.selectbox('Yıl Seçin', sorted(df['released_year'].unique(), reverse=True))

# Ana sayfa bölümleri
tab1, tab2, tab3 = st.tabs(["Genel Bilgiler", "Görselleştirmeler", "Şarkı Öneri"])

with tab1:
    st.header("Veri Önizleme")
    st.dataframe(df.head(3))
    
    st.subheader("Yıllara Göre Şarkı Dağılımı")
    year_counts = df['released_year'].value_counts().sort_index()
    st.line_chart(year_counts)

with tab2:
    st.header("Popülerlik Analizleri")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("En Popüler 20 Şarkı")
        top_streams = df.sort_values(by='streams', ascending=False).head(20)
        plt.figure(figsize=(10,6))
        sns.barplot(x='streams', y='track_name', data=top_streams)
        st.pyplot(plt)

    with col2:
        st.subheader("Sanatçı Özellikleri")
        artist_features = df.groupby('artist(s)_name')[['energy_%', 'danceability_%']].mean().nlargest(20, 'energy_%')
        plt.figure(figsize=(10,6))
        sns.scatterplot(x='energy_%', y='danceability_%', data=artist_features)
        st.pyplot(plt)

with tab3:
    st.header("Şarkı Öneri Sistemi")
    
    song_name = st.selectbox(
        "Bir şarkı seçin",
        df['track_name'].unique(),
        index=df['track_name'].tolist().index('Blinding Lights') if 'Blinding Lights' in df['track_name'].values else 0
    )
    
    recommendation_type = st.radio(
        "Öneri Türünü Seçin",
        ["Hybrid Öneri", "Feature-Based Öneri"]
    )
    
    if st.button("Öneri Al"):
        if recommendation_type == "Hybrid Öneri":
            try:
                popularity_scores = df['streams'] * 0.6 + df['toplam_listelerde'] * 0.4
                similar_scores = similarity_df[song_name]
                combined_scores = similar_scores * 0.7 + popularity_scores * 0.3
                recommendations = combined_scores.sort_values(ascending=False).index[1:6]
            except KeyError:
                st.error("Şarkı bulunamadı!")
        else:
            try:
                recommendations = similarity_df[song_name].sort_values(ascending=False).index[1:6]
            except KeyError:
                st.error("Şarkı bulunamadı!")
        
        st.subheader("Önerilen Şarkılar:")
        for i, song in enumerate(recommendations, 1):
            st.write(f"{i}. {song}")

st.sidebar.markdown("---")
st.sidebar.info("Spotify 2023 veri seti kullanılarak oluşturulmuş şarkı öneri sistemi")
