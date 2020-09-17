from base_instruction import BaseInstruction
from decompiler_data import DecompilerData
from integrity import Integrity
from register import Register
from type_of_reg import Type


class SAdd(BaseInstruction):
    def execute(self, node, instruction, flag_of_status, suffix):
        decompiler_data = DecompilerData.Instance()
        output_string = ""
        if suffix == 'u32':
            sdst = instruction[1]
            ssrc0 = instruction[2]
            ssrc1 = instruction[3]
            new_val, ssrc0_reg, ssrc1_reg = decompiler_data.make_op(node, ssrc0, ssrc1, " + ")
            if flag_of_status:
                if ssrc0_reg and ssrc1_reg:
                    if node.state.registers[ssrc0].type == Type.work_group_id_x_local_size \
                            and node.state.registers[ssrc1].type == Type.global_offset_x:
                        node.state.registers[sdst] = \
                            Register(new_val, Type.work_group_id_x_local_size_offset, Integrity.integer)
                    elif node.state.registers[ssrc0].type == Type.work_group_id_y_local_size \
                            and node.state.registers[ssrc1].type == Type.global_offset_y:
                        node.state.registers[sdst] = \
                            Register(new_val, Type.work_group_id_y_local_size_offset, Integrity.integer)
                    elif node.state.registers[ssrc0].type == Type.work_group_id_z_local_size \
                            and node.state.registers[ssrc1].type == Type.global_offset_z:
                        node.state.registers[sdst] = \
                            Register(new_val, Type.work_group_id_z_local_size_offset, Integrity.integer)
                    elif node.state.registers[ssrc0].type == Type.param or node.state.registers[ssrc1].type == Type.param:
                        node.state.registers[sdst] = \
                            Register(new_val, Type.param, Integrity.integer)
                    else:
                        node.state.registers[sdst] = \
                            Register(new_val, Type.unknown, Integrity.integer)
                else:
                    type_reg = Type.int32
                    if ssrc0_reg:
                        type_reg = node.state.registers[ssrc0].type
                    if ssrc1_reg:
                        type_reg = node.state.registers[ssrc1].type
                    node.state.registers[sdst] = \
                        Register(new_val, type_reg, Integrity.integer)
                node.state.make_version(decompiler_data.versions, sdst)
                if sdst in [ssrc0, ssrc1]:
                    node.state.registers[sdst].make_prev()
                node.state.registers[sdst].type_of_data = suffix
                return node
            return output_string
