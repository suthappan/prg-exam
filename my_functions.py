import os
import csv
import sys
import pandas as pd
from datetime import date
from datetime import timedelta

from fpdf import FPDF
from collections import Counter
from collections import defaultdict
from array import *

ROW_FONT_SIZE = 16
ROW_HEIGHT = 5.5


COL_SEAT = 14
COL_PAPER	=30
COL_REGNO	=45
COL_NAME	=65
COL_BLANK	= 30


def readSourceFile():
	sourceFileName = input("Enter source file name :") or "1.csv"
	if sourceFileName[-4:] != ".csv":
		print("Assuming filename as " + sourceFileName + ".csv")
		sourceFileName = sourceFileName + ".csv" 
	
	if not os.path.isfile(sourceFileName):
		return False
	
	removeTmpDir = input("Temporary folder will be overwritten. Do you want to continue (Y/n)? ") or "y"
	if removeTmpDir.lower() == 'y':
		print("...deleted temporary files and moving forward")
	else:
		exit("Exiting application!")
		
	os.system('rm -r ./tmp')
	os.system('mkdir ./tmp')
	os.system('cp ./' + sourceFileName + " ./tmp/" + sourceFileName)
	input("waiting....")
	return "./tmp/" + sourceFileName


def prepare_csv_file(inputFile):
	

	""" 	Function to extract records from csv with Header Names => 	
	"	Student,Course,Slot,Branch Name,Event,Exam Date,Exam Time new fileName is 1.csv

	"
	
	"	reads source fileName	default => 1.csv
	"
	"""	
	
	# replace Branch Names with abbreviations --		
	replace_with_abbreviations(inputFile)


	#fieldnames = ["000ExamDateYYYYMMDD","000ExamTimeQ","000Event","000Branch","000Slot","000Paper","000Student","000RegNo","000ExamDate","000ExamTime"]
	fieldnames = ["000ExamDateYYYYMMDD","000ExamTimeQ","000Slot","000Paper","000Branch","000RegNo","000Student","000ExamDate","000ExamTime","000Event"]

	
	#newCSV = open('./tmp/1.csv', 'w', newline='')
	os.system('echo "000ExamDateYYYYMMDD,000ExamTimeQ,000Slot,000Paper,000Branch,000RegNo,000Student,000ExamDate,000ExamTime,000Event" > tmp/1.csv')
	#writer = csv.DictWriter(newCSV, fieldnames=fieldnames)
	#writer.writeheader()
	
	filterCriteria=getFilterCriteria()

	oCount = 0

	with open(inputFile) as csvfile:
	
		reader = csv.DictReader(csvfile)
		iCount = 0

		for row in reader:
			#try:
			Student,RegNo = row['Student'].split("(")
			RegNo = RegNo.rstrip(RegNo[-1])
			Paper = row['Course'].split("(").pop()[:-3].strip()
			Slot = row['Slot']
			Branch = row['Branch Name']
			Event = row['Event']
			ExamDateYYYYMMDD = row['Exam Date'][6::1] + row['Exam Date'][3:5:1] + row['Exam Date'][0:2:1]
			if ExamDateYYYYMMDD == "":
				ExamDateYYYYMMDD = "-"
			
			ExamTimeQ = ExamTime = row['Exam Time']
			if ExamTimeQ == "":
				ExamTimeQ = "-"
				
			ExamDate = 	row['Exam Date']			
			#print(Student, RegNo, Paper, Slot, Branch,Event,ExamDate,ExamTime)
			if(validRecord(filterCriteria,ExamDateYYYYMMDD, ExamTimeQ, Slot, Paper, Branch) ):				

				#writer.writerow({
				#'000ExamDateYYYYMMDD': ExamDateYYYYMMDD, 
				#'000ExamTimeQ': ExamTimeQ,
				#'000Slot':Slot,
				#'000Paper':Paper,
				#'000Branch':Branch,
				#'000RegNo':RegNo,
				#'000Student':Student.title(),
				#'000ExamDate':ExamDate,
				#'000ExamTime':ExamTime,
				#'000Event': Event
				#})
				os.system('echo "' + 
				ExamDateYYYYMMDD  + ',' +  
				ExamTimeQ  + ',' +  
				Slot  + ',' +  
				Paper  + ',' +  
				Branch  + ',' +  
				RegNo  + ',' +  
				Student.title()  + ',' +  
				ExamDate  + ',' +  
				ExamTime  + ',' +  
				Event  +  '" >> tmp/1.csv')
				oCount = oCount + 1
			iCount = iCount + 1 

			#except:
			#	sys.exit("Pls ensure the headings in csv are exactly these: >>>>>>Student,Course,Slot,Branch Name,Event,Exam Date,Exam Time<<<<<<")
		print("Processed " + str(iCount) + " records.")
		#print("Number of records filtered oCount" + str(oCount))
		os.system('wc -l tmp/1.csv')
	# not working some records are randomly lost
	# do not know the reason...
	#sort_csv('tmp/1.csv',"tmp/2.csv",["000ExamDateYYYYMMDD","000ExamTimeQ","000Slot","000Paper","000Branch","000RegNo","000Student","000ExamDate","000ExamTime","000Event"])


	#input("This one")
	#os.system('wc -l tmp/1.csv')
	#input("End")


	os.system('sort -o tmp/2.csv -t ,  tmp/1.csv')
	

	
	
	
	
	return oCount

