import time
import streamlit as st
import yfinance as yf
import numpy as np
import plotly.express as px
from datetime import datetime

st.warning(
    "DISCLAIMER : Tools ini hanya 'membantu' Anda, bukan menjadi 'dasar' atau 'alasan utama' Anda untuk memilih saham yang Anda inginkan. Tools di situs ini tidak dimaksudkan sebagai nasihat keuangan, investasi, atau perdagangan. Investasi saham melibatkan risiko, termasuk kehilangan modal. Penggunaan teknologi Artificial Intelligence dalam investasi saham juga memiliki risikonya tersendiri dan tidak ada jaminan bahwa teknologi ini akan membantu Anda menghasilkan keuntungan yang pasti. Anda bertanggung jawab penuh atas keputusan investasi Anda sendiri. Kami tidak bertanggung jawab atas kerugian atau kerusakan yang mungkin timbul dari penggunaan tools yang disediakan di situs ini. Anda harus melakukan analisa Anda sendiri terlebih dahulu dan mengevaluasi informasi sebelum Anda mengambil tindakan apapun berdasarkan tools yang dibagikan di situs ini.",
    icon="⚠️")

st.title("Tools Resiko & Return Harga Saham")

ticker1 = st.text_input(
        "Ticker saham (pakai '.JK' di akhir ticker untuk saham Indonesia)",
        "ASSA.JK",
        placeholder='Masukkan ticker saham disini, misalnya ASSA.JK').upper()
data1 = yf.Ticker(ticker1).history(period="1y")
stck_pct1 = data1["Close"].pct_change()
rets1 = stck_pct1.dropna()

if not ticker1:
    st.warning("Masukkan ticker saham yang Anda inginkan. Gunakan '.JK' di akhir ticker untuk saham Indonesia. Misal, BBRI.JK",
        icon="⚠️")
