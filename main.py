


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from yahoo_finance import yahoo_finance_website
import csv
import re
from datetime import datetime


class stock(yahoo_finance_website):
    def __init__(self):
        self.asg2_obj = yahoo_finance_website('https://finance.yahoo.com')
        self.browser = self.asg2_obj.browser

    def main(self):

        a = input('Please enter stock code:').strip()
        if a.split('.')[1].upper() == 'HK' and a.split('.')[0].isdigit():
            try:
                # summary page
                self.summary(a)
                # sustainability page
                self.sustainability(a)                
                # statistics page
                self.statistics(a)

            except Exception as e:
                print(f'Error as: {e}')
        else:
            print('Invalid stock code')
            self.main()

    # summary page
    def summary(self, a):
        self.browser.get(f'https://finance.yahoo.com/quote/{a}?p={a}')
        # time
        now = datetime.now().strftime('%m/%d/%y')
        tim = datetime.now().strftime('%H:%M:%S')
        # wait
        wait = WebDriverWait(self.browser, 100)
        wait.until(EC.presence_of_element_located((By.ID, 'quote-summary')))
        # target value
        price = self.browser.find_element(By.XPATH,
                                          '//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]').text
        table = self.browser.find_element(By.ID, 'quote-summary')
        table1 = table.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > table > tbody')
        table2 = table.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > table > tbody')
        volume = table1.find_element(By.CSS_SELECTOR, 'tr:nth-child(7) > td:nth-child(2) > fin-streamer').text
        close = table1.find_element(By.CSS_SELECTOR, 'tr:nth-child(1) > td:nth-child(2)').text
        cap = table2.find_element(By.CSS_SELECTOR, 'tr:nth-child(1) > td:nth-child(2)').text
        eps = table2.find_element(By.CSS_SELECTOR, 'tr:nth-child(4) > td:nth-child(2)').text
        bid = table1.find_element(By.CSS_SELECTOR, 'tr:nth-child(3) > td:nth-child(2)').text
        ask = table1.find_element(By.CSS_SELECTOR, 'tr:nth-child(4) > td:nth-child(2)').text
        self.save(
            {'Data': now, 'Time': tim, 'Price': price, 'Volume': volume, 'Previous Close': close, 'Market Cap': cap,
             'EPS': eps, 'Bid': bid, 'Ask': ask}, a.split('.')[0])

    # statistics
    def statistics(self, a):
        self.browser.get(f'https://finance.yahoo.com/quote/{a}/key-statistics?p={a}')
        # wait
        wait = WebDriverWait(self.browser, 100)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Mstart\(a\).Mend\(a\)')))
        # target value
        table = self.browser.find_element(By.XPATH,
                                          '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[3]/div/div[4]/div/div')
        revenue = table.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > td:nth-child(2)').text
        share = table.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(2) > td:nth-child(2)').text
        quarterly = table.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(3) > td:nth-child(2)').text
        profit = table.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(4) > td:nth-child(2)').text
        ebitda = table.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(5) > td:nth-child(2)').text
        avi = table.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(6) > td:nth-child(2)').text
        eps = table.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(7) > td:nth-child(2)').text
        growth = table.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(8) > td:nth-child(2)').text
        # covert B as 1 * 10 ** 9
        revenue = self.BM(revenue)
        profit = self.BM(profit)
        avi = self.BM(avi)   
        # If EBITDA has B also convert as 1*10**9
        if str(ebitda)[0].isdigit():
            ebitda = self.BM(ebitda)

        # add dollar sign $ 
        eps = f'${eps}'
        # Quarterly Earnings Growth as decimals
        growth = float(growth.split('%')[0]) / 100
        self.save(
            {'Revenue': revenue, 'Revenue Per Share': share, 'Quarterly Revenue Growth': quarterly,
             'Gross Profit': profit, 'EBITDA': ebitda, 'Net Income Avi to Common': avi, 'Diluted EPS': eps,
             'Quarterly Earnings Growth': growth}, f'{a.split(".")[0]}IncomeStatement')

    # sustainability page
    def sustainability(self, a):
        self.browser.get(f'https://finance.yahoo.com/quote/{a}/sustainability?p={a}')
        # wait
        wait = WebDriverWait(self.browser, 100)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Mt\(15px\).smartphone_Mb\(20px\)')))
        # target value
        table = self.browser.find_element(By.ID, 'Col1-0-Sustainability-Proxy')
        table1 = table.find_element(By.CSS_SELECTOR, 'section > div:nth-child(1) > div')
        governance = table1.find_element(By.XPATH, 'div[4]/div/div[2]/div[1]').text
        social = table1.find_element(By.XPATH, 'div[3]/div/div[2]/div[1]').text
        environment = table1.find_element(By.XPATH, 'div[2]/div/div[2]/div[1]').text
        esg = table1.find_element(By.XPATH, 'div[1]/div/div[2]/div[1]').text
        controversy = table.find_element(By.XPATH, 'section/div[2]/div[2]/div/div/div/div[1]/div').text
        self.save(
            {'Governance Risk': governance, 'Social Risk': social, 'Environment Risk': environment,
             'ESG Risk': esg, 'Controversy Level': controversy}, f'{a.split(".")[0]}Sustainability')

    def BM(self, num):
        s = {'B': 10 ** 9, 'M': 10 ** 6}
        a = re.findall(r"[A-Z]", num)
        return int(float(num.split(f'{a[0]}')[0]) * s.get(a[0]))

    # save as CSV
    def save(self, data, name):
        try:
            with open(f'{name}.csv', 'w', newline='') as fp:
                writer = csv.DictWriter(fp, list(data))
                writer.writeheader()
                writer.writerow(data)
        except Exception as e:
            print(f'Failed to save file, error as {e}')
        fp.close()
        
        
        
    def check_YahooFinance_site(self):
        
        try:
            title = self.browser.title
            assert 'Yahoo Finance' in title
            return True
        except Exception as e:
            super().check_YahooFinance_site()


        

    def __del__(self):
        self.asg2_obj.browser.close()
        


if __name__ == '__main__':
    A = stock()
    A.check_YahooFinance_site()
    A.main()

