import mysql.connector

db = mysql.connector.connect(
    host="",
    user="Gortyy",
    password="",
    database="",
    autocommit=True
)
cursor = db.cursor()



def player(FirstName, LastName):
    query = "SELECT * FROM player WHERE FirstName = %s AND LastName = %s"
    cursor.execute(query, (FirstName,LastName))
    result = cursor.fetchone()
    return result[0]

def idfinder(id):
    query = "SELECT * FROM player WHERE user LIKE %s"
    pattern = f"%{id}"
    cursor.execute(query, (pattern,))
    result = cursor.fetchall()
    return result

def delete_player(id):
    
    delete_query = "DELETE FROM player WHERE user = %s"
    cursor.execute(delete_query, (id,))
    db.commit()

    delete_query = "DELETE FROM Vehicules WHERE owner = %s AND plaque NOT LIKE 'BT%'"
    cursor.execute(delete_query, (id,))
    db.commit()
