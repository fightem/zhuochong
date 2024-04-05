import csv

def file_get():
    file_name = "RumiaPet_main/data/web/web.csv"  ## 这个实现了动态打开我存储的网站的功能
    list1 = []
    try:
        with open(file_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Check if the row is not empty
                    dict1 = {}  # 创建一个新的字典对象
                    dict1['name'] = row[0]
                    dict1['href'] = row[1]
                    list1.append(dict1)
        return list1
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")


if __name__ == '__main__':
    list1 = file_get()
    print(list1)