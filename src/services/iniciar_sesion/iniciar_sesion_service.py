from google.cloud.firestore_v1.base_query import FieldFilter
from src.services.firebase_config import get_firestore_db

class InicioSesionService:

    @staticmethod
    def obtener_info_usuario_por_id(user_id):
        try:
            db = get_firestore_db()
            # Crear el filtro utilizando FieldFilter
            field_filter = FieldFilter("document_id", "==", user_id)
            # Aplicar el filtro utilizando el método `where` con el argumento `filter`
            user_ref = db.collection('personas').where(filter=field_filter)
            docs = user_ref.stream()

            user_data = next(docs, None)
            if user_data:
                return user_data.to_dict()
            else:
                return None
        except Exception as e:
            print(f"Error al obtener la información del usuario: {e}")
            return None