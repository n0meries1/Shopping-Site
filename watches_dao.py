

from sql_connection import get_sql_connection

def add_products(connection, watch_name, watch_quantity, watch_detail, watch_price, watch_image):
    cursor = connection.cursor()
    query = "INSERT INTO watch_store_page (watch_name, watch_quantity, watch_detail, watch_price, watch_image) VALUES (?, ?, ?, ?, ?)"
    values = (watch_name, watch_quantity, watch_detail, watch_price, watch_image)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

def get_products(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM watch_store_page"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    watches = []
    for row in data:
        watches.append({
            'watch_id': row[0],
            'watch_name': row[1],
            'watch_quantity': row[2],
            'watch_detail': row[3],
            'watch_price': row[4],
            'watch_image': row[5],
        })
    return watches

def get_product_by_id(connection, watch_id):
    cursor = connection.cursor()
    query = "SELECT * FROM watch_store_page WHERE watch_id = ?"
    cursor.execute(query, (watch_id,))
    watch = cursor.fetchone()
    return watch

def update_product_by_id(connection, watch_id, watch_name, watch_quantity, watch_price, watch_detail, watch_image):
    cursor = connection.cursor()
    query = "UPDATE watch_store_page SET watch_name = ?, watch_quantity = ?, watch_price = ?, watch_detail = ?, watch_image = ? WHERE watch_id = ?"
    cursor.execute(query, (watch_name, watch_quantity, watch_price, watch_detail, watch_image, watch_id))
    connection.commit()
    cursor.close()  

def delete_product_by_id(connection, watch_id):
    cursor = connection.cursor()
    query = "DELETE FROM watch_store_page WHERE watch_id = ?"
    cursor.execute(query, (watch_id,))
    connection.commit()
    cursor.close()

def create_new_user(connection, username, password):
    cursor = connection.cursor()
    query = "INSERT INTO userdata (username, password) VALUES (?, ?)"
    cursor.execute(query,(username, password))
    connection.commit()
    cursor.close()

def login_user(connection, username, password):
    cursor = connection.cursor()
    query = "SELECT * FROM userdata WHERE username = ? AND password = ?"
    cursor.execute(query,(username,password))
    if cursor.fetchall():
        return True
    else:
        return False
    
def check_unique_username(connection, username):
    cursor = connection.cursor()
    query = "SELECT * FROM userdata WHERE username = ?"
    cursor.execute(query, (username,))
    if (cursor.fetchall()):
        return False
    else:
        return True
if __name__ == '__main__' :
    connection = get_sql_connection()
