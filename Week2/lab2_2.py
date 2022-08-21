import re
import sqlite3

NAME_FILE01 = r"D:\Prog001\Mich_Py04_Using_Databases_with_Python_PY\Week1\mbox.txt"

my_dict01 = dict()

try:
    with open(NAME_FILE01) as my_file01:
        for my_line01 in my_file01:
            my_domain01 = re.findall(r"^From +\S+@(\S+)", my_line01.rstrip())
            if len(my_domain01) > 0:
                my_dict01[my_domain01[0]] = my_dict01.get(my_domain01[0], 0) +1

    my_query_line01 = """
    INSERT INTO Counts (org, count)
    VALUES\n"""
    for k, v in my_dict01.items():
        my_query_line01 = my_query_line01 + f"('{k}', {v}),\n"

    my_query_line01 = my_query_line01[0:len(my_query_line01) - 2] + ";"
    #print(my_dict01)
    #print(my_query_line01)


    my_conn01 = sqlite3.connect('emaildb.sqlite')
    my_cur01 = my_conn01.cursor()

    my_cur01.execute('''
    DROP TABLE IF EXISTS Counts''')

    my_cur01.execute('''
    CREATE TABLE Counts (org TEXT, count INTEGER)''')

    my_cur01.execute(my_query_line01)
    my_conn01.commit()


    print("Counts:")
    my_query_line02 = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
    for cur_row01 in my_cur01.execute(my_query_line02):
        print(str(cur_row01[0]), cur_row01[1])

    my_cur01.close()

except FileNotFoundError as e:
    print("We can not find this file!!!", e)
except Exception as e:
    print("ERROR!!!", e)