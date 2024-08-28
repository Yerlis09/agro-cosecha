class Herramienta:
    def __init__(self, nombre_equipo, funcionalidad_equipo, fecha_inicio_uti, fecha_fin_uti, activo, document_id=None):
        self.nombre_equipo = nombre_equipo
        self.funcionalidad_equipo = funcionalidad_equipo
        self.fecha_inicio_uti = fecha_inicio_uti
        self.fecha_fin_uti = fecha_fin_uti
        self.activo = activo
        self.document_id = document_id