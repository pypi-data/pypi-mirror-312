from pydantic import Field, ConfigDict
from typing import List
from moapy.auto_convert import MBaseModel
from moapy.enum_pre import enum_to_list, enConnectionType, enUnitLength, en_H_EN10365, enSteelMaterial_EN10025, en_H_AISC05_US, enBoltName, enBoltMaterialEC, enSteelMaterial_ASTM, en_H_AISC10_US, en_H_AISC10_SI, enUnitSystem, enAnchorType, enBoltMaterialASTM
from moapy.data_pre import Length, BucklingLength

# ==    == Steel DB ====
class SteelLength(BucklingLength):
    """
    Steel DB Length
    """
    l_b: Length = Field(default_factory=Length, title="Lb", description="Lateral unbraced length")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        instance = super().create_default(unit_system)
        if unit_system == enUnitSystem.US:
            instance.l_b = Length(value=15, unit=enUnitLength.IN)
        else:
            instance.l_b = Length(value=3000, unit=enUnitLength.MM)

        return instance

    model_config = ConfigDict(
        title="Member Length",
        description="Buckling length is the length at which a structural member, such as a column or plate, can resist the phenomenon of buckling. Buckling is the sudden deformation of a long member under compressive load along its own center of gravity, which has a significant impact on the safety of a structure. Buckling length is an important factor in analyzing and preventing this phenomenon."
    )

class SteelLength_EC(SteelLength):
    """
    Steel DB Length
    """
    l_t: Length = Field(default_factory=Length, title="Lt", description="Torsional Buckling Length")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        instance = super().create_default(unit_system)
        instance.l_t = Length(value=3000, unit=enUnitLength.MM)
        return instance

    model_config = ConfigDict(
        title="Member Length",
        description="Buckling length is the length at which a structural member, such as a column or plate, can resist the phenomenon of buckling. Buckling is the sudden deformation of a long member under compressive load along its own center of gravity, which has a significant impact on the safety of a structure. Buckling length is an important factor in analyzing and preventing this phenomenon."
    )

class SteelMomentModificationFactorLTB(MBaseModel):
    """
    Steel DB Moment Modification Factor
    """
    c_b: float = Field(default=1.0, title="Cb", description="Cb Modification Factor")

    model_config = ConfigDict(
        title="Steel Moment Modification Factor",
        description="It is calculated based on the moment distribution, using Mmax(the maximum moment within the unbraced length) and specific moments at certain points (Ma, Mb, Mc)"
    )

class SteelMomentModificationFactor(MBaseModel):
    """
    Steel DB Moment Modification Factor
    """
    c_mx: float = Field(default=1.0, title="Cmx", description="Cmx Modification Factor")
    c_my: float = Field(default=1.0, title="Cmy", description="Cmy Modification Factor")

    model_config = ConfigDict(
        title="Steel Moment Modification Factor",
        description="A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements. moment modification factor plays an important role in adjusting the moments to reflect the behavior and loading conditions of the structure."
    )

class SteelMomentModificationFactor_EC(SteelMomentModificationFactor):
    """
    Steel DB Moment Modification Factor
    """
    c1: float = Field(default=1.0, title="C1", description="ratio between the critical bending moment and the critical constant bending moment for a member with hinged supports")
    c_mlt: float = Field(default=1.0, title="Cmlt", description="equivalent uniform moment factor for LTB")

    model_config = ConfigDict(
        title="Steel Moment Modification Factor",
        description="A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements. moment modification factor plays an important role in adjusting the moments to reflect the behavior and loading conditions of the structure."
    )

class SteelSection(MBaseModel):
    """
    Steel DB Section
    """
    shape: str = Field(default='H', description="Shape of member section", readOnly=True)
    name: str = Field(default=None, description="Section Name", enum=[])

    @classmethod
    def create_default(cls, name: str, enum_list: List[str], description: str = "Steel DB Section"):
        """
        Creates an instance of SteelSection with a specific enum list and dynamic description for the name field.
        """
        section = cls()
        # Dynamically set the enum for the name field
        section.__fields__['name'].json_schema_extra['enum'] = enum_list
        # Set default name if enum_list is provided
        section.name = name
        # Change description dynamically
        cls.model_config["description"] = description
        return section

    model_config = ConfigDict(
        title="Steel DB Section",
        description="Steel DB Section"
    )

class SteelSection_AISC05_US(SteelSection):
    """
    Steel DB Section
    """
    shape: str = Field(default='H', description="Shape of member section", readOnly=True)
    name: str = Field(default='W40X362', description="Please select a section.", enum=enum_to_list(en_H_AISC05_US))

    model_config = ConfigDict(
        title="Steel DB Section",
        description="Currently, only H-sections are supported."
    )

