import sqlite3

connection = sqlite3.connect("clinical_trials.db")
cursor = connection.cursor()

ids = cursor.execute("SELECT NCTId FROM Study")
for i in range(10000):
    print(next(ids))

connection.close()
