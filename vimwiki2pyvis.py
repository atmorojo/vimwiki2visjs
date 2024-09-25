import re
import pathlib

from pyvis.network import Network


path = pathlib.Path.home() / "vimwiki"
index = path / "index.md"
link_pat = r"\[[^]]*\]\(([^#][^)]*)\)"  # use "\[\[(.*)\]\]" in .wiki files
net = Network()
net.barnes_hut()


def links_in_file(fpath):
    d = {fpath: []}
    with open(fpath, "r", encoding="utf8") as f:
        fdata = [line.strip() for line in f.readlines()]
    links = list()
    for line in fdata:
        for link in re.findall(link_pat, line):
            linked = (path/link).with_suffix(".md")
            if linked.exists():
                links.append(links_in_file(linked))
    d[fpath] = links
    return d


def graph(directory_dict):
    for file, linked_files in directory_dict.items():
        net.add_node(file.name)
        for linked_file in linked_files:
            for node, _ in linked_file.items():
                net.add_node(node.name)
                net.add_edge(file.name, node.name)
            graph(linked_file)


links = links_in_file(index)
graph(links)
net.show("index.html", notebook=False)
