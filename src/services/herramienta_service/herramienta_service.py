from src.services.firebase_config import get_firestore_db
from src.models.herramienta import Herramienta


class Herramienta_service:


    @staticmethod
    def agregar_nueva_herramienta(herramienta):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha_inicio_uti' in herramienta:
                herramienta['fecha_inicio_uti'] = herramienta['fecha_inicio_uti'].strftime('%Y-%m-%d')
            if 'fecha_fin_uti' in herramienta:
                herramienta['fecha_fin_uti'] = herramienta['fecha_fin_uti'].strftime('%Y-%m-%d')

            print(herramienta)
            
            # Agregar documento sin ID
            doc_ref = db.collection('herramienta').add(herramienta)[1]
            # Obtener ID generado por Firestore
            doc_id = doc_ref.id
            # Actualizar el documento con el ID
            db.collection('herramienta').document(doc_id).update({'document_id': doc_id})
            print("Herramienta guardado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al agregar nuevo herramienta a Firestore: {e}")
            raise


    @staticmethod
    def obtener_registros_herramientas():
        try:
            db = get_firestore_db()
            registros_ref = db.collection('herramienta')
            docs = registros_ref.stream()

            herramientas = []
            for doc in docs:
                data = doc.to_dict()
                herramienta = Herramienta(**data)
                herramientas.append(herramienta)

            return herramientas
        except Exception as e:
            print(f"Error al obtener herramientas de Firestore: {e}")
            raise


    @staticmethod
    def modificar_una_herramienta(doc_id, herramienta):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha_inicio_uti' in herramienta:
                herramienta['fecha_inicio_uti'] = herramienta['fecha_inicio_uti'].strftime('%Y-%m-%d')
            if 'fecha_fin_uti' in herramienta:
                herramienta['fecha_fin_uti'] = herramienta['fecha_fin_uti'].strftime('%Y-%m-%d')


            print(herramienta)

            db.collection('herramienta').document(doc_id).update(herramienta)

            print("Herramienta actualizado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al actualizar herramienta en Firestore: {e}")
            raise


    @staticmethod
    def obtener_herramienta_por_id(doc_id):
        try:
            db = get_firestore_db()

            herramienta_doc = db.collection('herramienta').document(doc_id).get()
            if herramienta_doc.exists:
                herramienta = herramienta_doc.to_dict()
                return herramienta
            else:
                return None
        except Exception as e:
            print(f"Error al obtener herramienta en Firestore: {e}")
            raise


    @staticmethod
    def eliminar_herramienta(doc_id):
        try:
            db = get_firestore_db()
            print(doc_id, "-------------")
            db.collection('herramienta').document(doc_id).delete()
            print(f"Herramienta con ID {doc_id} eliminado de Firestore")
            return True
        except Exception as e:
            print(f"Error al eliminar herramienta en Firestore: {e}")
            raise