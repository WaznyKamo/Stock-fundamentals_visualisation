from bs4 import BeautifulSoup
import requests
import pandas as pd

directory = r"C:\Users\Kamil\OneDrive\Python projects\Stock-visualisations\Data\WiG20_fundamental_indicators.csv"

url_wartosc_rynkowa = 'https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/'
url_rentownosc = 'https://www.biznesradar.pl/wskazniki-rentownosci/'
url_przeplywy_pieniezne = 'https://www.biznesradar.pl/wskazniki-przeplywow-pienieznych/'
url_zadluzenie = 'https://www.biznesradar.pl/wskazniki-zadluzenia/'
url_plynnosc = 'https://www.biznesradar.pl/wskazniki-plynnosci/'
url_aktywnosc = 'https://www.biznesradar.pl/wskazniki-aktywnosci/'
stock_list = ['ACP', 'ALE', 'ALR', 'CCC', 'CDR', 'CPS', 'DNP', 'JSW', 'KGHM', 'LPP', 'LTS',
              'MRC', 'OPL', 'PEO', 'PGE', 'PGN', 'PKN', 'PKO', 'PZU', 'SPL', 'TPE']

stock_data_list = []

quarters = []


def get_quarters(soup):
    dates = []
    for date_soup in soup.find_all('th', attrs={"class": "thq h"}):
        dates.append(date_soup.text.split()[0])
    dates.append(soup.find('th', attrs={"class": "thq h newest"}).text.split()[0])
    return dates


def get_indicator(soup, indicator_tag):
    indicator_raw = soup.find('tr', attrs={"data-field": indicator_tag})
    indicators = []
    if indicator_raw:
        for indicator_soup in indicator_raw.find_all("td", attrs={"class": "h"}):
            if indicator_soup.find("span", attrs={"class": "pv"}):
                indicators.append(indicator_soup.find("span", attrs={"class": "pv"}).text)
            else:
                indicators.append(None)
    else:
        indicators = [None for x in range(len(get_quarters(soup)))]
    return indicators


