import pytest
from ..main.Interpreter import Interpreter


@pytest.fixture
def interpreter() -> Interpreter:
    return Interpreter()


class TestInterpreter:

    def test_empty_program(self, interpreter):
        assert interpreter.eval("BEGIN END.") == {}

    def test_single_assignment(self, interpreter):
        result = interpreter.eval("BEGIN x := 10; END.")
        assert result == {"x": 10.0}

    def test_arithmetic_operations(self, interpreter):
        result = interpreter.eval("BEGIN x := 10; y := x + 2 * (3 - 1); END.")
        assert result == {"x": 10.0, "y": 14.0}

    def test_nested_blocks(self, interpreter):
        result = interpreter.eval("""
        BEGIN 
            BEGIN 
                x := 5; 
            END; 
            y := x + 2; 
        END.
        """)
        assert result == {"x": 5.0, "y": 7.0}

    def test_variable_reassignment(self, interpreter):
        result = interpreter.eval("BEGIN x := 1; x := x + 5; END.")
        assert result == {"x": 6.0}

    def test_unary_operations(self, interpreter):
        result = interpreter.eval("BEGIN x := -10; y := +x; z := -x; END.")
        assert result == {"x": -10.0, "y": -10.0, "z": 10.0}

    def test_variable_not_defined_error(self, interpreter):
        with pytest.raises(NameError, match="Variable 'z' is not defined"):
            interpreter.eval("BEGIN x := 10; y := z + 1; END.")

    def test_invalid_operator_error(self, interpreter):
        # Здесь нужно отключить закомментированный блок в `_visit_binop` для теста.
        interpreter._visit_binop = lambda node: (Exception(f"invalid operator: {node.op.value}"))
        with pytest.raises(Exception, match="Bad Token: ?"):
            interpreter.eval("BEGIN x := 10; y := x ? 5; END.")

    def test_missing_end_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid statement"):
            interpreter.eval("BEGIN x := 10; y := 5;; END.")

    def test_invalid_syntax_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid factor"):
            interpreter.eval("BEGIN x := 10 + ; END.")

    def test_empty_statement_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid statement"):
            interpreter.eval("BEGIN ; END.")

    def test_division_by_zero(self, interpreter):
        with pytest.raises(ZeroDivisionError):
            interpreter.eval("BEGIN x := 10 / 0; END.")

    def test_empty_nested_blocks(self, interpreter):
        result = interpreter.eval("""
        BEGIN 
            BEGIN 
            END; 
        END.
        """)
        assert result == {}

    def test_complex_expression(self, interpreter):
        result = interpreter.eval("BEGIN x := 2 + 3 * (4 - 1) / 3; END.")
        assert result == {"x": 5.0}

    def test_unary_op_node(self, interpreter):
        result = interpreter.eval("BEGIN x := -5; END.")
        assert result == {"x": -5.0}

    def test_compound_node(self, interpreter):
        result = interpreter.eval("""
        BEGIN
            BEGIN
                x := 10;
            END;
            y := x + 1;
        END.
        """)
        assert result == {"x": 10.0, "y": 11.0}

    def test_undefined_variable_error(self, interpreter):
        with pytest.raises(NameError, match="Variable 'z' is not defined"):
            interpreter.eval("BEGIN x := 1; y := z; END.")

    def test_invalid_statement(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid statement"):
            interpreter.eval("BEGIN 123 := x; END.")

    def test_invalid_character_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Bad Token: @"):
            interpreter.eval("BEGIN x := 5 @ 3; END.")

    def test_missing_end(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid token order"):
            interpreter.eval("BEGIN x := 10;")

    def test_extra_token_error(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid factor"):
            interpreter.eval("BEGIN x := 10 + ; END.")

    def test_without_end(self, interpreter):
        with pytest.raises(SyntaxError, match="Invalid factor"):
            interpreter.eval("BEGIN x := 10 + ;")
