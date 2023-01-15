


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class yahoo_finance_website(object):

    def __init__(self, link):
        self.url = link
        self.edge_options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        

    def check_YahooFinance_site(self):
        # This function needs to be overrided by student's program
        # The function returns True if this is YahooFinance site
        # # Otherwise it returns False 
        
        print("This is Demo program")
        return False
    
    def __str__(self):
        return "(Demo) This is Yahoo Finance."

    def __del__(self):
        print("Destructor is executed!!!")
        
        
if __name__ == '__main__':
    asg2_obj = yahoo_finance_website('https://finance.yahoo.com')
    print(asg2_obj)

    if asg2_obj.check_YahooFinance_site():
        print("This is Yahoo finance (confirmed by Selenium)")
    else:
        print("This is NOT Yahoo finance (confirmed by Selenium)")   