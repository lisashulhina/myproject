import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector


def read_file_csv(path):
    """ read cvs file from input path """
    cvs_path = path
    df = pd.read_csv(cvs_path)
    print(df)
    print("\n")
    return df


def read_file_database(user, password, host, database):
    """ read data from database """
    global table
    config = {
        'user': user,
        # root
        'password': password,
        # password
        'host': host,
        # localhost
        'database': database
        # database1
    }
    cnx = mysql.connector.connect(**config)

    table_flag = False
    while not table_flag:
        try:
            table = input("Input table name: ")
            df = pd.read_sql("select * from " + database + "." + table + ";", cnx)
            table_flag = True
        except:
            print("Something went wrong with input! Try again!")
    #PETSALE
    print(df)
    print("\n")
    return df


def bar_chart(dictionary1, dictionary2):
    """ create bar chart """
    bars = tuple(dictionary1)
    y_pos = np.arange(len(bars))
    # y-axis
    plt.bar(y_pos, dictionary2)
    # x-axis
    plt.xticks(y_pos, bars)
    plt.show()


def choice(df, dic_for_col):
    """ record choosen columns """
    global choice_quantitative, choice_categorical
    flag1 = False
    flag2 = False
    while not flag1 or not flag2:
        if not flag1:
            choice_quantitative_flag = False
            while not choice_quantitative_flag:
                try:
                    choice_quantitative = int(input("Enter quantitative column: "))
                    choice_quantitative_flag = True
                except:
                    print("Something went wrong with input! Try again!")
            if choice_quantitative in dic_for_col.keys() and (
                    str(type(df.iloc[0, choice_quantitative])) == "<class 'numpy.int64'>" or str(
                type(df.iloc[0, choice_quantitative])) == "<class 'numpy.float64'>"):
                flag1 = True
            else:
                print(choice_quantitative, "is not a quantitative column! Try again!")

        if not flag2 and flag1:
            choice_categorical_flag = False
            while not choice_categorical_flag:
                try:
                    choice_categorical = int(input("Enter categorical column: "))
                    choice_categorical_flag = True
                except:
                    print("Something went wrong with input! Try again!")
            if choice_categorical in dic_for_col.keys() and str(
                    type(df.iloc[0, choice_categorical])) == "<class 'str'>":
                flag2 = True
            else:
                print(choice_categorical, "is not a categorical column! Try again!")
    print("\n")
    return dic_for_col[choice_quantitative], dic_for_col[choice_categorical]


def write_to_list(df, choice_quantitative):
    """ write data to list """
    list = []
    count = 0
    for data in df[choice_quantitative]:
        list.append(data)
        count += 1
    return list


def count_average(list, choice_quantitative):
    """ calculate average from quantitative column """
    average = 0
    count = 0
    for elements in list:
        average += elements
        count += 1
    average /= count
    print("The average " + choice_quantitative + " for all is: " + str(format(average, '.2f')))
    print("\n")
    return average


def dic_with_count(df, choice_categorical):
    """ write data to dictionary from categorical column """
    dictionary = {}
    for element in df[choice_categorical]:
        if element not in dictionary.keys():
            dictionary[element] = 1
        else:
            dictionary[element] += 1

    return dictionary


def dic_with_full(df, choice_categorical, choice_quantitative):
    """ write data to dictionary from categorical and quantitative columns """
    new_dictionary = {}
    count = 0
    for elements in df[choice_categorical]:
        if elements not in new_dictionary.keys():
            new_dictionary[elements] = df.loc[count, choice_quantitative]
            count += 1
        else:
            new_dictionary[elements] += df.loc[count, choice_quantitative]
            count += 1

    return new_dictionary


def count_average2(new_dictionary, dictionary, choice_quantitative):
    """ write data to dictionary for averages """
    average = []
    for keys in new_dictionary.keys():
        average1 = new_dictionary[keys] / dictionary[keys]
        average.append(average1)
        print("For "+ str(keys) + "'s " + choice_quantitative + " the average is " + str(format(average1, '.2f')))
    print("\n")
    return average


def dic_for_col(df):
    """ write data to dictionary for choosing """
    print("Columns:")
    count = 0
    dic_for_col = {}
    for col in df.columns:
        print(count, " ", col)
        dic_for_col[count] = col
        count += 1
    return dic_for_col


