class Detector:
    def __init__(self, nombre, fecha, duracion, periocidad, nombre_bitacora, detectores_estimados, detectores_realizados, listSensor=None, document_id=None, id_bitacora=None):
        self.document_id = document_id
        self.nombre = nombre
        self.fecha = fecha
        self.duracion = duracion
        self.periocidad = periocidad
        self.nombre_bitacora = nombre_bitacora,
        self.detectores_estimados = detectores_estimados,
        self.detectores_realizados = detectores_realizados
        self.listSensor = listSensor
        self.id_bitacora = id_bitacora

    def to_dict(self):
        return {
            'document_id': self.document_id,
            'nombre': self.nombre,
            'fecha': self.fecha,
            'duracion': self.duracion,
            'periocidad': self.periocidad,
            'nombre_bitacora': self.nombre_bitacora,
            'detectores_estimados': self.detectores_estimados,
            'detectores_realizados': self.detectores_realizados,
            'listSensor': self.listSensor,
            'id_bitacora': self.id_bitacora
        }
