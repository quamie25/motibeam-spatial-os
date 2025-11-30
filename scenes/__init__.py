"""
MotiBeam Spatial OS - Scenes/Realms Module
All available spatial computing realms
"""

from .emergency_realm import EmergencyRealm
from .security_realm import SecurityRealm
from .enterprise_realm import EnterpriseRealm
from .aviation_realm import AviationRealm
from .maritime_realm import MaritimeRealm

__all__ = [
    'EmergencyRealm',
    'SecurityRealm',
    'EnterpriseRealm',
    'AviationRealm',
    'MaritimeRealm'
]
