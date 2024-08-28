from src.services.firebase_config import get_firestore_db
from src.models.planificacion_vuelo import PlanVuelo


class PlanVueloService:

    @staticmethod
    def agregar_nuevo_plan_vuelo(plan_vuelo):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha' in plan_vuelo:
                plan_vuelo['fecha'] = plan_vuelo['fecha'].strftime('%Y-%m-%d')

            plan_vuelo['vuelos_realizados'] = 0
            
            print(plan_vuelo)
            
            # Agregar documento sin ID
            doc_ref = db.collection('plan_vuelo').add(plan_vuelo)[1]
            # Obtener ID generado por Firestore
            doc_id = doc_ref.id
            # Actualizar el documento con el ID
            db.collection('plan_vuelo').document(doc_id).update({'document_id': doc_id})
            print("Plan vuelo guardado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al agregar nuevo plan vuelo a Firestore: {e}")
            raise


    @staticmethod
    def obtener_registros_plan_vuelos():
        try:
            db = get_firestore_db()
            registros_ref = db.collection('plan_vuelo')
            docs = registros_ref.stream()

            plan_vuelos = []
            for doc in docs:
                data = doc.to_dict()
                plan_vuelo = PlanVuelo(**data)
                plan_vuelos.append(plan_vuelo)

            return plan_vuelos
        except Exception as e:
            print(f"Error al obtener plan vuelos de Firestore: {e}")
            raise


    @staticmethod
    def modificar_un_plan_vuelo(doc_id, plan_vuelo):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha_vuelo' in plan_vuelo:
                plan_vuelo['fecha_vuelo'] = plan_vuelo['fecha_vuelo'].strftime('%Y-%m-%d')

            print(plan_vuelo)

            db.collection('plan_vuelo').document(doc_id).update(plan_vuelo)

            print("Plan vuelo actualizado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al actualizar plan_vuelo en Firestore: {e}")
            raise


    @staticmethod
    def obtener_plan_vuelo_por_id(doc_id):
        try:
            db = get_firestore_db()

            plan_vuelo_doc = db.collection('plan_vuelo').document(doc_id).get()
            if plan_vuelo_doc.exists:
                plan_vuelo = plan_vuelo_doc.to_dict()
                return plan_vuelo
            else:
                return None
        except Exception as e:
            print(f"Error al obtener plan vuelo en Firestore: {e}")
            raise


    @staticmethod
    def eliminar_plan_vuelo(doc_id):
        try:
            db = get_firestore_db()
            print(doc_id, "-------------")
            db.collection('plan_vuelo').document(doc_id).delete()
            print(f"Plan vuelo con ID {doc_id} eliminado de Firestore")
            return True
        except Exception as e:
            print(f"Error al eliminar plan_vuelo en Firestore: {e}")
            raise

    @staticmethod
    def agregar_vuelo_a_plan(doc_id, vuelo):
        try:
            db = get_firestore_db()

            plan_vuelo_ref = db.collection('plan_vuelo').document(doc_id)
            plan_vuelo_doc = plan_vuelo_ref.get()
            if plan_vuelo_doc.exists:
                plan_vuelo = plan_vuelo_doc.to_dict()
                if 'listVuelo' not in plan_vuelo:
                    plan_vuelo['listVuelo'] = []
                plan_vuelo['listVuelo'].append(vuelo)
                plan_vuelo_ref.update({'listVuelo': plan_vuelo['listVuelo']})
                print(f"Vuelo agregado al plan de vuelo con ID {doc_id}")
                return True
            else:
                print(f"Plan de vuelo con ID {doc_id} no encontrado")
                return False
        except Exception as e:
            print(f"Error al agregar vuelo al plan de vuelo en Firestore: {e}")
            raise

    @staticmethod
    def obtener_vuelos_por_plan(doc_id):
        try:
            db = get_firestore_db()
            plan_vuelo_ref = db.collection('plan_vuelo').document(doc_id)
            plan_vuelo_doc = plan_vuelo_ref.get()
            if plan_vuelo_doc.exists:
                plan_vuelo = plan_vuelo_doc.to_dict()
                return plan_vuelo.get('listVuelo', [])
            else:
                print(f"Plan de vuelo con ID {doc_id} no encontrado")
                return []
        except Exception as e:
            print(f"Error al obtener vuelos del plan de vuelo en Firestore: {e}")
            raise


    @staticmethod
    def actualizar_vuelo(plan_vuelo_id, vuelo_id, vuelo_data):
        try:
            print("prueba")
            db = get_firestore_db()
            plan_vuelo_ref = db.collection('plan_vuelo').document(plan_vuelo_id)
            plan_vuelo_doc = plan_vuelo_ref.get()

            if not plan_vuelo_doc.exists:
                print(f"Plan de vuelo con ID {plan_vuelo_id} no encontrado")
                return False

            plan_vuelo = plan_vuelo_doc.to_dict()
            list_vuelo = plan_vuelo.get('listVuelo', [])

            for i, vuelo in enumerate(list_vuelo):
                if vuelo['id'] == vuelo_id:
                    list_vuelo[i] = vuelo_data
                    break
            else:
                print(f"Vuelo con ID {vuelo_id} no encontrado en el plan de vuelo")
                return False

            plan_vuelo_ref.update({'listVuelo': list_vuelo})
            print(f"Vuelo actualizado con ID {vuelo_id}")
            return True
        except Exception as e:
            print(f"Error al actualizar vuelo en Firestore: {e}")
            raise

    @staticmethod
    def actualizar_vuelos_realizados(plan_vuelo_id, vuelos_realizados):
        try:
            db = get_firestore_db()
            plan_vuelo_ref = db.collection('plan_vuelo').document(plan_vuelo_id)
            plan_vuelo_ref.update({'vuelos_realizados': vuelos_realizados})
            print(f"Vuelos realizados actualizados para el plan de vuelo con ID {plan_vuelo_id}")
        except Exception as e:
            print(f"Error al actualizar vuelos_realizados en Firestore: {e}")
            raise