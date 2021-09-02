import sqlite3

def est_conn():
    return sqlite3.connect('/Users/Govind/PycharmProjects/task/task.db')

def send_message_fun(from_user,to_user,message):
    conn=est_conn()
    id=gen_id()
    conn.execute('insert into message values(?,?,?,?,?);',(id,from_user,to_user,message,0))
    conn.commit()
    conn.close()

def view_message_unread(user):
    from_user=[]
    message=[]
    mes_id=[]
    conn=est_conn()
    cur=conn.execute('select * from message where visited = 0 and to_user ='+str(user)+';')
    for row in cur:
        message.append(str(row[3]))
        from_user.append(get_username(row[1]))
        mes_id.append(str(row[0]))
    conn.close()
    return message,from_user,mes_id

def view_message_read(user):
    from_user=[]
    message=[]
    mes_id=[]
    conn=est_conn()
    cur=conn.execute('select * from message where visited = 1 and to_user ='+str(user)+';')
    for row in cur:
        message.append(str(row[3]))
        from_user.append(get_username(row[1]))
        mes_id.append(str(row[0]))
    conn.close()
    return message,from_user,mes_id



def gen_id():
    id=0
    conn=est_conn()
    cur=conn.execute('select max(id) from message;')
    if cur:
        for row in cur:
            id=row[0]+1
    conn.commit()
    conn.close()
    return id

def get_id(username):
    conn=est_conn()
    cur=conn.execute('select id from login where name like "'+username+'";')
    if cur:
        for row in cur:
            return row[0]
        conn.close()

def get_username(id):
    conn=est_conn()
    cur=conn.execute('select name from login where id='+str(id)+';')
    for row in cur:
        return row[0]

def get_unread(id):
    conn=est_conn()
    cur=conn.execute('select count(*) from message where to_user ='+str(id)+" and visited = 0;")
    for row in cur:
        row=row
    return row[0]

def mark_read(username,mes_id):
    user_id=get_id(username)
    conn=est_conn()
    conn.execute('update message set visited = 1 where to_user='+str(user_id)+' and id='+str(mes_id)+';')
    conn.commit()
    conn.close()

def delete_message(username,mes_id):
    user_id=get_id(username)
    conn=est_conn()
    conn.execute('delete from message where to_user='+str(user_id)+' and id='+str(mes_id)+';')
    conn.commit()
    conn.close()

def mark_as_unread1(username,mes_id):
    user_id=get_id(username)
    conn=est_conn()
    conn.execute('update message set visited = 0 where to_user='+str(user_id)+' and id='+str(mes_id)+';')
    conn.commit()
    conn.close()
