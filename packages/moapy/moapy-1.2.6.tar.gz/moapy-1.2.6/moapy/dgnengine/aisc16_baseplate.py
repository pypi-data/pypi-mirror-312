import ctypes
import json
import base64
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_post import ResultBytes
from moapy.data_pre import SectionForce, Stress, Force, Moment, Length
from moapy.steel_pre import AnchorBolt, BasePlate, SteelMaterial, SteelSection, SteelConnectMember_EC, SteelPlateMember_EC, ConnectType, SteelBolt_EC, Welding_EC, SteelMember_EC, SteelSection_EN10365, SteelMaterial_EC, BoltMaterial_EC, SteelBolt, BoltMaterial
from moapy.enum_pre import enum_to_list, en_H_AISC10_US, enSteelMaterial_ASTM, enBoltMaterialASTM, enUnitStress, enUnitForce, enUnitMoment, enUnitSystem, enUnitLength
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary

@auto_schema(
    title="AISC-LRFD16 Base Plate Design",
    description=(
        """
        The AISC-LRFD16 standard outlines the requirements for designing base plates that connect steel columns to foundations, emphasizing both safety and efficiency. Key considerations include:

        Verification of Bearing and Shear Capacities: The design evaluates the bearing strength of the base plate based on its material, thickness, and contact with the concrete foundation, ensuring the load transfer is safe under applied forces.
        Design for Axial, Shear, and Bending Forces: Resistance calculations for vertical, horizontal, and bending moments help maintain the structural integrity of the connection under varying load conditions.
        Bolt Group Effects and Anchor Design: The effects of bolt arrangements are analyzed to ensure that they can resist forces without excessive deformation or failure, while considering edge distances and concrete breakout strength as per ACI 318 provisions.
        Ductility and Stability Considerations: Flexibility is incorporated into the design to accommodate minor misalignments and differential movements, while ensuring stability under compression and tension forces.
        Concrete Bearing and Punching Checks: Additional verification ensures that the foundation can resist concentrated loads without experiencing punching failure or excessive cracking.
        The AISC approach integrates these factors into a unified design methodology, providing engineers with reliable tools and recommendations for designing safe and effective base plate connections.
        """)
)
def report_aisc16_baseplate(fck: Stress = Stress(value=3.0, unit=enUnitStress.ksi), baseplate: BasePlate = BasePlate.create_default(unit_system=enUnitSystem.US), sect: SteelSection = SteelSection.create_default(name="HP18X181", enum_list=enum_to_list(en_H_AISC10_US)),
                            force: SectionForce = SectionForce.create_default(unit_system=enUnitSystem.US), anchor: AnchorBolt = AnchorBolt.create_default(unit_system=enUnitSystem.US)) -> ResultBytes:
    dll = load_dll()
    json_data_list = [sect.json(), sect.json(), force.json(), baseplate.json(), anchor.json()]
    file_path = call_func(dll, 'Report_AISC16_BasePlate', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_aisc16_baseplate(fck: Stress = Stress(value=3.0, unit=enUnitStress.ksi), baseplate: BasePlate = BasePlate.create_default(unit_system=enUnitSystem.US), sect: SteelSection = SteelSection.create_default(name="HP18X181", enum_list=enum_to_list(en_H_AISC10_US)),
                          force: SectionForce = SectionForce.create_default(unit_system=enUnitSystem.US), anchor: AnchorBolt = AnchorBolt.create_default(unit_system=enUnitSystem.US)) -> dict:
    dll = load_dll()
    json_data_list = [fck.json(), sect.json(), force.json(), baseplate.json(), anchor.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_AISC16_BasePlate', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


# if __name__ == "__main__":
    # res = report_aisc16_baseplate(InputAISC16BasePlate())
    # print(res)