for stock_index in range(len(stock_list)):
    print('Loading data: ' + stock_list[stock_index])
    stock_url_wr = url_wartosc_rynkowa + stock_list[stock_index]
    response_wr = requests.get(stock_url_wr)
    soup_wr = BeautifulSoup(response_wr.text, features='html.parser')
    stock_quarters = get_quarters(soup_wr)
    # Market value indicators
    WK = get_indicator(soup_wr, 'WK')                      # book value
    C_WK = get_indicator(soup_wr, 'CWK')                   # price/book value
    Z = get_indicator(soup_wr, 'Z')                        # profit
    C_Z = get_indicator(soup_wr, 'CZ')                     # price/profit
    P = get_indicator(soup_wr, 'P')                        # income
    C_P = get_indicator(soup_wr, 'CP')                     # price/income
    ZO = get_indicator(soup_wr, 'ZO')                      # operational profit
    C_ZO = get_indicator(soup_wr, 'CZO')                   # price/operational profit
    WK_Graham = get_indicator(soup_wr, 'WKGraham')
    C_WK_Graham = get_indicator(soup_wr, 'CWKGraham')
    EV = get_indicator(soup_wr, 'EV')
    EV_P = get_indicator(soup_wr, 'EVP')
    EV_EBIT = get_indicator(soup_wr, 'EVEBIT')
    EV_EBITDA = get_indicator(soup_wr, 'EVEBITDA')
    stock_data = pd.DataFrame(list(zip(stock_quarters, WK, C_WK, Z, C_Z, P, C_P, ZO, C_ZO, WK_Graham, C_WK_Graham, EV, EV_P, EV_EBITDA, EV_EBIT)),
                              columns=['Kwarta??y', 'Warto???? ksi??gowa', 'Cena/WK', 'Zysk na akcj??','Cena/Zysk', 'Przych??d', 'Cena/Przych??d', 'Zysk operacyjny', 'Cena/Zysk operacyjny', 'Warto???? ksi??gowa Grahama',
                                       'Cena/Warto???? ksi??gowa Grahama', 'Warto???? przedsi??biorstwa', 'Warto???? przedsi??biorstwa/Przychody', 'Warto???? przedsi??biorstwa/EBIT', 'Warto???? przedsi??biorstwa/EBITDA'])
    stock_data.insert(0, 'Sp????ka', stock_list[stock_index])
    # Profitability indicators
    stock_url_rentownosc = url_rentownosc + stock_list[stock_index]
    response_rentownosc = requests.get(stock_url_rentownosc)
    soup_rentownosc = BeautifulSoup(response_rentownosc.text, features='html.parser')
    stock_data['ROE'] = get_indicator(soup_rentownosc, 'ROE')
    stock_data['ROA'] = get_indicator(soup_rentownosc, 'ROA')
    stock_data['Mar??a zysku operacyjnego'] = get_indicator(soup_rentownosc, 'OPM')
    stock_data['Mar??a zysku netto'] = get_indicator(soup_rentownosc, 'ROS')
    stock_data['Mar??a zysku ze sprzeda??y'] = get_indicator(soup_rentownosc, 'RS')
    stock_data['Mar??a zysku brutto'] = get_indicator(soup_rentownosc, 'GPM')
    stock_data['Mar??a zysku brutto ze sprzeda??y'] = get_indicator(soup_rentownosc, 'RBS')
    stock_data['Rentowno???? operacyjna aktyw??w'] = get_indicator(soup_rentownosc, 'ROPA')
    # Cash flow indicators
    stock_url_pp = url_przeplywy_pieniezne + stock_list[stock_index]
    response_pp = requests.get(stock_url_pp)
    soup_pp = BeautifulSoup(response_pp.text, features='html.parser')
    stock_data['Udzia?? zysku netto w przep??ywach operacyjnych'] = get_indicator(soup_pp, 'ZNPO')
    stock_data['Wska??nik ??r??de?? finansowania inwestycji'] = get_indicator(soup_pp, 'ZFI')
    # Liabilities indicators
    stock_url_zadluzenie = url_zadluzenie + stock_list[stock_index]
    response_zadluzenie = requests.get(stock_url_zadluzenie)
    soup_zadluzenie = BeautifulSoup(response_zadluzenie.text, features='html.parser')
    stock_data['Zad??u??enie og??lne'] = get_indicator(soup_zadluzenie, 'DTAR')
    stock_data['Zad??u??enie kapita??u w??asnego'] = get_indicator(soup_zadluzenie, 'CG')
    stock_data['Zad??u??enie d??ugoterminowe'] = get_indicator(soup_zadluzenie, 'LDER')
    stock_data['Zad??u??enie ??rodk??w trwa??ych'] = get_indicator(soup_zadluzenie, 'PZAT')
    stock_data['Pokrycie aktyw??w trwa??ych kapita??ami sta??ymi'] = get_indicator(soup_zadluzenie, 'PELDR')
    stock_data['Trwa??o???? struktury finansowania'] = get_indicator(soup_zadluzenie, 'TSF')
    stock_data['Zastosowanie kapita??u obcego'] = get_indicator(soup_zadluzenie, 'ZKO')
    stock_data['Wska??nik og??lnej sytuacji finansowej'] = get_indicator(soup_zadluzenie, 'OSF')
    stock_data['Zad??u??enie netto'] = get_indicator(soup_zadluzenie, 'NetDebt')
    stock_data['Zad??u??enie netto / EBITDA'] = get_indicator(soup_zadluzenie, 'NetDebtEBITDA')
    stock_data['Zad??u??enie finansowe netto'] = get_indicator(soup_zadluzenie, 'DebtFin')
    stock_data['Zad??u??enie finansowe netto / EBITDA'] = get_indicator(soup_zadluzenie, 'DebtFinEBITDA')
    # Liquidity indicators
    stock_url_plynnosc = url_plynnosc + stock_list[stock_index]
    response_plynnosc = requests.get(stock_url_plynnosc)
    soup_plynnosc = BeautifulSoup(response_plynnosc.text, features='html.parser')
    stock_data['I stopie?? pokrycia'] = get_indicator(soup_plynnosc, 'SP1')
    stock_data['II stopie?? pokrycia'] = get_indicator(soup_plynnosc, 'SP2')
    stock_data['P??ynno???? got??wkowa'] = get_indicator(soup_plynnosc, 'CAR')
    stock_data['P??ynno???? szybka'] = get_indicator(soup_plynnosc, 'QR')
    stock_data['P??ynno???? bie????ca'] = get_indicator(soup_plynnosc, 'CR')
    stock_data['P??ynno???? podwy??szona'] = get_indicator(soup_plynnosc, 'PP')
    stock_data['Pokrycie zobowi??za?? nale??no??ciami'] = get_indicator(soup_plynnosc, 'RCLR')
    stock_data['Udzia?? kapita??u pracuj??cego w aktywach'] = get_indicator(soup_plynnosc, 'KP')
    # Activity indicators
    stock_url_aktywnosc = url_aktywnosc + stock_list[stock_index]
    response_aktywnosc = requests.get(stock_url_aktywnosc)
    soup_aktywnosc = BeautifulSoup(response_aktywnosc.text, features='html.parser')
    stock_data['Pokrycie koszt??w kapita??em obrotowym'] = get_indicator(soup_aktywnosc, 'PKKO')
    stock_data['Rotacja nale??no??ci'] = get_indicator(soup_aktywnosc, 'RN')
    stock_data['Cykl nale??no??ci'] = get_indicator(soup_aktywnosc, 'CRN')
    stock_data['Cykl zobowi??za??'] = get_indicator(soup_aktywnosc, 'CPZ')
    stock_data['Rotacja zapas??w'] = get_indicator(soup_aktywnosc, 'RZ')
    stock_data['Cykl zapas??w'] = get_indicator(soup_aktywnosc, 'CRZ')
    stock_data['Rotacja maj??tku obrotowego'] = get_indicator(soup_aktywnosc, 'RMO')
    stock_data['Rotacja maj??tku trwa??ego'] = get_indicator(soup_aktywnosc, 'RMT')
    stock_data['Rotacja maj??tku og????em'] = get_indicator(soup_aktywnosc, 'RM')
    stock_data['Cykl operacyjny'] = get_indicator(soup_aktywnosc, 'COP')
    stock_data['Cykl konwersji got??wki'] = get_indicator(soup_aktywnosc, 'CSP')

    stock_data_list.append(stock_data)

final_dataframe = pd.concat(stock_data_list)

final_dataframe.to_csv(directory, index=False)
print('File created')

