import pandas as pd
from itertools import chain

df = pd.read_csv('skills.csv', names=['words', 'url', 'title'])
df = df.drop_duplicates(subset=['url'])

wl = [i.split("'")[1:-1:2] for i in df.iloc[:, 0].values]

wordseries = pd.Series(list(chain(*wl)))
wordseries.value_counts()
