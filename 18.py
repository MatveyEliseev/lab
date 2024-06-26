import psycopg2
from psycopg2.extensions import register_type, UNICODE
CONN_STR = "host='10.163.31.228' dbname='rpr' user='eliseev_m_n' password='d705088b'"

def print_lichn_sostav():
    register_type(UNICODE)
    conn = psycopg2.connect(CONN_STR)
    cur = conn.cursor()
    cur.execute('select * from lichn_sostav')
    cols = cur.description
    row = cur.fetchone()
    while row:
        for i in range(len(cols)): print(row[i])
        print('#'*10)
        row = cur.fetchone()
    cur.close()
    conn.close()

def add_sost(name,rota,rang,stash,nagradi,ychastie_v_voenn_merop):
    conn = psycopg2.connect(CONN_STR)
    cur = conn.cursor()
    cur.callproc('add_sost', [name,rota,rang,stash,nagradi,ychastie_v_voenn_merop])
    conn.commit()
    cur.close()
    conn.close()

def delete_sost(id_sos):
    conn = psycopg2.connect(CONN_STR)
    cur = conn.cursor()
    cur.callproc('delete_sost', [id_sos])
    conn.commit()
    cur.close()
    conn.close()

def update(_name, _rota , _rang , _stash: int, _nagradi , _ychastie_v_voenn_merop , _data_b, _god_pop_sl):
    conn = psycopg2.connect(CONN_STR)
    cur = conn.cursor()
    cur.callproc('update', [_name, _rota , _rang , _stash, _nagradi , _ychastie_v_voenn_merop , _data_b, _god_pop_sl])
    conn.commit()
    cur.close()
    conn.close()

def run():
    choice  = 0
    choices = {1 : lambda : print_lichn_sostav(),
               2 : lambda : add_sost(input('Введите имя: '),input('Введите роту: '), input('Введите ранг: ') ,int(input('Введите стаж:')),input('Введите награды:'),input('Введите участие в военных мероприятиях:')),
                3 : lambda : delete_sost(input('Для удаления введите id: ')),
                4 : lambda : update(input('Введите имя: '),input('Введите роту: '), input('Введите ранг: ') ,int(input('Введите стаж:')),input('Введите награды:'),input('Введите участие в военных мероприятиях:'),input('Введите дату рождения:'),input('Введите год службы:'))}
    while (choice != 5):
        print()
        print('1. Выписать таблицу lichn_sostav')
        print('2. Добавить служащего')
        print('3. Удалить id служащего')
        print('4. Изменить данные служащего')
        print('5. Выйти')
        print('Ваш выбор:')
        choice = int(input())
        if choice in choices:
            choices[choice]()
if __name__ == '__main__':
    run()

