from src.services.firebase_config import get_firestore_db
from src.models.zona import Zona


class ZonaService:

    @staticmethod
    def agregar_nuevo_zona(data):
        try:
            db = get_firestore_db()
            zona = Zona(**data)
            
            # Convertir el objeto Zona a un diccionario
            zona_data = zona.to_dict()
            
            # Agregar documento sin ID
            doc_ref = db.collection('zonas').add(zona_data)[1]
            # Obtener ID generado por Firestore
            doc_id = doc_ref.id
            # Actualizar el documento con el ID
            db.collection('zonas').document(doc_id).update({'document_id': doc_id})
            print("Zona guardado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al agregar nuevo zona a Firestore: {e}")
            raise


    @staticmethod
    def obtener_registros_zonas():
        try:
            db = get_firestore_db()
            registros_ref = db.collection('zonas')
            docs = registros_ref.stream()

            zonas = []
            for doc in docs:
                data = doc.to_dict()
                zona = Zona(**data)
                zonas.append(zona)

            return zonas
        except Exception as e:
            print(f"Error al obtener zona de Firestore: {e}")
            raise


    @staticmethod
    def modificar_una_zona(doc_id, zona):
        try:
            db = get_firestore_db()

            db.collection('zona').document(doc_id).update(zona)

            print("Zona actualizado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al actualizar zona en Firestore: {e}")
            raise


    @staticmethod
    def obtener_zona_por_id(doc_id):
        try:
            db = get_firestore_db()

            zona_doc = db.collection('zonas').document(doc_id).get()
            if zona_doc.exists:
                zona = zona_doc.to_dict()
                return zona
            else:
                return None
        except Exception as e:
            print(f"Error al obtener zona en Firestore: {e}")
            raise


    @staticmethod
    def eliminar_zona(doc_id):
        try:
            db = get_firestore_db()
            print(doc_id, "-------------")
            db.collection('zonas').document(doc_id).delete()
            print(f"Zona con ID {doc_id} eliminado de Firestore")
            return True
        except Exception as e:
            print(f"Error al eliminar zona en Firestore: {e}")
            raise

    @staticmethod
    def agregar_parcela_a_zona(doc_id, parcela):
        try:
            db = get_firestore_db()
            zona_ref = db.collection('zonas').document(doc_id)
            zona_doc = zona_ref.get()
            if zona_doc.exists:
                zona = zona_doc.to_dict()
                if 'parcelas' not in zona:
                    zona['parcelas'] = []
                zona['parcelas'].append(parcela)
                zona_ref.update({'parcelas': zona['parcelas']})
                print(f"Parcela agregada a la zona con ID {doc_id}")
                return True
            else:
                print(f"Zona con ID {doc_id} no encontrada")
                return False
        except Exception as e:
            print(f"Error al agregar parcela a la zona en Firestore: {e}")
            raise

  
        try:
            db = get_firestore_db()
            zona_doc = db.collection('zonas').document(doc_id).get()
            if zona_doc.exists:
                zona = zona_doc.to_dict()
                return Zona.from_dict(zona)
            else:
                return None
        except Exception as e:
            print(f"Error al obtener zona en Firestore: {e}")
            raise