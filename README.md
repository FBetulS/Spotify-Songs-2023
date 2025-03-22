# Most Streamed Spotify Songs 2023
# 🎶 2023 En Çok Dinlenen Spotify Şarkıları Projesi

Bu proje, 2023 yılında en çok dinlenen Spotify şarkılarını analiz etmek ve öneri sistemleri geliştirmek amacıyla hazırlanmıştır. Kullanıcıların sevdikleri şarkılara benzer müzik önerileri alabilmesi için çeşitli makine öğrenimi ve veri analizi teknikleri kullanılmaktadır.

## 🔗 Kaggle Veri Seti
[2023 En Çok Dinlenen Spotify Şarkıları]

## 🔗 Hugging Face Uygulaması
[Spotify Songs 2023 - Hugging Face Space]

## 📊 Proje Aşamaları
1. **Veri Yükleme ve Ön İşleme**:
   - Veri seti `spotify-2023.csv` dosyasından okunur.
   - Gerekli sütunlar sayısal değerlere dönüştürülür.
   - Boş değerler doldurulur ve yeni özellikler türetilir.

2. **Özellik Mühendisliği**:
   - `toplam_listelerde` özelliği, Spotify, Apple ve Deezer listelerindeki toplam şarkı sayısını hesaplar.
   - Kategorik değişkenler için dummy değişkenler oluşturulur.

3. **Öneri Sistemleri Geliştirme**:
   - **Hibrid Öneri Sistemi**: Cosine Similarity ve popülerlik skorları kullanılarak öneri yapılır.
   - **Özellik Tabanlı Öneri Sistemi**: Şarkıların özelliklerine göre benzerlik hesaplanır ve öneriler sunulur.

4. **Model Değerlendirme**:
   - Öneri sisteminin doğruluğu ve kullanıcı deneyimi değerlendirilir.

## 🔍 Öneri Fonksiyonları
- **`hybrid_recommendation(song_name, num_recommendations=5)`**: Belirtilen bir şarkıya benzer şarkıları önerir.
- **`feature_based_recommendation(song_name, num_recommendations=5)`**: Şarkının özelliklerine göre benzer şarkılar önerir.

## 📈 Sonuçlar
Projenin sonunda, kullanıcıların "Blinding Lights" gibi popüler şarkılar için benzer şarkılar alması sağlanmıştır. Örnek önerilen şarkılar aşağıda gösterilmektedir:

```python
recommended_songs = hybrid_recommendation("Blinding Lights")
print("Önerilen Şarkılar:", recommended_songs)
