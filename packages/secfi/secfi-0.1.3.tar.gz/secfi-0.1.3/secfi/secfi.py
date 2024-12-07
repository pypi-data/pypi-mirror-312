import pandas as pd
import requests
from bs4 import BeautifulSoup



def getCiks() -> pd.DataFrame:
    try:
        url_ciks = "https://www.sec.gov/files/company_tickers.json"
        headers = {"User-Agent":"osojuanferpity@xmail.com"}
        r_ciks = requests.get(url_ciks, headers = headers)
        ciks = pd.DataFrame(r_ciks.json()).T.set_index('ticker')
        ciks['cik'] = ciks['cik_str'].astype(str).str.zfill(10)
        return ciks
    except Exception as e:
        print(e)
        ciks = pd.DataFrame(columns=['cik_str', 'title', 'cik'])
        ciks.index.name = "ticker"
        return ciks


def getFils(ticker:str) -> pd.DataFrame:
    try:
        ciks = getCiks()
        cik = ciks.loc[ticker].cik
        url_subms = 'https://data.sec.gov/submissions'
        headers = {"User-Agent":"osojuanferpity@xmail.com"}
        r_subms = requests.get( f"{url_subms}/CIK{cik}.json", headers=headers)
        df = pd.DataFrame(r_subms.json().get('filings').get('recent'))
        base = f'https://www.sec.gov/Archives/edgar/data'
        df['url'] = base + '/' + cik + '/' + df['accessionNumber'].str.replace('-', '') + '/' + df['primaryDocument']
        return df
    except:
        print("Ticker not found")
        cols = ['accessionNumber', 'filingDate', 'reportDate', 'acceptanceDateTime',
                'act', 'form', 'fileNumber', 'filmNumber', 'items', 'core_type', 'size',
                'isXBRL', 'isInlineXBRL', 'primaryDocument', 'primaryDocDescription', 'url']
        return pd.DataFrame(columns=cols)


def scrapLatest(ticker:str, form:str) -> str:
    df = getFils(ticker)
    try:
        url = df.loc[df['form']==form].iloc[0].url
    except:
        print(f"Form {form} not found")
        url = ""

    text = ""
    try:
        if url != "":
            text = scrap(url)
    except Exception as e:
        print(e)
    return text



def scrap(url, timeout=15):
    try:
        headers = {"User-Agent":"osojuanferpity@xmail.com"}
        get_response = requests.get(url, headers=headers,timeout=timeout)
        if get_response.headers['Content-Type'].lower().find('html') != -1:
            soup = BeautifulSoup(get_response.content, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()    
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            # filter too long words (comp scripts, styles, tokens, links etc)
            max_length = 200
            words = text.split(' ')
            filtered_words = [word for word in words if len(word) <= max_length]
            text = ' '.join(filtered_words)
            return text
        else:
            return f"not supported content: {get_response.headers['Content-Type']}"
    except requests.Timeout:
        return "timeout error"
    except Exception as e:
        return f"Exception: {e}"

