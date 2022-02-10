from hashlib import new
from tokenize import String
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
import pytesseract as pytesseract
from wand.image import Image as wi
from flask_cors import CORS, cross_origin
from datetime import datetime
import os


app = Flask(__name__)
CORS(app, support_credentials=True)

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


@app.route('/')
def upload():
    return render_template("timetable.html")


@app.route('/show', methods=['POST'])
@cross_origin()
def show():

    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        data = process(f.filename)

        return jsonify(data)


def validation(line):

    if re.search("MON", line):
        if re.search('\sAM\s|\sPM\s', line):
            return line

    elif re.search("M-W", line):
        if re.search('\sAM\s|\sPM\s', line):
            return line

    elif re.search("TUE", line):
        if re.search('\sAM\s|\sPM\s', line):
            return line

    elif re.search("THU", line):
        if re.search('\sAM\s|\sPM\s', line):
            return line

    elif re.search("T-TH", line):
        if re.search('\sAM\s|\sPM\s', line):
            return line

    elif re.search("WED", line):
        if re.search('\sAM\s|\sPM\s', line):
            return line

    elif re.search("FRI", line):
        if re.search('\sAM\s|\sPM\s', line):
            return line

def process(f):

    # 1. CONVERT PDF FILES INTO TEXT
    pdf = wi(filename=f, resolution=300)
    pdfImage = pdf.convert('jpeg')

    imageBlobs = []

    for img in pdfImage.sequence:
        imgPage = wi(image=img)
        imageBlobs.append(imgPage.make_blob('jpeg'))

    recognized_text = []

    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang='eng')
        recognized_text.append(text)

    file = open('temp.txt', 'w')

    file.write(text)

    file.close()

    print("done")

# 2. TEXT EXTRACTED ARE PLACED INSIDE TEXT FILE IN ORDER TO READ LINE BY LINE

    with open("temp.txt", "r") as ins:
        temp_array = []
        for line in ins:
            temp_array.append(line)

    if os.path.exists("temp.txt"):
        os.remove("temp.txt")
        os.remove(f)
    else:
        print("The file does not exist")

# 3. INITIALIZE ARRAY TO START AN EXTRACTION PROCESS

    line = []
    parent_row_index = []

# 4. VALIDATES LINE THAT WE GONNA EXTRACT SO IT ONLY CONTAINS INFORMATION WE NEED

    valid_array = map(validation, temp_array)

    array = [i for i in valid_array if i]

# 5. EXTRACT LINE USING REGEX

# a) Find the subject index

    for i, x in enumerate(array):

        p = re.findall("\w{2,4}\s\d{4}", x)

        if(len(p) > 0):
            parent_row_index.append(i)

        # print(i,p)

    # print(parent_row_index)

    # parent row index contain only parent index while parent child row index contain both child and parent index

    parent_child_index = []*len(parent_row_index)

# b) Find the subject child

    for i, x in enumerate(parent_row_index):

        if(i < len(parent_row_index)-1):

            temp_index = []

            # The parent chil are store in the list first

            temp_index.append(parent_row_index[i])

            # find how many child the parent has

            child_index_count = parent_row_index[i]-parent_row_index[i+1]

            # then append the child along with their parent by increment the index ( note that number + 1 because number start with 0 )
            if(child_index_count < -1):
                for number in range((abs(child_index_count))-1):
                    temp_index.append(parent_row_index[i]+(number+1))

            parent_child_index.append(temp_index)

        else:

            temp_index = []

            temp_index.append(parent_row_index[i])

            if(parent_row_index[i] < len(array)):
                for number in range((parent_row_index[i])-(len(array))):
                    temp_index.append(parent_row_index[i]+(number+1))

            parent_child_index.append(temp_index)


# c) map the code course and course name

    mon = []
    tue = []
    wed = []
    thur = []
    fri = []
    saturday = []
    sunday = []

    # find the subject day

    parent_row_withData = []

    for i, x in enumerate(parent_row_index):

        temp = []

        subject, day = getData(array[x], parent_row_index[i])

        temp.append(subject)
        temp.append(day)

        parent_row_withData.append(temp)

    for i, x in enumerate(parent_child_index):

        for j, z in enumerate(parent_child_index[i]):

            # Append to subject

            if re.findall("\w{2,4}\s\d{4}", array[z]):

                subject = listToJson (parent_row_withData[i][0])

            else:

                temp_subject = getDataWithoutName(
                    array[z], parent_row_withData[i][0])
                
                subject = listToJson(temp_subject)

            day = ""

            keyword_list = ["MON", "M-W", "TUE", "THU", "T-TH", "WED", "FRI"]

            all_text = array[z]

            for item in keyword_list:
                if item in all_text:
                    day = item

            if(day == "MON"):
                mon.append(subject)

            elif (day == "M-W"):
                mon.append(subject)
                wed.append(subject)

            elif (day == "TUE"):

                tue.append(subject)

            elif (day == "THU"):

                thur.append(subject)

            elif (day == "T-TH"):

                tue.append(subject)
                thur.append(subject)

            elif (day == "WED"):

                wed.append(subject)

            elif (day == "FRI"):

                fri.append(subject)

            # print(parent_row_withData[i][1])

    # print(*wed, sep='\n')

    data = {
        "monday": mon,
        "tuesday": tue,
        "wednesday": wed,
        "thursday":  thur,
        "friday": fri,
    }

    return data

