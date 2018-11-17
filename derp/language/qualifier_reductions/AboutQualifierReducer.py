from lark import Transformer, v_args
from lark import Tree, Token


class AboutQualifierReducer(Transformer):
    """
    Find about check expressions and evaluate the data contained, converting
    the children to the list
    [ topic, negated ]
    """

    def about_qualifier(self, children):
        negate = False
        topic = None

        for child in children:
            # Check should have at most a FIELD and NEGATE token
            assert(isinstance(child, Token))

            if child.type == 'STRING':
                topic = child
            elif child.type == 'NEGATE':
                negate = True
            else:
                assert(False)

        assert(topic is not None)

        return Tree("about_qualifier", (topic, negate))
