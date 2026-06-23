"""Compatibility export for demand model.

New code should import from ``services.service_demand``.
"""

from services.service_demand import Demand, ServiceDemand

__all__ = ["Demand", "ServiceDemand"]
