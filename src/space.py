# space.py - AtomSpace for Equality Rules

from atom import Symbol, Expression, NotReducible

class AtomSpace:
    """A minimal AtomSpace to store and query equality facts (= ARG $body)."""

    def __init__(self):
        # Store rules as a list of Expression atoms: [..., (= head body), ...]
        self.rules = []

    def add_atom(self, atom):
        """Adds an atom to the space. Only handles equality expressions for now."""
        if atom.is_expression() and len(atom.value) == 3 and atom.head == Symbol("="):
            # The pattern is (= head body)
            self.rules.append(atom)
            return True
        # For data facts that are not rules (e.g., (SocioEconomicData ...))
        # a more complete system would store them separately, but here we keep it simple.
        # For Bite-Piper, data facts are often stored as rules: (= (DataQuery) Result)
        return False

    def query(self, pattern):
        """
        Searches the space for a fact that matches the pattern.
        Returns the body of the matched (= pattern body) rule.
        Uses a *very minimal* unification (simple head match for simplicity).
        """
        # In a real MeTTa implementation, full unification is used here.
        # For simplicity, we search for a rule where the 'head' matches the pattern.
        
        # 1. Look for (= pattern $body)
        for rule in self.rules:
            # rule is (= head body)
            rule_head = rule.value[1]
            rule_body = rule.value[2]

            # Minimal check: Do the head symbols match?
            if isinstance(rule_head, Expression) and isinstance(pattern, Expression):
                if rule_head.head == pattern.head:
                    # In a full MeTTa, we would unify rule_head and pattern
                    # to get the bindings for variables in rule_body.
                    # Here, we return the body directly, assuming simple rules like (= (foo) (bar))
                    # or grounded functions are handled elsewhere.
                    return rule_body
            
            # Simple Symbol match, e.g., (= A AA)
            elif rule_head == pattern:
                 return rule_body

        return NotReducible