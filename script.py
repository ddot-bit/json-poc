from jsonpath_ng.ext import parse
from jsonpath_ng import DatumInContext
from jsonpath_ng.jsonpath import Fields, Slice, Child
import json_merge_patch
from functools import reduce


def transform_path(dot_path: str) -> str:
    """Transforms json dot notation to jsonpatch notation"""
    # strs, replacements = dot_path, {".": "/", "[": "", "]": ""}
    # print("New Path", "/".join([replacements.get(c, c) for c in strs]))
    # new_path = "/" + dot_path.replace(".", "/").replace("[", "").replace("]", "")
    new_path = dot_path.split(".")
    print("New Path", new_path)
    return new_path


def create_new_doc(path: str, value, document: dict = None) -> dict:
    if not document:
        document = {}
    expr = parse(path)
    # Not in documentation
    expr.update_or_create(document, value)
    print("New Document:", document)
    return document if len(document) > 0 else None


if __name__ == "__main__":
    data = {
        "complex": [
            {"name": "Name1", "value": None},
            {"name": "Name2", "value": "value2"},
        ],
        "apples": [{}, {"orange": {"54189": {"tt": "lender"}}}],
    }
    mapping_doc = [
        "$.complex[?(@.name == Name1)].value",
        "$.complex[?(@.name==Name2)].value",
        # lib throw errors if the key starts with a number when using parse()
        # lib does not throw an error when defining the path using Fields(), Slice() and child()
        # Fields("apples")
        # .child(Slice())
        # .child(Fields("orange"))
        # .child(Fields("54189"))
        # .child(Fields("tt")),
        "$.apples.[*].orange.54189.tt",
        "not.a.valid.path[9]",
    ]
    # json_expr = parse(mapping_doc[0])
    # print(json_expr.filter(data))
    # doc = None
    json_doc = None
    for query in mapping_doc:
        print(isinstance(query, Child))
        jsonpath_expr = query if isinstance(query, Child) else parse(query)
        try:
            path_obj: DatumInContext = jsonpath_expr.find(data)[0]
            print("##### Path object", path_obj)
            path = str(path_obj.full_path)
            value = path_obj.value
            print(f"##### value: {value} path: {path}")
            json_doc = create_new_doc(path, value, json_doc)
            if not json_doc:
                print("could not create object. Continue processing")
                continue
            # json_doc.append(doc)
        except IndexError:
            # Not required since parse.find() returns []
            path_obj: str = "SPECIAL TOKEN"
            print(f"Path does not exist. VALUE: {path_obj}")

print("##### Json doc", json_doc)
# merged_doc = reduce(json_merge_patch.merge, json_doc)
# print("##### Merged doc", merged_doc)
