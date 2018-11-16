from derp.language.Grammar import Grammar
from derp.language.Grammar import merge_grammars

_basic_grammar = Grammar({
    '_article':  ('"a"i', '"an"i', '"the"i'),
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
    'create_expression':    '"create"i _article? "new"i? (selection | criteria)',

    'selection': '"selection"i',
    'criteria':  '"criteria"i'
})

_criteria_and_selection_modes_shared_grammar = Grammar({
    'expression':           ('save_expression',
                             'add_expression',
                             'remove_expression'),

    'recall_expression':    '"recall"i',
    'save_expression':      '"save as"i string',
    'add_expression':       '"add posts"i selector',
    'remove_expression':    '"remove posts"i selector',

    '?qualifier_or':     ('qualifier_or "or"i qualifier_and', 'qualifier_and'),
    '?qualifier_and':    ('qualifier_and "and"i? qualifier', 'qualifier'),

    'qualifier':    ('date_qualifier', 'substring_qualifier', 'boolean_qualifier',
                     'string_qualifier', 'number_qualifier', 'about_qualifier', 'match_qualifier'),

    'date_qualifier':       '_with_exp _article field _date_check date',
    'substring_qualifier':  '_with_exp string _substring_check field',
    'boolean_qualifier':    '_boolean_check field',
    'string_qualifier':     '_string_check field string',
    'number_qualifier':     '_number_check number field',
    'about_qualifier':      '_on_exp string',
    'match_qualifier':      '"matching"i string',

    '_with_exp': ('_with', 'without'),
    '_with':     '"with"i',
    'without':  '"without"i',

    '_date_check':   ('date_future', 'date_past', 'date_exact'),
    'date_future':   '"after"i',
    'date_past':     '"before"i',
    'date_exact':    ('"on"i', '"in"i'),

    'date':         '(month (day ","?)?)? year',
    'year':         'digit digit digit digit',
    '!month':        ('"january"i', '"february"i', '"march"i', '"april"i', '"may"i'
                      '"june"i', '"july"i', '"august"i', '"september"i', '"october"i',
                      '"november"i', '"december"i'),
    'day':          ('/[0-3]/ digit', '/[1-9]/'),

    '_substring_check':  '"in"i "the"i?',

    '_boolean_check':    '"which are"i negate?',

    '_string_check': '_with_exp "the exact"i',

    '_number_check': '_with_exp (number_above | number_below | number_exact | number_approx)',
    'number_above':   ('"over"i', '"greater than"i'),
    'number_below':   ('"under"i', '"less than"i'),
    'number_exact':   '"exactly"i',
    'number_approx':  '"roughly"i',

    '_on_exp':   'negate? ("on"i | "about"i)',
    'negate':    '"not"i',

    '!field': ''
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

_temporary_reddit_grammar = Grammar({
    'source':           'reddit_source',
    'reddit_source':    ('"reddit"', '"subreddit" string'),
    '!field':            ('"nsfw"', '"author"', '"title"', '"upvotes"', '"date"')
})

MAIN_MODE_GRAMMAR = merge_grammars(_basic_grammar, _main_mode_only_grammar)

CRITERIA_MODE_GRAMMAR = merge_grammars(
    _basic_grammar, _criteria_and_selection_modes_shared_grammar, _criteria_mode_only_grammar)

SELECTION_MODE_GRAMMAR = merge_grammars(
    _basic_grammar, _criteria_and_selection_modes_shared_grammar, _selection_mode_only_grammar)
