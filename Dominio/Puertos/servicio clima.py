from abc import ABC, abstractmethod

class ServicioClima(ABC):
    @abstractmethod
    def obtener_datos(self, ciudad: str):
        """Define el contrato para obtener datos climáticos actuales."""
        pass