from flask import Flask, render_template , url_for , request , flash , redirect
import sqlite3
from task_1 import *
from message import *
message_flag=0
app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('login.html')

@app.route('/login',methods=['post'])
def login():
    login_flag = 0
    mail=request.form['email']
    psw=request.form['password']
    conn=est_conn()
    cur = conn.execute("SELECT name,password,type FROM login WHERE name LIKE '"+mail+"';")
    for row in cur:
        if row[1] == psw:
            if row[2] == 'Manager':
                return redirect(url_for('manager',username=row[0]))
            elif row[2] == 'Employee':
                return redirect(url_for('employee',username=row[0]))
        else:
            message="Invalid Details"
            return render_template('login.html',message=message)
    conn.close()
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('sign_up.html')

@app.route('/sign_up',methods=['post'])
def sign_up():
    message='Enter Details'
    name=request.form['email']
    psw=request.form['password']
    rep_psw=request.form['rep_password']
    user_type=request.form['type']
    conn=est_conn()
    cur = conn.execute("select max(id) from login;")
    for row in cur:
        id = int(row[0])+1
    cur = conn.execute("INSERT INTO login(id,name,password,type) values(?,?,?,?)",(id,name,psw,user_type))
    conn.commit()
    conn.close()
    flag=1
    if flag==1:
        return redirect(url_for('home_page'))
    return render_template('sign_up.html',message=message)

@app.route('/manager/<username>/')
def manager(username):
    id_user=get_id(username)
    info = view_message_unread(id_user)
    size=len(info[0])
    no=get_unread(id_user)
    table_info=get_info(username)
    size_table=len(table_info[0])
    percentage_completion=cal_completion(username)
    string_per='width:'+str(percentage_completion)+'%'
    return render_template('manager.html',username=username,info=info,size=size,no=no,table_info=table_info,size_table=size_table,percentage_completion=percentage_completion,string_per=string_per)

@app.route('/manager/<username>/messages')
def messages(username):
    id_user=get_id(username)
    info = view_message_unread(id_user)
    size=len(info[0])
    info1=view_message_read(id_user)
    size1=len(info1[0])
    no=get_unread(id_user)
    global message_flag
    disp_message=""
    class_name=""
    if message_flag == 0:
        return render_template('message.html',username=username,info=info,size=size,info1=info1,size1=size1,no=no,disp_message=disp_message,class_name=class_name)
    else:
        message_flag=0
        class_name='alert alert-warning'
        disp_message="Message Sent"
        return render_template('message.html',username=username,info=info,size=size,info1=info1,size1=size1,no=no,disp_message=disp_message,class_name=class_name)

@app.route('/manager/<username>/messages/mark_vis/<mes_id>')
def mark_as_read(username,mes_id):
    mark_read(username,mes_id)
    return redirect(url_for('messages',username=username))

@app.route('/manager/<username>/messages/mar_not_vis/<mes_id>')
def mark_as_unread(username,mes_id):
    mark_as_unread1(username,mes_id)
    return redirect(url_for('messages',username=username))

@app.route('/manager/<username>/messages/del_message/<mes_id>')
def del_message(username,mes_id):
    delete_message(username,mes_id)
    return redirect(url_for('messages',username=username))

@app.route('/manager/<username>/allot_task/<emp_name>')
def allot_task(username,emp_name):
    id_user = get_id(username)
    info = view_message_unread(id_user)
    no = get_unread(id_user)
    task_info=read_task(emp_name)
    task_info1=read_task1(emp_name)
    size_task=len(task_info[0])
    size_task1=len(task_info1[0])
    return render_template('allot_task.html',username=username,info=info,no=no,emp_name=emp_name,task_info=task_info,size_task=size_task,task_info1=task_info1,size_task1=size_task1)

@app.route('/manager/<username>/allot_task/<emp_name>/allot',methods=['POST'])
def allot_task1(username,emp_name):
    task=request.form['task_alloc']
    allot_task_fun(username,emp_name,task)
    return redirect(url_for('allot_task',username=username,emp_name=emp_name))

@app.route('/manager/<username>/allot_task/<emp_name>/unalloted')
def allot_task_unalloted(username,emp_name):
    id_user = get_id(username)
    info = view_message_unread(id_user)
    no = get_unread(id_user)
    return render_template('allot_task1.html',username=username,emp_name=emp_name,info=info,no=no)

@app.route('/manager/<username>/allot_task/<emp_name>/unalloted1',methods=['POST'])
def allot_task_unalloted1(username,emp_name):
    task = request.form['task_alloc']
    allot_task_fun(username, emp_name, task)
    return redirect(url_for('allot_task',username=username,emp_name=emp_name))

@app.route('/manager/<username>/send_message')
def send_message(username):
    id_user = get_id(username)
    info = view_message_unread(id_user)
    no = get_unread(id_user)
    empId=get_empId(username)
    size_empId=len(empId)
    user_type=get_type(username)
    url=None
    if user_type == 'Manager':
        url=url_for('manager',username=username)
    if user_type == 'Employee':
        url=url_for('employee',username=username)
    return render_template('send_message.html',username=username,info=info,no=no,empId=empId,size_empId=size_empId,url=url)

@app.route('/manager/<username>/send_message/send',methods=['POST'])
def send_message1(username):
    emp_name=request.form['uname']
    mes=request.form['message-box']
    emp_id=get_id(emp_name)
    id=get_id(username)
    send_message_fun(id,emp_id,mes)
    global message_flag
    message_flag=1
    return redirect(url_for('messages',username=username))

@app.route('/manager/<username>/leaderboard')
def leaderboard(username):
    id_user=get_id(username)
    info = view_message_unread(id_user)
    size = len(info[0])
    no = get_unread(id_user)
    lead_info=leaderboard_ret()
    size_lead=len(lead_info)
    url=None
    user_type=get_type(username)
    if user_type == 'Manager':
        url = url_for('manager', username=username)
    if user_type == 'Employee':
        url = url_for('employee', username=username)
    return render_template('leaderboard.html',username=username,info=info,size=size,no=no,lead_info=lead_info,size_lead=size_lead,url=url)

@app.route('/employee/<username>/')
def employee(username):
    id_user=get_id(username)
    info = view_message_unread(id_user)
    size=len(info[0])
    no=get_unread(id_user)
    table_infoi = view_incomplete_task(username)
    size_tablei = len(table_infoi[0])
    table_infoc = view_complete_task(username)
    size_tablec = len(table_infoc[0])
    return render_template('employee.html',username=username,info=info,size=size,no=no,table_infoi=table_infoi,size_tablei=size_tablei,table_infoc=table_infoc,size_tablec=size_tablec)


@app.route('/employee/<username>/mark_taskc/<task_id>')
def mark_task_complete(username,task_id):
    mark_task_c(username,task_id)
    return redirect(url_for('employee',username=username))


@app.route('/employee/<username>/mark_taski/<task_id>')
def mark_task_incomplete(username,task_id):
    mark_task_i(username,task_id)
    return redirect(url_for('employee',username=username))




if __name__ == '__main__':
    app.run()
