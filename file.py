files = ["2023-10-21.txt", "2023-10-22.txt", "2023-10-23.txt",
         "2023-10-24.txt", "2023-10-25.txt", "2023-10-26.txt",
         "2023-10-27.txt"]
for f in files:
    with open(f"texts/{f}", 'r') as file:
        text = file.read()
        print(type(text))