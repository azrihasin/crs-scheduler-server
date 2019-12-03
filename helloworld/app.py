from flask import *
import re
import numpy as np
from array import *
import json
import itertools
import csv
import json
from tika import parser
import textract
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import cx_Oracle

app = Flask(__name__)



@app.route('/')
def upload():  
    return render_template("timetable.html")



@app.route('/show', methods = ['POST'])  
def show():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)
        data=process(f.filename)
        load = json.loads(data)
        return render_template("timetable.html", data=data) 
     
@app.route('/insert', methods = ['POST'])  
def insert():

    conn = cx_Oracle.connect('oracle/db@localhost/XE')
    cur=conn.cursor()

    if request.method == 'POST':  
        subject = request.form['subject']
        day = request.form['day']   
        timeS = request.form['time_start'] 
        timeE = request.form['time_end'] 

        x=timeS.split(':')
        y=timeE.split(':')

        time_start_h=x[0]
        time_start_m=x[1]
        time_end_h=y[0]
        time_end_m=y[1]

        format="AM"

        if int(time_start_h)>=12:
            format="PM"

        cur.execute('select schedule_id from schedule')

        count=0

        row = cur.fetchone()
        if row == None:
            print("There are no results for this query")
            count=count+1;
        else:
            cur.execute('select MAX(schedule_id)from schedule')    
            for line in cur:
                count = line[0]+1

        cur.execute(f"insert into schedule (schedule_id,subject,day,time_start_h,time_start_m,time_end_h,time_end_m,format) values ({count},'{subject}','{day}',{time_start_h},{time_start_m},{time_end_h},{time_end_m},'{format}')");
        #cur.execute(f"insert into schedule (schedule_id,doc_name) values ({b}, '{a}')"); 
        cur.execute('commit')  
        cur.close()
        conn.close() 

        return render_template("timetable.html") 

if __name__ == '__main__':  
    app.run(debug = True)  



