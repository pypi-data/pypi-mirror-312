from tree_sitter import Language, Parser, Node

from ._binding import language  # noqa: F401
from .nodes import (
    Variable,
    Expression,
    Quantity,
    UnitTerm,
    Call,
    BinaryOperator,
    Add,
    Subtract,
    Multiply,
    Divide,
    Power,
    UnaryOperator,
    Plus,
    Minus,
)

CAQTUS_LANGUAGE = Language(language())

parser = Parser(CAQTUS_LANGUAGE)

BINARY_OPERATOR_CLASSES = {
    "PLUS": Add,
    "MINUS": Subtract,
    "TIMES": Multiply,
    "DIVIDE": Divide,
    "POWER": Power,
}

UNARY_OPERATOR_CLASSES = {"PLUS": Plus, "MINUS": Minus}


def parse(code: str) -> Expression:
    """Compute a syntax tree for the given expression.

    Args:
        code: The expression to parse.

    Returns:
        An object representing the parsed expression.

    Raises:
        InvalidSyntaxError: If the expression is not correctly written.
    """

    tree = parser.parse(bytes(code, "utf-8"))

    root_node = tree.root_node

    assert root_node.text is not None

    if root_node.type in ("ERROR", "MISSING") or root_node.has_error:
        error_node = find_first_error(root_node)
        assert error_node is not None
        raise InvalidSyntaxError(
            f"Invalid syntax encountered while parsing expression <{code}>",
            (
                "",
                1,
                error_node.byte_range[0] + 1,
                root_node.text.decode("utf-8"),
                1,
                error_node.byte_range[1] + 1,
            ),
        )

    assert root_node.type == "expression", root_node.type

    return build_expression(tree.root_node)


def find_first_error(node: Node) -> Node | None:
    if node.is_error or node.is_missing:
        return node

    for child in node.children:
        error = find_first_error(child)
        if error:
            return error


def build_expression(node: Node) -> Expression:
    assert node.type == "expression"
    assert len(node.children) == 1
    return build_subexpression(node.children[0])


def build_subexpression(node: Node) -> Expression:
    assert node.text

    match node:
        case Node(type="variable"):
            return build_variable(node)
        case Node(type="integer"):
            return int(node.text.decode("utf-8"))
        case Node(type="float"):
            return float(node.text.decode("utf-8"))
        case Node(type="quantity"):
            return build_quantity(node)
        case Node(type="call"):
            return build_call(node)
        case Node(type="binary_operator"):
            return build_binary_operator(node)
        case Node(type="unary_operator"):
            return build_unary_operator(node)
        case Node(type="parenthesized_expression"):
            return build_parenthesized_expression(node)
        case _:
            raise AssertionError(f"Unexpected node type: {node.type}")


def build_parenthesized_expression(node: Node) -> Expression:
    assert node.type == "parenthesized_expression"
    expression = get_child_by_field_name(node, "expression")
    return build_subexpression(expression)


def build_variable(node: Node) -> Variable:
    assert node.type == "variable"

    names = []

    for child in node.named_children:
        assert child.text
        names.append(child.text.decode("utf-8"))

    return Variable(tuple(names))


def build_quantity(node: Node) -> Quantity:
    assert node.type == "quantity"

    magnitude_node = node.child_by_field_name("magnitude")
    assert magnitude_node is not None
    assert magnitude_node.type == "float"
    assert magnitude_node.text
    magnitude = float(magnitude_node.text.decode("utf-8"))

    unit_node = node.child_by_field_name("units")
    assert unit_node is not None
    assert unit_node.type == "units"

    multiplicative_units = [
        build_unit_term(get_child_by_field_name(unit_node, "first"))
    ]

    for multiplicative_node in unit_node.children_by_field_name("multiplicative"):
        if multiplicative_node.type != "TIMES":
            multiplicative_units.append(build_unit_term(multiplicative_node))

    divisional_units = [
        build_unit_term(divisional_node)
        for divisional_node in unit_node.children_by_field_name("divisive")
        if divisional_node.type != "DIVIDE"
    ]

    return Quantity(magnitude, tuple(multiplicative_units), tuple(divisional_units))


def build_unit_term(node: Node) -> UnitTerm:
    assert node.type == "unit_term"

    base_node = node.child_by_field_name("unit")
    assert base_node is not None
    assert base_node.type == "unit"
    assert base_node.text
    base = base_node.text.decode("utf-8")

    exponent_node = node.child_by_field_name("exponent")
    if exponent_node is None:
        return UnitTerm(base, None)
    else:
        assert exponent_node.type == "integer", exponent_node.type
        assert exponent_node.text
        exponent = int(exponent_node.text.decode("utf-8"))

        return UnitTerm(base, exponent)


def build_call(node: Node) -> Call:
    assert node.type == "call"

    function_node = node.child_by_field_name("function")
    assert function_node is not None
    assert function_node.type == "NAME"
    assert function_node.text
    function = function_node.text.decode("utf-8")

    arguments_node = node.child_by_field_name("args")
    if arguments_node is None:
        children = []
    else:
        assert arguments_node.type == "args"
        children = [child for child in arguments_node.children if child.type != ","]

    arguments = [build_subexpression(child) for child in children]
    return Call(function, tuple(arguments))


def build_binary_operator(node: Node) -> BinaryOperator:
    assert node.type == "binary_operator"

    operator_node = node.child_by_field_name("operator")
    assert operator_node is not None
    operator = operator_node.type

    left_node = node.child_by_field_name("left")
    assert left_node is not None
    left = build_subexpression(left_node)

    right_node = node.child_by_field_name("right")
    assert right_node is not None
    right = build_subexpression(right_node)

    assert operator in BINARY_OPERATOR_CLASSES
    return BINARY_OPERATOR_CLASSES[operator](left, right)


def build_unary_operator(node: Node) -> UnaryOperator:
    assert node.type == "unary_operator"
    operator_node = node.child_by_field_name("operator")
    assert operator_node is not None
    operator = operator_node.type

    operand_node = node.child_by_field_name("operand")
    assert operand_node is not None
    operand = build_subexpression(operand_node)

    assert operator in UNARY_OPERATOR_CLASSES, operator
    return UNARY_OPERATOR_CLASSES[operator](operand)


def get_child_by_field_name(node: Node, field_name: str) -> Node:
    result = node.child_by_field_name(field_name)
    assert result is not None
    return result


class ParsingError(Exception):
    pass


class InvalidSyntaxError(ParsingError, SyntaxError):
    pass
