#	Main module 

from my_functions import *


prg_path = os.path.abspath(os.path.dirname(__file__))

sourceFileName = readSourceFile()
if not sourceFileName:
	exit("\n\nSorry, Unable to find a proper source file...!")

number_of_records =  prepare_csv_file(sourceFileName)





print("\n\n..moving forward, source file complies with expected format")
print("Number of records = " + str(number_of_records))


#my_function.py.old

#capacities,rooms = fetch_rooms(number_of_records)
capacities,rooms,status=fetch_rooms(number_of_records)

#capacities,rooms,status = k
#print(capacities)
#print(rooms)
#print(status)

if status<0:
	print("We need more Rooms! " + str(status*-1) + " more student(s) to be accommodated." )
	exit()



	
#os.system('cut -d , -f 2- ./tmp/2.csv > ./tmp/3.csv')
os.system('cp tmp/2.csv tmp/3.csv')


number_of_records=len(pd.read_csv('./tmp/3.csv'))
assign_seat(rooms,capacities,number_of_records)	
os.system('paste -d "," ./tmp/room_seat.csv ./tmp/3.csv  > ./tmp/seating-001.csv')


os.system('sort -o tmp/seating-002-sorted-on-seat.csv  -t, tmp/seating-001.csv')

#sort_csv('./tmp/seating-001.csv',"./tmp/seating-002-sorted-on-seat.csv",["000Room","000Seat","000ExamDateYYYYMMDD","000ExamTimeQ","000Slot","000Paper","000Branch","000RegNo","000Student","000ExamDate","000ExamTime","000Event"])
#os.system('cut -d , -f 2- ./tmp/seating-002-sorted-on-seat.csv > ./tmp/seating-002-sorted-on-seat-001.csv')
os.system('cp tmp/seating-002-sorted-on-seat.csv tmp/seating-002-sorted-on-seat-001.csv')

#os.system("echo 'Room,Seat,Slot,Paper,Branch,RegNo,Student' > ./tmp/seating-0001.csv")
os.system('cut -d , -f 1,2,9,8,5,6 ./tmp/seating-002-sorted-on-seat-001.csv > ./tmp/final.csv')

#commandString = "BEGIN {FS=OFS=','} '{print $1,$2,$9,$8,$5,$6}'"
#os.system("awk " +  commandString  + " ./tmp/seating-002-sorted-on-seat-001.csv")
putSerialNumber('./tmp/final.csv')
#reorderFields('./tmp/final-001.csv')

#commandString = awk 'BEGIN {FS=OFS=","} {print $1,$2,$3,$7,$6,$4,$5}' ./tmp/final-001.csv>final-002.csv
commandString = 'awk \'BEGIN {FS=OFS=","} {print $1,$2,$3,$7,$6,$4,$5}\' ./tmp/final-001.csv> ./tmp/final-002.csv'
os.system(commandString)



os.system('perl ' + prg_path + '/trial.pl ./tmp/final-002.csv > ./tmp/summary.csv')
dt1=str(date.today()+timedelta(days=1)).replace("/","-")
dt = input(dt1)
if len(dt) == 1:
	dt = dt1[8:] + "{:02d}".format(dt)
elif dt == "":
	dt= dt1


mySession = input("Session :")

report_heading = dt + " " + mySession
print_summary(report_heading)
print_seating('tmp/seating-002-sorted-on-seat-001.csv',report_heading)
os.system('pdftk summary.pdf seating.pdf cat output ' + dt + mySession + '_seating.pdf')
