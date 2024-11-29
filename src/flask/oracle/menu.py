# Paulos db - Insert patients
def insert_patients(columns):
    ans = True
    while ans:
        choice = input("Would you like to add patients manually? (Y/N): ")
        if str.upper(choice) == "Y":
            # Manually entering patient data
            num_entries = int(input("Enter the number of patients to add: "))
            print(columns)
            data = []
            for i in range(num_entries):
                print(f"\n#### Patient {i+1} ####")
                data = data_entry(columns, data)

            print("Adding to table: ", data)
            return data

        elif str.upper(choice) == "N":
            # Automatically adding patient data
            return None

        elif choice != "":
            print("\nNot Valid Choice, try again")


# Adding patient data based on columns in the table
def data_entry(columns, data):
    temp_dict = {}
    for i in columns:
        x = input(f"Please enter the {i} for the patient (Leave blank to skip): ")
        if x:
            temp_dict[i] = x

    data.append(temp_dict)
    return data


# Paulos db - Delete patients
def delete_patients(columns):
    print(
        """
    1. Delete all rows
    2. Delete rows conditionally
    3. Delete specific row
    """
    )
    choice = input("What would you like to do? ")
    data = []
    if choice == "1":
        return True
    elif choice == "2":
        print(columns)
        column = input(
            "What column would you like to delete rows by? \n(Please make sure it matches table column name): "
        )
        condition = input(
            f"What value would you like to check and delete for in the {column} column?: "
        )
        data = {"column": column, "condition": condition}
        return data
    elif choice == "3":
        data = input("Which row would you like to delete? ")
    elif choice != "":
        print("\nNot Valid Choice, try again")


# Paulos db - Update patients
def update_patients(columns):
    ans = True
    while ans:
        choice = input("Would you like to update patients manually? (Y/N): ")
        if str.upper(choice) == "Y":
            print(columns)
            field_to_update = input(
                "What field would you like to update? \n(Please make sure it matches table name): "
            )
            new_value = input("What value would you like to update it to?: ")
            print(columns)
            condition_column = input(
                f"What column would you like to be the condition for the updates for {field_to_update}\n(Please make sure it matches table name):?: "
            )
            condition_value = input(
                f"What value in {condition_column} would you like to check for?: "
            )
            data = {
                "field_to_update": field_to_update,
                "new_value": new_value,
                "condition_column": condition_column,
                "condition_value": condition_value,
            }

            return data
        # Option to just auto-update patient with NewPatientUpdated
        elif str.upper(choice) == "N":

            return None
        elif choice != "":
            print("\nNot Valid Choice, try again")


# BCSS DB - Update message status
def call_update_message_status():
    message_id = input("Enter the message_id you would like to update: ")
    # Have list of accepted statuses, look notify spec
    status = input("Enter the status you would like to update it to: ")

    data = {"in_val1": message_id, "in_val2": status}
    return data
