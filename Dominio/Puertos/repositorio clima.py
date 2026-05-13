from abc import ABC, abstractmethod

class RepositorioClima(ABC):
    @abstractmethod
    def guardar(self, ciudad, temperatura, humedad, descripcion):
        """Guarda los datos en el historial local."""
        pass

    @abstractmethod
    def obtener_reciente(self, ciudad):
        """Recupera el último dato guardado para una ciudad."""
        pass