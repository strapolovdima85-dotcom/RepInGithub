import time
import ast
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import sys

def process_number(number):
    """Умножает число на 2 с задержкой 0.2 сек."""
    time.sleep(0.2)
    return number * 2

def doing():
    script_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
    try:
        with open(f"{script_dir}/test_list_numbers.txt", 'r') as f:
            content = f.read().strip()
            all_lists = ast.literal_eval(content) 
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return
    results_map = {}
    first_list_sum = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 3. Отправка задач (submit)
        future_to_list_id = {}
        
        for list_index, sublist in enumerate(all_lists):
            futures = [executor.submit(process_number, num) for num in sublist]
            # соответствие наборов futures к списку
            future_to_list_id[tuple(futures)] = list_index
            
        # 4. Отслеживание завершения 
        finished_lists = set()
        all_futures = [f for futures in future_to_list_id.keys() for f in futures]
        
        for future in as_completed(all_futures):
            # поток завершился, проверяем, готов ли список целиком
            for futures_tuple, list_index in future_to_list_id.items():
                if list_index not in finished_lists:
                    # все задачи в этом списке done
                    if all(f.done() for f in futures_tuple):
                        first_list_sum = sum(f.result() for f in futures_tuple)
                        finished_lists.add(list_index)
                        print(f"Сумма чисел в первом обработанном списке: {first_list_sum}")
                        return # Прекращаем работу, мы нашли первый

if __name__ == '__main__':
    doing()


# Сумма чисел в первом обработанном списке: 11090