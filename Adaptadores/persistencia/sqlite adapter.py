import sqlite3
from Dominio.Puertos.repositorio_clima import RepositorioClima

class SQLiteAdapter(RepositorioClima):
    def __init__(self, db_path):
        self.db_path = db_path
        self._inicializar_db()

    def _inicializar_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS historial 
                         (ciudad TEXT PRIMARY KEY, temp REAL, descripcion TEXT, humedad INTEGER)''')
            conn.commit()

    def guardar(self, ciudad, temperatura, humedad, descripcion):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO historial VALUES (?, ?, ?, ?)", 
                      (ciudad, temperatura, descripcion, humedad))
            conn.commit()

    def obtener_reciente(self, ciudad):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT temp, descripcion, humedad FROM historial WHERE ciudad = ?", (ciudad,))
            return c.fetchone()