from src.base_instruction import BaseInstruction
from src.decompiler_data import DecompilerData
from src.operation_status import OperationStatus


class SCbranchScc1(BaseInstruction):
    def execute(self, node, instruction, flag_of_status, suffix):
        decompiler_data = DecompilerData()
        reladdr = instruction[1]
        if flag_of_status == OperationStatus.to_fill_node:
            if decompiler_data.to_node.get(reladdr) is not None:
                node.add_child(decompiler_data.to_node[reladdr])
                decompiler_data.to_node[reladdr].add_parent(node)
            else:
                if decompiler_data.from_node.get(reladdr) is None:
                    decompiler_data.from_node[reladdr] = [node]
                else:
                    decompiler_data.from_node[reladdr].append(node)
            return node
        output_string = node.state.registers["scc"].val
        return output_string
        # decompiler_data.output_file.write("pc = scc1 == 0 ? " + reladdr + " : pc + 4\n")
