from my_functions import *


##
#	Main module
##



source_file_csv = input("Enter Source file: ")


# Default source file 	=> a.csv 
if source_file_csv == "":
	source_file_csv = "a.csv"
	
	
# Appends .csv if not there
if source_file_csv[-4:] != ".csv":
	source_file_csv = source_file_csv + ".csv"	
	


students, dt = input_papers(source_file_csv)
DateHeading = dt		## Assuming Date is entered and user wants this to be the name of output file
				## Later this has to be fixed -- bull shit
print("Total number of records = " + str(students))


capacities,rooms = fetch_rooms(students)



summary=[]
counter={}
r_i = 0
records = defaultdict(dict)


input_file =  "./" + dt + "/" + dt + "_001.csv"


with open(input_file ,"w") as file1, open(dt + "/" + dt + '.csv') as file2:
	pdf = FPDF('P', 'mm', 'A4')
	
	csvReader = csv.DictReader(file2)

	writer = csv.DictWriter(file1, fieldnames = ["No","Room","Seat","Student","RegNo","Slot","Paper"])
	writer.writeheader()

	room_list=[]
	paper_list=[]	
	room_index=0
	
	
	# Iterating Rooms
	#
	for room,capacity in zip(rooms,capacities):
		
				
		i=1
		room_index=room_index+1
		pdf.add_page()
		print_heading(DateHeading,room,pdf)
		
		
		# Iterating inside room
		#
		pdf.set_font('Times', '', 16)
		for i,row in zip(range(1,capacity+1),csvReader):
			
			#exception_one(room,row["RegNo"])
			
			studentName = row["Student"]
			
			studentName = exception_two(row["RegNo"],studentName)
					
								
			writer.writerow({'No':room_index,'Room':room,	'Seat':"A" + str(i).zfill(2),	'Student':studentName,
			'RegNo':row["RegNo"],'Slot':row["Slot"],'Paper':row["Paper"],})			


			#exception_three(row["RegNo"],i,room,rooms[1])

			print_pdf_row(row,i,pdf)
			

			i=i+1
			summary.append(str(room) + "^" + row["Paper"].lstrip())
			room_list.append(room)
			paper_list.append(row["Paper"])	

uniq_rooms = get_uniq_records(room_list)
uniq_papers = get_uniq_records(paper_list)

no_of_pages = pdf.page_no()			
pdf.output( dt + "/" + dt + '.pdf', 'F')


#actually this is dt.csv itself
summary_csv_file = input_file	

prg_path = os.path.abspath(os.path.dirname(__file__))
os.system("perl " + prg_path + "/trial.pl < "  +  summary_csv_file + " > " + dt + "/" + dt + "_summary.csv" )


#read summary text(not csv) and print

pdf_summary = print_heading_of_summary(DateHeading)	


with open(dt + "/" + dt + "_summary.csv") as csv_file:
	csv_reader = csv.DictReader(csv_file, delimiter=',')
	field_i=0
	line_count=0
	field_names=[]
	for row in csv_reader:
	
		cell_width = int(287/len(row))
		if cell_width > 20:
			cell_width = 20
			
		if line_count == 0:
			long_fields = print_table_row_heading(pdf_summary,row,cell_width)
			print_table_row(pdf_summary,row,long_fields, line_count,cell_width)
				
		else:
			#input(row)
			print_table_row(pdf_summary,row,long_fields, line_count,cell_width)
	

		line_count = line_count + 1
		
pdf_summary.output(dt + "/" + dt + '_summary.pdf', 'F')


os.system("pdftk " + dt + "/" + dt + "_summary.pdf " + dt + "/" + dt + ".pdf cat output " + dt + "/" + dt + "_seating.pdf")

if i==1:
	remove = input("Remove last page- N/y?")

	if remove in ['Y','y']:
		os.system('mv ' + dt + '/' + dt + '_seating.pdf ' + dt + "/" + dt + "_seating-001.pdf" )
		os.system('pdftk ' + dt + "/" + dt + "_seating-001.pdf" + ' cat 1-' + str(no_of_pages) + ' output ' +  dt + "/" + dt + '_seating.pdf')
		

if not os.path.isdir('./SeatingArrangement'):
	os.mkdir('./SeatingArrangement')

os.system('cp ' + dt + "/" + dt + '_seating.pdf ./SeatingArrangement/' + dt + '_seating.pdf')
os.system('cp ' + dt + "/" + dt + '.pdf ./SeatingArrangement/' + dt + '.pdf')


