from typing import Optional
from pydantic import Field, ConfigDict
from moapy.auto_convert import MBaseModel
from moapy.data_pre import Point, Stress_Strain_Component, Length, enUnitLength, Stress, enUnitStress, MaterialCurve, Area, enUnitArea, SectionRectangle
from moapy.enum_pre import enum_to_list, enUnitArea, enUnitLength, enUnitStress, enUnitThermalExpansion, enUnitAngle, enUnitTemperature, enDgnCode, enBoltName, enUnitMoment, enRebar_UNI, enUnitSystem
# ==== Concrete Material ====
class ConcreteGrade(MBaseModel):
    """
    GSD concrete class

    Args:
        design_code (str): Design code
        grade (str): Grade of the concrete
    """
    design_code: str = Field(
        default="ACI318M-19", description="Design code")
    grade: str = Field(
        default="C12", description="Grade of the concrete")

    model_config = ConfigDict(title="Concrete Grade")

class Concrete_General_Properties(MBaseModel):
    """
    GSD concrete general properties for calculation
    
    Args:
        strength (int): Grade of the concrete
        elastic_modulus (float): Elastic modulus of the concrete
        density (float): Density of the concrete
        thermal_expansion_coefficient (float): Thermal expansion coefficient of the concrete
        poisson_ratio (float): Poisson ratio of the concrete
    """
    strength: int = Field(
        gt=0, default=12, description="Grade of the concrete")
    elastic_modulus: float = Field(
        gt=0, default=30000, description="Elastic modulus of the concrete")
    density: float = Field(
        gt=0, default=2400, description="Density of the concrete")
    thermal_expansion_coefficient: float = Field(
        gt=0, default=0.00001, description="Thermal expansion coefficient of the concrete")
    poisson_ratio: float = Field(
        gt=0, default=0.2, description="Poisson ratio of the concrete")

    model_config = ConfigDict(title="Concrete General Properties")

class Concrete_Stress_ULS_Options_ACI(MBaseModel):
    """
    GSD concrete stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        factor_b1 (float): Plastic strain limit for ULS
        compressive_failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = Field(
        default="Rectangle", description="Material model for ULS")
    factor_b1: float = Field(
        default=0.85, description="Plastic strain limit for ULS")
    compressive_failure_strain: float = Field(
        default=0.003, description="Failure strain limit for ULS")

    model_config = ConfigDict(title="Concrete Stress Options for ULS")

class Concrete_Stress_ULS_Options_Eurocode(MBaseModel):
    """
    GSD concrete stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        partial_factor_case (float): Partial factor case for ULS
        partial_factor (float): Partial factor for ULS
        compressive_failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = Field(
        default="Rectangle", description="Material model for ULS")
    partial_factor_case: float = Field(
        default=1.0, description="Partial factor case for ULS")
    partial_factor: float = Field(
        default=1.5, description="Partial factor for ULS")
    compressive_failure_strain: float = Field(
        default=0.003, description="Failure strain limit for ULS")

    model_config = ConfigDict(title="Concrete Stress Options for ULS")

class Concrete_SLS_Options(MBaseModel):
    """
    GSD concrete stress options for SLS
    
    Args:
        material_model (str): Material model for SLS
        plastic_strain_limit (float): Plastic strain limit for SLS
        failure_compression_limit (float): Failure compression limit for SLS
        material_model_tension (str): Material model for SLS tension
        failure_tension_limit (float): Failure tension limit for SLS
    """
    material_model: str = Field(
        default="Linear", description="Material model for SLS")
    plastic_strain_limit: float = Field(
        default=0.002, description="Plastic strain limit for SLS")
    failure_compression_limit: float = Field(
        default=0.003, description="Failure compression limit for SLS")
    material_model_tension: str = Field(
        default="interpolated", description="Material model for SLS tension")
    failure_tension_limit: float = Field(
        default=0.003, description="Failure tension limit for SLS")

    model_config = ConfigDict(title="Concrete Stress Options for SLS")

