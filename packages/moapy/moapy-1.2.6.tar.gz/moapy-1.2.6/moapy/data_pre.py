import math
from enum import Enum
from typing import Tuple, Literal, TypeVar, Generic
from abc import ABC, abstractmethod
from pydantic import Field, ConfigDict
from moapy.auto_convert import MBaseModel
from moapy.enum_pre import (
    enUnitThermalExpansion, enum_to_list, enDgnCode, enEccPu, enReportType, enUnitSystem,
    enUnitTemperature, enUnitLength, enUnitStress, enUnitForce, enUnitMoment, enUnitLoad, enUnitAngle, enUnitArea, enUnitVolume, enUnitInertia)
from moapy.unit_converter import UnitConverter

T = TypeVar('T', bound=Enum)

class UnitPropertyMixin(Generic[T]):
    """
    Unit property mixin that provides unit-aware functionality
    """
    value: float
    unit: T

    def update_value(self, value: float) -> None:
        """
        값만 업데이트하고 기존 단위는 유지
        """
        self.value = value

    def convert_to(self, target_unit: T) -> None:
        """
        다른 단위로 변환 (하위 클래스에서 구현)
        """
        raise NotImplementedError

class Angle(MBaseModel, UnitPropertyMixin[enUnitAngle]):
    """
    Angle class
    """
    value: float = Field(default_factory=float, description="Angle value")
    unit: enUnitAngle = Field(default_factory=lambda: enUnitAngle.Degree)

    def convert_to(self, target_unit: enUnitAngle) -> None:
        if self.unit == target_unit:
            return

        if self.unit == enUnitAngle.Degree and target_unit == enUnitAngle.Radian:
            self.value = math.radians(self.value)
        elif self.unit == enUnitAngle.Radian and target_unit == enUnitAngle.Degree:
            self.value = math.degrees(self.value)

        self.unit = target_unit

class Load(MBaseModel, UnitPropertyMixin[enUnitLoad]):
    """
    Load class
    """
    value: float = Field(default_factory=float, description="Load value")
    unit: enUnitLoad = Field(default_factory=lambda: enUnitLoad.kN_m2)

class Temperature(MBaseModel, UnitPropertyMixin[enUnitTemperature]):
    """
    Thermal
    """
    value: float = Field(default_factory=float, description="Temperature")
    unit: enUnitTemperature = Field(default_factory=lambda: enUnitTemperature.Celsius)

    def convert_to(self, target_unit: enUnitTemperature) -> None:
        if self.unit == target_unit:
            return

        self.value = UnitConverter.temperature(self.value, self.unit, target_unit)
        self.unit = target_unit

class Length(MBaseModel, UnitPropertyMixin[enUnitLength]):
    """
    Length
    """
    value: float = Field(default_factory=float, description="Length")
    unit: enUnitLength = Field(default_factory=lambda: enUnitLength.MM)

    def convert_to(self, target_unit: enUnitLength) -> None:
        if self.unit == target_unit:
            return

        self.value = UnitConverter.length(self.value, self.unit, target_unit)
        self.unit = target_unit

class Area(MBaseModel, UnitPropertyMixin[enUnitArea]):
    """
    Area
    """
    value: float = Field(default_factory=float, description="Area")
    unit: enUnitArea = Field(default_factory=lambda: enUnitArea.MM2)

    def convert_to(self, target_unit: enUnitArea) -> None:
        if self.unit == target_unit:
            return

        self.value = UnitConverter.area(self.value, self.unit, target_unit)
        self.unit = target_unit

class Volume(MBaseModel, UnitPropertyMixin[enUnitVolume]):
    """
    Volumne
    """
    value: float = Field(default_factory=float, description="Volumne")
    unit: enUnitVolume = Field(default_factory=lambda: enUnitVolume.MM3)

    def convert_to(self, target_unit: enUnitVolume) -> None:
        if self.unit == target_unit:
            return

        self.value = UnitConverter.volume(self.value, self.unit, target_unit)
        self.unit = target_unit

class Inertia(MBaseModel, UnitPropertyMixin[enUnitInertia]):
    """
    Inertia
    """
    value: float = Field(default_factory=float, description="Inertia")
    unit: enUnitInertia = Field(default_factory=lambda: enUnitInertia.MM4)

    def convert_to(self, target_unit: enUnitInertia) -> None:
        if self.unit == target_unit:
            return

        self.value = UnitConverter.inertia(self.value, self.unit, target_unit)
        self.unit = target_unit

