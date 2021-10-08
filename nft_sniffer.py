from pandas.io import html
from selenium import webdriver
import pandas as pd
import time 

class_names = {'magiceden':'text-white fs-14px text-truncate','digitaleyes':'border border-color-main-secondary px-3.5 py-1 md:py-1.5 text-light-blue w-1/2 flex justify-end h-full items-center'}
marketplaces = {0:'magiceden',1:'digitaleyes'}

urls = {'magiceden':'https://magiceden.io/marketplace?collection_symbol=','digitaleyes':'https://digitaleyes.market/collections/'}
#TODO input from csv file
input_data = pd.read_csv('nft_collection.csv', sep=',', header=None) 
driver = webdriver.Firefox(executable_path=r'C:\Users\megam\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe')
data = {}
data['Collection'] = []
for j in range(input_data.shape[0]): 
    data['Collection'].append(input_data[0][j])
    for i in range(2): #1 
        marketplace = marketplaces[i]
        if (j == 0 and i == 0) or (j == 0 and i == 1):
            data[marketplace] = [] 
        marketplaceUrl = urls[marketplace]
        url = marketplaceUrl+input_data[i][j]
        print(url)
        driver.get(url)
        time.sleep(3)
        try:
            floorWindow = driver.find_element_by_xpath("(//*[contains(@class, '%s')])[1]"%class_names[marketplace])
            if i == 1:
                floorWindow= (floorWindow.find_element_by_tag_name('span').text)
                data[marketplace].append(floorWindow)
            else: 
                floorWindow = floorWindow.text
                data[marketplace].append(floorWindow)
        except:
            data[marketplace].append('Not found q.q')
    
driver.close()
print(data)
data = pd.DataFrame(data)
html = data.to_html()
text_file = open("index.html","w", encoding='utf-8')
text_file.write(html)
text_file.close()
