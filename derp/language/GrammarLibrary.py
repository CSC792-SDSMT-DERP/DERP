from derp.language.Grammar import Grammar
from derp.language.Grammar import merge_grammars

_basic_grammar = Grammar({
    'article':  ('"a"', '"an"', '"the"'),
    'digit':    '/[0-9]/',
    'number':   'digit+',
    'string':   'ESCAPED_STRING',

    'statement':    'expression',
    'expression':   ('stop_expression',
                     'recall_expression'),

    'stop_expression': ('"stop"', '"exit"')
}, 'statement')

_main_mode_only_grammar = Grammar({
    'expression': ('load_expression',
                   'unload_expression',
                   'clear_expression',
                   'read_expression',
                   'create_expression'),

    'load_expression':      '"load" string',
    'unload_expression':    '"unload" string',
    'recall_expression':    '"recall" string',
    'clear_expression':     '"clear" string',
    'read_expression':      '"read" string',
    'create_expression':    '"create" article? "new"? ("selection" | "criteria")'
})

_criteria_and_selection_modes_shared_grammar = Grammar({
    'expression':           ('save_expression',
                             'add_expression',
                             'remove_expression'),

    'recall_expression':    '"recall"',
    'save_expression':      '"save as" string',
    'add_expression':       '"add posts" selector',
    'remove_expression':    '"remove posts" selector',

    'qualifier_or':     ('qualifier_or "or" qualifier_and', 'qualifier_and'),
    'qualifier_and':    ('qualifier_and "and" qualifier', 'qualifier'),

    'qualifier':    ('with_exp article field date_check date',
                     'with_exp string substring_check field',
                     'boolean_check field',
                     'string_check field string',
                     'number_check number field',
                     'on_exp string',
                     '"matching" string'),

    'with_exp': ('"with"', '"without"'),

    'date_check':   '"date" ("on" | "after" | "before")',
    'date':         '(month day?)? year',
    'year':         'digit digit digit digit',
    'month':        ('"january"', '"february"', '"march"', '"april"', '"may"'
                     '"june"', '"july"', '"august"', '"september"', '"october"',
                     '"november"', '"december"'),
    'day':          '/[0-3]/ digit',

    'substring_check':  '"in" "the"?',

    'boolean_check':    '"which are" "not"?',

    'string_check': 'with_exp "the exact"',

    'number_check': 'with_exp ( "exactly" | above_exp | below_exp | "roughly")',
    'above_exp':   ('"over"', '"greater than"'),
    'below_exp':   ('"under"', '"less than"'),

    'on_exp':   '"not"? ("on" | "about")',

    'field': ''
})

_criteria_mode_only_grammar = Grammar({
    'selector': 'qualifier_or'
})

_selection_mode_only_grammar = Grammar({
    'expression':       'read_expression',
    'read_expression':  '"read"',

    'selector': ('qualifier_or', '"from" source qualifier_or?'),
    'source':   ('source ( "and" | "or" ) source', 'string')
})

MAIN_MODE_GRAMMAR = merge_grammars(_basic_grammar, _main_mode_only_grammar)

CRITERIA_MODE_GRAMMAR = merge_grammars(
    _basic_grammar, _criteria_and_selection_modes_shared_grammar, _criteria_mode_only_grammar)

SELECTION_MODE_GRAMMAR = merge_grammars(
    _basic_grammar, _criteria_and_selection_modes_shared_grammar, _selection_mode_only_grammar)
