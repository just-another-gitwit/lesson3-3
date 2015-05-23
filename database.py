# start sqlite3 in python
import sqlite3 as lite
import pandas as pd

cities = (
	('New York City', 'NY'),
	('Boston', 'MA'),
	('Chicago', 'IL'),
	('Miami', 'FL'),
	('Dallas', 'TX'),
	('Seattle', 'WA'),
	('Portland', 'OR'),
	('San Francisco', 'CA'),
	('Los Angeles', 'CA')
)

weather = (
	('New York City', '2013', 'July', 'January', '62'),
	('Boston', '2013', 'July', 'January', '59'),
	('Chicago', '2013', 'July', 'January', '59'),
	('Miami', '2013', 'August', 'January', '84'),
	('Dallas', '2013', 'July', 'January', '77'),
	('Seattle', '2013', 'July', 'January', '61'),
	('Portland', '2013', 'July', 'December', '63'),
	('San Francisco', '2013', 'September', 'December', '64'),
	('Los Angeles', '2013', 'September', 'December', '75')
)

# connect to database
con = lite.connect('getting_started.db')

with con:

	cur = con.cursor()

# drop and create cities table
	cur.execute("DROP TABLE IF EXISTS cities")
	cur.execute("CREATE TABLE cities (name text, state text)")
	cur.executemany ("INSERT INTO cities VALUES (?, ?)", cities)

# drop and create weather table
	cur.execute("DROP TABLE IF EXISTS weather")
	cur.execute("CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)")
	cur.executemany ("INSERT INTO weather VALUES (?, ?, ?, ?, ?)", weather)

#ask user for month
print "\n"
type_of_weather = raw_input("Enter requested Month: ")

#pass user-inputted month
#into cur.execute SELECT statement

with con:
	cur = con.cursor()
	cur.execute("SELECT name, state, warm_month FROM cities INNER JOIN weather ON name = city WHERE warm_month = ?", (type_of_weather,))
	rows = cur.fetchall()
	if len(rows) > 0:
		print "\n" + "*Using pandas dataframe output*\n"
		cols = [desc[0] for desc in cur.description]
		df = pd.DataFrame(rows, columns=cols)
		print df
		print "\n"
	else:
		print "\n"
		print "No cities have " + type_of_weather + " as the warmest month.\n"

	if len(rows) > 0:
		print "\n" + "*Using for loop: name, state only*\n"
		print "The cities with " + type_of_weather + " as the warmest month include:\n"
		for row in rows:
			print "%s" % row[0] + ", %s" % row[1] + "\n"