def getData(line, event_count):

    list = line.split(" ")

    formatIndex, dayIndex, statusIndex = getAllIndex(list)

    # Find start and End time of the subject

    time = (' '.join(list[dayIndex+1:formatIndex]))

    formattedTime = getStartAndEndTime(time)

    code = (' '.join(list[:statusIndex-1]))

    name = (' '.join(list[statusIndex+1:dayIndex-1]))

    section = list[statusIndex-1]

    start = formatTo24Hour(formattedTime[0], list[formatIndex])

    end = formatTo24Hour(formattedTime[1], list[formatIndex])

    day = list[dayIndex]

    format = list[formatIndex]

    venue = (' '.join(list[formatIndex+1:])).replace('\n', '')

    creditHour = list[dayIndex-1]

    # print(line)

    # print(creditHour)

    event = "event"

    eventNum = int(event_count) + 1

    event = "event-" + str(eventNum)
    
    subjectList = [code, section, name, creditHour, start, end, format, venue, event ]

    return subjectList, day

def getDataWithoutName(line, parent_line):

    list = line.split(" ")

    formatIndex, dayIndex, statusIndex = getAllIndex(list)

    # Find start and End time of the subject

    time = (' '.join(list[dayIndex+1:formatIndex]))

    formattedTime = getStartAndEndTime(time)

    code = parent_line[0]

    name = parent_line[2]

    section = parent_line[1]

    event = parent_line[8]

    start = formatTo24Hour(formattedTime[0], list[formatIndex])

    end = formatTo24Hour(formattedTime[1], list[formatIndex])

    day = list[dayIndex]

    format = list[formatIndex]

    venue = (' '.join(list[formatIndex+1:])).replace('\n', '')

    creditHour = parent_line[3]    

    subjectList = [code, section, name, creditHour, start, end, format, venue, event]

    return subjectList

def listToJson(line):

    code = line[0]

    name = line[2]

    section = line[1]

    event = line[8]

    start = line[4]

    end = line[5]

    format = line[6]

    venue = line[7]

    creditHour = line[3]

    subjectJson = {"code":code,"section":section, "name":name, "credit_hour":creditHour,"start_time":start, "end_time":end, "time_format":format, "venue":venue, "event":event}

    return subjectJson

def getStartAndEndTime(time):

    newTime = time.replace('-', ' ').replace('.', ':').split(' ')

    time_list = [x for x in newTime if x != '']

    return time_list

def getAllIndex(seperatedList):

    formatIndex = 0
    dayIndex = 0
    statusIndex = 0

    for i, sWord in enumerate(seperatedList):

        # Get format

        if sWord == "AM" or sWord == "AM\n":

            formatIndex = i

        elif sWord == "PM" or sWord == "PM\n":

            formatIndex = i

        # Get day

        if sWord == "MON":

            dayIndex = i

        elif sWord == "M-W":

            dayIndex = i

        elif sWord == "TUE":

            dayIndex = i

        elif sWord == "THU":

            dayIndex = i

        elif sWord == "T-TH":

            dayIndex = i

        elif sWord == "WED":

            dayIndex = i

        elif sWord == "FRI":

            dayIndex = i

        # Get status

        if(sWord == "R" or sWord == "RSV" or sWord == "R_"):

            statusIndex = i

    return formatIndex, dayIndex, statusIndex

def formatTo24Hour(time, format):

    formattedTime = ""

    #Make sure all time has double dot

    temp_time = addDoubleDot(time)   

    if(format == "AM"):

        formattedTime = temp_time

    elif(format == "PM"):

        x = temp_time.split(":")

        hour = x[0]
        minute = x[1]

        new_time = str(int(hour)+12)+":"+minute 

        formattedTime = new_time


    return formattedTime

def addDoubleDot(time):

    if ":" in time:

        return time

    else:

        temp_time = time + ":" +"00"
        
        return temp_time


if __name__ == '__main__':
    app.run(debug=True)
