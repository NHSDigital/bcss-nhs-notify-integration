import os
from datetime import date
import tabulate
import oracledb

# Create connection to Oracle Database
def create_connection(db):
    if str.upper(db) == "TEST":
        un = "admin"
        cs = "bcss-oracle-notify-testdatabase-2.cqger35bxcwy.eu-west-2.rds.amazonaws.com:1521/TSTBCS01"
        pw = os.getenv("TEST_AWS_DB_PASSWORD")
    else:
        un = "MPI_NOTIFY_USER"
        cs = "bcss-oracle-bcss-bcss-18668.cqger35bxcwy.eu-west-2.rds.amazonaws.com:1521/TSTBCS01"
        pw = os.getenv("AWS_DB_PASSWORD")
    connection = oracledb.connect(user=un, password=pw, dsn=cs)

    print("Successfully connected to Oracle Database!")
    return connection


# Read all columns from specified table
def print_table(cursor, table_name):  # Add condition to this
    # If no condition then read all rows else read rows based on condition
    columns = get_column_names(cursor, table_name)
    print(tabulate.tabulate(cursor, columns, tablefmt="pipe"))


def get_column_names(cursor, table_name):
    cursor.execute(f"select * from {table_name}")
    columns = [col[0] for col in cursor.description]
    return columns


# NHS Provided test data
# data = [
#     dict(person_family_name="HOLMES", person_given_name="Anita", nhs_number = "9733385859", person_birth_date="20151207", DATESTAMP=date.today()),
#     dict(person_family_name="CRUISE", person_given_name="Louisa", nhs_number = "9733385875", person_birth_date="19920816", DATESTAMP=date.today()),
#     dict(person_family_name="WAUGH", person_given_name="Larry", nhs_number = "9733385905", person_birth_date="20160609", DATESTAMP=date.today())
# ]

## Currently not using secure way to format the cursor.executes because you shouldn't use user-entered variables in the SQL string
## MAKE SURE TO CHANGE THIS BACK BEFORE PR ###################
## MOST LIKELY TO HANDLE JUST BCSS DATABASE AND COMMENT OUT ANYTHING FOR PAULOS TEST DATABASE
## Best way to do it will be to have every column name as a bind variable in the sql, then pass in the data dict
# and have any missing fields set to None or NULL or "" whatever is appropriate to make sure
# that the data is placed in the correct column
## e.g. data = dict(person_family_name="Test", person_given_name="Test", nhs_number=None, person_birth_date="20001229", DATESTAMP=date.today())


# Paulos DB - Delete patients
def delete_patients(cursor, table_name, data):
    sql = (
        f"""delete from {table_name}"""
        if data is True
        else f"""delete from {table_name}
            where {data["column"]}= '{data["condition"]}'
            """
    )
    # Delete all rows COMMENT OUT IF YOU WANT TO KEEP THE DATA
    cursor.execute(sql)
    print(cursor.rowcount, "Rows Deleted\n")


# Paulos db - Insert patients
def insert_patients(cursor, table_name, data):
    # Auto insert test patient
    if not data:
        test_patient_counter = str(cursor.rowcount - 1)
        data = {
            "person_family_name": "Patient",
            "person_given_name": "Test" + test_patient_counter,
            "nhs_number": "9999999999",
            "person_birth_date": "20001229",
            "DATESTAMP": date.today(),
        }

    # Insert single patient
    if len(data) <= 1:
        print("Adding 1 patient")
        # Format the insert string for SQL
        if table_name == "MPI":
            data[0]["DATESTAMP"] = date.today()

        insert_string = create_insert_string(data[0])
        values_string = create_values_string(insert_string)
        print(data[0])
        cursor.execute(
            f"""
            insert into {table_name} ({insert_string})
            values({values_string})""",
            data[0],
        )

    # Insert multiple patients
    elif len(data) > 1:
        print(f"Adding {len(data)} patients")
        for patient in data:
            patient["DATESTAMP"] = date.today()
            insert_string = create_insert_string(patient)
            values_string = create_values_string(insert_string)
            print(patient)
            cursor.execute(
                (
                    f"""
                insert into {table_name} ({insert_string})
                values({values_string})""",
                    patient,
                )
            )

    print(cursor.rowcount, "Rows Inserted\n")


# Create insert string for insert SQL
def create_insert_string(patient):
    insert_list = []
    for i in patient:
        if patient[i]:
            insert_list.append(i)
    insert_string = ", ".join(insert_list)
    print(insert_string)
    return insert_string


# Create values string for insert SQL
def create_values_string(insert_string):
    # Format the values string for SQL
    values_list = insert_string.split(", ")
    values_list = [f":{i}" for i in values_list]
    values_string = str.lower(", ".join(values_list))
    print(values_string)
    return values_string


# Paulos db - Hardcoded SQL for inserting patients
def insert_patient(table_name):  # table_name = "MPI"
    return f"""
    insert into {table_name} (person_family_name, person_given_name, nhs_number, person_birth_date, datestamp)
    values(:family_name, :given_name, :nhs_number, :dob, :datestamp)"""


# Paulos db - Updating patients
def update_patients(cursor, table_name, data):
    if not data:
        data = {
            "field_to_update": "person_family_name",
            "new_value": "NewPatientUpdated",
            "condition_column": "person_given_name",
            "condition_value": "Test6",
        }

    cursor.execute(
        f"""
        update {table_name}
        set {data["field_to_update"]} = '{data["new_value"]}'
        where {data["condition_column"]} = '{data["condition_value"]}'
        """
    )

    print(
        f"""{cursor.rowcount} Rows Updated\n
        Data entries with:\n{data['condition_column']} = {data['condition_value']}\n
        have been updated to\n{data['field_to_update']} = {data['new_value']}\n"""
    )


# BCSS DB - Call update message status function
def call_update_message_status(cursor, data):
    cursor.execute(
        """
        select * from all_procedures where object_name = 'PKG_NOTIFY_WRAP'
        """
    )

    var = cursor.var(int)
    data["out_val"] = var
    print(data)
    # Will need to loop through all the message_ids (in_val2) in a batch (in_val1) and update the status to the new status (in_val3)
    cursor.execute(
        """
            begin
                :out_val := pkg_notify_wrap.f_update_message_status(:in_val1, :in_val2, :in_val3);
            end;
        """,
        data,
    )
    response_code = var.getvalue()
    print(f"Response code: {response_code}")


def call_get_next_batch(cursor, data):
    var = cursor.var(str)
    data["out_val"] = var

    cursor.execute(
        """
            begin
                :out_val := pkg_notify_wrap.f_get_next_batch(:in_val1);
            end;
        """,
        data,
    )
    message_definition_id = var.getvalue()
    print(f"Message Definition ID: {message_definition_id}")
