from .Grammar import Grammar
from .Grammar import merge_grammars

_basic_grammar = Grammar({
    '_ARTICLE':  ('"an"i', '"a"i', '"the"i'),
    'NUMBER':   '/-?[0-9]+/',
    'string':   'ESCAPED_STRING',

    'statement':    '_expression?',
    '_expression':   ('stop_expression',
                      'recall_expression',
                      'clear_expression'
                      ),

    'stop_expression': ('"stop"i', '"exit"i')
}, 'statement')

_main_mode_only_grammar = Grammar({
    '_expression': ('load_expression',
                    'unload_expression',
                    'read_expression',
                    'create_expression'),

    'load_expression':      '"load"i string',
    'unload_expression':    '"unload"i string',
    'recall_expression':    '"recall"i string',
    'clear_expression':     '"clear"i string',
    'read_expression':      '"read"i string',
    'create_expression':    '"create"i _ARTICLE? "new"i? (SELECTION | CRITERIA)',

    'SELECTION': '"selection"i',
    'CRITERIA':  '"criteria"i'
})

_criteria_and_selection_modes_shared_grammar = Grammar({
    '_expression':           ('save_expression',
                              'add_expression',
                              'remove_expression'),

    'recall_expression':    '"recall"i',
    'clear_expression':     '"clear"i',
    'save_expression':      '"save"i "as"i string',
    'add_expression':       '"add"i "posts"i add_selector',
    'remove_expression':    '"remove"i "posts"i remove_selector',

    '?qualifier_or':     ('qualifier_or "or"i qualifier_and', 'qualifier_and'),
    '?qualifier_and':    ('qualifier_and "and"i? _qualifier', '_qualifier'),

    '_qualifier':    ('date_qualifier', 'substring_qualifier', 'boolean_qualifier',
                      'string_qualifier', 'number_qualifier', 'about_qualifier', 'match_qualifier'),

    'date_qualifier':       'WITH_EXP _ARTICLE? FIELD _date_check date',
    'substring_qualifier':  'WITH_EXP string _substring_check FIELD',
    'boolean_qualifier':    '_boolean_check FIELD',
    'string_qualifier':     '_string_check FIELD string',
    'number_qualifier':     '_number_check NUMBER FIELD',
    'about_qualifier':      'NEGATE? _ON_EXP string',
    'match_qualifier':      'NEGATE? "matching"i string',

    'WITH_EXP': '/with(out)?/i',

    '_date_check':   ('DATE_AFTER', 'DATE_BEFORE', 'DATE_EXACT'),
    'DATE_AFTER':    '"after"i',
    'DATE_BEFORE':   '"before"i',
    'DATE_EXACT':    '"on"i',

    'date':         '(MONTH (DAY)? ","?)? YEAR',
    'YEAR':         'NUMBER',
    'MONTH':        ('"january"i', '"february"i', '"march"i', '"april"i', '"may"i'
                     '"june"i', '"july"i', '"august"i', '"september"i', '"october"i',
                     '"november"i', '"december"i'),
    'DAY':          ('NUMBER'),

    '_substring_check':  '"in"i "the"i?',

    '_boolean_check':    '"which"i "are"i NEGATE?',

    '_string_check': 'WITH_EXP "the"i "exact"i',

    '_number_check': 'WITH_EXP (number_above | number_below | number_exact | number_approx)',
    'number_above':   ('"over"i', '"greater"i "than"i'),
    'number_below':   ('"under"i', '"less"i "than"i'),
    'number_exact':   '"exactly"i',
    'number_approx':  '"roughly"i',

    '_ON_EXP':   ('"on"i', '"about"i'),
    'NEGATE':    '"not"i',
})

_criteria_mode_only_grammar = Grammar({
    'remove_selector': 'qualifier_or -> selector',
    'add_selector': 'qualifier_or -> selector'
})

_selection_mode_only_grammar = Grammar({
    '_expression':       'read_expression',
    'read_expression':  '"read"i',

    'add_selector': ('"from"i source qualifier_or? -> selector'),
    'remove_selector': ('qualifier_or -> selector'),
    'source':   ('source ( "and"i | "or"i ) source -> source_or', 'string -> source_selection')
})

MAIN_MODE_GRAMMAR = merge_grammars(_basic_grammar, _main_mode_only_grammar)

# NOTE: Criteria and Selection mode grammars are not valid
# unless merged with a grammar containing a definition for the FIELD token
CRITERIA_MODE_GRAMMAR = merge_grammars(
    _basic_grammar, _criteria_and_selection_modes_shared_grammar, _criteria_mode_only_grammar)

SELECTION_MODE_GRAMMAR = merge_grammars(
    _basic_grammar, _criteria_and_selection_modes_shared_grammar, _selection_mode_only_grammar)