# ==== Rebar & Tendon Materials ====
class RebarGrade(MBaseModel):
    """
    GSD rebar grade class
    
    Args:
        design_code (str): Design code
        grade (str): Grade of the rebar
    """
    design_code: str = Field(
        default="ACI318M-19", description="Design code")
    grade: str = Field(
        default="Grade 420", description="Grade of the rebar")

    model_config = ConfigDict(title="Rebar Grade")

class TendonGrade(MBaseModel):
    """
    GSD Tendon grade class
    
    Args:
        design_code (str): Design code
        grade (str): Grade of the tendon
    """
    design_code: str = Field(
        default="ACI318M-19", description="Design code")
    grade: str = Field(default="Grade 420", description="Grade of the tendon")

    model_config = ConfigDict(title="Tendon Grade")

class RebarProp(MBaseModel):
    """
    GSD rebar prop

    Args:
        area (float): Area of the rebar
    """
    area: Area = Field(default=Area(value=287.0, unit=enUnitArea.MM2), description="Area of the rebar")

    model_config = ConfigDict(title="Rebar Properties")

class TendonProp(MBaseModel):
    """
    GSD Tendon prop

    Args:
        area (float): Area of the tendon
        prestress (float): Prestress of the tendon
    """
    area: Area = Field(default=Area(value=287.0, unit=enUnitArea.MM2), description="Area of the tendon")
    prestress: Stress = Field(default=Stress(value=0.0, unit=enUnitStress.MPa), description="Prestress of the tendon")

    model_config = ConfigDict(title="Tendon Properties")

class Rebar_General_Properties(MBaseModel):
    """
    GSD rebar general properties for calculation
    
    Args:
        strength (int): Grade of the rebar
        elastic_modulus (float): Elastic modulus of the rebar
        density (float): Density of the rebar
        thermal_expansion_coefficient (float): Thermal expansion coefficient of the rebar
        poisson_ratio (float): Poisson ratio of the rebar
    """
    strength: int = Field(
        default=420, description="Grade of the rebar")
    elastic_modulus: float = Field(
        default=200000, description="Elastic modulus of the rebar")
    density: float = Field(
        default=7850, description="Density of the rebar")
    thermal_expansion_coefficient: float = Field(
        default=0.00001, description="Thermal expansion coefficient of the rebar")
    poisson_ratio: float = Field(
        default=0.3, description="Poisson ratio of the rebar")

    model_config = ConfigDict(title="Rebar General Properties")

