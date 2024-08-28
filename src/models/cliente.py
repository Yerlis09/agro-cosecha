class Cliente:
    def __init__(self, tipo_identificacion, nombres, apellido, departamento, municipio, direccion, identificacion, experiencia, estudios_realizados, correo, clave, rol, celular, document_id=None):
        self.tipo_identificacion = tipo_identificacion
        self.nombres = nombres
        self.apellido = apellido
        self.departamento = departamento
        self.municipio = municipio
        self.direccion = direccion
        self.identificacion = identificacion
        self.experiencia = experiencia
        self.estudios_realizados = estudios_realizados
        self.correo = correo
        self.clave = clave
        self.rol = rol
        self.celular = celular
        self.document_id = document_id

