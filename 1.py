#	Main module 

from my_functions import *




sourceFileName = readSourceFile()
if not sourceFileName:
	exit("\n\nSorry, Unable to find a proper source file...!")
	

number_of_records =  prepare_csv_file(sourceFileName)
print("\n\n..moving forward, source file complies with expected format")
print("Number of records = " + str(number_of_records))


#my_function.py.old

#capacities,rooms = fetch_rooms(number_of_records)
k=fetch_rooms(number_of_records)

capacities,rooms,status = k
print(capacities)
print(rooms)
print(status)

if status<0:
	print("We need more Rooms! " + str(status*-1) + " more student(s) to be accommodated." )
	exit()
	
os.system('cut -d , -f 2- 2.csv > 3.csv')
assign_seat(rooms,capacities)	


