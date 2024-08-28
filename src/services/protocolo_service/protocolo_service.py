from google.cloud.firestore_v1.base_query import FieldFilter

from src.services.firebase_config import get_firestore_db
from src.models.protocolo import Protocolo

import json

class ProtocoloService:

    @staticmethod
    def agregar_nuevo_protocolo(protocolo):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha_inicio_pres' in protocolo:
                protocolo['fecha_inicio_pres'] = protocolo['fecha_inicio_pres'].strftime('%Y-%m-%d')
            if 'fecha_fin_pres' in protocolo:
                protocolo['fecha_fin_pres'] = protocolo['fecha_fin_pres'].strftime('%Y-%m-%d')

            print(protocolo)
            
            # Agregar documento sin ID
            doc_ref = db.collection('protocolos').add(protocolo)[1]
            # Obtener ID generado por Firestore
            doc_id = doc_ref.id
            # Actualizar el documento con el ID
            db.collection('protocolos').document(doc_id).update({'document_id': doc_id})
            print("Protocolo guardado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al agregar nuevo protocolo a Firestore: {e}")
            raise

    @staticmethod
    def obtener_registros_protocolos():
        try:
            db = get_firestore_db()
            registros_ref = db.collection('protocolos')
            docs = registros_ref.stream()

            listProtocolos = []
            for doc in docs:
                data = doc.to_dict()
                protocolo = Protocolo(**data)
                listProtocolos.append(protocolo)

            return listProtocolos
        
        except Exception as e:
            print(f"Error al obtener protocolos de Firestore: {e}")
            raise

    @staticmethod
    def modificar_un_protocolo(doc_id, protocolo):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha_inicio_pres' in protocolo:
                protocolo['fecha_inicio_pres'] = protocolo['fecha_inicio_pres'].strftime('%Y-%m-%d')
            if 'fecha_fin_pres' in protocolo:
                protocolo['fecha_fin_pres'] = protocolo['fecha_fin_pres'].strftime('%Y-%m-%d')

            print(protocolo)

            db.collection('protocolos').document(doc_id).update(protocolo)

            print("Protocolo actualizado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al actualizar protocolo en Firestore: {e}")
            raise

    @staticmethod
    def obtener_protocolo_por_id(doc_id):
        try:
            db = get_firestore_db()

            protocolo_doc = db.collection('protocolos').document(doc_id).get()
            if protocolo_doc.exists:
                protocolo = protocolo_doc.to_dict()
                return protocolo
            else:
                return None
        except Exception as e:
            print(f"Error al obtener protocolo en Firestore: {e}")
            raise

    @staticmethod
    def eliminar_protocolo(doc_id):
        try:
            db = get_firestore_db()
            db.collection('protocolos').document(doc_id).delete()
            print(f"Protocolo con ID {doc_id} eliminado de Firestore")
            return True
        except Exception as e:
            print(f"Error al eliminar protocolo en Firestore: {e}")
            raise


    @staticmethod
    def filtrar_planes_vuelo_por_cuaderno(cuaderno_id):
        try:
            db = get_firestore_db()
            # Crear el filtro utilizando FieldFilter
            field_filter = FieldFilter("id_bitacora", "==", cuaderno_id)
            # Aplicar el filtro utilizando el método `where` con el argumento `filter`
            registros_ref = db.collection('plan_vuelo').where(filter=field_filter)
            docs = registros_ref.stream()

            listPlanesVuelo = []
            for doc in docs:
                data = doc.to_dict()
                listPlanesVuelo.append(data)

            return listPlanesVuelo
        except Exception as e:
            print(f"Error al obtener planes de vuelo de Firestore: {e}")
            raise


    @staticmethod
    def filtrar_detectores_por_cuaderno(cuaderno_id):
        try:
            db = get_firestore_db()
            # Crear el filtro utilizando FieldFilter
            field_filter = FieldFilter("id_bitacora", "==", cuaderno_id)
            # Aplicar el filtro utilizando el método `where` con el argumento `filter`
            registros_ref = db.collection('detectores').where(filter=field_filter)
            docs = registros_ref.stream()

            listDetectores = []
            for doc in docs:
                data = doc.to_dict()
                listDetectores.append(data)

            return listDetectores
        except Exception as e:
            print(f"Error al obtener detectores de Firestore: {e}")
            raise
    

    @staticmethod  
    def filtrar_inspecciones_campo_por_cuaderno(cuaderno_id):
        try:
            db = get_firestore_db()
            # Crear el filtro utilizando FieldFilter
            field_filter = FieldFilter("id_bitacora", "==", cuaderno_id)
            # Aplicar el filtro utilizando el método `where` con el argumento `filter`
            registros_ref = db.collection('inspecciones_campo').where(filter=field_filter)
            docs = registros_ref.stream()

            listInspeccionesCampo = []
            for doc in docs:
                data = doc.to_dict()
                listInspeccionesCampo.append(data)

            return listInspeccionesCampo
        except Exception as e:
            print(f"Error al obtener inspecciones de campo de Firestore: {e}")
            raise
    
    
    @staticmethod
    def filtrar_herramientas_por_cuaderno(cuaderno_id):
        try:
            db = get_firestore_db()
            # Crear el filtro utilizando FieldFilter
            field_filter = FieldFilter("document_id", "==", cuaderno_id)
            # Aplicar el filtro utilizando el método `where` con el argumento `filter`
            registros_ref = db.collection('bitacora').where(filter=field_filter)
            docs = registros_ref.stream()
            
            listHerramientas = []
            for doc in docs:
                data = doc.to_dict()
                herramientas = eval(data.get('lista_herramientas', '[]'))
                listHerramientas.extend(herramientas)

            return listHerramientas
        except Exception as e:
            print(f"Error al obtener herramientas de Firestore: {e}")
            raise