class Force(MBaseModel, UnitPropertyMixin[enUnitForce]):
    """
    Force
    """
    value: float = Field(default_factory=float, description="Force")
    unit: enUnitForce = Field(default_factory=lambda: enUnitForce.kN)

    def convert_to(self, target_unit: enUnitForce) -> None:
        if self.unit == target_unit:
            return

        self.value = UnitConverter.force(self.value, self.unit, target_unit)
        self.unit = target_unit

class Moment(MBaseModel, UnitPropertyMixin[enUnitMoment]):
    """
    Moment
    """
    value: float = Field(default_factory=float, description="Moment")
    unit: enUnitMoment = Field(default_factory=lambda: enUnitMoment.kNm)

    def convert_to(self, target_unit: enUnitMoment) -> None:
        if self.unit == target_unit:
            return

        self.value = UnitConverter.moment(self.value, self.unit, target_unit)
        self.unit = target_unit

class Stress(MBaseModel, UnitPropertyMixin[enUnitStress]):
    """
    Stress
    """
    value: float = Field(default_factory=float, description="Stress")
    unit: enUnitStress = Field(default_factory=lambda: enUnitStress.MPa)

    def convert_to(self, target_unit: enUnitStress) -> None:
        if self.unit == target_unit:
            return

        self.value = UnitConverter.stress(self.value, self.unit, target_unit)
        self.unit = target_unit

class ThermalExpansionCoeff(MBaseModel, UnitPropertyMixin[enUnitThermalExpansion]):
    """
    Thermal Expansion Coefficient
    """
    value: float = Field(default_factory=float, description="Thermal Expansion Coefficient")
    unit: enUnitThermalExpansion = Field(default_factory=lambda: enUnitThermalExpansion.PER_CELSIUS)

# ==== Length ====
class EffectiveLengthFactor(MBaseModel):
    """
    Effective Length class
    """
    kx: float = Field(default=1.0, title="Kx", description="Effect buckling length factor(x direction)")
    ky: float = Field(default=1.0, title="Ky", description="Effect buckling length factor(y direction)")

    model_config = ConfigDict(
        title="Effective Length factor",
        description="The Effective Length Factor is an important parameter used to evaluate the ability of a column or member in a structure to resist buckling. This factor adjusts the actual length of the member to help analyze buckling based on the anchorage conditions of the column. The effective buckling length factor defines the relationship between the buckling length and the column's anchorage conditions."
    )

