import requests
import os
import datetime
from datetime import timedelta

from tuesday import get_tuesdays_of_year_to_now

from dirs import make_dirs

make_dirs()

# get all tuesdays
dates = [(tues.strftime("%Y"), tues.strftime("%m%d%y")) for tues in get_tuesdays_of_year_to_now()]

types = [
    "EURO FX - CHICAGO MERCANTILE EXCHANGE",
    "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE", 
    "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE", 
    "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE", 
    "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE", 
    "EURO FX - CHICAGO MERCANTILE EXCHANGE", 
    "EURO FX/BRITISH POUND XRATE - CHICAGO MERCANTILE EXCHANGE",
    "E-MINI S&P 500 - CHICAGO MERCANTILE EXCHANGE", 
    "RUSSELL E-MINI - CHICAGO MERCANTILE EXCHANGE",
    "BITCOIN - CHICAGO MERCANTILE EXCHANGE",
    "NASDAQ MINI - CHICAGO MERCANTILE EXCHANGE",
    "ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE",
    "NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE",
    "MICRO ETHER - CHICAGO MERCANTILE EXCHANGE",

    "E-MINI S&P FINANCIAL INDEX - CHICAGO MERCANTILE EXCHANGE",
    "E-MINI S&P TECHNOLOGY INDEX - CHICAGO MERCANTILE EXCHANGE",
    "E-MINI S&P UTILITIES INDEX - CHICAGO MERCANTILE EXCHANGE",
    "E-MINI S&P REAL ESTATE INDEX - CHICAGO MERCANTILE EXCHANGE",
    "E-MINI S&P ENERGY INDEX - CHICAGO MERCANTILE EXCHANGE",


    ]

for (year, date) in dates:
    if not os.path.exists(f"./data/futures/{date}.html"):

        response = requests.get(f"https://www.cftc.gov/sites/default/files/files/dea/cotarchives/{year}/futures/deacmesf{date}.htm")

        file = open(f"./data/futures/{date}.html", "w")
        file.write(response.text)
        file.close()
        
        if response.status_code >= 200:
            print(f"Fetched: {date} - Created File")
    else:
        print(f"File: {date} - Already Exsists")

print("------")


output = {
    ty: [] for ty in types
    
}
for (year, date) in dates:
    file = open(f"./data/futures/{date}.html", 'r')

    lines = open(f"./data/futures/{date}.html", 'r').readlines()

    print(f"Date: {date}\n")

    
    for line_number, line in enumerate(file):
        
        for ty in types:

            if line.find(ty) == 0:
                print(f"{ty} @ Line: {line_number}")
                oi = lines[line_number+7].split()[-1].replace(",", "")
                t = lines[line_number+9].split()
                t = [int(l.replace(",", "")) for l in t]
                
                output[ty].append( [oi, t[0], t[1], t[3], t[4]])
                break; # only one type per line
    
    print("\n[---------------]")



for ty in types:
    fy = str(ty).replace("/", "_")
    file = open(f"./final/{fy}.csv", "w") 
    outstr = "Date,OI,Non-Commercial Long,Non-Comercial Short,Commercial Long,Commercial Short\n"

    for (_year, date), c in zip(dates, output[ty]):
        outstr += ",".join([date] + [str(s) for s in c]) + '\n'

    file.write(outstr)
    file.close()

    
        

        

