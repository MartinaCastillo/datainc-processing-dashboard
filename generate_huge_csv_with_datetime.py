# generate_huge_csv_with_datetime.py

import csv
from random import randint, choice

ROWS = 1_000_000

names = [
    "martina",
    "juan",
    "pedro",
    "maria",
    "sofia",
    "lucia",
    "jose",
]

cities = [
    "valencia",
    "madrid",
    "barcelona",
    "sevilla",
]

def random_datetime():
    day = randint(1, 28)
    month = randint(1, 12)
    year = randint(1980, 2010)
    hour = randint(0, 23)
    minute = randint(0, 59)
    second = randint(0, 59)

    return f"{day:02d}/{month:02d}/{year} {hour:02d}:{minute:02d}:{second:02d}"


with open(
    "huge_test_with_datetime.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:
    writer = csv.writer(f)

    writer.writerow([
        "name",
        "email",
        "birth_date",
        "city",
        "address"
    ])

    for i in range(ROWS):
        writer.writerow([
            choice(names),
            f"user{i}@mail.com",
            random_datetime(),
            choice(cities),
            f"street {i}"
        ])

print(f"Generated {ROWS:,} rows")