class Rebar_Stress_ULS_Options_ACI(MBaseModel):
    """
    GSD rebar stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = Field(
        default="Elastic-Plastic", description="Material model for ULS")
    failure_strain: float = Field(
        default=0.7, description="Failure strain limit for ULS")

    model_config = ConfigDict(title="Rebar Stress Options for ULS")

class Rebar_Stress_SLS_Options(MBaseModel):
    """
    GSD rebar stress options for SLS
    
    Args:
        material_model (str): Material model for SLS
        failure_strain (float): Failure strain limit for SLS
    """
    material_model: str = Field(
        default="Elastic-Plastic", description="Material model for SLS")
    failure_strain: float = Field(
        default=0.7, metadata={"default" : 0.7, "description": "Failure strain limit for SLS"})

    model_config = ConfigDict(title="Rebar Stress Options for SLS")

class MaterialRebar(MaterialCurve):
    """
    GSD rebar class
    
    Args:
        grade (RebarGrade): Grade of the rebar
        curve_uls (list[Stress_Strain_Component]): Stress strain curve for ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve for SLS
    """
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0025, stress=500.0), Stress_Strain_Component(strain=0.05, stress=500.0)], description="Stress strain curve")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0025, stress=500.0), Stress_Strain_Component(strain=0.05, stress=500.0)], description="Stress strain curve")

    model_config = ConfigDict(title="Material Rebar")

class MaterialTendon(MaterialCurve):
    """
    GSD tendon class
    
    Args:
        grade (TendonGrade): Grade of the tendon
        curve_uls (list[Stress_Strain_Component]): Stress strain curve for ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve for SLS
    """
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.00725, stress=1450.0), Stress_Strain_Component(strain=0.05, stress=1750.0)], description="Stress strain curve")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.00725, stress=1450.0), Stress_Strain_Component(strain=0.05, stress=1750.0)], description="Stress strain curve")

    model_config = ConfigDict(title="Material Tendon")

class MaterialConcrete(MaterialCurve):
    """
    GSD material for Concrete class
    
    Args:
        curve_uls (list[Stress_Strain_Component]): Stress strain curve concrete ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve
    """
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=34.0), Stress_Strain_Component(strain=0.003, stress=34.0)], description="Stress strain curve concrete ULS")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.001, stress=32.8)], description="Stress strain curve")

    model_config = ConfigDict(title="Material Concrete")

class Material(MBaseModel):
    """
    GSD concrete class

    Args:
        concrete (MaterialConcrete): Concrete properties
        rebar (MaterialRebar): Rebar properties
        tendon (MaterialTendon): Tendon properties
    """
    concrete: MaterialConcrete = Field(default=MaterialConcrete(), description="Concrete properties")
    rebar: Optional[MaterialRebar] = Field(default=MaterialRebar(), description="Rebar properties")
    tendon: Optional[MaterialTendon] = Field(default=MaterialTendon(), description="Tendon properties")

    def __post_init__(self):
        if self.rebar is None and self.tendon is None:
            raise ValueError("Either rebar or tendon must be provided.")

    model_config = ConfigDict(title="Material")

class MaterialNative(MBaseModel):
    """
    Material Native Data
    """
    fck: Stress = Field(default_factory=Stress, title="fck", description="Concrete strength")
    fy: Stress = Field(default_factory=Stress, title="fy", description="Rebar strength")
    fys: Stress = Field(default_factory=Stress, title="fys", description="Stirrup strength")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(
                fck=Stress(value=3500.0, unit="psi"),  # US units (psi)
                fy=Stress(value=58000.0, unit="psi"),  # US units (psi)
                fys=Stress(value=58000.0, unit="psi"),  # US units (psi)
            )
        else:  # SI units by default
            return cls(
                fck=Stress(value=24.0, unit="MPa"),  # SI units (MPa)
                fy=Stress(value=400.0, unit="MPa"),  # SI units (MPa)
                fys=Stress(value=400.0, unit="MPa"),  # SI units (MPa)
            )

class ConcreteGeometry(MBaseModel):
    """
    GSD concrete geometry class
    
    Args:
        outerPolygon (list[Point]): Outer polygon of the concrete
        innerPolygon (list[Point]): Inner polygon of the concrete
    """
    outerPolygon: list[Point] = Field(default=[Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), 
                                               Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM)), Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM))], description="Outer polygon of the concrete")
    innerPolygon: list[Point] = Field(default=[Point(x=Length(value=80.0, unit=enUnitLength.MM), y=Length(value=80.0, unit=enUnitLength.MM)), Point(x=Length(value=320.0, unit=enUnitLength.MM), y=Length(value=80.0, unit=enUnitLength.MM)),
                                               Point(x=Length(value=320.0, unit=enUnitLength.MM), y=Length(value=520.0, unit=enUnitLength.MM)), Point(x=Length(value=80.0, unit=enUnitLength.MM), y=Length(value=520.0, unit=enUnitLength.MM))], description="Inner polygon of the concrete")

    model_config = ConfigDict(title="Concrete Geometry")

class RebarGeometry(MBaseModel):
    """
    GSD rebar geometry class

    Args:
        prop (RebarProp): properties of the rebar
        points (list[Point]): Rebar Points
    """
    prop: RebarProp = Field(default=RebarProp(), description="properties of the rebar")
    points: list[Point] = Field(default=[Point(x=Length(value=40.0, unit=enUnitLength.MM), y=Length(value=40.0, unit=enUnitLength.MM)), Point(x=Length(value=360.0, unit=enUnitLength.MM), y=Length(value=40.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=360.0, unit=enUnitLength.MM), y=Length(value=560.0, unit=enUnitLength.MM)), Point(x=Length(value=40.0, unit=enUnitLength.MM), y=Length(value=560.0, unit=enUnitLength.MM))], description="Rebar Points")

    model_config = ConfigDict(title="Rebar Geometry")

class TendonGeometry(MBaseModel):
    """
    GSD tendon geometry class
    
    Args:
        prop (TendonProp): properties of the tendon
        points (list[Point]): Tendon Points
    """
    prop: TendonProp = Field(default=TendonProp(), description="properties of the tendon")
    points: list[Point] = Field(default=[], description="Tendon Points")

    model_config = ConfigDict(title="Tendon Geometry")

class Geometry(MBaseModel):
    """
    GSD geometry class

    Args:
        concrete (ConcreteGeometry): Concrete geometry
        rebar (RebarGeometry): Rebar geometry
        tendon (TendonGeometry): Tendon geometry
    """
    concrete: ConcreteGeometry = Field(default=ConcreteGeometry(), description="Concrete geometry")
    rebar: Optional[list[RebarGeometry]] = Field(default=[RebarGeometry()], description="Rebar geometry")
    tendon: Optional[list[TendonGeometry]] = Field(default=[TendonGeometry()], description="Tendon geometry")

    model_config = ConfigDict(title="Geometry")

class SlabMember_EC(MBaseModel):
    """
    Slab Member
    """
    fck: Stress = Field(default=Stress(value=24.0, unit=enUnitStress.MPa), title="fck", description="Concrete strength")
    thickness: Length = Field(default=Length(value=150.0, unit=enUnitLength.MM), title="Slab thick", description="Slab thickness")

    model_config = ConfigDict(title="Slab Member", description="Slab Member with concrete strength and thickness")

class GirderLength(MBaseModel):
    """
    Girder Length
    """
    span: Length = Field(default=Length(value=10.0, unit=enUnitLength.M), title="Span length", description="Span Length")
    spacing: Length = Field(default=Length(value=3.0, unit=enUnitLength.M), title="Spacing", description="Spacing")

    model_config = ConfigDict(
        title="Girder Length",
        description="Provides the information needed to define the lengths and spacing of lattice beams in a structure. This information is essential to ensure that spans and spacing are properly accounted for in the structural design to ensure load distribution and safety. "
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(span=Length(value=30, unit=enUnitLength.FT), spacing=Length(value=8, unit=enUnitLength.FT))
        else:
            return cls(span=Length(value=10, unit=enUnitLength.M), spacing=Length(value=3, unit=enUnitLength.M))

class NeutralAxisDepth(MBaseModel):
    """
    Neutral Axis Depth
    """
    depth: Length = Field(default=Length(value=0.0, unit=enUnitLength.MM), title="Neutral Axis Depth", description="Neutral Axis Depth")

    model_config = ConfigDict(title="Neutral Axis Depth", description="Neutral Axis Depth")

class RebarNumberNameCover(MBaseModel):
    """
    Rebar Number
    """
    number: int = Field(default=2, title="Number", description="Number of Rebar")
    name: str = Field(default="P26", title="Name", description="Rebar Name", enum=enum_to_list(enRebar_UNI))
    cover: Length = Field(default_factory=Length, title="Cover", description="Distance from centroid of reinforcement to the nearest surface of the concrete")

    model_config = ConfigDict(title="Rebar Number", description="Rebar Number")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(cover=Length(value=1.5, unit=enUnitLength.IN))
        else:  # SI units by default
            return cls(cover=Length(value=40, unit=enUnitLength.MM))

class RebarNumberRowNameCover(MBaseModel):
    """
    Rebar Number
    """
    number: int = Field(default=4, title="Number", description="Number of Rebar")
    row: int = Field(default=2, title="row", description="row number of Rebar")
    name: str = Field(default="P26", title="Name", description="Rebar Name", enum=enum_to_list(enRebar_UNI))
    cover: Length = Field(default_factory=Length, title="Cover", description="Distance from centroid of reinforcement to the nearest surface of the concrete")

    model_config = ConfigDict(title="Rebar Number & Row", description="Rebar Number & Row")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(cover=Length(value=2, unit=enUnitLength.IN))
        else:  # SI units by default
            return cls(cover=Length(value=60, unit=enUnitLength.MM))

class RebarNumberNameSpace(MBaseModel):
    """
    Rebar Number Name Space
    """
    number: int = Field(default=2, title="Number", description="Number of legs")
    name: str = Field(default="P10", title="Name", description="Rebar Name", enum=enum_to_list(enRebar_UNI))
    space: Length = Field(default_factory=Length, title="Space", description="Distance between rebars")

    model_config = ConfigDict(title="Rebar Number Name Space", description="Rebar Number Name Space")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(space=Length(value=10, unit=enUnitLength.IN))
        else:  # SI units by default
            return cls(space=Length(value=100, unit=enUnitLength.MM))

class RebarPointName(MBaseModel):
    """
    Rebar Point Name
    """
    point: Point = Field(default=Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), title="Point", description="Rebar Point")
    name: str = Field(default="P26", title="Name", description="Rebar Name", enum=enum_to_list(enRebar_UNI))

    model_config = ConfigDict(title="Rebar Point Name", description="Rebar Point Name")

class BeamRebarPattern(MBaseModel):
    top: list[RebarNumberNameCover] = Field(default_factory=list, title="Top", description="Top Rebar")
    bot: list[RebarNumberNameCover] = Field(default_factory=list, title="Bot", description="Bottom Rebar")
    stirrup: RebarNumberNameSpace = Field(default_factory=RebarNumberNameSpace, title="Stirrup", description="Stirrup Rebar")

    model_config = ConfigDict(title="Beam Rebar Pattern", description="Beam Rebar Pattern")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(top=[RebarNumberNameCover.create_default(enUnitSystem.US)], bot=[RebarNumberNameCover.create_default(enUnitSystem.US)], stirrup=RebarNumberNameSpace.create_default(enUnitSystem.US))
        else:  # SI units by default
            return cls(top=[RebarNumberNameCover.create_default(enUnitSystem.SI)], bot=[RebarNumberNameCover.create_default(enUnitSystem.SI)], stirrup=RebarNumberNameSpace.create_default(enUnitSystem.SI))

class ColumnRebarPattern(MBaseModel):
    main: list[RebarNumberRowNameCover] = Field(default_factory=list, title="Main Rebar", description="Main Rebar")
    end_stirrup: RebarNumberNameSpace = Field(default_factory=RebarNumberNameSpace, title="End stirrup", description="End Stirrup Rebar")
    mid_stirrup: RebarNumberNameSpace = Field(default_factory=RebarNumberNameSpace, title="Middle stirrup", description="Middle Stirrup Rebar")

    model_config = ConfigDict(title="Column Rebar Pattern", description="Column Rebar Pattern")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(main=[RebarNumberRowNameCover.create_default(enUnitSystem.US)], end_stirrup=RebarNumberNameSpace.create_default(enUnitSystem.US), mid_stirrup=RebarNumberNameSpace.create_default(enUnitSystem.US))
        else:  # SI units by default
            return cls(main=[RebarNumberRowNameCover.create_default(enUnitSystem.SI)], end_stirrup=RebarNumberNameSpace.create_default(enUnitSystem.SI), mid_stirrup=RebarNumberNameSpace.create_default(enUnitSystem.SI))

class GeneralRebarPattern(MBaseModel):
    main: list[RebarPointName] = Field(default=[RebarPointName(point=Point(x=Length(value=40), y=Length(value=40))), RebarPointName(point=Point(x=Length(value=360), y=Length(value=40))),
                                                RebarPointName(point=Point(x=Length(value=40), y=Length(value=560))), RebarPointName(point=Point(x=Length(value=360), y=Length(value=560)))], title="Main Rebar", description="Main Rebar")
    cover: Length = Field(default=Length(value=22.0, unit=enUnitLength.MM), title="Cover", description="Cover")
    stirrup: RebarNumberNameSpace = Field(default=RebarNumberNameSpace(), title="Stirrup", description="Stirrup Rebar")

    model_config = ConfigDict(title="General Rebar Pattern", description="General Rebar Pattern")

class EquivalentAreaGeneralSect(MBaseModel):
    """
    Equivalent Area for General Section
    """
    b: Length = Field(default=Length(value=300.0, unit=enUnitLength.MM), title="Effective Width", description="Effective Width")
    d: Length = Field(default=Length(value=300.0, unit=enUnitLength.MM), title="Effective Depth", description="Effective Depth")

    model_config = ConfigDict(title="Equivalent Area for General Section", description="Equivalent Area for General Section")