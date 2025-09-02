import requests
import os
import datetime
from datetime import timedelta

from tuesday import get_tuesdays_of_year_to_now
from dirs import make_dirs

make_dirs()
# get all tuesdays
dates = [tues.strftime("%m%d") for tues in get_tuesdays_of_year_to_now()]
# dates = ["0107"]
types = [
    "GOLD",
    "SILVER",
    "COPPER #1"
    
    ]

for date in dates:
    if not os.path.exists(f"./data/metals/{date}.html"):

        response = requests.get(f"https://www.cftc.gov/sites/default/files/files/dea/cotarchives/2025/futures/deacmxsf{date}25.htm")

        file = open(f"./data/metals/{date}.html", "w")
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
for date in dates:
    file = open(f"./data/metals/{date}.html", 'r')

    lines = open(f"./data/metals/{date}.html", 'r').readlines()

    print(f"Date: {date}\n")

    
    for line_number, line in enumerate(file):
        
        for ty in types:

            if line.find(ty) == 0:
                print(f"{ty} @ Line: {line_number}")
                oi = lines[line_number+7].split()[-1].replace(",", "")
                t = lines[line_number+9].replace(":", "").split()
                t = [int(l.replace(",", "")) for l in t]
                
                output[ty].append( [oi, t[0], t[1], t[3], t[4]])
                break; # only one type per line
    
    print("\n[---------------]")



for ty in types:
    file = open(f"./final/{ty}.csv", "w") 
    outstr = "Date,OI,Non-Commercial Long,Non-Comercial Short,Commercial Long,Commercial Short\n"

    for date, c in zip(dates, output[ty]):
        outstr += ",".join([date] + [str(s) for s in c]) + '\n'

    file.write(outstr)
    file.close()

    
        

        

