import json
import sys

from util import split_in_blocks, add_terminators

trace_file_name = sys.argv[1]
program_file_name = sys.argv[2]

program = json.load(open(program_file_name))
trace = dict(json.load(open(trace_file_name)))


def inline_function(func, caller):
    """
    Given an input function and its caller, generates the
    inline code of this function to inject it to the caller.
    :param func: The input function
    :param caller: The calling function
    :return: The inline code
    """
    args = func["args"]
    instructions = func["instrs"]

    inline_instructions = []

    # Rename the arguments of the function.
    # For example, let's assume the following y definition: y(x) = x + 1
    # If f calls y like i = 5; res = y(x), then the inline code of y inside x should look like
    # i + 1 (instead of x + 1), that is, x should renamed to i.
    for idx, arg in enumerate(args):
        new_ins = {"dest": arg["name"], "op": "id", "args": [caller["args"][idx]]}
        inline_instructions.append(new_ins)

    for instr in instructions:
        if "op" in instr and instr["op"] == "ret":
            # Assign the returning value to caller's dest variable
            dest = {"dest": caller["dest"], "op": "id", "args": [instr["args"][0]]}
            inline_instructions.append(dest)
        else:
            inline_instructions.append(instr)

    return inline_instructions


functions = dict([(f["name"], f) for f in  program["functions"]])

for func_name in functions:
    func = functions[func_name]

    if func_name in trace:
        blocks = split_in_blocks(func)
        blocks = add_terminators(blocks)
        blocks = dict([(b.get_block_name(), b) for b in blocks])

        new_instrs = []

        for instr in func["instrs"]:
            if "label" in instr:
                pass
            elif "op" in instr and instr["op"] == "br":
                labels = instr["labels"]

                left_label_block = blocks[labels[0]]
                left_instrs = left_label_block.get_instr_list()

                new_instrs.append({"op": "speculate"})
                #new_instrs.append({"op": "print", "args": ["one"]})

                # Inject the instructions in speculate mode
                for i in left_instrs:
                    if 'label' in i:
                        pass
                    elif 'labels' in i:
                        pass
                    elif 'op' in i and  i['op'] == "call":
                        # Do the inlining stuff here
                        invocation_name = i["funcs"][0]
                        for inline in inline_function(functions[invocation_name], i):
                            new_instrs.append(inline)
                    else:
                        new_instrs.append(i)

                # Add the guard
                guard_args = instr["args"]

                new_instrs.append({"op": "guard", "args": guard_args, "labels": ["deoptimize"]})
                new_instrs.append({"op": "commit"})
                new_instrs.append({"label": "deoptimize"})

            new_instrs.append(instr)

        func["instrs"] = new_instrs

print(json.dumps(program, indent=2))

