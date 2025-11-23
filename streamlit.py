import pandas as pd
import streamlit as st

# Tämän tehtävän välivaiheita tarkastellaan debug.ipynb-tiedostossa.

# Datan esikäsittely ##########################################################

# Haetaan CSV:stä DataFrameksi omaan muuttujaansa data, joka sisältää 
# Helsinki-Vantaan ja Rovaniemen lentokenttien matkustajamäärätiedot vuonna 
# 2024 kuukausittain ryhmiteltyinä:
flights_df = pd.read_csv("https://pxdata.stat.fi/PxWeb/sq/a74f5130-03b1-426d-94b3-158f4e262286", encoding="latin1")

# Haetaan DataFramesta sellaiset sarakkeet, jotka kuvaavat kunkin kuukauden 
# matkustajiamääriä:
month_columns = [name for name in flights_df.columns if "2024M" in name]

# Muodostetaan Yhteensä-sarake siten, että sen arvoksi lasketaan kummankin 
# lentokentän riville lentokentän kuukausittaisten matkustajamäärien 
# summa:
flights_df["Yhteensä"] = flights_df[month_columns].sum(axis=1)


def get_seasonal_travel_percent(row, month1, month2, month3):
    # Muunnetaan rivin eli Series-instanssin indeksiobjekti listaksi ja 
    # haetaan GeeksforGeeksin (2025) esimerkkiä hyödyntäen mm. parametrien 
    # avulla määriteltyjen kuukausialkioiden indeksinumerot tästä listasta: 
    month1_i = list(row.index).index(f"2024M{month1}")
    month2_i = list(row.index).index(f"2024M{month2}")
    month3_i = list(row.index).index(f"2024M{month3}")
    year_total_i = list(row.index).index("Yhteensä")

    # Haetaan Series-instanssia edustavan row-parametrin values-attribuutin 
    # avulla mm. parametrien määrittelemien kuukausien matkustajamääräarvot 
    # niihin liittyvien indeksien perusteella, jotta mm. vuodenajan 
    # kuukausittaiset matkustajamäärät saadaan summattua:
    season_total = row.values[month1_i] + row.values[month2_i] + row.values[month3_i]
    year_total = row.values[year_total_i]
    
    # Palautetaan vuodenajan kuukausien yhteenlasketun matkustajamäärän 
    # ja vuoden kokonaismatkustajamäärän osamäärä pyöristettynä: 
    return round(season_total / year_total * 100)

# Muodostetaan uusiin vuodenaikoja kuvaaviin sarakkeisiin arvot 
# rivikohtaisesti hyödyntämällä DataFrame-luokan apply-metodia ja edelleen 
# get_seasonal_travel_percent-funktiota apply-metodin parametrina olevan 
# lambda-funktion tuloksena. get_seasonal_travel_percent-funktiolle syötettävä 
# lambda-funktion row-parametri on DataFramen yksittäinen rivi, sillä 
# apply-metodissa käsitellään nimenomaan DataFramen rivejä axis-parametrin 
# arvon ollessa 1 (pandas a).
flights_df["Talvi 2024"] = flights_df.apply(lambda row: get_seasonal_travel_percent(row, "12", "01", "02"), axis=1)
flights_df["Kevät 2024"] = flights_df.apply(lambda row: get_seasonal_travel_percent(row, "03", "04", "05"), axis=1)
flights_df["Kesä 2024"] = flights_df.apply(lambda row: get_seasonal_travel_percent(row, "06", "07", "08"), axis=1)
flights_df["Syksy 2024"] = flights_df.apply(lambda row: get_seasonal_travel_percent(row, "09", "10", "11"), axis=1)

# Jätetään DataFrameen ainoastaan filter-metodissa määritellyt sarakkeet, 
# sillä muita sarakkeita ei visualisointiin tarvita. Metodi siis muodostaa 
# alitaulukon, johon on sisällytetty ainaostaan ne rivit/sarakkeet, jotka 
# items-parametrilla määritellään. Antamalla axis-parametrin arvoksi 1 
# kerrotaan, että kyseessä on sarakesuunta. (pandas b.)
flights_df= flights_df.filter(items=["Ilmoittava lentoasema", 
                                     "Talvi 2024", 
                                     "Kevät 2024", 
                                     "Kesä 2024", 
                                     "Syksy 2024"], axis=1)

###############################################################################

# Tiedon visualisoiminen käyttöliittymässä ####################################

st.header("Bonustehtävä 5: Lentokenttädatan visualisointi Streamlit-sovelluksena")

st.subheader("Matkustajamäärien prosentuaalinen jakautuminen vuodenajoittain lentokenttäkohtaisesti")

