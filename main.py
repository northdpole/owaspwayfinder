from pprint import pprint

import graphviz as gz
import yaml


def cluster(root_graph:gz.Digraph,name:str,label:str, nodes):
    result = gz.Digraph(name=name)
    result.attr(label=label)
    result.attr(color='blue')
    for name,attrs in nodes.items():
        prev_index = list(nodes.keys()).index(name) -1
        prev_node = list(nodes.keys())[prev_index]
        result.node(name)
        result.edge(f"{prev_node}:{nodes[prev_node]['port_next']}", f"{name}:{attrs['port_previous']}")
        prev_group=name
        for group,elements in steps[name].items():
            group_subgraph_name=f"cluster-{name}-{group}"
            group_subgraph = gz.Digraph(name=group_subgraph_name)
            group_subgraph.attr(rankdir="TB")
            group_subgraph.attr(label=group)
            group_subgraph.attr(color='blue')
            for project in elements:
                group_subgraph.node(project['name'],
                                    href=project['href'],
                                    _attributes={"shape":"plaintext"})
                result.edge(prev_group,
                            group_subgraph_name,
                            label=group,
                            _attributes={"lhead":name,"ltail":group_subgraph_name})                
            prev_group=group_subgraph_name
                
            root_graph.subgraph(group_subgraph)
            # result.edge(default_nodes[i],project['name'],_attributes={"lhead":group})
    root_graph.subgraph(result)
    return root_graph

default_nodes={"Requirements":{"port_previous":"e","port_next":"w","port_external":"nw"},
               "Design":{"port_previous":"s","port_next":"n","port_external":"nw"},
               "Implementation":{"port_previous":"s","port_next":"n","port_external":"nw"},
               "Verification":{"port_previous":"s","port_next":"n","port_external":"nw"},
               "Policy Gap Evaluation":{"port_previous":"s","port_next":"e","port_external":"nw"},
               "Metrics":{"port_previous":"w","port_next":"s","port_external":"nw"},
               "Training/Education":{"port_previous":"n","port_next":"s","port_external":"nw"},
               "Culture Building and Process Maturing":{"port_previous":"n","port_next":"s","port_external":"nw"},
               "Operation":{"port_previous":"n","port_next":"w","port_external":"nw"}}
dot = gz.Digraph(filename="/tmp/wayfinder.dot",strict=True)
dot.attr(label="Application Security Wayfinder")
dot.attr(overlap='false')
# dot.attr(splines='true')
dot.attr(layout="fdp") #circo
dot.attr(color='blue')

# load data
with open("projects.yaml") as projs:
    data = yaml.safe_load(projs)['projects']

steps = dict([(key,{})for key in default_nodes])
stps = {}
# group by step
for dat in data:
    for s in dat["step"]:
        if dat["group"] not in steps[s]:
            steps[s][dat["group"]] = []
        steps[s][dat["group"]].append(dat)


dot = cluster(root_graph=dot,name="cluster-devops",label="The DEVOPs cycle",nodes=default_nodes)
# print(dot)
dot.render("/tmp/wayfinder.svg",view=True)
