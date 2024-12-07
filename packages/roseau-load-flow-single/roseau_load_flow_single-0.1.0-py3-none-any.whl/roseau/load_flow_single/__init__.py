import importlib.metadata

from roseau.load_flow import exceptions, license, show_versions, testing, typing, units, utils
from roseau.load_flow.exceptions import RoseauLoadFlowException, RoseauLoadFlowExceptionCode
from roseau.load_flow.license import License, activate_license, deactivate_license, get_license
from roseau.load_flow.units import Q_, ureg
from roseau.load_flow.utils import Insulator, LineType, Material, constants
from roseau.load_flow_single.__about__ import (
    __authors__,
    __copyright__,
    __credits__,
    __email__,
    __license__,
    __maintainer__,
    __status__,
    __url__,
)
from roseau.load_flow_single.models import (
    AbstractBranch,
    AbstractLoad,
    Bus,
    Control,
    CurrentLoad,
    Element,
    FlexibleParameter,
    ImpedanceLoad,
    Line,
    LineParameters,
    PowerLoad,
    Projection,
    Switch,
    Transformer,
    TransformerParameters,
    VoltageSource,
)
from roseau.load_flow_single.network import ElectricalNetwork

__version__ = importlib.metadata.version("roseau-load-flow-single")

__all__ = [
    # RLFS elements
    "__authors__",
    "__copyright__",
    "__credits__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__status__",
    "__url__",
    "__version__",
    "Element",
    "Line",
    "LineParameters",
    "Bus",
    "ElectricalNetwork",
    "VoltageSource",
    "PowerLoad",
    "AbstractLoad",
    "CurrentLoad",
    "ImpedanceLoad",
    "Switch",
    "Transformer",
    "TransformerParameters",
    "FlexibleParameter",
    "Projection",
    "Control",
    "AbstractBranch",
    # Other imports from RLF to have the same interface
    # utils
    "Insulator",
    "LineType",
    "Material",
    "utils",
    "constants",
    # License
    "License",
    "activate_license",
    "deactivate_license",
    "get_license",
    "license",
    # Units
    "Q_",
    "units",
    "ureg",
    # Exceptions
    "RoseauLoadFlowException",
    "RoseauLoadFlowExceptionCode",
    "exceptions",
    # Other
    "show_versions",
    "testing",
    "typing",
]
