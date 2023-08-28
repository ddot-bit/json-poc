import jmespath
from jmespath import functions
from typing import Dict, NewType, Any


# 1. Create a subclass of functions.Functions.
#    The function.Functions base class has logic
#    that introspects all of its methods and automatically
#    registers your custom functions in its function table.
class CustomFunctions(functions.Functions):
    # 2 and 3.  Create a function that starts with _func_
    # and decorate it with @signature which indicates its
    # expected types.
    # In this example, we're creating a jmespath function
    # called "unique_letters" that accepts a single argument
    # with an expected type "string".
    @functions.signature({"types": ["string"]})
    def _func_unique_letters(self, s):
        # Given a string s, return a sorted
        # string of unique letters: 'ccbbadd' ->  'abcd'
        return "".join(sorted(set(s)))

    # Here's another example.  This is creating
    # a jmespath function called "my_add" that expects
    # two arguments, both of which should be of type number.
    @functions.signature(
        {"types": ["string"]},
        {"types": ["object", "number", "string", "boolean", "array", "null"]},
    )
    def _func_full_path(self, path, data):
        path_parts = path.split(".")
        return x + y

    @functions.signature(
        {"types": ["string"]},
        {"types": ["object", "number", "string", "boolean", "array", "null"]},
    )
    def _func_key_does_not_exist(path, data):
        parent, child = path.split(".")[:-2]
        return jmespath.search(f"contains(keys({parent}), {child})")

    KeyType = NewType("KeyType", Any)

    @staticmethod
    def deep_traversal(
        path_parts: list[str], mapping: Dict[KeyType, Any]
    ) -> Dict[KeyType, Any]:
        updated_mapping = mapping.copy()
        for path in path_parts:
            for k, v in updated_mapping.items():
                if (
                    k in updated_mapping
                    and isinstance(updated_mapping[k], dict)
                    and isinstance(v, dict)
                ):
                    updated_mapping[k] = deep_traversal(updated_mapping[k], v)
                else:
                    updated_mapping[k] = jmespath.search("keys()")
        return updated_mapping


# 4. Provide an instance of your subclass in a Options object.
options = jmespath.Options(custom_functions=CustomFunctions())

# Provide this value to jmespath.search:
# This will print 3
# print(jmespath.search("full_path(`1`, `2`)", {}, options=options))

parent, child = "a.b[?(c==`3`)].value".split(".")[-2:]
print(parent, child)
print(
    jmespath.search(
        f"contains(keys({parent}), {child})",
        {"a": {"b": [1, {"c": 3, "value": "lending"}]}},
    )
)
# print(
#     jmespath.search(
#         "keys(a.b[?(c==`3`)].value) | [0]",
#         {"a": {"b": [1, {"c": 3, "value": "lending"}]}},
#     )
# )
