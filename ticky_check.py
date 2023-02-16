#!/usr/bin/env python3
import re
import csv
import sys
import operator


errorPattern = r"ticky: ERROR ([\w ]*) \(([\w.]*)\)"
userPattern = r"ticky: ([INFO | ERROR]) ([\w ]*) \(([\w.]*)\)"


def sort_by_key(dict):
    return sorted(dict.items(), key=operator.itemgetter(0))


def sort_by_value_reverse(dict):
    return sorted(dict.items(), key=operator.itemgetter(1), reverse=True)


def get_count_errors(lines):
    errors = {}
    for line in lines:
        result = re.search(errorPattern, line)
        if result is not None:
            errorName = result.groups()[0]
            if errorName in errors:
                errors[errorName] += 1
            else:
                errors[errorName] = 1
    errors = sort_by_value_reverse(errors)
    return errors


def get_count_users(lines):
    users = {}
    for line in lines:
        result = re.search(userPattern, line)
        if result is not None:
            username = result.groups()[2]
            if username in users.keys():
                if result.groups()[0] == "INFO":
                    users[username]["INFO"] += 1
                else:
                    users[username]["ERROR"] += 1
            else:
                users[username] = {"INFO": 0, "ERROR": 0}
                if result.groups()[0] == "INFO":
                    users[username]["INFO"] += 1
                else:
                    users[username]["ERROR"] += 1
    users = sort_by_key(users)
    return users


def format_users(users):
    usersList = []
    usernames = [u[0] for u in users]
    infos = [i[1]["INFO"] for i in users]
    errors = [e[1]["ERROR"] for e in users]
    usersList = list(zip(usernames, infos, errors))
    return usersList


def save_to_csv(list_to_write, filename, header):
    with open(filename, "w") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(header)
        writer.writerows(list_to_write)


def main():
    try:
        file = open(sys.argv[1])
        lines = file.readlines()
        file.close()

        errors = get_count_errors(lines)
        users = format_users(get_count_users(lines))

        save_to_csv(errors, "error_message.csv", ["Error", "Count"])
        save_to_csv(users, "user_statistics.csv",
                    ["Username", "INFO", "ERROR"])

        print("Files printed successfully.")
        sys.exit(0)
    except IndexError:
        print("Missing argument, you need to pass a file name,")
        sys.exit(2)
    except IOError:
        print("Can't read or write the file.")
        sys.exit(1)


if __name__ == '__main__':
    main()