else:
    if data1.empty:
        st.warning(
            "Data dari ticker saham ini tidak ditemukan. Gunakan '.JK' dibelakang ticker saham untuk saham Indonesia. Misal BBCA.JK",
            icon="⚠️")
    else:

        return_naik = (stck_pct1.mean() + stck_pct1.std()) * 100
        return_turun = (stck_pct1.mean() - stck_pct1.std()) * 100

        st.subheader("Grafik Return Harga Saham")
        st.line_chart(rets1, x_label="Tanggal", y_label="Return Harga Saham")

        if stck_pct1.max() > 0:
            st.write(
                "Return harga saham tertinggi dalam 1 tahun terakhir : :green[%.2f]%%"
                % (stck_pct1.max() * 100))
        else:
            st.write(
                "Return harga saham tertinggi dalam 1 tahun terakhir : :red[%.2f]%%"
                % (stck_pct1.max() * 100))

        if stck_pct1.min() > 0:
            st.write(
                "Return harga saham terendah dalam 1 tahun terakhir : :green[%.2f]%%"
                % (stck_pct1.min() * 100))
        else:
            st.write(
                "Return harga saham terendah dalam 1 tahun terakhir : :red[%.2f]%%"
                % (stck_pct1.min() * 100))

        if stck_pct1.mean() > 0:
            st.write(
                "Rata - rata return harga saham dalam 1 tahun terakhir : :green[%.2f]%%"
                % (stck_pct1.mean() * 100))
        else:
            st.write(
                "Rata - rata return harga saham dalam 1 tahun terakhir : :red[%.2f]%%"
                % (stck_pct1.mean() * 100))

        st.write(
            "Return harga saham dalam 1 tahun terakhir naik dan turun sebesar : :blue[%.2f]%% dari rata - rata return harga sahamnya"
            % (stck_pct1.std() * 100))

    st.subheader("Resiko vs Keuntungan Harga Saham")

    if data1.empty:
        st.warning("Tidak ada data yang ditemukan", icon="⚠️")
    else:
        days = st.slider("Tentukan jumlah hari yang kalian inginkan", 2, 365,
                         365)

        dt = 1 / days
        mu = rets1.mean()
        sigma = rets1.std()

        def stock_monte_carlo(start_price, days, mu, sigma):

            price = np.zeros(days)
            price[0] = start_price
            shock = np.zeros(days)
            drift = np.zeros(days)

            for x in range(1, days):

                shock[x] = np.random.normal(loc=mu * dt,
                                            scale=sigma * np.sqrt(dt))
                drift[x] = mu * dt
                price[x] = price[x - 1] + (price[x - 1] * (drift[x] +
                                                           (shock[x] * 7)))

            return price

        start_price = data1['Close'][-1]
        runs = 1000
        simulations = np.zeros(runs)
        np.set_printoptions(threshold=5)

        for run in range(runs):
            simulations[run] = stock_monte_carlo(start_price, days, mu,
                                                 sigma)[days - 1]

        q = np.percentile(simulations, 1)
        max_price = simulations.max()

        if ticker1.endswith('.JK'):
            if 1 < days <= 90:
                st.write(
                    "99% kemungkinan :red[resiko kerugian] yang bisa Anda alami dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    " untuk :blue[1 lot] nya adalah sebesar  :red[-Rp.%.0f]"
                    % (((start_price - q) * 100) * 0.2),
                    ", 1% kemungkinan :red[resiko kerugian] bisa lebih dari itu"
                )
                st.write(
                    "Kemungkinan :green[keuntungan] yang bisa Anda dapat dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lot] nya adalah sebesar :green[Rp.%.0f]"
                    % (((max_price - start_price) * 100) * 0.1))
            elif 91 < days <= 180:
                st.write(
                    "99% kemungkinan :red[resiko kerugian] yang bisa Anda alami dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    " untuk :blue[1 lot] nya adalah sebesar :red[-Rp.%.0f]"
                    % (((start_price - q) * 100) * 0.4),
                    ", 1% kemungkinan :red[resiko kerugian] bisa lebih dari itu")
                st.write(
                    "Kemungkinan :green[keuntungan] yang bisa Anda dapat dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lot] nya adalah sebesar :green[Rp.%.0f]"
                    % (((max_price - start_price) * 100) * 0.2))
            elif 181 < days <= 270:
                st.write(
                    "99% kemungkinan :red[resiko kerugian] yang bisa Anda alami dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    " untuk :blue[1 lot] nya adalah sebesar :red[-Rp.%.0f]"
                    % (((start_price - q) * 100) * 0.7),
                    ", 1% kemungkinan :red[resiko kerugian] bisa lebih dari itu")
                st.write(
                    "Kemungkinan :green[keuntungan] yang bisa Anda dapat dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lot] nya adalah sebesar :green[Rp.%.0f]"
                    % (((max_price - start_price) * 100) * 0.3))
            elif 271 < days <= 365:
                st.write(
                    "99% kemungkinan :red[resiko kerugian] yang bisa Anda alami dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    " untuk :blue[1 lot] nya adalah sebesar :red[-Rp.%.0f]"
                    % ((start_price - q) * 100),
                    ", 1% kemungkinan :red[resiko kerugian] bisa lebih dari itu")
                st.write(
                    "Kemungkinan :green[keuntungan] yang bisa Anda dapat dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lot] nya adalah sebesar :green[Rp.%.0f]"
                    % (((max_price - start_price) * 100) * 0.4))

        else:

            if 0 < days <= 90:
                st.write(
                    "99% kemungkinan :red[resiko kerugian] yang bisa Anda alami dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lembar] nya adalah sebesar :red[-Rp.%.0f]"
                    % (((start_price - q) * 16000) * 0.2),
                    ", 1% kemungkinan :red[resiko kerugian] bisa lebih dari itu (kurs: Rp.16,000)"
                )
                st.write(
                    "Kemungkinan :green[keuntungan] yang bisa Anda dapat dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lembar] nya adalah sebesar :green[Rp.%.0f]"
                    % (((max_price - start_price) * 16000) * 0.1),
                    "(kurs: Rp.16,000)")
            elif 91 < days <= 180:
                st.write(
                    "99% kemungkinan :red[resiko kerugian] yang bisa Anda alami dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lembar] nya adalah sebesar :red[-Rp.%.0f]"
                    % (((start_price - q) * 16000) * 0.4),
                    ", 1% kemungkinan :red[resiko kerugian] bisa lebih dari itu (kurs: Rp.16,000)"
                )
                st.write(
                    "Kemungkinan :green[keuntungan] yang bisa Anda dapat dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lembar] nya adalah sebesar :green[Rp.%.0f]"
                    % (((max_price - start_price) * 16000) * 0.2),
                    "(kurs: Rp.16,000)")
            elif 181 < days <= 270:
                st.write(
                    "99% kemungkinan :red[resiko kerugian] yang bisa Anda alami dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lembar] nya adalah sebesar :red[-Rp.%.0f]"
                    % (((start_price - q) * 16000) * 0.7),
                    ", 1% kemungkinan :red[resiko kerugian] bisa lebih dari itu (kurs: Rp.16,000)"
                )
                st.write(
                    "Kemungkinan :green[keuntungan] yang bisa Anda dapat dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lembar] nya adalah sebesar :green[Rp.%.0f]"
                    % (((max_price - start_price) * 16000) * 0.3),
                    "(kurs: Rp.16,000)")
            elif 271 < days <= 365:
                st.write(
                    "99% kemungkinan :red[resiko kerugian] yang bisa Anda alami dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lembar] nya adalah sebesar :red[-Rp.%.0f]"
                    % ((start_price - q) * 16000),
                    ", 1% kemungkinan :red[resiko kerugian] bisa lebih dari itu (kurs: Rp.16,000)"
                )
                st.write(
                    "Kemungkinan :green[keuntungan] yang bisa Anda dapat dalam",
                    days, "hari kedepan jika Anda memilih saham", ticker1,
                    "untuk :blue[1 lembar] nya adalah sebesar :green[Rp.%.0f]"
                    % (((max_price - start_price) * 16000) * 0.4),
                    "(kurs: Rp.16,000)")

st.warning(
        " DISCLAIMER : Tools ini hanya 'membantu' Anda, bukan menjadi 'dasar' atau 'alasan utama' Anda untuk memilih saham yang Anda inginkan. Tools di situs ini tidak dimaksudkan sebagai nasihat keuangan, investasi, atau perdagangan. Investasi saham melibatkan risiko, termasuk kehilangan modal. Penggunaan teknologi Artificial Intelligence dalam investasi saham juga memiliki risikonya tersendiri dan tidak ada jaminan bahwa teknologi ini akan membantu Anda menghasilkan keuntungan yang pasti. Anda bertanggung jawab penuh atas keputusan investasi Anda sendiri. Kami tidak bertanggung jawab atas kerugian atau kerusakan yang mungkin timbul dari penggunaan tools yang disediakan di situs ini. Anda harus melakukan analisa Anda sendiri terlebih dahulu dan mengevaluasi informasi sebelum Anda mengambil tindakan apapun berdasarkan tools yang dibagikan di situs ini.",
        icon="⚠️")