# Visualisoidaan lentokenttien matkustajamäärien prosentuaalinen osuus 
# vuodenaikakohtaisesti pylväskaaviona Streamlitin st.bar_chart-funktion 
# avulla. Funktio ottaa data-parametrina vastaan DataFramen, jonka sarakkeiden
# perusteella visualisointi tehdään. x- ja y-parametrien arvoiksi annetaan
# sarakkeiden nimet, joiden mukaan akselit muodostetaan. y-parametrin arvoksi 
# voidaan asettaa myös useampi sarake listana. Kun stack-parametrin arvoksi 
# puolestaan asetetaan False, yksittäisen ryhmän pylväät ryhmitellään 
# vierekkäin eikä päällekäin kasattuina. Pylväsryhmät piirretään vaakatasoon, 
# kun horizontal-parametrin arvo asetetaan todeksi. Metodilta löytyy myös 
# sort-parametri, mutta sen avulla pylväsryhmän pylväitä ei saada kuitenkaan 
# keskenään järjesteltyä suurusjärjestykseen. (Snowflake Inc c.) Annetaan 
# x-akselille siis lentoasemat ja y-akselille vuodenajat.
st.bar_chart(flights_df, 
             x="Ilmoittava lentoasema", 
             y=["Talvi 2024", "Kevät 2024", "Kesä 2024", "Syksy 2024"], 
             stack=False, 
             sort=True, 
             horizontal=True, 
             y_label="", 
             x_label="Prosentuaalinen osuus matkustajien lentokenttäkohtaisesta kokonaismäärästä vuonna 2024")

# Pythonin usean rivin kommentti toimii Streamlitissä taikakomentona, jolloin 
# kommentin sisältämä teksti visualisoidaan käyttöliittymään (Snowflake Inc b): 
"""
Helsinki-Vantaan lentokentän vilkkain vuodenaika matkustajamäärien osalta 
vuonna 2024 oli kesä, kun taas Rovaniemen lentokentällä vilkkainta oli 
talvella. Rovaniemen lentokenttää käyttävien matkustajien osalta seuraavaksi 
suosituin vuodenaika oli syksy. Kuitenkin matkustajamäärien prosentuaalinen 
ero suosituimman ja toisiksi suosituimman vuodenajan välillä oli merkittävä - 
yli 30 prosenttiyksikköä. Rovaniemelle tai Rovaniemen kautta Lappiin 
matkaavien osalta talvi oli siis selvästi pääsesonki. 

Sen sijaan Helsinki-Vantaan lentokentän kävijämäärissä ei vuonna 2024 ollut 
yhtä suuria eroja eri vuodenaikojen välillä. Suosituimman vuodenajan eli 
kesän ja toisiksi suosituimman vuodenajan eli syksyn välillä ero 
matkailijamäärissä oli vain kaksi prosenttiyksikköä. Kesän suosio voisi 
selittyä suomalaisten kesälomasesongilla, jolloin lomailijat saattavat 
suunnata ulkomaille ja sieltä takaisin.
"""

# Download-napin toimintojen taustalogiikan toteuttamisessa mukaillaan
# Snowflake Incin (d) esimerkkiä. Tehdään convert_for_download-funktio, joka
# nimensä mukaisesti muuttaa parametrina saadun DataFramen utf-8-enkoodatuksi 
# CSV-tiedostoksi. Funktion yllä käytetään st.cache_data-dekoraattoria, jolla 
# toimintaa saadaan nopeutettua: sen sijaan, että funktiota ajetaan jokaisen 
# käyttäjätapahtuman yhteydessä uudestaan samoilla arvoilla, kuten kaikkia 
# muita koodielementtejä, funktio ajetaan vain kerran. (Snowflake Inc a).
@st.cache_data
def convert_for_download(df):
    return df.to_csv().encode("utf-8")

# Haetaan flights_csv-muuttujaan CSV-formaattiin muunnettu DataFrame 
# convert_for_download-funktion avulla.
flights_csv = convert_for_download(flights_df)

# Muodostetaan latausnappi Streamlitin download_button-funktion avulla.
# data-parametrin arvoksi asetetaan flights_csv-muuttujaan talletettu 
# matkustajamäärien vuodenaikakohtaiset osuudet sisältävä CSV-tiedosto, joka 
# latautuu napin painalluksesta.
st.download_button(label="Lataa tiedot CSV:nä", 
                   data=flights_csv, 
                   file_name="Matkustajamäärien prosentuaalinen jakautuminen vuodenajoittain lentokenttäkohtaisesti.csv",
                   mime="text/csv",
                   icon=":material/download:")

###############################################################################

# Lähteet 

# GeeksforGeeks 2025. Python List index() - Find Index of Item. Viitattu 23.11.2025 https://www.geeksforgeeks.org/python/python-list-index/.
# pandas a. pandas.DataFrame.apply. Viitattu 23.11.2025 https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html.
# pandas b. pandas.DataFrame.filter. Viitattu 23.11.2025 https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.filter.html.
# Snowflake Inc a. Caching overview. Viitattu 23.11.2025 https://docs.streamlit.io/develop/concepts/architecture/caching.
# Snowflake Inc b. Magic. Viitattu 23.11.2025 https://docs.streamlit.io/develop/api-reference/write-magic/magic.
# Snowflake Inc c. st.bar_chart. Viitattu 23.11.2025 https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart.
# Snowflake Inc d. st.download_button. Viitattu 23.11.2025 https://docs.streamlit.io/develop/api-reference/widgets/st.download_button.