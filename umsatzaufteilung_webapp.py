
from datetime import timedelta
import pandas as pd
import streamlit as st

st.title("Umsatzaufteilung auf Monate")

uploaded_file = st.file_uploader("Excel-Datei mit Gästedaten hochladen", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Anzeige der Originaldaten
    st.subheader("Originaldaten")
    st.dataframe(df)

    # Datumsfelder in datetime-Objekte umwandeln
    df['Check-in'] = pd.to_datetime(df['Check-in'], format='%d.%m.%Y')
    df['Check-out'] = pd.to_datetime(df['Check-out'], format='%d.%m.%Y')

    monatserloese = []

    for index, row in df.iterrows():
        gesamt_naechte = (row['Check-out'] - row['Check-in']).days
        if gesamt_naechte <= 0:
            continue
        umsatz_pro_nacht = row['Gesamtumsatz'] / gesamt_naechte

        aktuelles_datum = row['Check-in']
        while aktuelles_datum < row['Check-out']:
            monat = aktuelles_datum.strftime('%Y-%m')
            monatserloese.append({
                'Name': row['Name'],
                'Monat': monat,
                'Umsatz': umsatz_pro_nacht
            })
            aktuelles_datum += timedelta(days=1)

    df_monate = pd.DataFrame(monatserloese)
    umsatz_pro_monat = df_monate.groupby(['Name', 'Monat']).sum().reset_index()

    st.subheader("Aufgeteilter Umsatz pro Monat")
    st.dataframe(umsatz_pro_monat)

    # Download-Link
    output_file = 'umsatz_pro_monat.xlsx'
    umsatz_pro_monat.to_excel(output_file, index=False)
    with open(output_file, 'rb') as f:
        st.download_button(
            label="Ergebnis als Excel herunterladen",
            data=f,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