class BucklingLength(MBaseModel):
    """
    Axial Length
    """
    l_x: Length = Field(default_factory=Length, title="Lx", description="Unbraced length(x-direction)")
    l_y: Length = Field(default_factory=Length, title="Ly", description="Unbraced length(y-direction)")

    model_config = ConfigDict(
        title="Buckling Length",
        description="Buckling length is the length at which a structural member, such as a column or plate, can resist the phenomenon of buckling. Buckling is the sudden deformation of a long member under compressive load along its own center of gravity, which has a significant impact on the safety of a structure. Buckling length is an important factor in analyzing and preventing this phenomenon."
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(l_x=Length(value=15, unit=enUnitLength.IN), l_y=Length(value=15, unit=enUnitLength.IN))
        else:
            return cls(l_x=Length(value=3000, unit=enUnitLength.MM), l_y=Length(value=3000, unit=enUnitLength.MM))

# ==== Forces ====
class UnitLoads(MBaseModel):
    """
    Unit Loads class
    """
    construction: Load = Field(default_factory=Load, title="Construction load", description="Input construction load")
    live: Load = Field(default_factory=Load, title="Live load", description="Input live load")
    finish: Load = Field(default_factory=Load, title="Finish load", description="Input finishing load")

    model_config = ConfigDict(
        title="Unit Loads",
        description="You need to define the different loads that need to be considered in architectural and structural design. By providing specific information about each type of load, engineers can evaluate and design the safety and performance of structures."
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(construction=Load(value=0, unit=enUnitLoad.kip_ft2), live=Load(value=0, unit=enUnitLoad.kip_ft2), finish=Load(value=0, unit=enUnitLoad.kip_ft2))
        else:  
            return cls(construction=Load(value=0, unit=enUnitLoad.kN_m2), live=Load(value=0, unit=enUnitLoad.kN_m2), finish=Load(value=0, unit=enUnitLoad.kN_m2))

class SectionForce(MBaseModel):
    """Force class

    Args:
        Fz (Length): Axial force
        Mx (Length): Moment about x-axis
        My (Length): Moment about y-axis
        Vx (Length): Shear about x-axis
        Vy (Length): Shear about y-axis
    """
    Fz: Force = Field(default_factory=Force, title="Fz", description="Axial force")
    Mx: Moment = Field(default_factory=Moment, title="Mx", description="Moment about x-axis")
    My: Moment = Field(default_factory=Moment, title="My", description="Moment about y-axis")
    Vx: Force = Field(default_factory=Force, title="Vx", description="Shear about x-axis")
    Vy: Force = Field(default_factory=Force, title="Vy", description="Shear about y-axis")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(Fz=Force(unit=enUnitForce.kip),
                       Mx=Moment(unit=enUnitMoment.kipft),
                       My=Moment(unit=enUnitMoment.kipft),
                       Vx=Force(unit=enUnitForce.kip),
                       Vy=Force(unit=enUnitForce.kip))
        else:
            return cls(Fz=Force(unit=enUnitForce.kN),
                       Mx=Moment(unit=enUnitMoment.kNm),
                       My=Moment(unit=enUnitMoment.kNm),
                       Vx=Force(unit=enUnitForce.kN),
                       Vy=Force(unit=enUnitForce.kN))

    model_config = ConfigDict(
        title="Member Force",
        description="Enter the member forces for the design load combination."
    )

class MemberForce(MBaseModel):
    """
    Member Force class
    """
    i: SectionForce = Field(default_factory=SectionForce, title="i", description="Member Force i")
    j: SectionForce = Field(default_factory=SectionForce, title="j", description="Member Force j")

    model_config = ConfigDict(
        title="Member Force",
        description="Enter the member forces for the design load combination."
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(i=SectionForce.create_default(enUnitSystem.US), j=SectionForce.create_default(enUnitSystem.US))
        else:  # SI units by default
            return cls(i=SectionForce.create_default(enUnitSystem.SI), j=SectionForce.create_default(enUnitSystem.SI))

class AxialForceOpt(MBaseModel):
    """
    Moment Interaction Curve
    """
    Nx: Force = Field(default_factory=Force, title="Nx", description="Axial Force")

    model_config = ConfigDict(title="Axial Force Option")

class DesignCode(MBaseModel):
    """Design Code class

    Args:
        design_code (str): Design code
        sub_code (str): Sub code
    """    
    design_code: str = Field(default="ACI 318-19", max_length=30)
    sub_code: str = Field(default="SI")

    model_config = ConfigDict(title="Design Code")

class DgnCode(MBaseModel):
    """
    DgnCode
    """
    name: str = Field(default="", description="DgnCode")

    model_config = ConfigDict(title="DgnCode")

# ==== Lcoms ====
class Lcom(MBaseModel):
    """
    Lcom class

    Args:
        name (str): load combination name
        f (Force): load combination force
    """
    name: str = Field(default="lcom", description="load combination name")
    f: SectionForce = Field(default_factory=SectionForce, title="force", description="load combination force")

    model_config = ConfigDict(title="Lcom Result")

class Lcoms(MBaseModel):
    """
    Lcoms class

    Args:
        lcoms (list[Lcom]): load combination result
    """
    lcoms: list[Lcom] = Field(default=[Lcom(name="uls1", f=SectionForce(Fz=Force(value=100.0, unit=enUnitForce.kN),
                                                                                 Mx=Moment(value=10.0, unit=enUnitMoment.kNm),
                                                                                 My=Moment(value=50.0, unit=enUnitMoment.kNm)))], description="load combination result")

    model_config = ConfigDict(title="Strength Result")

class AngleOpt(MBaseModel):
    """
    Angle Option
    """
    theta: Angle = Field(default_factory=Angle, title="angle", description="theta")

    model_config = ConfigDict(title="Angle Option")

class ElasticModulusOpt(MBaseModel):
    """
    Elastic Modulus Option
    """
    E: Stress = Field(default=Stress(value=200.0, unit=enUnitStress.MPa), title="E", description="Elastic Modulus")

    model_config = ConfigDict(title="Elastic Modulus Option")

class Unit(MBaseModel):
    """
    GSD global unit class
    
    Args:
        force (str): Force unit
        length (str): Length unit
        section_dimension (str): Section dimension unit
        pressure (str): Pressure unit
        strain (str): Strain unit
    """
    force: str = Field(
        default="kN", description="Force unit")
    length: str = Field(
        default="m", description="Length unit")
    section_dimension: str = Field(
        default="mm", description="Section dimension unit")
    pressure: str = Field(
        default="MPa", description="Pressure unit")
    strain: str = Field(
        default="%", description="Strain unit")

    model_config = ConfigDict(title="Unit")

# ==== Stress Strain Curve ====
class Stress_Strain_Component(MBaseModel):
    """Stress Strain Component class

    Args:
        stress (Length): Stress
        strain (Length): Strain
    """
    stress: float = Field(default=0.0, description="Stress")
    strain: float = Field(default=0.0, description="Strain")

    model_config = ConfigDict(title="Stress Strain Component")

# ==== Materials ====
class MaterialCurve(MBaseModel):
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=34.0), Stress_Strain_Component(strain=0.003, stress=34.0)], description="Stress strain curve concrete ULS")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.001, stress=32.8)], description="Stress strain curve")

