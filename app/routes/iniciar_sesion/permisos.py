# permissions.py

PERMISSIONS = {
    'R-A1': {  # Administrador
        'zonas': ['C', 'R', 'U', 'D'],
        'parcelas': ['C', 'R', 'U', 'D'],
        'personas': ['C', 'R', 'U', 'D'],
        'herramienta': ['C', 'R', 'U', 'D'],
        'bitacora': ['C', 'R', 'U', 'D'],
        'plan_vuelo': ['C', 'R', 'U', 'D'],
        'detectores': ['C', 'R', 'U', 'D'],
        'inspecciones_campo': ['C', 'R', 'U', 'D'],
        'protocolos': ['C', 'R', 'U', 'D']
    },
    'R-AG2': {  # Agronomo
        'zonas': [],
        'parcelas': [],
        'personas': [],
        'herramienta': [],
        'bitacora': [],
        'plan_vuelo': ['C', 'R', 'U', 'D'],
        'detectores': ['C', 'R', 'U', 'D'],
        'inspecciones_campo': ['R'],
        'protocolos': ['C', 'R', 'U', 'D']
    },
    'R-R3': {  # Responsable
        'zonas': ['R'],
        'parcelas': ['C', 'R', 'U', 'D'],
        'personas': ['C', 'R', 'U', 'D'],
        'herramienta': ['C', 'R', 'U', 'D'],
        'bitacora': ['C', 'R', 'U', 'D'],
        'plan_vuelo': ['C', 'R', 'U', 'D'],
        'detectores': ['C', 'R', 'U', 'D'],
        'inspecciones_campo': ['R'],
        'protocolos': []
    },
    'R-AGR4': {  # Agricultor
        'zonas': [],
        'parcelas': [],
        'personas': [],
        'herramienta': [],
        'bitacora': ['R'],
        'plan_vuelo': [],
        'detectores': [],
        'inspecciones_campo': ['C', 'R', 'U'],
        'protocolos': ['R']
    },
    'R-O5': {  # Otro
        'zonas': [],
        'parcelas': [],
        'personas': [],
        'herramienta': [],
        'bitacora': ['R'],
        'plan_vuelo': [],
        'detectores': [],
        'inspecciones_campo': ['R'],
        'protocolos': ['R']
    }
}
