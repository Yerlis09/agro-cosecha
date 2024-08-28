from src.services.firebase_config import get_firestore_db
from src.models.bitacora import Bitacora


class Bitacora_service:


    @staticmethod
    def agregar_nueva_bitacora(bitacora):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha_apertura' in bitacora:
                bitacora['fecha_apertura'] = bitacora['fecha_apertura'].strftime('%Y-%m-%d')
            if 'fecha_inicio' in bitacora:
                bitacora['fecha_inicio'] = bitacora['fecha_inicio'].strftime('%Y-%m-%d')
            if 'fecha_fin' in bitacora:
                bitacora['fecha_fin'] = bitacora['fecha_fin'].strftime('%Y-%m-%d')

            print(bitacora)
            
            # Agregar documento sin ID
            doc_ref = db.collection('bitacora').add(bitacora)[1]
            # Obtener ID generado por Firestore
            doc_id = doc_ref.id
            # Actualizar el documento con el ID
            db.collection('bitacora').document(doc_id).update({'document_id': doc_id})
            print("Bitacora guardado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al agregar nuevo bitacora a Firestore: {e}")
            raise


    @staticmethod
    def obtener_registros_bitacoras():
        try:
            db = get_firestore_db()
            registros_ref = db.collection('bitacora')
            docs = registros_ref.stream()

            bitacoras = []
            for doc in docs:
                data = doc.to_dict()
                bitacora = Bitacora(**data)
                bitacoras.append(bitacora)

            return bitacoras
        except Exception as e:
            print(f"Error al obtener bitacoras de Firestore: {e}")
            raise


    @staticmethod
    def modificar_una_bitacora(doc_id, bitacora):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha_apertura' in bitacora:
                bitacora['fecha_apertura'] = bitacora['fecha_apertura'].strftime('%Y-%m-%d')
            if 'fecha_inicio' in bitacora:
                bitacora['fecha_inicio'] = bitacora['fecha_inicio'].strftime('%Y-%m-%d')
            if 'fecha_fin' in bitacora:
                bitacora['fecha_fin'] = bitacora['fecha_fin'].strftime('%Y-%m-%d')


            print(bitacora)

            db.collection('bitacora').document(doc_id).update(bitacora)

            print("Bitacora actualizado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al actualizar bitacora en Firestore: {e}")
            raise


    @staticmethod
    def obtener_bitacora_por_id(doc_id):
        try:
            db = get_firestore_db()

            bitacora_doc = db.collection('bitacora').document(doc_id).get()
            if bitacora_doc.exists:
                bitacora = bitacora_doc.to_dict()
                return bitacora
            else:
                return None
        except Exception as e:
            print(f"Error al obtener bitacora en Firestore: {e}")
            raise


    @staticmethod
    def eliminar_bitacora(doc_id):
        try:
            db = get_firestore_db()
            print(doc_id, "-------------")
            db.collection('bitacora').document(doc_id).delete()
            print(f"Bitacora con ID {doc_id} eliminado de Firestore")
            return True
        except Exception as e:
            print(f"Error al eliminar bitacora en Firestore: {e}")
            raise