# ==== Geometry ====
class Point(MBaseModel):
    """
    Point class

    Args:
        x (Length): x-coordinate
        y (Length): y-coordinate
    """
    x: Length
    y: Length

    model_config = ConfigDict(title="Point")

class Points(MBaseModel):
    """
    GSD Points class

    Args:
        points (list[Point]): Points
    """
    points: list[Point] = Field(default=[Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM))], description="Points")

    model_config = ConfigDict(title="Points")

class OuterPolygon(MBaseModel):
    """
    GSD Outer Polygon class

    Args:
        points (list[Point]): Points
    """
    points: list[Point] = Field(default=[Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM))], description="Outer Polygon")

    model_config = ConfigDict(title="Outer Polygon")

class InnerPolygon(MBaseModel):
    """
    GSD Inner Polygon class

    Args:
        points (list[Point]): Points
    """
    points: list[Point] = Field(default=[Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM))], description="Inner Polygon")

    model_config = ConfigDict(title="Inner Polygon")

class Lcb(MBaseModel):
    """
    GSD load combination class

    Args:
        uls (Lcoms): uls load combination
    """
    uls: Lcoms = Field(default=Lcoms(), description="uls load combination")

    model_config = ConfigDict(title="Load Combination")

# ==== options ====
class PMOptions(MBaseModel):
    """
    GSD options class
    
    Args:
        dgncode (str): Design code
        by_ecc_pu (str): ecc
    """
    dgncode: str = Field(default=enDgnCode.Eurocode2_04, description="Design code", enum=enum_to_list(enDgnCode))
    by_ecc_pu: str = Field(default="ecc", description="ecc or P-U", enum=enum_to_list(enEccPu))

    model_config = ConfigDict(title="Options")

class ReportType(MBaseModel):
    """
    Report Type class
    
    Args:
        report_type (str): Report type
    """
    type: str = Field(default="markdown", description="Report type", enum=enum_to_list(enReportType))

    model_config = ConfigDict(title="Report Type")

# ==== Section ====
# Abstract Base Class (Parent Class)
class Section(MBaseModel, ABC):
    """
    Abstract Section class with an abstract method do_convert_point.
    """
    @abstractmethod
    def create_default(cls, unit_system: enUnitSystem):
        pass

    @abstractmethod
    def get_unitsystem(self) -> enUnitSystem:
        pass

    model_config = ConfigDict(title="Section")

