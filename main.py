from pprint import pprint

import graphviz as gz
import yaml


def cluster(root_graph:gz.Digraph,name:str,label:str, nodes,rfrom,rto):
    result = gz.Digraph(name=name)
    result.attr(label=label)
    result.attr(color='blue')
    for i in range(rfrom,rto):
        result.node(nodes[i])
        result.edge(nodes[i-1],nodes[i])
        prev_group=nodes[i]
        for group,elements in steps[nodes[i]].items():
            group_subgraph_name=f"cluster-{nodes[i]}-{group}"
            group_subgraph = gz.Digraph(name=group_subgraph_name)
            group_subgraph.attr(rankdir="TB")
            group_subgraph.attr(label=group)
            group_subgraph.attr(color='blue')
            for project in elements:
                group_subgraph.node(project['name'],href=project['href'],_attributes={"shape":"plaintext"})
                result.edge(prev_group,group_subgraph_name,label=group,
                            _attributes={"lhead":nodes[i],"ltail":group_subgraph_name})                
            prev_group=group_subgraph_name
                
            root_graph.subgraph(group_subgraph)
            # result.edge(default_nodes[i],project['name'],_attributes={"lhead":group})
    root_graph.subgraph(result)
    return root_graph

default_nodes=["Requirements",
               "Design",
               "Implementation",
               "Verification",
               "Policy Gap Evaluation",
               "Metrics",
               "Training/Education",
               "Culture Building and Process Maturing",
               "Operation"]
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


dot = cluster(root_graph=dot,name="cluster-devops",label="The DEVOPs cycle",nodes=default_nodes,rfrom=0,rto=int(len(default_nodes)))
# print(dot)
dot.render("/tmp/wayfinder.svg",view=True)
