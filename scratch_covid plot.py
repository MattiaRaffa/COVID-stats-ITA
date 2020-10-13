import pandas as pd
import matplotlib.pyplot as plt
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

df = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv', index_col=False)

df2 = pd.DataFrame(df.data.str.split("T").tolist(), columns="data ora".split())
df2['data'] = df2['data'].str.split('-', 1).str[1]

df2['tamponi'] = df[['tamponi']].diff(periods=1)/1000
df2['d positivi'] = df[['variazione_totale_positivi']]/10
df2['tasso'] = ((df['nuovi_positivi']*100)/(df['tamponi'].diff(periods=1)))*10
#df2['data'] = df['data'].str.split("T", n = 1, expand = False)


#df2['EMA'] = df2.iloc[:,1].ewm(span=14, adjust=False).mean()
df2['SMA'] = df2.iloc[:,3].rolling(window=7).mean()
print(df2.tail(15))

df2.index = df2.data
plt.figure(figsize=[15,8])
plt.grid(True)
plt.plot(df2['tasso'],label='tasso positività', color='#ae3737')
plt.plot(df2['d positivi'],label='Δ positivi x10', color='#bf9000')
plt.plot(df2['tamponi'],label='tamponi x1000', color='#0c343d')
#plt.plot(df2['EMA'],label='EMA')
plt.plot(df2['SMA'],label='SMA Δ positivi', color='#6f6868')
plt.axhline(y=234, xmin=0, linestyle="--", label="lockdown +30% x10", linewidth=1.0, color='#6f6868')
plt.axhline(y=50, xmin=0, linestyle="--", label="limite tasso WHO x10", linewidth=1.0, color='#ae3737')
plt.legend(loc=2, fancybox=False)

plt.show()