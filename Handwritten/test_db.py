import os

import pymysql
from dotenv import load_dotenv


load_dotenv()


host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT", "3306"))
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")


print()
print("=" * 55)
print("PYMYSQL DIAGNOSTIC")
print("=" * 55)

print("Host:", repr(host))
print("Port:", repr(port))
print("User:", repr(user))
print("Database:", repr(database))

if password is None:
    print("Password: NOT FOUND")
else:
    print("Password length:", len(password))
    print("Password starts with:", repr(password[:1]))
    print("Password ends with:", repr(password[-1:]))

print()
print("Testing .env credentials...")
print()


try:

    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset="utf8"
    )

    print("SUCCESS! .env credentials work.")

    connection.close()


except Exception as error:

    print("FAILED!")
    print()
    print(type(error).__name__)
    print(error)


print()
print("=" * 55)
print("TESTING EXPLICIT CREDENTIAL")
print("=" * 55)
print()


try:

    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="mj",
        database="handwritten_notes",
        charset="utf8"
    )

    print("SUCCESS! Explicit credentials work.")

    connection.close()


except Exception as error:

    print("FAILED!")
    print()
    print(type(error).__name__)
    print(error)