from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, task_name TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# عرض المهام
@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# إضافة مهمة جديدة
@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name, status) VALUES (?, ?)", (task_name, 'pending'))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# تحديث حالة المهمة
@app.route('/update/<int:task_id>')
def update_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = ? WHERE id = ?", ('completed', task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# حذف مهمة
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # إعداد قاعدة البيانات عند بدء التشغيل
    app.run(host="0.0.0.0", port=5001, debug=True)
