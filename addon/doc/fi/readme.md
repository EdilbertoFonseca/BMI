# Kehon painoindeksin (BMI) laskeminen

* **Author**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Creation Date**: 11/08/2022.
* **Versio**: 2026.2.1
* **Lisenssi**: [GPL v2](https://www.gnu.org/licenses/gpl-2.0.html)
* **Viimeksi tarkistettu**: 04.05.2026

## Johdanto

Tervetuloa BMI-lisäosan pariin! Tämä on lisäosa, joka on suunniteltu auttamaan kehon painoindeksin (BMI) määrittämisessä. Se on kansainvälinen mittari, jota käytetään henkilön kehon rasvatason arviointiin. Tämän lisäosan avulla voit helposti laskea painoindeksisi syöttämällä pituutesi ja painosi.

Perinteisen BMI-laskennan lisäksi tämä uusi versio tarjoaa lisäominaisuuksia, kuten ihanteellisen BMI:n laskemisen pituuden perusteella sekä yksityiskohtaisen luokituksen Maailman terveysjärjestön (WHO) kriteerien mukaan tarjoten henkilökohtaista terveysopastusta. Lisäosa tallentaa nyt myös viimeisimmät 10 laskelmaa, joihin pääsee nopeasti Alt+H-pikanäppäimellä.

Huomautus: BMI:n asianmukaisessa tulkinnassa on tärkeää ottaa huomioon muut tekijät, kuten kehon koostumus, rasvan jakautuminen, ikä, sukupuoli ja yleinen terveydentila. On aina suositeltavaa kääntyä terveydenhuollon ammattilaisen, kuten lääkärin tai ravitsemusterapeutin, puoleen tarkemman arvioinnin ja asianmukaisten terveys- ja paino-ohjeiden saamiseksi.

## Asennus

Tässä ovat vaiheittaiset ohjeet BMI-lisäosan asentamiseksi NVDA-ruudunlukuohjelmaan:

1. Avaa NVDA:ssa **Työkalut**-valikko ja etsi **Lisäosakauppa**.
2. Siirry **Saatavilla olevat lisäosat** -välilehdellä **Etsi**-kenttään.
3. Hae sanalla "BMI". Paina tuloksissa **Enter** tai **Käytä** ja valitse sitten **Asenna**.
4. Käynnistä NVDA uudelleen ottaaksesi muutokset käyttöön.

Olet nyt valmis käyttämään BMI-lisäosaa ja laskemaan kehon painoindeksisi suoraan NVDA:ssa.

## Asetukset

Lisäosalle ei ole konfigurointiohjeita, sillä sen käyttö on yksinkertaista ja suoraviivaista.

## Käyttö

Paina `Alt+Windows+I` tai käytä NVDA-valikkoa `NVDA+N`, Työkalut > Laske BMI käynnistääksesi lisäosan. Näkyviin tulee valintaikkuna, jossa on kaksi syötekenttää:

1. Pituus – johon pituutesi senttimetreinä (CM) tulee valita tai syöttää.
2. Paino – johon painosi kiloina (KG) tulee valita tai syöttää.

Kun olet täyttänyt kaikki kentät, paina Laske-painiketta pikanäppäimellä `Alt+A` tai paina Enter Laske-painikkeen kohdalla.

NVDA lukee valintaikkunan, joka sisältää:

* Nykyisen BMI-laskelmasi tuloksen.
* Yksityiskohtaisen luokituksesi WHO:n parametrien mukaan (alipaino, normaali paino, ylipaino, lihavuusaste I, II tai III).
* Pituuteesi perustuvan arvioidun ihanteellisen BMI-arvon.
* Ohjeviestin, jossa korostetaan lisätekijöiden merkitystä terveyden arvioinnissa.

Valintaikkunan lopussa kurssori on OK-painikkeen kohdalla. Enter-näppäimen painaminen siirtää kursorin takaisin pituuskenttään.

## Pikanäppäimet

### Päävalintaikkuna

* `Alt+A`: Suorittaa BMI-laskennan.
* `Alt+L`: Tyhjentää kentät ja asettaa kursorin pituuskenttään.
* `Alt+H`: Näyttää laskentahistorian.
* `Alt+C`: Sulkee valintaikkunan (voit käyttää myös Esc-näppäintä).

## Kiitokset

Erityiskiitokset avustajille Rui Fonte, Noelia ja Dalen, joiden apu teki tämän projektin mahdolliseksi.

## Kääntäjät

* **Portugali (Brasilia), pt_BR**: Edilberto Fonseca.
* **Portugali (Portugali), pt_PT**: Edilberto Fonseca.
* **Venäjä, ru**: Danil Kostenkov.
* **Turkki, tr**: Umut KORKMAZ.
