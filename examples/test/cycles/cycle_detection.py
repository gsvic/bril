import json


def init_graph(input_json):
    """
    Initializes the function call graph.

    :return: The graph metadata in JSON format.
    """
    meta = json.loads(input_json)
    graph_info = dict()

    for f in meta["functions"]:
        f_name = f["name"]

        if f_name not in graph_info:
            graph_info[f_name] = list()

        # Search for function invocations
        for instruction in f["instrs"]:
            if instruction["op"] == "call":
                for func in instruction["funcs"]:
                    graph_info[f_name].append(func)

    return graph_info


def detect_method_cycles(graph_info):
    """
    Detects cycles in the invocation call graph.

    :param graph_info: The graph information dict
    :return: None
    """
    detected_cycles = list()

    for func in graph_info.items():
        name = func[0]
        cycle_found = check_node(graph_info, func, set())

        if cycle_found:
            detected_cycles.append(cycle_found)
            # print("Cycle found! [{}]".format(cycle))
        else:
            pass
            # print("Method {}: Ok.".format(name))

    return detected_cycles


def check_node(graph_info, node, seen):
    """
    Checks for a cycle given a source node from the invocation call graph.

    :param graph_info: The graph information dict
    :param node: The input node (contains the function name and its neighbors
    :param seen: A set, containing the nodes (functions) that are already visited
    :return: The function name in case a cycle is detected, None otherwise.
    """
    name = node[0]
    neighbors = node[1]

    seen.add(name)

    for neighbor in neighbors:
        if neighbor in seen:
            return name + " -> " + neighbor
        else:
            check = check_node(graph_info, (neighbor, graph_info[neighbor]), seen.copy())
            if check:
                return name + " -> " + check

    return None


if __name__ == "__main__":
    import fileinput

    input_json = ""
    for line in fileinput.input():
        input_json += line

    graph_info = init_graph(input_json)
    cycles = detect_method_cycles(graph_info)

    if cycles:
        for cycle in cycles:
            print(cycle)
    else:
        print("-")
