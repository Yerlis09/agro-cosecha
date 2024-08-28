class InspeccionCampo:
    def __init__(self, nombre_bitacora, nombre, fecha, listInspeccion=None, document_id=None, id_bitacora=None):
        self.nombre_bitacora = nombre_bitacora
        self.nombre = nombre
        self.fecha = fecha
        self.listInspeccion = listInspeccion
        self.document_id = document_id
        self.id_bitacora = id_bitacora

    def to_dict(self):
        return {
            'nombre_bitacora': self.nombre_bitacora,
            'nombre': self.nombre,
            'fecha': self.fecha,
            'listInspeccion': self.listInspeccion,
            'document_id': self.document_id,
            'id_bitacora': self.id_bitacora
        }