from collections import deque

import ijson
from rdflib import BNode, Literal, Namespace


def parse_dict(data, **kwargs):
    """Generates RDFlib triples from a python dictionary using a direct mapping."""

    def basic_parse(data):
        if isinstance(data, dict):  # start_map
            yield "start_map", None
            for k, v in data.items():
                yield "map_key", k
                for event, value in basic_parse(v):
                    yield event, value
            yield "end_map", None
        elif isinstance(data, list):  # start_list
            yield "start_array", None
            for i in data:
                for event, value in basic_parse(i):
                    yield event, value
            yield "end_array", None
        elif data is None:
            yield "null", data
        elif isinstance(data, str):
            yield "string", data
        elif isinstance(data, bool):
            yield "boolean", data
        elif isinstance(data, int):
            yield "integer", data
        elif isinstance(data, float):
            yield "double", data

    events = basic_parse(data)
    return _parse_events(events, **kwargs)


def parse_json(json, **kwargs):
    """
    Generates RDFlib triples from a file-like object
    or a string using a direct mapping.
    """

    #   parse json
    events = ijson.basic_parse(json, use_float=True)

    return _parse_events(events, **kwargs)


def _parse_events(events, **kwargs):
    """
    Internal method that generates RDFlib triples
    from a generator function that yields event, value pairs.
    """

    # initalize defaults
    namespace = Namespace("http://localhost/")
    instance_ns = None

    if "namespace" in kwargs and isinstance(kwargs["namespace"], Namespace):
        namespace = kwargs["namespace"]

    if "instance_ns" in kwargs and isinstance(kwargs["instance_ns"], Namespace):
        instance_ns = kwargs["instance_ns"]

    # initializing deque
    subject_stack = deque([])
    array_properties = {}
    prop = None

    i = 0
    for event, value in events:
        if event == "start_array" and subject_stack and prop is not None:
            # fetching the last subject
            s = subject_stack[-1]
            array_properties[s] = prop

        if event == "end_array" and subject_stack:
            # fetching the last subject
            s = subject_stack[-1]
            array_properties.pop(s, None)

        if event == "start_map":
            if instance_ns is not None:
                subject = instance_ns[str(i)]
                i += 1
            else:
                subject = BNode()
            # add triple with current array property, if any
            if prop is not None and subject_stack:
                # fetching the last subject
                s = subject_stack[-1]
                yield (s, prop, subject)
            subject_stack.append(subject)

        if event == "end_map":
            subject_stack.pop()

            # restore previous array property, if there was any
            if subject_stack and subject_stack[-1] in array_properties:
                prop = array_properties[subject_stack[-1]]

        if event in ["boolean", "integer", "double", "number"]:
            yield (subject_stack[-1], prop, Literal(value))

        if event == "string" and prop is not None:
            yield (subject_stack[-1], prop, Literal(value))
            # yield (subjectStack[-1], property, Literal(value, datatype=XSD.string))

        if event == "map_key":
            prop = namespace[value]