def replace_with_abbreviations(inputFile):

	#Remove "Appearing Student"
	os.system("sed --in-place '/Appearing Student/d' " + inputFile)

	#Replace " 	Course" with "Course"
	os.system("sed -i 's/ \tCourse/Course/' " + inputFile)


	# replace Branch names with their abbreviations
	os.system("sed -i 's/ELECTRONICS & COMMUNICATION ENGG/EC...../g' " + inputFile)
	os.system("sed -i 's/MECHANICAL ENGINEERING/ME...../g' " + inputFile)
	os.system("sed -i 's/COMPUTER SCIENCE & ENGINEERING/CS...../g' " + inputFile)
	os.system("sed -i 's/ELECTRONICS AND BIOMEDICAL ENGINEERING/EB...../g' " + inputFile)
	os.system("sed -i 's/ELECTRICAL AND ELECTRONICS ENGINEERING/EE...../g' " + inputFile)
	os.system("sed -i 's/Computer Science and Business Systems/CSBS.../g' " + inputFile)

	os.system("sed -i 's/INFORMATION TECHNOLOGY/IT...../g' " + inputFile)
	os.system("sed -i 's/CIVIL ENGINEERING/CE...../g' " + inputFile)
	os.system("sed -i 's/CHEMICAL ENGINEERING/ChmEng./g' " + inputFile)
	os.system("sed -i 's/APPLIED ELECTRONICS & INSTRUMENTATION ENGINEERING/AE-IE../g' " + inputFile)
	os.system("sed -i 's/INDUSTRIAL ENGINEERING/Ind.Eng/g' " + inputFile)
	os.system("sed -i 's/Robotics and Automation/RA...../g' " + inputFile)


 
 
def sort_csv(infile,outfile,columns):

	df = pd.read_csv(infile) 
	result = df.sort_values(columns) 
	result.to_csv(outfile)





def getFilterCriteria():
	""" filter criteria for => ExamDateYYYYMMDD, ExamTimeQ, Slot, Paper, Branch
	"""

	filterDate = input("Enter Date : ")
	filterTime = input("Enter time : ")
	filterSlot = input("Enter Slot : ")
	filterPaper = input("Enter Paper : ")
	filterBranch = input("Enter Branch : ")
	return( filterDate, filterTime, filterSlot, filterPaper, filterBranch)
	#return( filterCriteria)




	
def validRecord(filterCriteria,ExamDateYYYYMMDD, ExamTime, Slot, Paper, Branch):

	retVal = True

	filterDate = filterCriteria[0]
	filterTime = filterCriteria[1]
	filterSlot = filterCriteria[2]
	filterPaper = filterCriteria[3]
	filterBranch = filterCriteria[4]
	
	

	

	#if((ExamDateYYYYMMDD not in filterDate.split(",")) or filterDate == ""):
	if(filterDate != ""):
		if(ExamDateYYYYMMDD not in filterDate.split(",")):
			retVal = False
	
	if(filterTime != ""):
		if(ExamTime not in filterTime.split(",")):
			retVal = False



	#input(Slot+"  " + filterSlot + "   .")
	
	#if((Slot in filterSlot.split(",")) or filterSlot == ""):
	#	print("Valid record")
	#else:		
	#	retVal = False
	#	print("inValid record")

	
	if(filterSlot != ""):
		#print("not null")
		if(Slot not in filterSlot.split(",")):
			#print("not present..")
			retVal = False


	if(filterPaper != ""):
		if(Paper not in filterPaper.split(",")):
			retVal = False


	if(filterBranch != ""):
		if(Branch not in filterBranch.split(",")):
			retVal = False
	
	
	return retVal
	
	
