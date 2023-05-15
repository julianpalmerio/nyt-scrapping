def save_csv(data: list, csv_path: str):
    with open(csv_path, "w") as file:
        for row in data:
            string_row = '","'.join((map(str, row)))
            file.write(f'"{string_row}"\n')
