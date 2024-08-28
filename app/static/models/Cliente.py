class Cliente:
    def __init__(self, codigo, identificacion, nombres, apellido, departamento, direccion, ubicacion, responsable, id=None):
        self.id = id
        self.codigo = codigo
        self.identificacion = identificacion
        self.nombres = nombres
        self.apellido = apellido
        self.departamento = departamento
        self.direccion = direccion
        self.ubicacion = ubicacion
        self.responsable = responsable
