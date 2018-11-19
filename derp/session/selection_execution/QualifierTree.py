import numbers
from datetime import date


class QualifierTree:
    def __init__(self, root_node):
        self.__root_node = root_node

    def root(self):
        return self.__root_node

    def evaluate(self, post):
        return self.__root_node.evaluate(post)


class QualifierTreeNode:

    def evaluate(self, post):
        pass


class ParentNode(QualifierTreeNode):

    def children(self):
        pass

class LeafNode(QualifierTreeNode):

    def data(self):
        pass

class FieldCheckNode(LeafNode):

    def field(self):
        pass


class AndNode(ParentNode):

    def __init__(self, left_qualifier, right_qualifier):
        assert(isinstance(left_qualifier, QualifierTreeNode) and isinstance(right_qualifier, QualifierTreeNode))
        self.__children = (left_qualifier, right_qualifier)

    def children(self):
        return self.__children

    def evaluate(self, post):
        return all([child.evaluate(post) for child in self.__children])


class OrNode(ParentNode):

    def __init__(self, left_qualifier, right_qualifier):
        self.__children = (left_qualifier, right_qualifier)

    def children(self):
        return self.__children

    def evaluate(self, post):
        return any([child.evaluate(post) for child in self.__children])


class DateCheck(FieldCheckNode):

    def __init__(self, comparison_date, field):
        assert(isinstance(comparison_date, date))
        self.__date = comparison_date
        self.__field = field

    def data(self):
        return self.__date

    def field(self):
        return self.__field


class DateOnCheck(DateCheck):

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, date):
            return False
        return post_data == self.data()


class DateAfterCheck(DateCheck):

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, date):
            return False
        return post_data > self.data()

class DateBeforeCheck(DateCheck):

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, date):
            return False
        return post_data < self.data()

class StringCheck(FieldCheckNode):

    def __init__(self, string, field):
        assert(isinstance(string, str))
        self.__string = string
        self.__field = field

    def data(self):
        return self.__string

    def field(self):
        return self.__field

class SubstringCheck(StringCheck):

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, str):
            return False
        return self.data() in post_data

class ExactStringCheck(StringCheck):

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, str):
            return False
        return self.data() in post_data

class NumberCheck(FieldCheckNode):

    def __init__(self, number, field):
        assert isinstance(number, numbers.Number)
        self.__number = number
        self.__field = field

    def data(self):
        return self.__number

    def field(self):
        return self.__field

class ExactNumberCheck(NumberCheck):

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, numbers.Number):
            return False
        return post_data == self.data()

class OverNumberCheck(NumberCheck):

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, numbers.Number):
            return False
        return post_data > self.data()

class UnderNumberCheck(NumberCheck):

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, numbers.Number):
            return False
        return post_data > self.data()

class RoughlyNumberCheck(NumberCheck):
    ROUGHLY_INTERVAL_PERCENTAGE = 0.1

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, numbers.Number):
            return False
        return (1 - RoughlyNumberCheck.ROUGHLY_INTERVAL_PERCENTAGE) * self.data() <= \
               post_data <= \
               (1 + RoughlyNumberCheck.ROUGHLY_INTERVAL_PERCENTAGE) * self.data()

class BooleanCheck(FieldCheckNode):

    def __init__(self, bool_value, field):
        assert(isinstance(bool_value, bool))
        self.__bool = bool_value
        self.__field = field

    def data(self):
        return self.__bool

    def field(self):
        return self.__field

    def evaluate(self, post):
        post_data = post.field_data(self.field())
        if not isinstance(post_data, bool):
            return False
        return post_data is self.data()

class AboutCheck(LeafNode):

    def __init__(self, string):
        assert(isinstance(string, str))
        self.__string = string

    def evaluate(self, post):
        return post.about(self.data())