def dic_for_data(df, choice_quantitative, choice_categorical, choice):
    """ write data to dictionary for chosen category """
    dictionary = {}
    count = 0
    dict_count = 0
    for element in df[choice_quantitative]:
        if df.loc[count, choice_categorical] == choice:
            dictionary[dict_count] = df.loc[count, choice_quantitative]
            dict_count += 1
        count += 1
    return dictionary


def line_chart(df, choice_quantitative, choice_categorical, choice):
    """ create line chart for chosen category """
    # create data
    temp_dic = dic_for_data(df, choice_quantitative, choice_categorical, choice)
    x = list(temp_dic.keys())
    y = list(temp_dic.values())
    plt.plot(x, y)
    plt.show()


def choice_category(df, choice_categorical):
    """ write dictionary to chose """
    global choice_category_to_show
    dictionary = {}
    count = 0
    for element in df[choice_categorical]:
        if element not in dictionary.values():
            print(count, " ", element)
            dictionary[count] = element
            count += 1

    flag = False
    while not flag:
        choice_category_to_show_flag = False
        while not choice_category_to_show_flag:
            try:
                choice_category_to_show = int(input("What category do you want to show? "))
                choice_category_to_show_flag = True
            except:
                print("Something went wrong with input! Try again!")
        if choice_category_to_show not in dictionary.keys():
            print("It is not a category! Try again!")
        else:
            flag = True
    return dictionary[choice_category_to_show]


def choose_data_source():
    """ chose your data between file or database """
    print("Where is your data? (Enter number only) ")
    flag = False
    while not flag:
        try:
            choice = input("1 CSV file on your computer \n2 Database\n")
            if choice.isnumeric() == False:
                raise TypeError
            else:
                choice = int(choice)

            if choice == 1 or choice == 2:
                flag = True
            else:
                raise ValueError
        except ValueError:
            print("Your value must be 1 or 2! try again!")
        except TypeError:
            print("Enter integer, please! Try again!")
    return choice


def read_file(choice1):
    """ reading data from file or database """
    global user, password, host, database
    if choice1 == 1:
        path_flag = False
        while not path_flag:
            try:
                path = input("Enter path :")
                df = read_file_csv(path)
                path_flag = True
            except:
                print("You entered wrong path! Try again!")
        # /Users/liza/Downloads/YB.csv
        return df
    elif choice1 == 2:
        flag = False
        while not flag:
            try:
                user_flag = False
                while not user_flag:
                    try:
                        user = input("Enter database user:")
                        user_flag = True
                    except:
                        print("You enter wrong user type! Try again!")

                password_flag = False
                while not password_flag:
                    try:
                        password = input("Enter database password:")
                        password_flag = True
                    except:
                        print("You enter wrong password type ! Try again!")

                host_flag = False
                while not host_flag:
                    try:
                        host = input("Enter database host:")
                        host_flag = True
                    except:
                        print("You enter wrong host type! Try again!")

                database_flag = False
                while not database_flag:
                    try:
                        database = input("Enter database name:")
                        database_flag = True
                    except:
                        print("You enter wrong database type ! Try again!")

                df = read_file_database(user, password, host, database)
                flag = True
                return df
            except:
                print("Can't find database! Try again!")
    else:
        print("Can't find data")


def main():
    # choosing from where to read data from a file or database
    data_choise = choose_data_source()

    # read data from chosen directory
    df = read_file(data_choise)

    # choosing quantitative and categorical columns
    choice_quantitative, choice_categorical = choice(df, dic_for_col(df))

    # creating list with quantitative values
    list1 = write_to_list(df, choice_quantitative)

    # calculating average
    count_average(list1, choice_quantitative)

    # creating list with categorical values
    dictionary = dic_with_count(df, choice_categorical)

    # creating dictionary with quantitative and categorical values
    new_dictionary = dic_with_full(df, choice_categorical, choice_quantitative)

    # calculating average for each category
    average = count_average2(new_dictionary, dictionary,choice_quantitative)

    # creating line chart
    line_chart(df, choice_quantitative, choice_categorical, choice_category(df, choice_categorical))

    # creating bar chart
    bar_chart(dictionary.keys(), average)