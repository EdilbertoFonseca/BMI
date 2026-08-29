# Vücut Kitle İndeksi (VKİ) Hesaplaması

* **Yazar**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Oluşturulma Tarihi**: 11/08/2022.
* **Sürüm**: 2026.2.1
* **Lisans**: [GPL v2](https://www.gnu.org/licenses/gpl-2.0.html)
* **Son Güncelleme**: 04/05/2026

## Giriş

VKİ Eklentisine Hoş Geldiniz! Bu, bir kişinin vücut yağ seviyesini değerlendirmek için kullanılan uluslararası bir ölçüt olan Vücut Kitle İndeksini (VKİ) belirlemeye yardımcı olmak amacıyla tasarlanmış bir eklentidir. Bu eklenti ile boyunuzu ve kilonuzu girerek VKİ'nizi kolayca hesaplayabilirsiniz.

Geleneksel VKİ hesaplamasına ek olarak bu yeni sürüm, boya dayalı ideal VKİ hesaplama ve Dünya Sağlık Örgütü (DSÖ) kriterlerine göre ayrıntılı bir sınıflandırma sunarak kişiselleştirilmiş sağlık rehberliği sağlama gibi ek özellikler sunar. Eklenti artık Alt+H kısayolu kullanılarak hızla erişilebilen son 10 hesaplamayı da kaydeder.

Not: VKİ'nin doğru bir şekilde yorumlanması için vücut kompozisyonu, yağ dağılımı, yaş, cinsiyet ve genel sağlık durumu gibi diğer faktörlerin de dikkate alınması önemlidir. Daha doğru bir değerlendirme ile uygun sağlık ve kilo rehberliği için her zaman bir doktor veya diyetisyen gibi bir sağlık uzmanına danışmanız önerilir.

## Kurulum

VKİ Eklentisini NVDA'ya kurmak için adım adım talimatlar şunlardır:

1. NVDA'da **Araçlar** menüsünü açın ve **Eklenti Mağazası**'nı arayın.
2. **Mevcut Eklentiler** sekmesinde **Ara** alanına gidin.
3. "BMI" veya "VKİ" aramasını yapın. Sonuçlarda **Enter** veya **Uygula**'ya basın, ardından **Kur**'u seçin.
4. Değişiklikleri uygulamak için NVDA'yı yeniden başlatın.

Artık VKİ Eklentisini kullanmaya ve Vücut Kitle İndeksinizi doğrudan NVDA'da hesaplamaya hazırsınız.

## Ayarlar

Kullanımı oldukça basit olduğundan eklenti için herhangi bir yapılandırma talimatı yoktur.

## Kullanım

Eklentiyi başlatmak için `Alt+Windows+I` tuşlarına basın veya `NVDA+N` NVDA menüsünü kullanıp Araçlar > VKİ'nizi Hesaplayın seçeneğine gidin. İki giriş alanı içeren bir iletişim kutusu görünecektir:

1. Boy – santimetre (CM) cinsinden boyunuzun seçilmesi veya girilmesi gereken alan.
2. Kilo – kilogram (KG) cinsinden kilonuzun seçilmesi veya girilmesi gereken alan.

Tüm alanları doldurduktan sonra `Alt+A` kısayolunu kullanarak Hesapla düğmesine basın veya Hesapla düğmesi üzerindeyken Enter tuşuna basın.

NVDA aşağıdakileri içeren bir iletişim kutusunu okuyacaktır:

* Mevcut VKİ hesaplamanızın sonucu.
* DSÖ parametrelerine göre ayrıntılı sınıflandırmanız (düşük kilolu, normal kilolu, fazla kilolu, I., II. veya III. derece obezite).
* Boyunuza göre tahmini ideal VKİ değeriniz.
* Sağlık değerlendirmesinde ek faktörlerin önemini vurgulayan bir rehberlik mesajı.

İletişim kutusunun sonunda imleç Tamam düğmesi üzerinde konumlanacaktır. Enter tuşuna basılması imleci yeniden boy alanına konumlandıracaktır.

## Klavye Kısayolları

### Ana İletişim Kutusu

* `Alt+A`: VKİ hesaplamasını gerçekleştirir.
* `Alt+L`: Alanları temizler ve imleci boy alanına yerleştirir.
* `Alt+H`: Hesaplama geçmişini görüntüler.
* `Alt+C`: İletişim kutusunu kapatır (Esc tuşunu da kullanabilirsiniz).

## Teşekkürler

Yardımları bu projeyi mümkün kılan katkıda bulunanlar Rui Fonte, Noelia ve Dalen'e özel teşekkürler.

## Çevirmenler

* **Portekizce (Brezilya), pt_BR**: Edilberto Fonseca tarafından.
* **Portekizce (Portekiz), pt_PT**: Edilberto Fonseca tarafından.
* **Rusça, ru**: Danil Kostenkov tarafından.
* **Türkçe, tr**: Umut KORKMAZ tarafından.
