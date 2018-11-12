from derp.language.Grammar import Grammar
from derp.language.Grammar import merge_grammars

basic_grammar = Grammar({
    'article':  ('"a"', '"an"', '"the"'),
    'digit':    '/[0-9]/',
    'number':   'digit+',
    'string':   'ESCAPED_STRING',

    'statement':    'expression',
    "expression":   "stop_expression",

    'stop_expression': ('"stop"', '"exit"')
}, 'statement')

main_mode_only_grammar = Grammar({
    'expression': ('load_expression',
                   'unload_expression',
                   'recall_expression',
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

MAIN_MODE_GRAMMAR = merge_grammars(basic_grammar, main_mode_only_grammar)
