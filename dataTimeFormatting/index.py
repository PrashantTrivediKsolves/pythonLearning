# The datetime module is used for date creation, parsing, and manipulation.


# datetime – Working with Dates & Times
# The datetime module is used for date creation, parsing, and manipulation.


from datetime import datetime

now = datetime.now()
print("Now:", now)
print("Formatted:", now.strftime("%Y-%m-%d %H:%M:%S"))






# Create a specific date:

from datetime import date

d = date(2025, 5, 30)
print("Custom date:", d)




# Parse a string into a date:

from datetime import datetime

date_str = "2025-05-30 14:45:00"
dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print("Parsed:", dt)





from datetime import date

d1 = date(2025, 6, 1)
d2 = date(2025, 5, 30)
delta = d1 - d2
print("Days difference:", delta.days)









# Quick Recap



# Module	Purpose	Key Functions
# os	OS file and path operations	os.getcwd(), os.mkdir(), os.remove()
# sys	Command-line arguments & system	sys.argv, sys.exit()
# datetime	Work with dates and times	datetime.now(), strptime(), timedelta