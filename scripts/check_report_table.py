import sqlite3
conn = sqlite3.connect('db.sqlite3')
rows = list(conn.execute("PRAGMA table_info('hr_management_report')"))
if not rows:
    print('No table or no columns')
else:
    for r in rows:
        print(r)
conn.close()
