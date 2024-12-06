__all__ = ["dump_to_yaml", "pss_dedent"]
from textwrap import dedent

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString
from ruamel.yaml.comments import CommentedSeq


def pss_dedent(x: str) -> PreservedScalarString:
    return PreservedScalarString(dedent(x))


fgi = YAML(typ=["rt", "string"])
fgi.indent(sequence=4, offset=2)
fgi.preserve_quotes = True
fgi.width = 4096
fgi.Emitter.flow_seq_start = "[ "  # defaults to '['
fgi.Emitter.flow_seq_end = " ]"  # defaults to ']'
fgi.Emitter.flow_seq_separator = " ,"


def dump_to_yaml(data: dict) -> str:
    def seq(*_):
        s = CommentedSeq(*_)
        s.fa.set_flow_style()
        return s

    data["brief-description"] = pss_dedent(data["brief-description"])
    data["description"] = pss_dedent(data["description"])
    for i in data["authors"]:
        i["role"] = seq(i["role"])
    temp = fgi.dump_to_string(data)  # type: ignore
    for i in list(data.keys())[1:]:
        temp = temp.replace("\n" + i, "\n\n" + i)
    temp = temp.replace("description: |-", "description: |")
    return temp
