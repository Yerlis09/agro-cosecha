class Bitacora:
    def __init__(self, nombre, fecha_apertura, fecha_inicio, fecha_fin, tipo_cultivo, nombre_encargado, nro_ident_enc, nombre_zona, coordenadas_zona, id_zona, lista_parcelas=None, lista_herramientas=None,listPersonas=None, document_id=None):
        self.nombre = nombre
        self.fecha_apertura = fecha_apertura
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo_cultivo = tipo_cultivo
        self.nombre_encargado = nombre_encargado
        self.nro_ident_enc = nro_ident_enc
        self.listPersonas = listPersonas
        self.nombre_zona = nombre_zona
        self.coordenadas_zona = coordenadas_zona
        self.id_zona = id_zona
        self.lista_parcelas = lista_parcelas
        self.lista_herramientas = lista_herramientas
        self.document_id = document_id

    def to_dict(self):
        return {
            'document_id': self.document_id,
            'nombre': self.nombre,
            'coordenadas_zona': self.coordenadas_zona,
            'fecha_apertura': self.fecha_apertura,
            'fecha_fin': self.fecha_fin,
            'fecha_inicio': self.fecha_inicio,
            'id_zona': self.id_zona,
            'listPersonas': self.listPersonas,
            'lista_herramientas': self.lista_herramientas,
            'lista_parcelas': self.lista_parcelas,
            'nombre_encargado': self.nombre_encargado,
            'nombre_zona': self.nombre_zona,
            'nro_ident_enc': self.nro_ident_enc,
            'tipo_cultivo': self.tipo_cultivo
        }