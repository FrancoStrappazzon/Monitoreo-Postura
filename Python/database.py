import mysql.connector

def create_database_and_table():
    #conexion al servidor de MySQL
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "your_new_password"
    )
    
    cursor = conn.cursor()
    
    #creo la base de datos si no existe
    cursor.execute("CREATE DATABASE IF NOT EXISTS posture_monitoring")
    
    #Conecto a la base de datos
    conn.database = "posture_monitoring"
    
    #Creo la tabla si no existe
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS posture_data (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       distance INT,
                       posture_status VARCHAR(50)
                   )
                   """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
#funcion para insertar los datos de distancia y postura
def insert_data(distance, posture_status):
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "your_new_password",
        database = "posture_monitoring"
    )
    cursor = conn.cursor()
    
    #Inserto datos a la tabla
    cursor.execute("INSERT INTO posture_data (distante, posture_status) VALUES (%s, %s)", (distance, posture_status))
    
    conn.commit()
    cursor.close()
    conn.close()
            
#esto es para que no se ejecute este archivo si lo importo desde otro script
if __name__ == "__main__":
    create_database_and_table()
                   