class SteelSection_AISC10_US(SteelSection):
    """
    Steel DB Section
    """
    shape: str = Field(default='H', description="Shape of member section", readOnly=True)
    name: str = Field(default='W40X183', description="Please select a section.", enum=enum_to_list(en_H_AISC10_US))

    model_config = ConfigDict(
        title="Steel DB Section",
        description="Currently, only H-sections are supported."
    )

class SteelSection_AISC10_SI(SteelSection):
    """
    Steel DB Section
    """
    shape: str = Field(default='H', description="Shape of member section", readOnly=True)
    name: str = Field(default="W360X72", description="Please select a section.", enum=enum_to_list(en_H_AISC10_SI))

    model_config = ConfigDict(
        title="Steel DB Section",
        description="Currently, only H-sections are supported."
    )

class SteelSection_EN10365(SteelSection):
    """
    Steel DB Section wit
    """
    shape: str = Field(default='H', description="Shape of member section", readOnly=True)
    name: str = Field(default='HD 260x54.1', description="Use DB stored in EN10365", enum=enum_to_list(en_H_EN10365))

    model_config = ConfigDict(
        title="Steel DB Section",
        description="EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."
    )

class SteelMaterial(MBaseModel):
    """
    Steel DB Material
    """
    code: str = Field(default_factory=str, description="Material Code", readOnly=True)
    name: str = Field(default_factory=str, description="Material Name", enum=[])

    @classmethod
    def create_default(cls, code: str, enum_list: List[str], description: str = "Steel DB Material"):
        """
        Create a SteelMaterial instance with customizable values including description.
        """
        material = cls()
        material.model_config["description"] = description
        # Set the enum options for the name field dynamically
        material.__fields__['name'].json_schema_extra['enum'] = enum_list
        material.code = code
        material.name = enum_list[0] if enum_list else None
        return material

    model_config = ConfigDict(
        title="Steel DB Material",
        description="Steel DB Material"
    )

class SteelMaterial_EC(SteelMaterial):
    """
    Steel DB Material
    """
    code: str = Field(default='EN10025', description="Material code", readOnly=True)
    name: str = Field(default=enSteelMaterial_EN10025.S275, description="Material of steel member", enum=enum_to_list(enSteelMaterial_EN10025))

    model_config = ConfigDict(
        title="Steel DB Material",
        description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type."
    )

class BoltMaterial(MBaseModel):
    """
    Bolt Material
    """
    name: str = Field(default='F10T', description="Bolt Material Name", enum=[])

    @classmethod
    def create_default(cls, name: str, enum_list: List[str]):
        material = cls()
        material.__fields__['name'].json_schema_extra['enum'] = enum_list
        material.name = name
        return material

    model_config = ConfigDict(
        title="Bolt Material",
        description="Bolt Material"
    )

class BoltMaterial_EC(BoltMaterial):
    """
    Bolt Material
    """
    name: str = Field(default='4.8', description="Bolt Material Name", enum=enum_to_list(enBoltMaterialEC))

    model_config = ConfigDict(
        title="Bolt Material",
        description="Bolt Material"
    )

class SteelMember(MBaseModel):
    """
    Steel Member
    """
    sect: SteelSection = Field(default_factory=SteelSection, description="Section")
    matl: SteelMaterial = Field(default_factory=SteelMaterial, description="Material")

    model_config = ConfigDict(
        title="Steel Member",
        description="Steel sections and material inputs are fundamental elements of structural design, each requiring proper selection based on their characteristics and requirements. This maximizes the strength, stability, and durability of the structure and contributes to designing a safe and efficient structure."
    )

class SteelMember_EC(SteelMember):
    """
    Steel Member
    """
    sect: SteelSection_EN10365 = Field(default=SteelSection_EN10365(), title="Section", description="Shape of section")
    matl: SteelMaterial_EC = Field(default=SteelMaterial_EC(), title="Material", description="Material of steel member")

    model_config = ConfigDict(
        title="Steel Member",
        description="Steel sections and material inputs are fundamental elements of structural design, each requiring proper selection based on their characteristics and requirements. This maximizes the strength, stability, and durability of the structure and contributes to designing a safe and efficient structure."
    )

class SteelConnectMember(MBaseModel):
    """
    Steel Connect Member
    """
    supporting: SteelMember = Field(default_factory=SteelMember, description="Supporting Member")
    supported: SteelMember = Field(default_factory=SteelMember, description="Supported Member")

    model_config = ConfigDict(
        title="Steel Connect Member",
        description="Supporting and supported sections play complementary roles in bolted connections and make important contributions to the load bearing and transfer of the structure. The correct design and analysis of these two sections is essential to ensure the stability and durability of the structure."
    )

