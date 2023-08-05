from ._computed import computed
from ._core import Config, MetaBase, Section
from ._environment import Environment
from ._future_value import FutureValue, ValueType
from ._lazy_environment import LazyEnvironment
from ._version import version

__version__ = version
__all__ = ("Config", "Section", "computed", "env", "Environment", "lazy_env", "LazyEnvironment",
           "FutureValue", "ValueType", "MetaBase",)

# type hint for PyCharm
env: Environment = Environment()
lazy_env: LazyEnvironment = LazyEnvironment()
