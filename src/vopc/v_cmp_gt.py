from base_instruction import BaseInstruction
from decompiler_data import DecompilerData
from integrity import Integrity
from register import Register
from type_of_reg import Type


class VCmpGt(BaseInstruction):
    def execute(self, node, instruction, flag_of_status, suffix):
        decompiler_data = DecompilerData.Instance()
        output_string = ""
        if suffix == "u64":
            sdst = instruction[1]
            src0 = instruction[2]
            src1 = instruction[3]
            decompiler_data.output_file.write(sdst + " = (ulong)" + src0 + " > (uint)" + src1 + "\n")

        elif suffix == "i32":
            sdst = instruction[1]
            src0 = instruction[2]
            src1 = instruction[3]
            if flag_of_status:
                new_val, src0_flag, src1_flag = decompiler_data.make_op(node, src0, src1, " > ")
                node.state.registers[sdst] = Register(new_val, Type.unknown, Integrity.integer)
                node.state.make_version(decompiler_data.versions, sdst)
                if sdst in [src0, src1]:
                    node.state.registers[sdst].make_prev()
                node.state.registers[sdst].type_of_data = suffix
                return node
            return output_string
