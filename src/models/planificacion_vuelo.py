class PlanVuelo:
    def __init__(self, nombre, fecha, duracion, periocidad, nombre_bitacora, vuelos_estimados, vuelos_realizados, listVuelo=None, document_id=None, id_bitacora=None):
        self.document_id = document_id
        self.nombre = nombre
        self.fecha = fecha
        self.duracion = duracion
        self.periocidad = periocidad
        self.nombre_bitacora = nombre_bitacora
        self.vuelos_estimados = vuelos_estimados
        self.vuelos_realizados = vuelos_realizados
        self.listVuelo = listVuelo
        self.id_bitacora = id_bitacora

    def to_dict(self):
        return {
            'document_id': self.document_id,
            'nombre': self.nombre,
            'fecha': self.fecha,
            'duracion': self.duracion,
            'periocidad': self.periocidad,
            'nombre_bitacora': self.nombre_bitacora,
            'vuelos_estimados': self.vuelos_estimados,
            'vuelos_realizados': self.vuelos_realizados,
            'listVuelo': self.listVuelo,
            'id_bitacora': self.id_bitacora
        }

