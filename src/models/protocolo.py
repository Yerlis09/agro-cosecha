class Protocolo:
    def __init__(self, nombre_bitacora, fecha_inicio_pres, fecha_fin_pres, nombre_pres, alt_no_quimica, descr_alt_no_quimica, detec_plaga, hidrat_cultivo, nutren_suelo, dosis_util, infor_obt_desde, lista_detectores=None, lista_vuelos=None, lista_inspecciones = None, lista_herramientas=None, document_id=None, id_bitacora=None):
        self.nombre_bitacora = nombre_bitacora
        self.id_bitacora = id_bitacora
        self.fecha_inicio_pres = fecha_inicio_pres
        self.fecha_fin_pres = fecha_fin_pres
        self.nombre_pres = nombre_pres
        self.alt_no_quimica = alt_no_quimica
        self.descr_alt_no_quimica = descr_alt_no_quimica
        self.detec_plaga = detec_plaga
        self.hidrat_cultivo = hidrat_cultivo
        self.nutren_suelo = nutren_suelo
        self.dosis_util = dosis_util
        self.infor_obt_desde = infor_obt_desde
        self.lista_detectores = lista_detectores
        self.lista_vuelos = lista_vuelos
        self.lista_inspecciones = lista_inspecciones
        self.lista_herramientas = lista_herramientas
        self.document_id = document_id