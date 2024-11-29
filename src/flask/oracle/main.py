import sql
import menu

db_choices = ["TEST", "BCSS"]
db = True
while db not in db_choices:
    db = str.upper(
        input("Please enter which DB you would like to connect to (TEST/BCSS): ")
    )
    if db not in db_choices:
        print("DB not found, please try again")

connection = sql.create_connection(db)
cursor = connection.cursor()
tables = []

if db == "TEST":
    cursor.execute("SELECT table_name FROM user_tables")
    print("Available tables:")
    for row in cursor:
        print(row)
        tables += row

else:
    cursor.execute("SELECT table_name FROM user_synonyms")
    print("Available synonyms:")
    for row in cursor:
        print(row)
        tables += row

table_name = True
while table_name not in tables:
    table_name = str.upper(input("Which would you like to interact with?: "))
    if table_name not in tables:
        print("Table not found, please try again")


## BCSS DB
if db == "BCSS":
    ans = True
    while ans:
        print(
            """
        1. Fetch all patients
        2. Update message status
        3. Exit
        """
        )
        choice = input("What would you like to do? ")
        columns = sql.get_column_names(cursor, table_name)
        if choice == "1":
            sql.print_table(cursor, table_name)
        elif choice == "2":
            sql.print_table(cursor, table_name)
            data = menu.call_update_message_status()
            sql.call_update_message_status(cursor, data)
            connection.commit()
            sql.print_table(cursor, table_name)
        elif choice == "3":
            cursor.close()
            connection.close()
            ans = False
        elif choice != "":
            print("\nNot Valid Choice, try again")


## Paulos DB
if db == "TEST":
    ans = True
    while ans:
        print(
            """
        1. Add Patient(s)
        2. Delete Patient(s)
        3. Update Patient(s)
        4. Fetch all Patients
        5. Exit
        """
        )
        choice = input("What would you like to do? ")
        columns = sql.get_column_names(cursor, table_name)
        if choice == "1":
            data = menu.insert_patients(columns)
            sql.insert_patients(cursor, table_name, data)
            connection.commit()
            sql.print_table(cursor, table_name)
        elif choice == "2":
            data = menu.delete_patients(columns)
            sql.delete_patients(cursor, table_name, data)
            connection.commit()
            sql.print_table(cursor, table_name)
        elif choice == "3":
            data = menu.update_patients(columns)
            sql.update_patients(cursor, table_name, data)
            connection.commit()
            sql.print_table(cursor, table_name)
        elif choice == "4":
            sql.print_table(cursor, table_name)
        elif choice == "5":
            cursor.close()
            connection.close()
            ans = False
        elif choice != "":
            print("\nNot Valid Choice, try again")
