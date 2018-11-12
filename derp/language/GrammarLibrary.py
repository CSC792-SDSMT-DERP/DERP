from derp.language.Grammar import Grammar
from derp.language.Grammar import merge_grammars

_basic_grammar = Grammar({
    'article':  ('"a"i', '"an"i', '"the"i'),
    'digit':    '/[0-9]/',
    'number':   'digit+',
    'string':   'ESCAPED_STRING',

    'statement':    'expression',
    'expression':   ('stop_expression',
                     'recall_expression'),

    'stop_expression': ('"stop"i', '"exit"i')
}, 'statement')

_main_mode_only_grammar = Grammar({
    'expression': ('load_expression',
                   'unload_expression',
                   'clear_expression',
                   'read_expression',
                   'create_expression'),

    'load_expression':      '"load"i string',
    'unload_expression':    '"unload"i string',
    'recall_expression':    '"recall"i string',
    'clear_expression':     '"clear"i string',
    'read_expression':      '"read"i string',
    'create_expression':    '"create"i article? "new"i? ("selection"i | "criteria"i)'
})

_criteria_and_selection_modes_shared_grammar = Grammar({
    'expression':           ('save_expression',
                             'add_expression',
                             'remove_expression'),

    'recall_expression':    '"recall"i',
    'save_expression':      '"save as"i string',
    'add_expression':       '"add posts"i selector',
    'remove_expression':    '"remove posts"i selector',

    'qualifier_or':     ('qualifier_or "or"i qualifier_and', 'qualifier_and'),
    'qualifier_and':    ('qualifier_and "and"i? qualifier', 'qualifier'),

    'qualifier':    ('with_exp article field date_check date',
                     'with_exp string substring_check field',
                     'boolean_check field',
                     'string_check field string',
                     'number_check number field',
                     'on_exp string',
                     '"matching"i string'),

    'with_exp': ('"with"i', '"without"i'),

    'date_check':   '"date"i ("on"i | "after"i | "before"i)',
    'date':         '(month (day ","?)?)? year',
    'year':         'digit digit digit digit',
    'month':        ('"january"i', '"february"i', '"march"i', '"april"i', '"may"i'
                     '"june"i', '"july"i', '"august"i', '"september"i', '"october"i',
                     '"november"i', '"december"i'),
    'day':          ('/[0-3]/ digit', '/[1-9]/'),

    'substring_check':  '"in"i "the"i?',

    'boolean_check':    '"which are"i "not"i?',

    'string_check': 'with_exp "the exact"i',

    'number_check': 'with_exp ( "exactly"i | above_exp | below_exp | "roughly"i)',
    'above_exp':   ('"over"i', '"greater than"i'),
    'below_exp':   ('"under"i', '"less than"i'),

    'on_exp':   '"not"i? ("on"i | "about"i)',

    'field': ''
})

_criteria_mode_only_grammar = Grammar({
    'selector': 'qualifier_or'
})

_selection_mode_only_grammar = Grammar({
    'expression':       'read_expression',
    'read_expression':  '"read"i',

    'selector': ('qualifier_or', '"from"i source qualifier_or?'),
    'source':   ('source ( "and"i | "or"i ) source', 'string')
})

MAIN_MODE_GRAMMAR = merge_grammars(_basic_grammar, _main_mode_only_grammar)

CRITERIA_MODE_GRAMMAR = merge_grammars(
    _basic_grammar, _criteria_and_selection_modes_shared_grammar, _criteria_mode_only_grammar)

SELECTION_MODE_GRAMMAR = merge_grammars(
    _basic_grammar, _criteria_and_selection_modes_shared_grammar, _selection_mode_only_grammar)