class SteelConnectMember_EC(SteelConnectMember):
    """
    Steel Connect Member
    """
    supporting: SteelMember_EC = Field(default_factory=SteelMember_EC, title="Supporting member", description="Supporting Member")
    supported: SteelMember_EC = Field(default_factory=SteelMember_EC, title="Supported member", description="Supported Member")

    model_config = ConfigDict(
        title="Steel Connect Member",
        description="Supporting and supported sections play complementary roles in bolted connections and make important contributions to the load bearing and transfer of the structure. The correct design and analysis of these two sections is essential to ensure the stability and durability of the structure."
    )

class SteelBoltConnectionForce(MBaseModel):
    """
    Steel Bolt Connection Force
    """
    percent: float = Field(default=30.0, title="Strength design(%)", description="Generally section of steel beam is determined by bending moment, typically shear is set 30% as default because there is no problem even if shear is assumed to about 30 % of member strength. If it is required to consider 100% of member strength, change the entered value.")

    model_config = ConfigDict(
        title="Steel Bolt Connection Force",
        description="Steel Bolt Connection Force"
    )

class SteelBolt(MBaseModel):
    """
    Steel Bolt
    """
    name: str = Field(default='M16', title="bolt name", description="bolt size", enum=enum_to_list(enBoltName))
    matl: BoltMaterial = Field(default_factory=BoltMaterial, title="bolt material", description="Material of bolt")

    model_config = ConfigDict(
        title="Steel Bolt",
        description="Steel Bolt"
    )

