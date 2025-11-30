"""
MotiBeam Spatial OS - Core Module
Base architecture and spatial computing engine
"""

from .base_realm import SpatialRealm
from .spatial_engine import SpatialEngine, BeamNetworkProtocol

__all__ = ['SpatialRealm', 'SpatialEngine', 'BeamNetworkProtocol']
