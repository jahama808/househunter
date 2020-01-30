#!/usr/bin/python


from bs4 import BeautifulSoup
import requests
from serial import Serial
import pandas as pd
import time
from datetime import datetime


def main():

    #create the results dataframe

    results_df= pd.DataFrame(columns = ['mls','price','days'])


    #use this for Raspberry Pi's
    port=Serial(port='/dev/ttyAMA0',baudrate=9600, timeout=1.0)


    eof = "\xff\xff\xff"


    mls1 = 0
    mls2 = 0
    mls3 = 0
    price1 = 0
    price2 = 0
    price3 = 0
    days1 = 0
    days2 = 0
    days3 = 0

    port.write('page 1'+eof)
    time.sleep(30)

    while True:


        now = datetime.now()
        current_time = int(now.strftime("%H"))

        if (current_time > 6 and current_time < 22):
            
            port.write('page 0'+eof)
            

            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

            }

            source = requests.get('http://www.oahure.com/Honolulu-Real-Estate2.php?Status=Active&PropertyType=CND&MLSAreaMajor=Hawaii+Kai&ListPriceMin=&ListPriceMax=800000&BedsTotalMin=3&BathsTotalMin=2&SQFTRoofedLivingMin=500&LotSizeAreaMin=&YearBuiltMin=&OrderBy=Status+Asc%2C+CloseDate+Desc%2C+ListPrice+Asc&LandTenure=Fee+Simple&Screen=LargePhoto&AssociationFeeTotalMax=&FloorNumberMin=&Neighborhood=&StreetName=&BuildingName=&btnsubmit=Search',headers=headers).text

            soup = BeautifulSoup(source,'html5lib')

            results_df.append({'mls':'25','price':888,'days':7},ignore_index=True)
            count = 1
            for listing in soup.find_all('li'):
                
                description = listing.text


                picture = listing.find('img')['src']
                pictureWeb = ("http://www.oahure.com/"+picture)
                MLSID = int(description[description.find('MLS Number:')+len('MLS Number:')+1:description.find('List Price')])
                price = description[description.find('List Price:')+len('List Price:')+1:description.find(',')+4]
                days = int(description[description.find('Days on Market:')+len('Days on Market')+2:description.find('Days on Market:')+len('Days on Market')+5])

                results_df=results_df.append({'mls':MLSID,'price':price,'days':days},ignore_index=True)

                count +=1
                print("MLS:{}     - Price: {}   - days: {}".format(MLSID,price,days))

            results_df = results_df.sort_values(by=['days'])

            port.write('page0.mls1.txt="'+str(results_df.iloc[0].iloc[0])+'"'+eof)
            port.write('page0.mls2.txt="'+str(results_df.iloc[1].iloc[0])+'"'+eof)
            port.write('page0.mls3.txt="'+str(results_df.iloc[2].iloc[0])+'"'+eof)
            port.write('page0.mls4.txt="'+str(results_df.iloc[3].iloc[0])+'"'+eof)
            port.write('page0.price1.txt="'+str(results_df.iloc[0].iloc[1])+'"'+eof)
            port.write('page0.price2.txt="'+str(results_df.iloc[1].iloc[1])+'"'+eof)
            port.write('page0.price3.txt="'+str(results_df.iloc[2].iloc[1])+'"'+eof)
            port.write('page0.price4.txt="'+str(results_df.iloc[3].iloc[1])+'"'+eof)
            port.write('page0.days1.txt="'+str(results_df.iloc[0].iloc[2])+'"'+eof)
            port.write('page0.days2.txt="'+str(results_df.iloc[1].iloc[2])+'"'+eof)
            port.write('page0.days3.txt="'+str(results_df.iloc[2].iloc[2])+'"'+eof)
            port.write('page0.days4.txt="'+str(results_df.iloc[3].iloc[2])+'"'+eof)
            port.write('page0.activenumber.txt="'+str(results_df.shape[0])+'"'+eof)

            print(results_df)
            print(results_df.shape[0])

            print ("DEBUG: GOING INTO WAIT STATE...")
            time.sleep(3600)

            #Panda Cleaning
            results_df = results_df.iloc[0:0]

        else:
            port.write('page 1'+eof)

        print ("DEBUG: GOING INTO WAIT STATE...")
        time.sleep(3600)

if __name__=="__main__":
    main()