def fetch_rooms(students=0):
# fetch rooms and respective capacities
	status=0
	

	total_no_of_students = students
	if students == "" or students == "0":
		return nil
	
	alter = input("Alteration?")
	if alter == "":
		alter = 0
	else:
		alter = int(alter)
		
	


	details=[]
	rooms=[]
	capacities=[]
	max_capacities=[]
	current_capacities=[]

	total = 0
	prg_path = os.path.abspath(os.path.dirname(__file__))
	
	no_of_students_accommodated = 0
	with open(prg_path + "/rooms.txt") as file1:
		
		for line in file1:
			line_i = line.rstrip()
			details = line_i.split(",")
			rooms.append(details[0])
			max_capacities.append(details[1])
			current_capacities.append(details[2])

			capacity = int(details[1]) + alter
			no_of_students_accommodated = no_of_students_accommodated + capacity

			#input("student = " + str(students) + ", accomodated = " + str( no_of_students_accommodated) + ", Capacity=" +  str(capacity) )
			
			if capacity >= students:
				capacities.append(capacity)
				break
			elif students > capacity:
				students = students - capacity
				capacities.append(capacity)

		#input("accomodated =" + str( no_of_students_accommodated)+", total = " + str(total_no_of_students) )					
		if no_of_students_accommodated < total_no_of_students:
			status = no_of_students_accommodated - total_no_of_students
			
			
		elif no_of_students_accommodated == total_no_of_students:
			status = 0
		else:
			#status = total_no_of_students - no_of_students_accommodated
			status = no_of_students_accommodated - total_no_of_students
							

		return capacities,rooms,status
	
	
def assign_seat(rooms,capacities,students):
	os.system('echo "000Room,000Seat" > ./tmp/room_seat.csv')
	stud = 1
	for capacity,room in zip(capacities,rooms):
		seat = 1
		while seat<=capacity//2 and stud <= students//2 :
			os.system("echo " + str(room) + ",A" + "{:02d}".format(seat) + ">> ./tmp/room_seat.csv" )
			seat=seat+1
			stud = stud + 1

		lastRoomStudents=seat-1

	stud = 1
	for capacity,room in zip(capacities,rooms):
		if capacity%2 == 1:
			capacity = capacity + 1
		if students%2 == 1:
			students = students + 1
		seat=1		
		while seat<=capacity//2 and stud <= students//2 :
			os.system("echo " + str(room) + ",B" + "{:02d}".format(seat) + ">> ./tmp/room_seat.csv" )
			seat=seat+1
			stud = stud + 1

	if (lastRoomStudents+seat-1) != 0  and (lastRoomStudents+seat-1)<(capacity*.7):
		os.system('echo  "Last room has ' + str(lastRoomStudents+seat-1) + ' students"')



def putSerialNumber(fileName):
	with open(fileName) as file1:
	
		#Slno	Room	Seat	Student	RegNo	Slot	Subject
		#os.system('echo "Slno,Room,Seat,Slot,Subject,RegNo,Student"> ./tmp/final-001.csv')
		os.system('touch ./tmp/final-001.csv')
		slno=0
		prev_room = 0
		for line in file1:
			line_i = line.rstrip()
			details = line_i.split(",")
			room = details[0]
			seat = details[1] 
			student = details[2] 
			regno = details[3] 
			slot = details[4] 
			subject = details[5] 
			
			if room[:3] != "000":
			
				if prev_room != room:
					slno = slno + 1
					
				os.system('echo "' + str(slno) + ',' + room + ',' + seat + ',' + student + ',' + regno + ',' + slot + ',' + subject + '">> ./tmp/final-001.csv')
				prev_room = room


def print_summary(report_heading):
	input_file = "./tmp/summary.csv"
	class PDF(FPDF):
		def header(self):
			# Logo
			#self.image('MEC_logo.png', 5, 5, 33)
			self.image('MEC_logo.png', 5,5,20)
			# Arial bold 15
			self.set_text_color(128,128,128)
			self.set_font('Arial', 'B', 15)
			# Move to the right
			self.cell(80)
			# Title
			self.cell(1, 5, 'Model Engg. College, Thrikkakara', 0, 1, 'C')
			self.set_font('Arial', 'B', 15)
			self.cell(80)
			self.set_text_color(0,0,0)
			self.cell(1, 5, 'Examination Seating Arrangement', 0, 1, 'C')
			self.set_font('Arial', 'B', 20)
			self.cell(0, 5, report_heading, 0, 1, 'R')
			
			
			
			
			# Line break
			self.ln(20)

		def footer(self):
			# Position at 1.5 cm from bottom
			self.set_y(-15)
			# Arial italic 8
			self.set_font('Arial', 'I', 8)
			# Page number
			self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

	# Instantiation of inherited class
	pdf = PDF()
	pdf.alias_nb_pages()
	pdf.add_page()
	pdf.set_font('Times', 'B', 14)
	#for i in range(1, 41):
	#   pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
	page_width = 152
	with open('./tmp/summary.csv') as file1:    	 
		for line in file1:
			pdf.set_font('Times', 'B', 14)
			fields = line.count(',')
			col_width = (page_width/(fields))

			i=0
			for col in line.split(','):
				cellValue=col.replace('"','')
				if cellValue=="0":
					cellValue=""
					
				if i== fields:
					nextLine=1
				else:
					nextLine=0
				if i== 0:
					pdf.set_font('Times', 'B', 14)
				else:
					pdf.set_font('Times', '', 14)	
					
				pdf.cell(col_width,10,cellValue,1,nextLine,'C')
				i = i + 1
			pdf.set_font('Times', '', 14)
	pdf.set_font('Times', 'B', 16)			
	pdf.cell(0,10,"Total number of students : " + cellValue,0,nextLine,'R')  
	pdf.output('summary.pdf', 'F')


