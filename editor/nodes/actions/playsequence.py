from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicMaterialNode
from ...sockets import NodeSocketLogicPlayMode
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatPositive
import bpy


@node_type
class LogicNodePlaySequence(LogicNodeActionType):
    bl_idname = "NLPlayMaterialSequence"
    bl_label = "Play Sequence"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULPaySequence"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicMaterial, 'Material')
        self.add_input(NodeSocketLogicMaterialNode, 'Node Name', {'ref_index': 1})
        self.add_input(NodeSocketLogicPlayMode, "Mode", {'enabled': False})
        self.add_input(NodeSocketLogicBoolean, 'Continue', {'enabled': False})
        self.add_input(NodeSocketLogicVectorXY, "Frames", {'enabled': False})
        self.add_input(NodeSocketLogicFloatPositive, "FPS", {'enabled': False, 'value': 60})
        self.add_output(NodeSocketLogicCondition, "On Start")
        self.add_output(NodeSocketLogicCondition, "Running")
        self.add_output(NodeSocketLogicCondition, "On Finish")
        self.add_output(NodeSocketLogicParameter, "Current Frame")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        mat = self.inputs[1].value
        if mat:
            nde = self.inputs[2].value
            target = mat.node_tree.nodes.get(nde)
            if not isinstance(target, bpy.types.ShaderNodeTexImage):
                col = layout.column()
                col.label(text='Selected Node', icon='ERROR')
                col.label(text='not Image Texture!')

    def update_draw(self, context=None):
        if not self.ready:
            return
        mat = self.inputs[1]
        nde = self.inputs[2]
        mod = self.inputs[3]
        fra = self.inputs[5]
        fps = self.inputs[6]
        subs = [mod, fra, fps]
        target = mat.value.node_tree.nodes.get(nde.value) if mat.value else None
        valid = isinstance(target, bpy.types.ShaderNodeTexImage)
        self.inputs[4].enabled = '3' in mod.value
        if (mat.value or mat.is_linked) and (nde.value or nde.is_linked) and valid:
            for ipt in subs:
                ipt.enabled = True
        else:
            for ipt in subs:
                ipt.enabled = False

    def get_input_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            'play_mode',
            'play_continue',
            "frames",
            'fps'
        ]

    def get_output_names(self):
        return ['ON_START', 'RUNNING', 'ON_FINISH', 'FRAME']
