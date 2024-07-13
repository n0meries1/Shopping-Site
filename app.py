from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import watches_dao
import os
from sql_connection import get_sql_connection
import hashlib

UPLOAD_FOLDER = 'C:\Code\Shopping Site\static\watch_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

connection = get_sql_connection()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    watches = watches_dao.get_products(connection)
    return render_template('index.html', watches=watches)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    username = request.form['username-input']
    password = request.form['password-input']
    password = hashlib.sha256(password.encode()).hexdigest()
    outcome = watches_dao.login_user(connection, username, password)
    if (outcome):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/create_new_user', methods=['POST'])
def create_new_user():
    username = request.form['username-input-login']
    password = request.form['password-input-login']
    password = hashlib.sha256(password.encode()).hexdigest()
    if (watches_dao.check_unique_username(connection, username)):
        watches_dao.create_new_user(connection, username, password)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

    

@app.route('/get_watch_name')
def get_watch_names():
    watches = watches_dao.get_products(connection)
    return jsonify(watches)    

@app.route('/add_watch', methods=['POST'])
def add_watch():
    watch_name = request.form['Add_Watch_Name']
    watch_price = request.form['Add_Watch_Price']
    watch_details = request.form['Add_Watch_Details']
    watch_quantity = request.form['Add_Watch_Quantity']
    file = request.files['Add_Watch_Image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        watch_image = os.path.join('static\watch_images', filename)
        watch_image = watch_image.replace('\\', '/')
    else:
        return 'Invalid file type', 400

    print("File saved at:", watch_image)
    watches_dao.add_products(connection, watch_name, watch_quantity, watch_details, watch_price, watch_image)
    return redirect(url_for('index'))

@app.route('/get_watch/<int:watch_id>', methods=['GET'])
def get_watch_by_id(watch_id):
    watch = watches_dao.get_product_by_id(connection, watch_id)
    watch_data = {
        'watch_id': watch[0],
        'watch_name': watch[1],
        'watch_quantity': watch[2],
        'watch_detail': watch[3],
        'watch_price': watch[4],
        'watch_image': watch[5],
    }
    return jsonify(watch_data)

@app.route('/update_watch', methods=['POST'])
def update_watch():
    watch_id = request.form['Edit_Watch_Select']
    watch_name = request.form['Edit_Watch_Name']
    watch_price = request.form['Edit_Watch_Price']
    watch_detail = request.form['Edit_Watch_Detail']
    watch_quantity = request.form['Edit_Watch_Quantity']
    file = request.files['Edit_Watch_Image']
    old_watch = watches_dao.get_product_by_id(connection, watch_id)
    old_watch_image_raw = old_watch['watch_image']
    old_watch_image = os.path.join('C:/Code/Shopping Site', old_watch_image_raw)
    old_watch_image = old_watch_image.replace('\\', '/')
    if file.filename == "":
        watch_image = old_watch_image_raw
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        watch_image = os.path.join('static\watch_images', filename)
        watch_image = watch_image.replace('\\', '/')
        os.remove(old_watch_image)
    watches_dao.update_product_by_id(connection, watch_id, watch_name, watch_quantity, watch_price, watch_detail, watch_image)
    return redirect(url_for('index'))

@app.route('/delete_watches', methods=['POST'])
def delete_watches():
    data = request.get_json()
    watch_ids = data.get('watch_ids', [])

    if not watch_ids:
        return jsonify({'message': 'No watch id available'})
    
    for watch_id in watch_ids:
        watch = watches_dao.get_product_by_id(connection, watch_id)
        if watch:
            watch_image = os.path.join('C:/Code/Shopping Site', watch['watch_image'])
            if watch_image and os.path.exists(watch_image):
                os.remove(watch_image)
        watches_dao.delete_product_by_id(connection, watch_id)
    return jsonify({'message': 'Watches deleted successfully'})

if __name__ == "__main__":
    print("starting Python flask server for shopping")
    app.run(debug=True)
