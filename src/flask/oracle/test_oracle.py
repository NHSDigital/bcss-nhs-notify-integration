import getpass
import oracledb

UN = "SYS"
CS = "localhost:1522/FREE"
pw = getpass.getpass("Enter password: ")


connection = oracledb.connect(
    user=UN, password=pw, dsn=CS, mode=oracledb.AUTH_MODE_SYSDBA
)

print("Successfully connected to Oracle Database")

cursor = connection.cursor()

cursor.execute("select * from v$version")
res = cursor.fetchall()
for row in res:
    print(row, "\n")

# Delete table if it already exists, then create a table

cursor.execute(
    """
    begin
        execute immediate 'drop table todoitem';
        exception when others then if sqlcode <> -942 then raise; end if;
    end;"""
)


cursor.execute(
    """
    create table todoitem (
        id number generated always as identity,
        description varchar2(4000),
        creation_ts timestamp with time zone default current_timestamp,
        done number(1,0),
        primary key (id))"""
)

# Insert some data

rows = [("Task 1", 0), ("Task 2", 0), ("Task 3", 1), ("Task 4", 0), ("Task 5", 1)]

cursor.executemany("insert into todoitem (description, done) values(:1, :2)", rows)
print(cursor.rowcount, "Rows Inserted")

connection.commit()

# Now query the rows back
for row in cursor.execute("select description, done from todoitem"):
    if row[1]:
        print(row[0], "is done")
    else:
        print(row[0], "is NOT done")

# Query the row columns, print raw
cursor.execute("select description, done from todoitem")
columns = [col[0] for col in cursor.description]
print("\n", columns)
for r in cursor:
    print(r)


# Fetch the entire rows
cursor.execute("select * from todoitem")
rows = cursor.fetchall()
print("\nRows:")
for row in rows:
    print(row)


cursor.close()
connection.close()