def process(f):

    pdf = wi(filename = f, resolution = 300)
    pdfImage = pdf.convert('jpeg')

    imageBlobs = []

    for img in pdfImage.sequence:
        imgPage = wi(image = img)
        imageBlobs.append(imgPage.make_blob('jpeg'))

    recognized_text = []

    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang = 'eng')
        recognized_text.append(text)
    
    
    file = open('a.txt', 'w')

    file.write(text) 


    file.close()

    print("done")

    with open("a.txt", "r") as ins:
        array = []
        for line in ins:
            array.append(line)


    #print(array)

    #array.append(text)'''


    monformat=[]
    tueformat=[]
    wedformat=[]
    thurformat=[]
    friformat=[]



    mon=[]
    tue=[]
    wed=[]
    thur=[]
    fri=[]


    montime=[]
    tuetime=[]
    wedtime=[]
    thurtime=[]
    fritime=[]

    i=0
    a=0
    b=0
    c=0
    d=0
    e=0
    f=0




    prevline="";



    while i< len(array):
    
    
    
        if re.search("MON",array[i]):

            
            
            if re.findall("\w{2,4}\s\d{4}",array[i]):
                
                code = re.findall("\w{2,4}\s\d{4}",array[i])
            
                mon.append(code)

            
            

            elif re.findall("\w{2,4}\s\d{4}",prevline):

                code1 = re.findall("\w{2,4}\s\d{4}",prevline)
                
                mon.append(code1)

            elif re.findall("\w{2,4}\s\d{4}",array[i-2]):

                code2 = re.findall("\w{2,4}\s\d{4}",array[i-2])
                
                mon.append(code2)

            else:

                code3 = re.findall("\w{2,4}\s\d{4}",array[i-3])
                
                mon.append(code3)

            #for time


            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i])

                montime.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i])

                montime.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                
                montime.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i]):
    
                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                
                montime.append(date)

            #for format

            if re.search('\sAM\s',array[i]):

                monformat.append("AM")
                print(monformat)

            elif re.search('\sPM\s',array[i]):

                monformat.append("PM")

        elif re.search("M-W",array[i]):

            

            if re.findall("\w{2,4}\s\d{4}",array[i]):

            
                code = re.findall("\w{2,4}\s\d{4}",array[i])

                mon.append(code)
                wed.append(code)

            elif re.findall("\w{2,4}\s\d{4}",prevline):

                code1 = re.findall("\w{2,4}\s\d{4}",prevline)
                
                mon.append(code1)
                wed.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}",array[i-2])
                
                mon.append(code2)
                wed.append(code2)


            #for time


            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i])

                montime.append(date)
                wedtime.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i])

                montime.append(date)
                wedtime.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                
                montime.append(date)
                wedtime.append(date)
                
            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i]):
    
                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                
                montime.append(date)
                wedtime.append(date)
            #for format

            if re.search('\sAM\s',array[i]):

                monformat.append("AM")
                wedformat.append("AM")

            elif re.search('\sPM\s',array[i]):

                monformat.append("PM")
                wedformat.append("PM")

        elif re.search("TUE",array[i]):

        

            if re.findall("\w{2,4}\s\d{4}",array[i]):
            
                code = re.findall("\w{2,4}\s\d{4}",array[i])


                tue.append(code)

            elif re.findall("\w{2,4}\s\d{4}",prevline):

                code1 = re.findall("\w{2,4}\s\d{4}",prevline)
                
                tue.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}",array[i-2])
                
                tue.append(code2)


            #for time


            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i])

                
                tuetime.append(date)
                

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i])

                
                tuetime.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\s\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s\s[\\-]\s\d{1,2}\.\d{2}",array[i])

                
                tuetime.append(date)


            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                tuetime.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i]):
    
                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                tuetime.append(date)

            #for format

            if re.search('\sAM\s',array[i]):

                tueformat.append("AM")
            

            elif re.search('\sPM\s',array[i]):

                tueformat.append("PM")
            

        elif re.search("THU",array[i]):

    

            if re.findall("\w{2,4}\s\d{4}",array[i]):
            
                code = re.findall("\w{2,4}\s\d{4}",array[i])

                thur.append(code)

            elif re.findall("\w{2,4}\s\d{4}",prevline):

                code1 = re.findall("\w{2,4}\s\d{4}",prevline)
                
                thur.append(code1)


            else:

                code2 = re.findall("\w{2,4}\s\d{4}",array[i-2])
                
                thur.append(code2)

            #for time


            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i])

                
                thurtime.append(date)
                

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i])

                
                thurtime.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                thurtime.append(date)


            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i]):
    
                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                thurtime.append(date)

            #for format

            if re.search('\sAM\s',array[i]):

                thurformat.append("AM")
            

            elif re.search('\sPM\s',array[i]):

                thurformat.append("PM")
                

        elif re.search("T-TH",array[i]):
            

            if re.findall("\w{2,4}\s\d{4}",array[i]):
                code = re.findall("\w{2,4}\s\d{4}",array[i])

                tue.append(code)
                thur.append(code)

                

            elif re.findall("\w{2,4}\s\d{4}",prevline):

                code1 = re.findall("\w{2,4}\s\d{4}",prevline)
                
                tue.append(code1)
                thur.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}",array[i-2])
                
                tue.append(code2)
                thur.append(code2)


            #for time


            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i])

                
                
                tuetime.append(date)
                thurtime.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i])

                
                tuetime.append(date)
                thurtime.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                
                tuetime.append(date)
                thurtime.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i]):
    
                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                
                tuetime.append(date)
                thurtime.append(date)

            #for format

            if re.search('\sAM\s',array[i]):

                tueformat.append("AM")
                thurformat.append("AM")

            elif re.search('\sPM\s',array[i]):

                tueformat.append("PM")
                thurformat.append("PM")

        elif re.search("WED",array[i]):
            
            
            if re.findall("\w{2,4}\s\d{4}",array[i]):
                code = re.findall("\w{2,4}\s\d{4}",array[i])

                
                wed.append(code)
            

            elif re.findall("\w{2,4}\s\d{4}",prevline):

                code1 = re.findall("\w{2,4}\s\d{4}",prevline)
                
                wed.append(code1)

            elif re.findall("\w{2,4}\s\d{4}",array[i-2]):

                code1 = re.findall("\w{2,4}\s\d{4}",array[i-2])
                
                wed.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}",array[i-3])
                
                wed.append(code2)
            

            #for time


            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i])

                
                wedtime.append(date)
                

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i])

                
            
                wedtime.append(date)

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                wedtime.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i]):
    
                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                wedtime.append(date) 

            #for format

            if re.search('\sAM\s',array[i]):

            
                wedformat.append("AM")

            elif re.search('\sPM\s',array[i]):

                
                wedformat.append("PM")
                
        elif re.search("FRI",array[i]):
        
            if re.findall("\w{2,4}\s\d{4}",array[i]):
            
                code = re.findall("\w{2,4}\s\d{4}",array[i])

                fri.append(code)

            elif re.findall("\w{2,4}\s\d{4}",prevline):

                code1 = re.findall("\w{2,4}\s\d{4}",prevline)
                
                fri.append(code1)

            elif re.findall("\w{2,4}\s\d{4}",array[i-2]):

                code1 = re.findall("\w{2,4}\s\d{4}",array[i-2])
                
                fri.append(code1)

            else:

                code2 = re.findall("\w{2,4}\s\d{4}",array[i-3])
                
                fri.append(code2)


            #for time


            if re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}\.\d{2}",array[i])

                
                
                fritime.append(date)
            

            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\s\d{1,2}",array[i])

                
                fritime.append(date)
        
            elif re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i]):

                date = re.findall("\d{1,2}\.\d{2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                fritime.append(date)

            elif re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i]):
    
                date = re.findall("\d{1,2}\s[\\-]\d{1,2}\.\d{2}",array[i])

                fritime.append(date)

            #for format

            if re.search('\sAM\s',array[i]):

                friformat.append("AM")
            

            elif re.search('\sPM\s',array[i]):

                friformat.append("PM")
                

        else :

            None



        prevline=array[i]
        i+=1;


    lengthmon=len(mon)
    lengthtue=len(tue)
    lengthwed=len(wed)
    lengththur=len(thur)
    lengthfri=len(fri)

    daymon=[]
    daytue=[]
    daywed=[]
    daythur=[]
    dayfri=[]



    i=0

    while i< len(mon):
        daymon.insert(i, "MON")
        
        i+=1
        
    i=0    
    while i< len(tue):
        daytue.insert(i, 'TUE')

        i+=1
        
    i=0
    while i< len(wed):
        daywed.insert(i, 'WED')

        i+=1
        
    i=0
    while i< len(thur):
        daythur.insert(i, 'THUR')

        i+=1
        
    i=0
    while i< len(fri):
        dayfri.insert(i, 'FRI')

        i+=1






    day=[]
    start_time=[]

    mon = [i[0] for i in mon]
    montime = [i[0] for i in montime]
    tue = [i[0] for i in tue]
    tuetime = [i[0] for i in tuetime]
    wed = [i[0] for i in wed]
    wedtime = [i[0] for i in wedtime]
    thur = [i[0] for i in thur]
    thurtime = [i[0] for i in thurtime]
    fri = [i[0] for i in fri]
    fritime = [i[0] for i in fritime]

    start_time=[i.split('-')[0] for i in montime] 
    end_time=[i.split('-')[1] for i in montime]

    start_time_tue=[i.split('-')[0] for i in tuetime] 
    end_time_tue=[i.split('-')[1] for i in tuetime]

    start_time_wed=[i.split('-')[0] for i in wedtime] 
    end_time_wed=[i.split('-')[1] for i in wedtime]

    start_time_thur=[i.split('-')[0] for i in thurtime] 
    end_time_thur=[i.split('-')[1] for i in thurtime]

    start_time_fri=[i.split('-')[0] for i in fritime] 
    end_time_fri=[i.split('-')[1] for i in fritime]

    day1=tuple(zip(daymon,mon,start_time,end_time,monformat))
    day2=tuple(zip(daytue,tue,start_time_tue,end_time_tue,tueformat))
    day3=tuple(zip(daywed,wed,start_time_wed,end_time_wed,wedformat))
    day4=tuple(zip(daythur,thur,start_time_thur,end_time_thur,thurformat))
    day5=tuple(zip(dayfri,fri,start_time_fri,end_time_fri,friformat))




    document=day1+day2+day3+day4+day5


    #print(document)

    header=['DAY','SUBJECT','START','END','FORMAT']


            
    with open('timetable.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(header)

    with open('timetable.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(document)


            


    csvFilePath = "timetable.csv"
    jsonFilePath = "timetable.json"
    arr = []
    #read the csv and add the arr to a arrayn

    with open (csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        #print(csvReader)
        for csvRow in csvReader:
            arr.append(csvRow)
                    

    '''with open(jsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, indent = 5))'''

    data=json.dumps(arr, indent = 5);
    
    return data;

