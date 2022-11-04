import numpy as np
import pandas as pd
# import tensorflow as tf
import matplotlib.pyplot as plt
import pandas_datareader as data
# from tensorflow.keras.models import load_model
import streamlit as st
import math

top50 = ["ADANIPORTS.NS","ASIANPAINT.NS","AXISBANK.NS","BAJFINANCE.NS","BAJAJFINSV.NS",
          "BHARTIARTL.NS","BPCL.NS","BRITANNIA.NS","CIPLA.NS","COALINDIA.NS","DIVISLAB.NS",
          "DRREDDY.NS","EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFC.NS","HDFCBANK.NS","HDFCLIFE.NS",
          "HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS","ICICIBANK.NS","INDUSINDBK.NS","INFY.NS","IOC.NS",
          "ITC.NS","JSWSTEEL.NS","KOTAKBANK.NS","LT.NS","M&M.NS","MARUTI.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS",
          "POWERGRID.NS","RELIANCE.NS","SBIN.NS","SBILIFE.NS","SUNPHARMA.NS","TATACONSUM.NS","TATAMOTORS.NS",
          "TATASTEEL.NS","TCS.NS","TECHM.NS","TITAN.NS","ULTRACEMCO.NS","UPL.NS","WIPRO.NS"]

# start = "2010-01-01"
# end = "2022-03-01"

st.title("Stock strategy maker")

start = st.text_input("Enter start date(yyyy-mm--dd) ","2020-10-01")

end = st.text_input("Enter end date(yyyy-mm--dd) ","2022-10-01")

invstm = int(st.text_input("investment ","1000000"))

top = int(st.text_input("top n stocks  ","10"))

res = st.button("start")

if res:
    x = [i+"_open" for i in top50]
    y = [i+"_close" for i in top50]
    q = [i+"_qty" for i in top50]
    dv = [i+"_dv" for i in top50]

    z = x+y+q+dv

    lst = pd.DataFrame(columns=z)
    #invstm = 1000000
    pps = invstm//50


    for i in top50:
        df = data.DataReader(i,'yahoo',start,end)
        lst[i+"_open"] = df.Open
        lst[i+"_close"] = df.Close
        lst[i+"_qty"] = pps//lst[i+"_open"].iloc[0]
        lst[i+"_dv"] = lst[i+"_close"] * lst[i+"_qty"]

    dv = [i+"_dv" for i in top50]
    # dv
    lst["ec"] = lst[dv].sum(axis=1)
    # lst.head()

    past100 = {}
    for i in top50:
        past100[i] = lst[i+"_close"].iloc[-1]/(lst[i+"_close"].iloc[-100]-1)

    best = sorted(past100.items(), key=lambda x: x[1],reverse=True)
    top10 = []
    for i in range(top):
        top10.append(best[i][0])

    st.write("TOP N selected stocks")
    st.write(top10)


    pps1 = invstm//top
    #pps1


    x1 = [i+"_open" for i in top10]
    y1 = [i+"_close" for i in top10]
    q1 = [i+"_qty" for i in top10]
    dv1 = [i+"_dv" for i in top10]

    z1 = x1+y1+q1+dv1

    lst1 = pd.DataFrame(columns=z1)
    # lst1


    for i in top10:
        df = data.DataReader(i,'yahoo',start,end)
        lst1[i+"_open"] = df.Open
        lst1[i+"_close"] = df.Close
        lst1[i+"_qty"] = pps1//lst1[i+"_open"].iloc[0]
        lst1[i+"_dv"] = lst1[i+"_close"] * lst1[i+"_qty"]

    dv1 = [i+"_dv" for i in top10]
    lst1["ec"] = lst1[dv1].sum(axis=1)

    nf = data.DataReader('^NSEI','yahoo',start,end)
    nf["qty"]= invstm//nf.Open.iloc[0]
    nf["ec"] = nf["qty"]*nf["Close"]





    #Visualizations

    st.subheader("Daily Closing Price of investment")
    fig = plt.figure(figsize=(10,5))
    # plt.plot(df.Close)
    lst.ec.plot(label = "benchmark")
    nf.ec.plot(label = "nifty")
    lst1.ec.plot(label = "strategy")
    plt.title("Daily Closing Price of investment", fontsize=20)
    plt.legend(loc="upper left")
    st.pyplot(fig)



    nf_cagr = ((nf.ec.iloc[-1]/nf.ec.iloc[0])**0.5)*100
    lst_cagr = ((lst.ec.iloc[-1]/lst.ec.iloc[0])**0.5)*100
    lst1_cagr = ((lst1.ec.iloc[-1]/lst1.ec.iloc[0])**0.5)*100
    st.write("CAGR")
    st.write("NIFTY    BENCHMARK    STRATEGY  ")
    st.write(nf_cagr,lst_cagr,lst1_cagr)

    nf["dr"] = nf.ec.pct_change(1)
    lst["dr"] = lst.ec.pct_change(1)
    lst1["dr"] = lst1.ec.pct_change(1)

    nf_vol = (nf.dr.std()*math.sqrt(252))*100
    lst_vol = (lst.dr.std()*math.sqrt(252))*100
    lst1_vol = (lst1.dr.std()*math.sqrt(252))*100
    st.write("VOLATILITY")
    st.write("NIFTY    BENCHMARK    STRATEGY  ")
    st.write(nf_vol,lst_vol,lst1_vol)


    nf_shr = (nf.dr.mean()/nf.dr.std())*math.sqrt(252)
    lst_shr = (lst.dr.mean()/lst.dr.std())*math.sqrt(252)
    lst1_shr = (lst1.dr.mean()/lst1.dr.std())*math.sqrt(252)
    st.write("SHARPE")
    st.write("NIFTY    BENCHMARK    STRATEGY  ")
    st.write(nf_shr,lst_shr,lst1_shr)