class SectionRectangle(Section):
    """
    Section Rectangle class

    Args:
        b (Length): Width
        h (Length): Height
    """
    section_type: Literal["Solid_Rectangle"] = Field("Solid_Rectangle")
    b: Length = Field(default_factory=Length, title="b", description="Width")
    h: Length = Field(default_factory=Length, title="h", description="Height")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(b=Length(value=15, unit=enUnitLength.IN), h=Length(value=20, unit=enUnitLength.IN))
        else:
            return cls(b=Length(value=400, unit=enUnitLength.MM), h=Length(value=600, unit=enUnitLength.MM))

    def get_unitsystem(self) -> enUnitSystem:
        if self.h.unit == enUnitLength.MM:
            return enUnitSystem.SI
        else:
            return enUnitSystem.US

    def do_convert_point(self) -> list[Tuple[float, float]]:
        """
        Converts the rectangle into a list of points forming the outer polygon (rectangle corners).

        Returns:
            list[Tuple[float, float]]: List of points forming the outer polygon.
        """
        points = []

        # Half dimensions
        half_b = self.b.value * 0.5
        half_h = self.h.value * 0.5

        # Define the rectangle vertices
        points.append((-half_b, -half_h))  # Bottom-left
        points.append((+half_b, -half_h))  # Bottom-right
        points.append((+half_b, +half_h))  # Top-right
        points.append((-half_b, +half_h))  # Top-left

        return points

    model_config = ConfigDict(title="Section Rectangle")

# Concrete Class (Child Class for L-shaped section)
class SectionShapeL(Section):
    """
    Section L-Shape class, inheriting from Section.

    Args:
        b (Length): Width
        h (Length): Height
        tw (Length): Thickness of the web
        tf (Length): Thickness of the flange
    """
    section_type: Literal["Angle"] = Field("Angle")
    b: Length = Field(default_factory=Length, title="b", description="Width")
    h: Length = Field(default_factory=Length, title="h", description="Height")
    tw: Length = Field(default_factory=Length, title="tw", description="Thickness of the web")
    tf: Length = Field(default_factory=Length, title="tf", description="Thickness of the flange")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(b=Length(unit=enUnitLength.IN), h=Length(unit=enUnitLength.IN), tw=Length(unit=enUnitLength.IN), tf=Length(unit=enUnitLength.IN))
        else:
            return cls(b=Length(unit=enUnitLength.MM), h=Length(unit=enUnitLength.MM), tw=Length(unit=enUnitLength.MM), tf=Length(unit=enUnitLength.MM))

    def get_unitsystem(self) -> enUnitSystem:
        if self.h.unit == enUnitLength.MM:
            return enUnitSystem.SI
        else:
            return enUnitSystem.US

    def do_convert_point(self) -> list[Tuple[float, float]]:
        """
        Converts the L-shape into a list of points forming the outer polygon (L-shape corners).

        Returns:
            list[Tuple[float, float]]: List of points forming the outer polygon.
        """
        points = []

        # Half dimensions
        half_b = self.b.value * 0.5
        half_h = self.h.value * 0.5
        tf = self.tf.value
        tw = self.tw.value

        points.append((-half_b, -half_h))             # Bottom-left
        points.append((-half_b + tw, -half_h))        # Bottom-right of the left web
        points.append((-half_b + tw, +half_h - tf))   # Top-right of the left web
        points.append((+half_b, +half_h - tf))        # Top-left of the flange
        points.append((+half_b, +half_h))             # Top-right
        points.append((-half_b, +half_h))             # Top-left

        return points

    model_config = ConfigDict(title="Section L-Shape")

