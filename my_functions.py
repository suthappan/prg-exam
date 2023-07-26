import os
import csv
import sys
import pandas as pd

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



	
	newCSV = open('./tmp/1.csv', 'w', newline='')
	#fieldnames = ["000ExamDateYYYYMMDD","000ExamTimeQ","000Event","000Branch","000Slot","000Paper","000Student","000RegNo","000ExamDate","000ExamTime"]
	fieldnames = ["000ExamDateYYYYMMDD","000ExamTimeQ","000Slot","000Paper","000Branch","000RegNo","000Student","000ExamDate","000ExamTime","000Event"]
	writer = csv.DictWriter(newCSV, fieldnames=fieldnames)
	writer.writeheader()
	
	filterCriteria=getFilterCriteria()

	oCount = 0

	with open(inputFile) as csvfile:
	
		reader = csv.DictReader(csvfile)
		iCount = 0

		for row in reader:
			#print("lll ..............")
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

				#input("Valid record")
				writer.writerow({
				'000ExamDateYYYYMMDD': ExamDateYYYYMMDD, 
				'000ExamTimeQ': ExamTimeQ,
				'000Slot':Slot,
				'000Paper':Paper,
				'000Branch':Branch,
				'000RegNo':RegNo,
				'000Student':Student.title(),
				'000ExamDate':ExamDate,
				'000ExamTime':ExamTime,
				'000Event': Event
				})
				oCount = oCount + 1

				
			#print(".", endln="")
			iCount = iCount + 1 
				
				
			#except:
			#	sys.exit("Pls ensure the headings in csv are exactly these: >>>>>>Student,Course,Slot,Branch Name,Event,Exam Date,Exam Time<<<<<<")
		print("Processed " + str(iCount) + " records.")
		print("Number of records filtered " + str(oCount))


	sort_csv('tmp/1.csv',"tmp/2.csv",["000ExamDateYYYYMMDD","000ExamTimeQ","000Slot","000Paper","000Branch","000RegNo","000Student","000ExamDate","000ExamTime","000Event"])
	
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

			if capacity >= students:
				break
			elif students > capacity:
				students = students - capacity
							
			capacities.append(students)
					
		if no_of_students_accommodated < total_no_of_students:
			status = no_of_students_accommodated - total_no_of_students
		elif no_of_students_accommodated == total_no_of_students:
			status = 0
		else:
			status = total_no_of_students - no_of_students_accommodated
				
		
			

		return capacities,rooms,status
	#print("students = ",students)
	
	
def assign_seat(rooms,capacities):
	i=1
	for capacity,room in zip(capacities,rooms):
		#for room in rooms:
		print(str(room) + "," + str(capacity) )
	

