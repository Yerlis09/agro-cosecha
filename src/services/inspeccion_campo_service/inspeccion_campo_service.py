from src.services.firebase_config import get_firestore_db
from src.models.inspeccion_campo import InspeccionCampo


class InspeccionCampoService:

    @staticmethod
    def agregar_nueva_inspeccion_campo(inspeccion_campo):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha' in inspeccion_campo:
                inspeccion_campo['fecha'] = inspeccion_campo['fecha'].strftime('%Y-%m-%d')

            print(inspeccion_campo)
            
            # Agregar documento sin ID
            doc_ref = db.collection('inspecciones_campo').add(inspeccion_campo)[1]
            # Obtener ID generado por Firestore
            doc_id = doc_ref.id
            # Actualizar el documento con el ID
            db.collection('inspecciones_campo').document(doc_id).update({'document_id': doc_id})
            print("Inspección de campo guardada en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al agregar nueva inspección de campo a Firestore: {e}")
            raise


    @staticmethod
    def obtener_registros_inspecciones_campo():
        try:
            db = get_firestore_db()
            registros_ref = db.collection('inspecciones_campo')
            docs = registros_ref.stream()

            listInspeccionesCampo = []
            for doc in docs:
                data = doc.to_dict()
                inspeccion_campo = InspeccionCampo(**data)
                listInspeccionesCampo.append(inspeccion_campo)

            return listInspeccionesCampo
        
        except Exception as e:
            print(f"Error al obtener inspecciones de campo de Firestore: {e}")
            raise


    @staticmethod
    def modificar_una_inspeccion_campo(doc_id, inspeccion_campo):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha_inspeccion_campo' in inspeccion_campo:
                inspeccion_campo['fecha_inspeccion_campo'] = inspeccion_campo['fecha_inspeccion_campo'].strftime('%Y-%m-%d')

            print(inspeccion_campo)

            db.collection('inspecciones_campo').document(doc_id).update(inspeccion_campo)

            print("Inspección de campo actualizada en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al actualizar inspecciones de campo en Firestore: {e}")
            raise


    @staticmethod
    def obtener_inspeccion_campo_por_id(doc_id):
        try:
            db = get_firestore_db()

            inspecciones_campo_doc = db.collection('inspecciones_campo').document(doc_id).get()
            if inspecciones_campo_doc.exists:
                inspeccion_campo = inspecciones_campo_doc.to_dict()
                return inspeccion_campo
            else:
                return None
        except Exception as e:
            print(f"Error al obtener inspección de campo en Firestore: {e}")
            raise


    @staticmethod
    def eliminar_inspeccion_campo(doc_id):
        try:
            db = get_firestore_db()
            db.collection('inspecciones_campo').document(doc_id).delete()
            print(f"Inspección de campo con ID {doc_id} eliminada de Firestore")
            return True
        except Exception as e:
            print(f"Error al eliminar inspecciones de campo en Firestore: {e}")
            raise

    @staticmethod
    def agregar_inspeccion_a_inspeccion_campo(doc_id, inspeccion):
        try:
            db = get_firestore_db()

            inspeccion_campo_ref = db.collection('inspecciones_campo').document(doc_id)
            inspeccion_campo_doc = inspeccion_campo_ref.get()
            if inspeccion_campo_doc.exists:
                inspeccion_campo = inspeccion_campo_doc.to_dict()
                if 'listInspeccion' not in inspeccion_campo:
                    inspeccion_campo['listInspeccion'] = []
                inspeccion_campo['listInspeccion'].append(inspeccion)
                inspeccion_campo_ref.update({'listInspeccion': inspeccion_campo['listInspeccion']})
                print(f"Inspección agregada a la inspección de campo con ID {doc_id}")
                return True
            else:
                print(f"Inspección de campo con ID {doc_id} no encontrada")
                return False
        except Exception as e:
            print(f"Error al agregar inspección a la inspección de campo en Firestore: {e}")
            raise

    @staticmethod
    def obtener_inspecciones_por_inspeccion_campo(doc_id):
        try:
            db = get_firestore_db()
            inspeccion_campo_ref = db.collection('inspecciones_campo').document(doc_id)
            inspeccion_campo_doc = inspeccion_campo_ref.get()
            if inspeccion_campo_doc.exists:
                inspeccion_campo = inspeccion_campo_doc.to_dict()
                return inspeccion_campo.get('listInspeccion', [])
            else:
                print(f"Inspección de campo con ID {doc_id} no encontrada")
                return []
        except Exception as e:
            print(f"Error al obtener inspecciones de la inspección de campo en Firestore: {e}")
            raise


    @staticmethod
    def actualizar_inspeccion(inspeccion_campo_id, inspeccion_id, inspeccion_data):
        try:
            db = get_firestore_db()
            inspeccion_campo_ref = db.collection('inspecciones_campo').document(inspeccion_campo_id)
            inspeccion_campo_doc = inspeccion_campo_ref.get()

            if not inspeccion_campo_doc.exists:
                print(f"Inspección de campo con ID {inspeccion_campo_id} no encontrada")
                return False

            inspeccion_campo = inspeccion_campo_doc.to_dict()
            list_inspeccion = inspeccion_campo.get('listInspeccion', [])

            for i, inspeccion in enumerate(list_inspeccion):
                if inspeccion['id'] == inspeccion_id:
                    list_inspeccion[i] = inspeccion_data
                    break
            else:
                print(f"Inspección con ID {inspeccion_id} no encontrada en la inspección de campo")
                return False

            inspeccion_campo_ref.update({'listInspeccion': list_inspeccion})
            print(f"Inspección actualizada con ID {inspeccion_id}")
            return True
        except Exception as e:
            print(f"Error al actualizar inspección en Firestore: {e}")
            raise


    @staticmethod
    def actualizar_inspecciones_realizadas(inspeccion_campo_id, inspecciones_realizadas):
        try:
            db = get_firestore_db()
            inspeccion_campo_ref = db.collection('inspecciones_campo').document(inspeccion_campo_id)
            inspeccion_campo_ref.update({'inspecciones_realizadas': inspecciones_realizadas})
            print(f"Inspecciones realizadas actualizadas para la inspección de campo con ID {inspeccion_campo_id}")
        except Exception as e:
            print(f"Error al actualizar inspecciones realizadas en Firestore: {e}")
            raise