# Concrete Class (Child Class for Channel-shaped section)
class SectionShapeC(Section):
    """
    Section Channel class, inheriting from Section.

    Args:
        b (Length): Width
        b2 (Length): Secondary width for the channel
        h (Length): Height
        tw (Length): Thickness of the web
        tf1 (Length): Thickness of the top flange
        tf2 (Length): Thickness of the bottom flange
    """
    section_type: Literal["Channel"] = Field("Channel")
    b1: Length = Field(default_factory=Length, title="b", description="Width")
    b2: Length = Field(default_factory=Length, title="b2", description="Secondary width for channel")
    h: Length = Field(default_factory=Length, title="h", description="Height")
    tw: Length = Field(default_factory=Length, title="tw", description="Thickness of the web")
    tf1: Length = Field(default_factory=Length, title="tf1", description="Thickness of the top flange")
    tf2: Length = Field(default_factory=Length, title="tf2", description="Thickness of the bottom flange")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(b1=Length(unit=enUnitLength.IN), b2=Length(unit=enUnitLength.IN), h=Length(unit=enUnitLength.IN), tw=Length(unit=enUnitLength.IN), tf1=Length(unit=enUnitLength.IN), tf2=Length(unit=enUnitLength.IN))
        else:
            return cls(b1=Length(unit=enUnitLength.MM), b2=Length(unit=enUnitLength.MM), h=Length(unit=enUnitLength.MM), tw=Length(unit=enUnitLength.MM), tf1=Length(unit=enUnitLength.MM), tf2=Length(unit=enUnitLength.MM))

    def get_unitsystem(self) -> enUnitSystem:
        if self.h.unit == enUnitLength.MM:
            return enUnitSystem.SI
        else:
            return enUnitSystem.US

    def do_convert_point(self) -> list[Tuple[float, float]]:
        """
        Converts the channel shape into a list of points forming the outer polygon (channel corners).

        Returns:
            list[Tuple[float, float]]: List of points forming the outer polygon.
        """
        points = []

        # Half dimensions
        half_bmax = 0.5 * max(self.b1.value, self.b2.value)
        half_h = 0.5 * self.h.value

        # Define the channel shape vertices based on the given dimensions
        points.append((-half_bmax, +half_h))                                   # Top-left
        points.append((-half_bmax + self.b1.value, +half_h))                    # Top-right of top flange
        points.append((-half_bmax + self.b1.value, +half_h - self.tf1.value))   # Bottom-right of top flange
        points.append((-half_bmax + self.tw.value, +half_h - self.tf1.value))  # Right side of web top
        points.append((-half_bmax + self.tw.value, -half_h + self.tf2.value))  # Left side of web bottom
        points.append((-half_bmax + self.b2.value, -half_h + self.tf2.value))  # Top-left of bottom flange
        points.append((-half_bmax + self.b2.value, -half_h))                   # Bottom-left of bottom flange
        points.append((-half_bmax, -half_h))                                   # Bottom-left

        return points

    model_config = ConfigDict(title="Section Channel")

# Concrete Class (Child Class for H-shaped section)
class SectionShapeH(Section):
    """
    Section H-Shape class, inheriting from Section.

    Args:
        b (Length): Top width
        b2 (Length): Bottom width
        h (Length): Height
        tw (Length): Thickness of the web
        tf1 (Length): Thickness of the top flange
        tf2 (Length): Thickness of the bottom flange
    """
    section_type: Literal["H_Section"] = Field("H_Section")
    b1: Length = Field(default_factory=Length, title="b", description="Top width")
    b2: Length = Field(default_factory=Length, title="b2", description="Bottom width")
    h: Length = Field(default_factory=Length, title="h", description="Height")
    tw: Length = Field(default_factory=Length, title="tw", description="Thickness of the web")
    tf1: Length = Field(default_factory=Length, title="tf1", description="Thickness of the top flange")
    tf2: Length = Field(default_factory=Length, title="tf2", description="Thickness of the bottom flange")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(b1=Length(unit=enUnitLength.IN), b2=Length(unit=enUnitLength.IN), h=Length(unit=enUnitLength.IN), tw=Length(unit=enUnitLength.IN), tf1=Length(unit=enUnitLength.IN), tf2=Length(unit=enUnitLength.IN))
        else:
            return cls(b1=Length(unit=enUnitLength.MM), b2=Length(unit=enUnitLength.MM), h=Length(unit=enUnitLength.MM), tw=Length(unit=enUnitLength.MM), tf1=Length(unit=enUnitLength.MM), tf2=Length(unit=enUnitLength.MM))

    def get_unitsystem(self) -> enUnitSystem:
        if self.h.unit == enUnitLength.MM:
            return enUnitSystem.SI
        else:
            return enUnitSystem.US

    def do_convert_point(self) -> list[Tuple[float, float]]:
        """
        Converts the H-shape into a list of points forming the outer polygon (H-shape corners).

        Returns:
            list[Tuple[float, float]]: List of points forming the outer polygon.
        """
        points = []

        # Half dimensions
        half_bt = self.b1.value * 0.5
        half_bb = self.b2.value * 0.5
        half_h = self.h.value * 0.5
        half_tw = self.tw.value * 0.5
        tf1 = self.tf1.value
        tf2 = self.tf2.value

        # Define the H-shape vertices based on the given dimensions
        points.append((-half_bt, +half_h))               # Top-left
        points.append((+half_bt, +half_h))               # Top-right
        points.append((+half_bt, +half_h - tf1))         # Bottom-right of top flange
        points.append((+half_tw, +half_h - tf1))         # Right side of web top
        points.append((+half_tw, -half_h + tf2))         # Right side of web bottom
        points.append((+half_bb, -half_h + tf2))         # Top-right of bottom flange
        points.append((+half_bb, -half_h))               # Bottom-right
        points.append((-half_bb, -half_h))               # Bottom-left
        points.append((-half_bb, -half_h + tf2))         # Top-left of bottom flange
        points.append((-half_tw, -half_h + tf2))         # Left side of web bottom
        points.append((-half_tw, +half_h - tf1))         # Left side of web top
        points.append((-half_bt, +half_h - tf1))         # Bottom-left of top flange

        return points

    model_config = ConfigDict(title="Section H-Shape")

