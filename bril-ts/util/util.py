from lib import Block

TERMINATORS = {"jmp", "br", "ret"}


def split_in_blocks(input):
    """
    Splits the input set of instructions into blocks
    :param input: The set of instructions
    :return: A list of blocks
    """
    blocks = []
    current_block = []

    for instr in input['instrs']:
        if 'op' in instr:
            current_block.append(instr)
            if instr['op'] in TERMINATORS:
                blocks.append(Block(current_block))
                current_block = []
        else:
            if current_block:
                blocks.append(Block(current_block))
            current_block = [instr]

    if current_block:
        blocks.append(Block(current_block))

    return blocks


def add_terminators(blocks):
    """
    Adds terminators to the input blocks, in case there is no strict connection between
    two blocks, or, and ending instruction (e.g. `ret`urtn)
    :param blocks:
    :return:
    """
    n_blocks = len(blocks)

    for idx, block in enumerate(blocks):
        instructions = block.get_instr_list()
        if idx == n_blocks - 1:
            if 'op' not in instructions[-1] or instructions[-1]['op'] not in TERMINATORS:
                block.add_instr({'op': 'ret', 'args': []})
        else:
            if 'op' not in instructions[-1] or instructions[-1]['op'] not in TERMINATORS:
                next_block = blocks[idx + 1]
                block.add_instr({'op': 'jmp', 'labels': [next_block.get_block_name()]})

    return blocks