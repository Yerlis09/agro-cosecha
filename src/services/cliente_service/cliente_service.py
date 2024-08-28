from src.services.firebase_config import get_firestore_db
from src.models.cliente import Cliente

class Cliente_service:

    @staticmethod
    def agregar_nuevo_cliente(cliente, uid):
        try:
            db = get_firestore_db()

            # Agregar documento con UID
            doc_ref = db.collection('personas').document(uid)
            cliente['document_id'] = uid
            doc_ref.set(cliente)
            
            print("Cliente guardado en Firestore con ID:", uid)
            return 1
        except Exception as e:
            print(f"Error al agregar nuevo cliente a Firestore: {e}")
            raise


    @staticmethod
    def obtener_registros_clientes():
        try:
            db = get_firestore_db()
            registros_ref = db.collection('personas')
            docs = registros_ref.stream()

            clientes = []
            for doc in docs:
                data = doc.to_dict()
                cliente = Cliente(**data)
                clientes.append(cliente)

            return clientes
        except Exception as e:
            print(f"Error al obtener clientes de Firestore: {e}")
            raise

    @staticmethod
    def modificar_un_cliente(doc_id, cliente):
        try:
            db = get_firestore_db()

             # Remover la clave del diccionario si está presente
            if 'clave' in cliente:
                del cliente['clave']

            db.collection('personas').document(doc_id).update(cliente)

            print("Cliente actualizado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al actualizar cliente en Firestore: {e}")
            raise

    @staticmethod
    def obtener_cliente_por_id(doc_id):
        try:
            db = get_firestore_db()

            cliente_doc = db.collection('personas').document(doc_id).get()
            if cliente_doc.exists:
                cliente = cliente_doc.to_dict()
                return cliente
            else:
                return None
        except Exception as e:
            print(f"Error al obtener cliente en Firestore: {e}")
            raise

    @staticmethod
    def eliminar_cliente(doc_id):
        try:
            db = get_firestore_db()
            db.collection('personas').document(doc_id).delete()
            print(f"Cliente con ID {doc_id} eliminado de Firestore")
            return True
        except Exception as e:
            print(f"Error al eliminar cliente en Firestore: {e}")
            raise