from src.services.firebase_config import get_firestore_db
from src.models.detector import Detector


class DetectorService:

    @staticmethod
    def agregar_nuevo_detector(detector):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha' in detector:
                detector['fecha'] = detector['fecha'].strftime('%Y-%m-%d')

            detector['detectores_realizados'] = 0
            
            print(detector)
            
            # Agregar documento sin ID
            doc_ref = db.collection('detectores').add(detector)[1]
            # Obtener ID generado por Firestore
            doc_id = doc_ref.id
            # Actualizar el documento con el ID
            db.collection('detectores').document(doc_id).update({'document_id': doc_id})
            print("Detector guardado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al agregar nuevo detector a Firestore: {e}")
            raise


    @staticmethod
    def obtener_registros_detectores():
        try:
            db = get_firestore_db()
            registros_ref = db.collection('detectores')
            docs = registros_ref.stream()

            listDetectores = []
            for doc in docs:
                data = doc.to_dict()
                detector = Detector(**data)
                listDetectores.append(detector)

            return listDetectores
        
        except Exception as e:
            print(f"Error al obtener detectores de Firestore: {e}")
            raise


    @staticmethod
    def modificar_un_detector(doc_id, detector):
        try:
            db = get_firestore_db()

            # Convertir fechas a cadenas
            if 'fecha_detector' in detector:
                detector['fecha_detector'] = detector['fecha_detector'].strftime('%Y-%m-%d')

            print(detector)

            db.collection('detectores').document(doc_id).update(detector)

            print("Detector actualizado en Firestore con ID:", doc_id)
            return 1
        except Exception as e:
            print(f"Error al actualizar detectores en Firestore: {e}")
            raise


    @staticmethod
    def obtener_detector_por_id(doc_id):
        try:
            db = get_firestore_db()

            detectores_doc = db.collection('detectores').document(doc_id).get()
            if detectores_doc.exists:
                detector = detectores_doc.to_dict()
                return detector
            else:
                return None
        except Exception as e:
            print(f"Error al obtener detector en Firestore: {e}")
            raise


    @staticmethod
    def eliminar_detector(doc_id):
        try:
            db = get_firestore_db()
            db.collection('detectores').document(doc_id).delete()
            print(f"Detector con ID {doc_id} eliminado de Firestore")
            return True
        except Exception as e:
            print(f"Error al eliminar detectores en Firestore: {e}")
            raise

    @staticmethod
    def agregar_sensor_a_detector(doc_id, sensor):
        try:
            db = get_firestore_db()

            detector_ref = db.collection('detectores').document(doc_id)
            detector_doc = detector_ref.get()
            if detector_doc.exists:
                detector = detector_doc.to_dict()
                if 'listSensor' not in detector:
                    detector['listSensor'] = []
                detector['listSensor'].append(sensor)
                detector_ref.update({'listSensor': detector['listSensor']})
                print(f"Sensor agregado al detector con ID {doc_id}")
                return True
            else:
                print(f"Detector con ID {doc_id} no encontrado")
                return False
        except Exception as e:
            print(f"Error al agregar sensor al detector en Firestore: {e}")
            raise

    @staticmethod
    def obtener_sensor_por_detector(doc_id):
        try:
            db = get_firestore_db()
            detector_ref = db.collection('detectores').document(doc_id)
            detector_doc = detector_ref.get()
            if detector_doc.exists:
                detector = detector_doc.to_dict()
                return detector.get('listSensor', [])
            else:
                print(f"Detector con ID {doc_id} no encontrado")
                return []
        except Exception as e:
            print(f"Error al obtener sensor del detector en Firestore: {e}")
            raise


    @staticmethod
    def actualizar_sensor(detector_id, sensor_id, sensor_data):
        try:
            db = get_firestore_db()
            detector_id_ref = db.collection('detectores').document(detector_id)
            detector_id_doc = detector_id_ref.get()

            if not detector_id_doc.exists:
                print(f"Plan de sensor con ID {detector_id} no encontrado")
                return False

            detector_id = detector_id_doc.to_dict()
            list_sensor = detector_id.get('listSensor', [])

            for i, sensor in enumerate(list_sensor):
                if sensor['id'] == sensor_id:
                    list_sensor[i] = sensor_data
                    break
            else:
                print(f"Sensor con ID {sensor_id} no encontrado en el plan de sensor")
                return False

            detector_id_ref.update({'listSensor': list_sensor})
            print(f"Sensor actualizado con ID {sensor_id}")
            return True
        except Exception as e:
            print(f"Error al actualizar sensor en Firestore: {e}")
            raise


    @staticmethod
    def actualizar_sensor_realizados(sensor_id, sensor_realizado):
        try:
            db = get_firestore_db()
            detector_ref = db.collection('detectores').document(sensor_id,)
            detector_ref.update({'sensor realizado': sensor_realizado})
            print(f"Sensor actualizados para detectores con ID {sensor_id}")
        except Exception as e:
            print(f"Error al actualizar sensor realizados en Firestore: {e}")
            raise