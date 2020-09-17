from base_instruction import BaseInstruction
from decompiler_data import DecompilerData
from integrity import Integrity
from register import Register
from type_of_reg import Type


class SLshl(BaseInstruction):
    def execute(self, node, instruction, flag_of_status, suffix):
        decompiler_data = DecompilerData.Instance()
        output_string = ""
        if suffix == 'b32':
            sdst = instruction[1]
            ssrc0 = instruction[2]
            ssrc1 = instruction[3]
            if flag_of_status:
                new_val, ssrc0_flag, ssrc1_flag = decompiler_data.make_op(node, ssrc0, str(pow(2, int(ssrc1))), " * ")
                if node.state.registers[ssrc0].type == Type.work_group_id_x:
                    node.state.registers[sdst] = Register(new_val, Type.work_group_id_x_local_size, Integrity.integer)
                    node.state.registers["scc"] = Register(sdst + "!= 0", Type.int32, Integrity.integer)
                elif node.state.registers[ssrc0].type == Type.work_group_id_y:
                    node.state.registers[sdst] = Register(new_val, Type.work_group_id_y_local_size, Integrity.integer)
                    node.state.registers["scc"] = Register(sdst + "!= 0", Type.int32, Integrity.integer)
                elif node.state.registers[ssrc0].type == Type.work_group_id_z:
                    node.state.registers[sdst] = Register(new_val, Type.work_group_id_z_local_size, Integrity.integer)
                    node.state.registers["scc"] = Register(sdst + "!= 0", Type.int32, Integrity.integer)
                else:
                    node.state.registers[sdst] = Register(new_val, node.state.registers[ssrc0].type, Integrity.integer)
                node.state.make_version(decompiler_data.versions, sdst)
                node.state.registers[sdst].type_of_data = suffix
                node.state.make_version(decompiler_data.versions, "scc")
                node.state.registers["scc"].type_of_data = suffix
                if sdst in [ssrc0, ssrc1]:
                    node.state.registers[sdst].make_prev()
                return node
            return output_string
        if suffix == 'b64':
            sdst = instruction[1]
            ssrc0 = instruction[2]
            ssrc1 = instruction[3]
            if flag_of_status:
                first_to, last_to, num_of_registers, from_registers, to_registers, name_of_register, name_of_from, first_from \
                    = node.state.find_first_last_num_to_from(sdst, ssrc0)
                from_registers1 = name_of_from + str(first_from + 1)
                to_registers1 = name_of_register + str(first_to + 1)
                new_val0, ssrc0_flag0, ssrc1_flag0 = decompiler_data.make_op(node, from_registers, str(pow(2, int(ssrc1))), " * ")
                new_val1, ssrc0_flag1, ssrc1_flag1 = decompiler_data.make_op(node, from_registers1, str(pow(2, int(ssrc1))), " * ")
                node.state.registers[to_registers] = \
                    Register(new_val0, node.state.registers[from_registers].type, Integrity.low_part)
                node.state.registers[to_registers1] = \
                    Register(new_val1, node.state.registers[from_registers1].type, Integrity.high_part)
                node.state.make_version(decompiler_data.versions, to_registers)
                node.state.registers[to_registers].type_of_data = suffix
                if to_registers in [from_registers, ssrc1]:
                    node.state.registers[to_registers].make_prev()
                node.state.make_version(decompiler_data.versions, to_registers1)
                node.state.registers[to_registers1].type_of_data = suffix
                if to_registers1 in [from_registers1, ssrc1]:
                    node.state.registers[to_registers1].make_prev()
                return node
            return output_string
