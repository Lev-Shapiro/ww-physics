from __future__ import annotations

from abc import ABC, abstractmethod

from domain.universal.pressure import PsiaPressure
from domain.universal.temperature import Temperature
from rocketcea.cea_obj import CEA_Obj

# RocketCEA chamber density is lbm/ft³; convert to kg/m³ (same basis as ft→m in characteristic_velocity).
_LBM_PER_FT3_TO_KG_PER_M3 = 0.45359237 / (0.3048**3)


class CEACalculator(ABC):
    """RocketCEA-backed equilibrium properties; subclasses supply propellant from domain models."""

    _chamber_pressure: PsiaPressure
    __cea_obj: CEA_Obj

    def __init__(self, chamber_pressure: PsiaPressure) -> None:
        self._chamber_pressure = chamber_pressure
        self.__cea_obj = self._build_cea_obj()

    @abstractmethod
    def _build_cea_obj(self) -> CEA_Obj:
        """Build and return a configured RocketCEA object."""
        raise NotImplementedError

    @property
    def molecular_weight(self) -> float:
        mw, _ = self.__cea_obj.get_Chamber_MolWt_gamma(
            Pc=self._chamber_pressure.psia,
            MR=1.0,
            eps=10.0,
        )
        return float(mw)

    @property
    def chamber_pressure(self) -> PsiaPressure:
        return self._chamber_pressure
    
    @property
    def flame_temperature(self) -> Temperature:
        t_comb_rankine = self.__cea_obj.get_Tcomb(Pc=self._chamber_pressure.psia, MR=1.0)
        t_comb_kelvin = t_comb_rankine * 5.0 / 9.0
        return Temperature.from_kelvin(float(t_comb_kelvin))

    @property
    def gamma(self) -> float:
        _, gamma = self.__cea_obj.get_Chamber_MolWt_gamma(
            Pc=self._chamber_pressure.psia,
            MR=1.0,
            eps=10.0,
        )
        return float(gamma)

    @property
    def chamber_density(self) -> float:
        rho_lbm_per_ft3 = self.__cea_obj.get_Chamber_Density(
            Pc=self._chamber_pressure.psia,
            MR=1.0,
            eps=10.0,
        )
        return float(rho_lbm_per_ft3 * _LBM_PER_FT3_TO_KG_PER_M3)

    @property
    def characteristic_velocity(self) -> float:
        c_star_ft_per_second = self.__cea_obj.get_Cstar(Pc=self._chamber_pressure.psia, MR=1.0)
        return float(c_star_ft_per_second * 0.3048)