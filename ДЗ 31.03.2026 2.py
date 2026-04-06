
import os
import zipfile
from multiprocessing import Pool
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
ARCHIVE_1 = f"{script_dir}/path_8_8.zip"
ARCHIVE_2 = f"{script_dir}/recursive_challenge_8_8.zip"
#При прямом проходе закисает все. Видимо zip тупит при проходе внутри. Пришлось загнать в кэш
data_map_1 = {}
data_map_2 = {}

def init_worker(p1, p2):
    global data_map_1, data_map_2
    with zipfile.ZipFile(p1, 'r') as z1:
        for name in z1.namelist():
            if not name.endswith('/'):
                # Вот тут, толи моя версия py как то не так настроена, толи файлы открывались криво, но долго не могу победить эти слешы
                # то в одну строну, то в другую. Отработало только в таком виде.
                path_from_file = z1.read(name).decode('utf-8').strip()
                data_map_1[name] = path_from_file.replace('/', '\\')
    
    #второй архив: ключ — полный путь к файлу с числами
    with zipfile.ZipFile(p2, 'r') as z2:
        for name in z2.namelist():
            if not name.endswith('/'):
                # в архиве оказалась лишняя корневая папка. Долго не могу понять почему ничего не работает.
                try:
                    content = z2.read(name).decode('utf-8').strip()
                    win_path = name.replace('/', '\\')
                    data_map_2[win_path] = int(content)
                except:
                    continue

def process_file(file_name):
    try:
        full_path = data_map_1.get(file_name)
        value = data_map_2.get(full_path)
        return value if value is not None else 0
    except:
        return 0

def main():
    
    with zipfile.ZipFile(ARCHIVE_1, 'r') as z:
        file_list = [n for n in z.namelist() if not n.endswith('/')]

    tasks = [(name,) for name in file_list]

    with Pool(initializer=init_worker, initargs=(ARCHIVE_1, ARCHIVE_2)) as pool:
        results = pool.starmap(process_file, tasks)
    print(f"Итоговая сумма: {sum(results)}")

if __name__ == '__main__':
    main()


# Итоговая сумма: 5152208