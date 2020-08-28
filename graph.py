import pandas as pd
import matplotlib.pyplot as plt
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

df = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv', index_col=False)

df2 = pd.DataFrame(df.data.str.split("T").tolist(), columns="data ora".split())
df2['tamponi'] = df[['tamponi']].diff(periods=1)/1000
df2['Δ positivi'] = df[['variazione_totale_positivi']]/10
#df2['data'] = df['data'].str.split("T", n = 1, expand = False)


#df2['EMA'] = df2.iloc[:,1].ewm(span=14,adjust=False).mean()
df2['SMA'] = df2.iloc[:,3].rolling(window=7).mean()
print(df2.tail(15))

df2.index = df2.data
plt.figure(figsize=[15,8])
plt.grid(True)
plt.plot(df2['Δ positivi'],label='Δ positivi · 10')
plt.plot(df2['tamponi'],label='tamponi · 1000')
#plt.plot(df2['EMA'],label='EMA')
plt.plot(df2['SMA'],label='SMA', color='#000000')
plt.legend(loc=2)
plt.axhline(y=234, xmin=0, linestyle="--", label="lockdown +30% · 10", linewidth=1.0, color='#ff0000')

plt.show()