# Concrete Class (Child Class for T-shaped section)
class SectionShapeT(Section):
    """
    Section T-Shape class, inheriting from Section.

    Args:
        b (Length): Flange width
        h (Length): Height
        tw (Length): Thickness of the web
        tf (Length): Thickness of the flange
    """
    section_type: Literal["T_Section"] = Field("T_Section")
    b: Length = Field(default_factory=Length, title="b", description="Flange width")
    h: Length = Field(default_factory=Length, title="h", description="Height")
    tw: Length = Field(default_factory=Length, title="tw", description="Thickness of the web")
    tf: Length = Field(default_factory=Length, title="tf", description="Thickness of the flange")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(b=Length(unit=enUnitLength.IN), h=Length(unit=enUnitLength.IN), tw=Length(unit=enUnitLength.IN), tf=Length(unit=enUnitLength.IN))
        else:
            return cls(b=Length(unit=enUnitLength.MM), h=Length(unit=enUnitLength.MM), tw=Length(unit=enUnitLength.MM), tf=Length(unit=enUnitLength.MM))

    def get_unitsystem(self) -> enUnitSystem:
        if self.h.unit == enUnitLength.MM:
            return enUnitSystem.SI
        else:
            return enUnitSystem.US

    def do_convert_point(self) -> list[Tuple[float, float]]:
        """
        Converts the T-shape into a list of points forming the outer polygon (T-shape corners).

        Returns:
            list[Tuple[float, float]]: List of points forming the outer polygon.
        """
        points = []

        # Half dimensions
        half_b = self.b.value * 0.5
        half_h = self.h.value * 0.5
        half_tw = self.tw.value * 0.5
        tf = self.tf.value

        # Define the T-shape vertices based on the given dimensions
        points.append((-half_b, +half_h))              # Top-left of flange
        points.append((+half_b, +half_h))              # Top-right of flange
        points.append((+half_b, +half_h - tf))         # Bottom-right of flange
        points.append((+half_tw, +half_h - tf))        # Right side of web top
        points.append((+half_tw, -half_h))             # Bottom-right of web
        points.append((-half_tw, -half_h))             # Bottom-left of web
        points.append((-half_tw, +half_h - tf))        # Left side of web top
        points.append((-half_b, +half_h - tf))         # Bottom-left of flange

        return points

    model_config = ConfigDict(title="Section T-Shape")

