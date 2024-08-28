class Zona:
    def __init__(self, nombre_zona, area_cultivada, especie, variedad, tratamiento, secano_regio, proteccion_cult, captac_agua, descripcion_zona, n_puntos, ubicacion, parcelas=None, document_id=None):
        self.nombre_zona = nombre_zona
        self.area_cultivada = area_cultivada
        self.especie = especie
        self.variedad = variedad
        self.tratamiento = tratamiento
        self.secano_regio = secano_regio
        self.proteccion_cult = proteccion_cult
        self.captac_agua = captac_agua
        self.descripcion_zona = descripcion_zona
        self.n_puntos = n_puntos
        self.ubicacion = ubicacion
        self.parcelas = parcelas if parcelas else []
        self.document_id = document_id

    def to_dict(self):
        return {
            'nombre_zona': self.nombre_zona,
            'area_cultivada': self.area_cultivada,
            'especie': self.especie,
            'variedad': self.variedad,
            'tratamiento': self.tratamiento,
            'secano_regio': self.secano_regio,
            'proteccion_cult': self.proteccion_cult,
            'captac_agua': self.captac_agua,
            'descripcion_zona': self.descripcion_zona,
            'n_puntos': self.n_puntos,
            'ubicacion': self.ubicacion,
            'parcelas': self.parcelas,
            'document_id': self.document_id
        }