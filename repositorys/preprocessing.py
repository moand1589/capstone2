import pandas as pd

data = pd.read_csv(r'C:\Users\USER\Desktop\수집데이터_iloveyou2.csv',encoding='ANSI')
data["content"] = data["content"].str.replace(pat=r'[^\w]', repl=r' ', regex=True)
data.to_csv(r'C:\Users\USER\Desktop\수집데이터_iloveyou2.csv',encoding='ANSI')