# Concrete Class (Child Class for Box-shaped section)
class SectionShapeBox(Section):
    """
    Section Box Shape class, inheriting from Section.

    Args:
        b (Length): Width
        h (Length): Height
        tw (Length): Thickness of the web
        tf1 (Length): Thickness of the top flange
        tf2 (Length): Thickness of the bottom flange
    """
    section_type: Literal["Box"] = Field("Box")
    b: Length = Field(default_factory=Length, title="b", description="Width")
    h: Length = Field(default_factory=Length, title="h", description="Height")
    tw: Length = Field(default_factory=Length, title="tw", description="Thickness of the web")
    tf1: Length = Field(default_factory=Length, title="tf1", description="Thickness of the top flange")
    tf2: Length = Field(default_factory=Length, title="tf2", description="Thickness of the bottom flange")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(b=Length(unit=enUnitLength.IN), h=Length(unit=enUnitLength.IN), tw=Length(unit=enUnitLength.IN), tf1=Length(unit=enUnitLength.IN), tf2=Length(unit=enUnitLength.IN))
        else:
            return cls(b=Length(unit=enUnitLength.MM), h=Length(unit=enUnitLength.MM), tw=Length(unit=enUnitLength.MM), tf1=Length(unit=enUnitLength.MM), tf2=Length(unit=enUnitLength.MM))

    def get_unitsystem(self) -> enUnitSystem:
        if self.h.unit == enUnitLength.MM:
            return enUnitSystem.SI
        else:
            return enUnitSystem.US

    def do_convert_point(self) -> Tuple[list[Tuple[float, float]], list[list[Tuple[float, float]]]]:
        """
        Converts the Box shape into a list of points forming the outer polygon (Box shape corners).

        Returns:
            list[Tuple[float, float]]: List of points forming the outer polygon.
        """
        outer_polygon = []
        inner_polygon = []

        # Half dimensions
        half_b = self.b.value * 0.5
        half_h = self.h.value * 0.5
        half_b_in = half_b - self.tw.value
        half_h_itop = half_h - self.tf1.value
        half_h_ibot = half_h - self.tf2.value

        # Define the Box shape vertices based on the given dimensions
        outer_polygon.append((-half_b, +half_h))                    # Top-left outer
        outer_polygon.append((+half_b, +half_h))                    # Top-right outer
        outer_polygon.append((+half_b, -half_h))                    # Bottom-right outer
        outer_polygon.append((-half_b, -half_h))                    # Bottom-left outer

        inner_polygon.append((-half_b_in, +half_h_itop))            # Top-left inner
        inner_polygon.append((-half_b_in, -half_h_ibot))            # Bottom-left inner
        inner_polygon.append((+half_b_in, -half_h_ibot))            # Bottom-right inner
        inner_polygon.append((+half_b_in, +half_h_itop))            # Top-right inner

        return outer_polygon, inner_polygon

    model_config = ConfigDict(title="Section Box Shape")

# Concrete Class (Child Class for Pipe-shaped section)
class SectionShapePipe(Section):
    """
    Section Pipe Shape class, inheriting from Section.

    Args:
        r (Length): Outer radius
        t (Length): Wall thickness
    """
    section_type: Literal["Pipe"] = Field("Pipe")
    d: Length = Field(default_factory=Length, title="d", description="dia")
    tw: Length = Field(default_factory=Length, title="tw", description="thickness")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(d=Length(unit=enUnitLength.IN), tw=Length(unit=enUnitLength.IN))
        else:
            return cls(d=Length(unit=enUnitLength.MM), tw=Length(unit=enUnitLength.MM))

    def get_unitsystem(self) -> enUnitSystem:
        if self.d.unit == enUnitLength.MM:
            return enUnitSystem.SI
        else:
            return enUnitSystem.US

    def do_convert_point(self) -> Tuple[list[Tuple[float, float]], list[list[Tuple[float, float]]]]:
        """
        Converts the pipe shape into two lists of points forming the outer and inner circles.

        Returns:
            Tuple[list[Tuple[float, float]], list[list[Tuple[float, float]]]]: 
                Tuple containing the list of points forming the outer circle and the list of points forming the inner circle.
        """
        segments = 72
        outer_points = []
        inner_points = []

        # Calculate inner radius
        r = self.d.value * 0.5
        r2 = r - self.tw.value

        # Calculate angle increment
        theta = 2.0 * math.pi / segments

        # Modified radii to account for circular segment approximation
        modifier1 = math.sqrt(theta / math.sin(theta)) * r
        modifier2 = math.sqrt(theta / math.sin(theta)) * r2

        # Generate points for the outer circle
        for idx in range(segments):
            angle = idx * theta
            x = math.cos(angle) * modifier1
            y = math.sin(angle) * modifier1
            outer_points.append((x, y))

        # Generate points for the inner circle
        for idx in range(segments):
            angle = idx * theta
            x = math.cos(angle) * modifier2
            y = math.sin(angle) * modifier2
            inner_points.append((x, y))

        return outer_points, inner_points

    model_config = ConfigDict(title="Section Pipe Shape")