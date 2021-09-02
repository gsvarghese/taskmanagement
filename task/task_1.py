import sqlite3
from message import est_conn,get_id,get_username

def allot_task_fun(username,emp_name,task_info):
    conn=est_conn()
    from_user=get_id(username)
    to_user=get_id(emp_name)
    conn.execute('insert into tasks values(?,?,?,?,?)',(gen_id(),from_user,to_user,task_info,0))
    conn.commit()
    conn.close()

def read_task(emp_username):
    user_id=get_id(emp_username)
    conn=est_conn()
    task=[]
    status=[]
    count=[]
    task_id=[]
    cur=conn.execute('select task,completed,id from tasks where completed=0 and to_user='+str(user_id))
    i=1
    for row in cur:
        task.append(row[0])
        if row[1] == 0:
            status.append('Not Completed')
        else:
            status.append('Completed')
        count.append(i)
        task_id.append(row[2])
        i=i+1
    conn.close()
    return count,task,status,task_id

def read_task1(emp_username):
    user_id=get_id(emp_username)
    conn=est_conn()
    task=[]
    status=[]
    count=[]
    task_id=[]
    cur=conn.execute('select task,completed,id from tasks where completed=1 and to_user='+str(user_id))
    i=1
    for row in cur:
        task.append(row[0])
        if row[1] == 0:
            status.append('Not Completed')
        else:
            status.append('Completed')
        count.append(i)
        task_id.append(row[2])
        i=i+1
    conn.close()
    return count,task,status,task_id

def gen_id():
    id=0
    conn=est_conn()
    cur=conn.execute('select max(id) from tasks;')
    if cur:
        for row in cur:
            id=row[0]+1
    conn.close()
    return id

def get_info(manager_username):
    conn=est_conn()
    cur=conn.execute('select id from login where type = "Employee"')
    employee_id=[]
    for row in cur:
        employee_id.append(row[0])
    manager_id=get_id(manager_username)
    name=[]
    complete=[]
    total=[]
    id_to_user=[]
    not_allocated=[]
    cur=conn.execute('select to_user from tasks group by to_user')
    for row in cur:
        id_to_user.append(row[0])
    for id in employee_id:
        cur=conn.execute('select to_user from tasks where from_user="'+str(manager_id)+'" and to_user='+str(id)+' group by to_user;')
        for row in cur:
            cur1=conn.execute('select count(*) from tasks where to_user='+str(row[0]))
            (count_total_task,)=cur1.fetchone()
            total.append(count_total_task)
            cur2=conn.execute('select count(*) from tasks where to_user='+str(row[0])+' and completed=1')
            (count_completed_task,)=cur2.fetchone()
            complete.append(count_completed_task)
            name.append(get_username(row[0]))
    for id in employee_id:
        if get_username(id) not in name:
            not_allocated.append(get_username(id))
    return name,total,complete,not_allocated

def cal_completion(username):
    conn=est_conn()
    manager_id=get_id(username)
    cur=conn.execute('select count(*) from tasks where from_user='+str(manager_id))
    total_task=0
    completed_task=0
    for row in cur:
        total_task=row[0]
    cur=conn.execute('select count(*) from tasks where from_user='+str(manager_id)+' and completed=1')
    for row in cur:
        completed_task=row[0]
        if total_task == 0:
            total_task=1
    return int(completed_task/total_task*100)

def get_empId(username):
    conn=est_conn()
    cur=conn.execute('select id from login where name !="'+username+'" and name!="root"')
    empId=[]
    for row in cur:
        empId.append(get_username(row[0]))
    return empId

def leaderboard_ret():
    conn=est_conn()
    cur=conn.execute('select to_user,count(*) from tasks where completed=1 group by to_user order by count(*) desc')
    emp_name=[]
    no=[]
    for row in cur:
        emp_name.append(get_username(row[0]))
        no.append(row[1])
    return emp_name,no

def view_incomplete_task(emp_username):
    user_id = get_id(emp_username)
    conn = est_conn()
    task = []
    count = []
    task_id = []
    cur = conn.execute('select task,id from tasks where to_user='+str(user_id)+' and completed = 0')
    i = 1
    for row in cur:
        task.append(row[0])
        count.append(i)
        task_id.append(row[1])
        i = i+1
    conn.close()
    return count, task, task_id


def view_complete_task(emp_username):
    user_id = get_id(emp_username)
    conn = est_conn()
    task = []
    count = []
    task_id = []
    cur = conn.execute('select task,id from tasks where to_user='+str(user_id)+' and completed = 1')
    i = 1
    for row in cur:
        task.append(row[0])
        count.append(i)
        task_id.append(row[1])
        i = i+1
    conn.close()
    return count, task, task_id


def mark_task_c(username,task_id):
    user_id=get_id(username)
    conn=est_conn()
    conn.execute('update tasks set completed = 1 where to_user='+str(user_id)+' and id='+str(task_id)+';')
    conn.commit()
    conn.close()

def mark_task_i(username,task_id):
    user_id=get_id(username)
    conn=est_conn()
    conn.execute('update tasks set completed = 0 where to_user='+str(user_id)+' and id='+str(task_id)+';')
    conn.commit()
    conn.close()

def get_type(username):
    user_id=get_id(username)
    conn=est_conn()
    row=conn.execute("select type from login where id="+str(user_id))
    (user_type,)=row.fetchone()
    conn.close()
    return user_type