def print_seating(input_file,report_heading):

	class PDF(FPDF):
		def header(self):
			# Logo
			#self.image('MEC_logo.png', 5, 5, 33)
			self.image('MEC_logo.png', 5,5,20)
			# Arial bold 15
			self.set_text_color(128,128,128)
			self.set_font('Arial', 'B', 15)
			# Move to the right
			self.cell(80)
			# Title
			self.cell(1, 5, 'Model Engg. College, Thrikkakara', 0, 1, 'C')
			self.set_font('Arial', 'B', 15)
			self.cell(80)
			self.set_text_color(0,0,0)
			self.cell(1, 5, 'Examination Seating Arrangement', 0, 1, 'C')
			# Line break
			#self.ln(20)
			self.ln(2)

		def footer(self):
		
		
			self.set_y(-35)
			pdf.set_font('Times', 'B', 14)			
			pdf.cell(0,10,"Invigilator : ",0,1,'L')  
			pdf.cell(0,20,"Absentees : ",1,1,'L')  
			start_reporting = True		

			# Position at 1.5 cm from bottom
			self.set_y(-10)
			# Arial italic 8
			self.set_font('Arial', 'I', 8)
			# Page number
			self.cell(0, 7, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

	# Instantiation of inherited class
	pdf = PDF()
	pdf.alias_nb_pages()
	#pdf.add_page()
	pdf.set_font('Times', 'B', 14)
	#for i in range(1, 41):
	#   pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
	page_width = 152
	#printRoom=True
	current_room = ""
	row = 1
	with open(input_file) as file1:	 
		for line in file1:
			if row == 1:
				row = 2
				#do nothing
			else:
			
				firstRow = False
				#-------------------
				fields = line.count(',')
				col_width = (page_width/4)

				i=0
				for col in line.split(','):
					cellValue=col.replace('"','')
					
					if cellValue != current_room and i == 0:	#Room
						pdf.add_page()
						pdf.set_font('Times', 'B', 20)					
						pdf.cell(0,6,"Room No: " + cellValue + "         " + report_heading,0,1,'R')
						pdf.set_font('Times', 'B', ROW_FONT_SIZE-1)					
						pdf.cell(COL_SEAT,ROW_HEIGHT-1,"Seat",1,0,'L')	
						pdf.cell(COL_PAPER,ROW_HEIGHT-1,"Paper",1,0,'L')	
						pdf.cell(COL_REGNO,ROW_HEIGHT-1,"RegNo",1,0,'L')	
						pdf.cell(COL_NAME,ROW_HEIGHT-1,"Name",1,0,'L')		
						pdf.cell(COL_BLANK,ROW_HEIGHT-1,"",1,1,'L')			

						
					elif i ==1:							#seat				
						pdf.set_font('Times', '', ROW_FONT_SIZE)
						pdf.cell(COL_SEAT,ROW_HEIGHT,cellValue,1,0,'L')
					elif i ==7:							#RegNo
						pdf.set_font('Times', '', ROW_FONT_SIZE)
						pdf.cell(COL_REGNO,ROW_HEIGHT,cellValue,1,0,'L')	
						
					elif i ==8:							# Name
						pdf.set_font('Times', '', ROW_FONT_SIZE)
						pdf.cell(COL_NAME,ROW_HEIGHT,cellValue,1,0,'L')	
						pdf.cell(COL_BLANK,ROW_HEIGHT,"",1,1,'L')	
						
						
					elif i ==5:							#Paper
						pdf.set_font('Times', '', ROW_FONT_SIZE)
						pdf.cell(COL_PAPER,ROW_HEIGHT,cellValue,1,0,'L')	
						
					if i == 0:
						current_room = cellValue	
						
					
					i = i + 1
				#-------------------
			


	pdf.output('seating.pdf', 'F')


