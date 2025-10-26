# metta_atoms.py - Foundation Atom Structures for Minimal MeTTa

class Atom:
    """Base class for all Minimal MeTTa atoms."""
    
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        """Atoms are equal if their values match."""
        return isinstance(other, Atom) and self.value == other.value
    
    def __hash__(self):
        """Hash based on value for use in sets/dicts."""
        return hash((self.__class__.__name__, self.value))
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"
    
    def is_expression(self):
        """Check if this atom is an Expression."""
        return isinstance(self, Expression)


class Symbol(Atom):
    """Named constants and function names (e.g., RegionA, +, PovertyRate)."""
    
    def __init__(self, name):
        if not isinstance(name, str):
            name = str(name)
        super().__init__(name)
    
    def __repr__(self):
        return self.value


class Variable(Atom):
    """Logic variables prefixed with $ (e.g., $x, $data)."""
    
    def __init__(self, name):
        if not isinstance(name, str):
            name = str(name)
        # Ensure variable name starts with $
        if not name.startswith("$"):
            name = "$" + name
        super().__init__(name)
    
    def __repr__(self):
        return self.value


class Expression(Atom):
    """S-expressions for compound atoms (e.g., (+ 1 2), (RegionData RegionA))."""
    
    def __init__(self, atoms):
        """
        Args:
            atoms: List of Atom instances
        """
        if not isinstance(atoms, (list, tuple)):
            raise TypeError("Expression requires a list or tuple of atoms")
        # Store as immutable tuple for hashing
        super().__init__(tuple(atoms))
    
    @property
    def head(self):
        """First atom in the expression (the function/operator)."""
        return self.value[0] if len(self.value) > 0 else None
    
    @property
    def tail(self):
        """Remaining atoms after the head (the arguments)."""
        return list(self.value[1:]) if len(self.value) > 1 else []
    
    def __repr__(self):
        inner = " ".join(str(atom) for atom in self.value)
        return f"({inner})"
    
    def __len__(self):
        return len(self.value)


# Special atoms for control flow and evaluation results
NotReducible = Symbol("NotReducible")
Empty = Symbol("Empty")
TrueAtom = Symbol("True")
FalseAtom = Symbol("False")
