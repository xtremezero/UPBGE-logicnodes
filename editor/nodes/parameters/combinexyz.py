from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeCombineXYZ(LogicNodeParameterType):
    bl_idname = "NLParameterVector3SimpleNode"
    bl_label = "Combine XYZ"
    nl_module = 'uplogic.nodes.parameters'

    search_tags = [
        ['Combine XYZ', {}],
        ['Vector XYZ', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, 'X')
        self.add_input(NodeSocketLogicFloat, 'Y')
        self.add_input(NodeSocketLogicFloat, 'Z')
        self.add_output(NodeSocketLogicVectorXYZ, "Vector")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULVectorXYZ"

    def get_output_names(self):
        return ["OUTV"]

    def get_input_names(self):
        return ["input_x", "input_y", "input_z"]
