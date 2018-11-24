import numbers
from datetime import date
from typing import Iterable


class QualifierTreeNode:

    def evaluate(self, post):
        """
        :param post: A derp.posts.IPost to evaluate this qualifier on
        :return: Whether the post matches the qualifier or not
        """
        pass

    def __str__(self):
        pass



class ParentNode(QualifierTreeNode):

    def children(self):
        """
        :return: the child qualifier tree nodes
        :rtype: Iterable
        """
        pass

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, ", ".join([str(child) for child in self.children()]))


class LeafNode(QualifierTreeNode):

    def data(self):
        """
        :return: the data involved in this qualifier
        """
        pass

    def __str__(self):
        return "{0}{{data={1}}}".format(self.__class__.__name__, self.data())



class FieldCheckNode(LeafNode):

    def field(self):
        """
        :return: the name of the field to be checked
        :rtype: str
        """
        pass

    def __str__(self):
        return "{0}{{field={1},data={2}}}".format(self.__class__.__name__, self.field(), self.data())


class AndNode(ParentNode):

    def __init__(self, left_qualifier, right_qualifier):
        assert (isinstance(left_qualifier, QualifierTreeNode) and isinstance(right_qualifier, QualifierTreeNode))
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


class NotNode(ParentNode):
    def __init__(self, sub_qualifier):
        self.__children = (sub_qualifier,)

    def children(self):
        return self.__children

    def evaluate(self, post):
        return not self.__children[0].evaluate()


class DateCheck(FieldCheckNode):

    def __init__(self, field, comparison_date):
        assert (isinstance(comparison_date, date))
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

    def __init__(self, field, string):
        assert (isinstance(string, str))
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

    def __init__(self, field, number):
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
        return post_data < self.data()


class BooleanCheck(FieldCheckNode):

    def __init__(self, field, bool_value):
        assert (isinstance(bool_value, bool))
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
        assert (isinstance(string, str))
        self.__string = string

    def data(self):
        return self.__string

    def evaluate(self, post):
        return post.about(self.data())