class AnchorBolt(MBaseModel):
    """
    Anchor Bolt
    """
    type: str = Field(default=enAnchorType.CIP, title="Anchor bolt install type", description="Anchor bolt install type", enum=enum_to_list(enAnchorType))
    steelbolt: SteelBolt = Field(default_factory=SteelBolt, title="Steel Bolt", description="Steel Bolt")
    length: float = Field(default=25.0, title="Length", description="Length of anchor bolt(Length x Diameter)")
    pos_x: Length = Field(default_factory=Length, title="Position X", description="Position X")
    pos_y: Length = Field(default_factory=Length, title="Position Y", description="Position Y")
    num_x: int = Field(default=2, title="Number X", description="Number X")
    num_y: int = Field(default=2, title="Number Y", description="Number Y")

    model_config = ConfigDict(
        title="Anchor Bolt",
        description="Anchor bolts are used to secure structures to concrete foundations. They are designed to withstand the forces and loads that are applied to the structure, providing stability and support. Anchor bolts are available in various sizes and materials to suit different applications and requirements."
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(steelbolt=SteelBolt(name='M16', matl=BoltMaterial.create_default(name=enBoltMaterialASTM.A193_B7, enum_list=enum_to_list(enBoltMaterialASTM))),
                       pos_x=Length(value=1.5, unit=enUnitLength.IN),
                       pos_y=Length(value=1.5, unit=enUnitLength.IN))
        else:
            return cls(steelbolt=SteelBolt(name='M16', matl=BoltMaterial.create_default(name=enBoltMaterialASTM.A193_B7, enum_list=enum_to_list(enBoltMaterialASTM))),
                       pos_x=Length(value=50, unit=enUnitLength.MM),
                       pos_y=Length(value=50, unit=enUnitLength.MM))

class SteelBolt_EC(MBaseModel):
    """
    Steel Bolt
    """
    name: str = Field(default='M20', title="Bolt name", description="Bolt size", enum=enum_to_list(enBoltName))
    matl: BoltMaterial_EC = Field(default=BoltMaterial_EC(), title="Bolt material", description="Material of bolt")

    model_config = ConfigDict(
        title="Steel Bolt",
        description="""A bolt is a mechanical element that connects members of a structure and is used to transfer loads.\n
            Diameter: The outer diameter of a bolt, usually expressed in a metric system such as M6, M8, M10, etc.\n
            Length: The overall length of the bolt, determined by the thickness of the connecting members.\n
            Class: The strength rating, expressed as a class, for example 8.8, 10.9, etc., where higher numbers increase strength.
            """
    )

class ShearConnector(MBaseModel):
    """
    ShearConnector
    """
    bolt: SteelBolt = Field(default_factory=SteelBolt, description="stud bolt")
    num: int = Field(default=1, description="stud column")
    space: Length = Field(default_factory=lambda: Length(value=300.0, unit=enUnitLength.MM), description="stud spacing")
    length: Length = Field(default_factory=lambda: Length(value=100.0, unit=enUnitLength.MM), description="stud length")

    model_config = ConfigDict(
        title="Shear Connector",
        description="Shear Connector"
    )

class ShearConnector_EC(MBaseModel):
    """
    ShearConnector
    """
    bolt: SteelBolt_EC = Field(default=SteelBolt_EC(name="M19"), title="Bolt specifications", description="Stud bolt")
    num: int = Field(default=1, title="Number", description="Stud column")
    space: Length = Field(default=Length(value=300.0, unit=enUnitLength.MM), title="Stud Spacing", description="Stud spacing")
    length: Length = Field(default=Length(value=100.0, unit=enUnitLength.MM), title="Stud Length", description="Stud length")

    model_config = ConfigDict(
        title="Shear Connector",
        description="Shear connections play an important role in ensuring the strength and stability of a structure, and they come in a variety of shapes and materials to meet different structural requirements. When used properly and in accordance with design criteria, shear connections can contribute to the safety and durability of a structure."
    )

class Welding(MBaseModel):
    """
    Welding
    """
    matl: SteelMaterial = Field(default_factory=SteelMaterial, description="Material")
    length: Length = Field(default_factory=Length, description="Leg of Length")

    model_config = ConfigDict(
        title="Welding",
        description="Welding"
    )

class Welding_EC(Welding):
    """
    Welding
    """
    matl: SteelMaterial_EC = Field(default=SteelMaterial_EC(), description="Material")
    length: Length = Field(default=Length(value=6.0, unit=enUnitLength.MM), description="Leg of Length")

    model_config = ConfigDict(
        title="Welding",
        description="Information for reviewing welds on supporting members."
    )

class SteelPlateMember(MBaseModel):
    """
    Steel Plate Member
    """
    matl: SteelMaterial = Field(default_factory=SteelMaterial, title="Plate material", description="Material")
    bolt_num: int = Field(default=4, title="Number of bolt", description="Number of Bolts")
    thk: Length = Field(default_factory=Length, title="Thickness", description="Thickness")

    model_config = ConfigDict(
        title="Steel Plate Member",
        description="Steel Plate Member"
    )

class SteelPlateMember_EC(SteelPlateMember):
    """
    Steel Plate Member
    """
    matl: SteelMaterial_EC = Field(default=SteelMaterial_EC(), title="Plate material", description="Material")
    bolt_num: int = Field(default=4, title="Number of bolt", description="Number of Bolts")
    thk: Length = Field(default=Length(value=6.0, unit=enUnitLength.MM), title="Thickness", description="Thickness of plate")

    model_config = ConfigDict(
        title="Steel Plate Member",
        description="Steel Plate Member"
    )

class ConnectType(MBaseModel):
    """
    Connect Type class

    Args:
        type (str): Connection type
    """
    type: str = Field(default="Fin Plate - Beam to Beam", title="Connect type", description="Connect type", enum=enum_to_list(enConnectionType))

    model_config = ConfigDict(
        title="Connection Type",
        description="""
            The four types of bolted connections mentioned are described below:
            \n
            1. Fin Plate - Beam to Beam (Fin_B_B) \n
            This is the use of a fin plate to connect two beams, where a fin plate is attached to the end of each beam to connect them together.
            \n\n
            2. Fin Plate - Beam to Column (Fin_B_C)\n
            A method of connecting beams to columns, where fin plates are attached to the sides of the columns and the ends of the beams to create a solid connection.
            \n\n
            3. End Plate - Beam to Beam (End_B_B)\n
            A method of connecting two beams using end plates at the ends. An end plate is attached to the end of each beam and connected via bolts.
            \n\n
            4. End Plate - Beam to Column (End_B_C)\n
            This method of connecting beams to columns uses end plates attached to the sides of the columns to connect with the ends of the beams. Bolts are secured to the column through the end plate.
            """
    )

class BasePlate(MBaseModel):
    """
    Base Plate
    """
    matl: SteelMaterial = Field(default_factory=SteelMaterial, description="Material")
    thk: Length = Field(default_factory=Length, description="Thickness")
    width: Length = Field(default_factory=Length, description="Width")
    height: Length = Field(default_factory=Length, description="Height")

    model_config = ConfigDict(
        title="Base Plate",
        description="Base Plate"
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(matl=SteelMaterial.create_default(code="ASTM", enum_list=enum_to_list(enSteelMaterial_ASTM)),
                       thk=Length(value=1, unit=enUnitLength.IN),
                       width=Length(value=18, unit=enUnitLength.IN),
                       height=Length(value=18, unit=enUnitLength.IN))
        else:
            return cls(matl=SteelMaterial.create_default(code="ASTM", enum_list=enum_to_list(enSteelMaterial_ASTM)),
                       thk=Length(value=6, unit=enUnitLength.MM),
                       width=Length(value=390, unit=enUnitLength.MM),
                       height=Length(value=400, unit=enUnitLength.MM))