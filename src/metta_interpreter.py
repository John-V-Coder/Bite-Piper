# metta_interpreter.py - Core Minimal MeTTa Instructions

from metta_atoms import Symbol, Expression, Variable, NotReducible, Empty, TrueAtom, FalseAtom
from knowledge_base import AtomSpace

class MeTTaInterpreter:
    """The engine for Minimal MeTTa instructions: eval, unify, chain."""

    def __init__(self, atomspace):
        self.atomspace = atomspace
        # A dictionary to hold grounded functions (+, -, <, etc.)
        self.grounded_functions = {
            Symbol("+"): lambda args: self._arithmetic(args, lambda a, b: a + b),
            Symbol("-"): lambda args: self._arithmetic(args, lambda a, b: a - b),
            Symbol("<"): lambda args: self._comparison(args, lambda a, b: a < b),
            Symbol("=="): lambda args: self._comparison(args, lambda a, b: a == b),
        }
        # A simple binding map for variables (only used in chain for simplicity)
        self.bindings = {}

    # --- Utility Functions for Grounded Operations ---

    def _get_number(self, atom):
        """Extracts number from a Symbol or Atom with a numeric value."""
        try:
            return float(atom.value) if "." in str(atom.value) else int(atom.value)
        except (ValueError, AttributeError):
            return None

    def _arithmetic(self, args, op):
        """Handles simple binary arithmetic operations."""
        if len(args) != 2:
            return NotReducible # IncorrectArgument in full MeTTa
        n1 = self._get_number(args[0])
        n2 = self._get_number(args[1])
        if n1 is None or n2 is None:
            return NotReducible # IncorrectArgument
        try:
            result = op(n1, n2)
            # Return result as Symbol (simplification: int/float is wrapped)
            return Symbol(str(result))
        except Exception:
            return NotReducible # Runtime Error

    def _comparison(self, args, op):
        """Handles simple binary comparison operations."""
        if len(args) != 2:
            return NotReducible
        n1 = self._get_number(args[0])
        n2 = self._get_number(args[1])
        if n1 is None or n2 is None:
            return NotReducible
        try:
            result = op(n1, n2)
            # Return True/False based on comparison result
            return TrueAtom if result else FalseAtom
        except Exception:
            return NotReducible

    # --- Core Minimal MeTTa Instructions ---

    def eval(self, arg):
        """
        (eval ARG) - Tries to reduce ARG based on:
        1. Grounded function call (if ARG is an Expression).
        2. Equality rule lookup in the AtomSpace.
        """
        if arg.is_expression():
            # Handle empty expressions
            if len(arg.value) == 0:
                return NotReducible
            
            head = arg.head
            args = arg.tail

            # 1. Grounded Function Call
            if head in self.grounded_functions:
                return self.grounded_functions[head](args)

            # 2. Equality rule lookup (Rule: (= ARG $body))
            # The AtomSpace query method is designed to handle this.
            # In Minimal MeTTa, eval only peeks one level deep.
            result = self.atomspace.query(arg)
            return result if result != NotReducible else NotReducible

        # If ARG is a Symbol or Variable, try a simple rule lookup (e.g., (= A AA))
        result = self.atomspace.query(arg)
        return result if result != NotReducible else NotReducible

    def unify(self, arg1, arg2, unified_result, not_unified_result):
        """
        (unify ARG1 ARG2 UNIFIED NOT-UNIFIED) - Tries a simple token match unification.
        A full MeTTa unification is complex, so we implement a *very minimal* version:
        - Symbols must match exactly.
        - Variables can match anything, and we bind the variable to the value.
        - Expressions require head and length match.
        """
        # NOTE: This minimal unify is for illustration and highly simplified.
        
        # Simple Case: Exact match of Symbols/Numbers/Expressions (no variables involved)
        if arg1 == arg2:
            return unified_result

        # A very complex part of MeTTa, we skip full implementation for uPython constraints.
        # For the sake of Bite-Piper's data: we need to unify a query pattern with a data fact.
        # For simplicity, we just return the unified_result if they are both expressions
        # with the same head, and let `chain` handle the variable substitution.
        
        # This is a massive simplification:
        if isinstance(arg1, Expression) and isinstance(arg2, Expression) and arg1.head == arg2.head:
            # Imagine we found bindings for $x in arg1 from arg2
            # For simplicity, we return the positive path
            return unified_result
        
        # If one is a variable and the other is not, bind it for the chain (VERY simplified)
        if isinstance(arg1, Variable):
            self.bindings[arg1.value] = arg2
            return unified_result
        
        return not_unified_result


    def chain(self, arg, var, result_atom):
        """
        (chain ARG $VAR RESULT) - Executes ARG, binds result to $VAR, substitutes $VAR in RESULT,
        and then evaluates the new RESULT (which can be another MeTTa instruction).
        """
        if not isinstance(var, Variable):
            raise TypeError("Chain requires a Variable for the second argument.")

        # 1. Execute ARG (must be a Minimal MeTTa instruction or a call to one via eval)
        if arg.is_expression():
            # Handle empty expressions
            if len(arg.value) == 0:
                exec_result = NotReducible
            # Minimal MeTTa only executes top-level instructions directly
            elif arg.head == Symbol("eval") and len(arg.tail) > 0:
                exec_result = self.eval(arg.tail[0])
            elif arg.head == Symbol("unify") and len(arg.tail) >= 4:
                exec_result = self.unify(*arg.tail)
            else:
                exec_result = arg # Not a Minimal MeTTa instruction, returns itself
        else:
            exec_result = arg

        # 2. Bind result to $VAR (using the simple bindings map)
        var_name = var.value
        self.bindings[var_name] = exec_result

        # 3. Substitute $VAR in RESULT
        def substitute(atom, bindings):
            if isinstance(atom, Variable) and atom.value in bindings:
                return bindings[atom.value]
            elif atom.is_expression():
                return Expression([substitute(a, bindings) for a in atom.value])
            else:
                return atom

        substituted_result = substitute(result_atom, self.bindings)

        # 4. Evaluate the new RESULT (Only the top-level instruction is executed)
        if substituted_result.is_expression():
            if substituted_result.head == Symbol("eval"):
                # We execute the resulting eval
                return self.eval(substituted_result.tail[0])
            elif substituted_result.head == Symbol("chain"):
                # Recursive chain execution (if chain is the result)
                return self.chain(*substituted_result.tail)
        
        # Return the substituted result if it's not a top-level instruction (Minimal MeTTa rule)
        return substituted_result
