from backend.tokens import *

EPSILON = "λ"

PREDICT = {

    # 1) PROGRAM
    "<program>": {
        TK_SACRED:          ["<global_dec_opt>", "<rite_seq>"],
        TK_DTYPE_TALLY:     ["<global_dec_opt>", "<rite_seq>"],
        TK_DTYPE_DIVINE:    ["<global_dec_opt>", "<rite_seq>"],
        TK_DTYPE_SIGIL:     ["<global_dec_opt>", "<rite_seq>"],
        TK_DTYPE_SCRIPTURE: ["<global_dec_opt>", "<rite_seq>"],
        TK_DTYPE_VERITY:    ["<global_dec_opt>", "<rite_seq>"],
        TK_OTHERS_ORDER:    ["<global_dec_opt>", "<rite_seq>"],
        TK_OTHERS_ORDAIN:   ["<global_dec_opt>", "<rite_seq>"],
        TK_CF_RITE:         ["<global_dec_opt>", "<rite_seq>"],
    },

    # 2) GLOBAL DECLS
    "<global_dec_opt>": {
        TK_SACRED:          ["<global_dec_list>"],
        TK_DTYPE_TALLY:     ["<global_dec_list>"],
        TK_DTYPE_DIVINE:    ["<global_dec_list>"],
        TK_DTYPE_SIGIL:     ["<global_dec_list>"],
        TK_DTYPE_SCRIPTURE: ["<global_dec_list>"],
        TK_DTYPE_VERITY:    ["<global_dec_list>"],
        TK_OTHERS_ORDER:    ["<global_dec_list>"],
        TK_OTHERS_ORDAIN:   ["<global_dec_list>"],
        TK_CF_RITE:         [EPSILON],
    },

    "<global_dec_list>": {
        TK_SACRED:          ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_TALLY:     ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_DIVINE:    ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_SIGIL:     ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_SCRIPTURE: ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_VERITY:    ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_OTHERS_ORDER:    ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_OTHERS_ORDAIN:   ["<global_dec_item>", "<global_dec_list_tail>"],
    },

    "<global_dec_list_tail>": {
        TK_SACRED:          ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_TALLY:     ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_DIVINE:    ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_SIGIL:     ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_SCRIPTURE: ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_DTYPE_VERITY:    ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_OTHERS_ORDER:    ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_OTHERS_ORDAIN:   ["<global_dec_item>", "<global_dec_list_tail>"],
        TK_CF_RITE:         [EPSILON],
    },

    "<global_dec_item>": {
        # sacred <data_type> <sacred_init_list> ;
        TK_SACRED: [TK_SACRED, "<data_type>", "<sacred_init_list>", TK_SYM_SEMICOL],

        # <data_type> <var_decl_group> ;
        TK_DTYPE_TALLY:     ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],
        TK_DTYPE_DIVINE:    ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],
        TK_DTYPE_SIGIL:     ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],
        TK_DTYPE_SCRIPTURE: ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],
        TK_DTYPE_VERITY:    ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],

        # order identifier { <member_list_opt> } ;
        TK_OTHERS_ORDER:  [TK_OTHERS_ORDER, TK_IDENTIFIER, TK_SYM_OPBRACE, "<member_list_opt>", TK_SYM_CLSBRACE, TK_SYM_SEMICOL],

        # ordain identifier <ordain_dec_list> ;
        TK_OTHERS_ORDAIN: [TK_OTHERS_ORDAIN, TK_IDENTIFIER, "<ordain_dec_list>", TK_SYM_SEMICOL],
    },

    # 3) RITES / FUNCTIONS
    "<rite_seq>": {
        TK_CF_RITE: [TK_CF_RITE, "<return_type_any>", "<rite_after_type>"]
    },

    "<return_type_any>": {
        TK_DTYPE_TALLY:     ["<data_type_id>"],
        TK_DTYPE_DIVINE:    ["<data_type_id>"],
        TK_DTYPE_SIGIL:     ["<data_type_id>"],
        TK_DTYPE_SCRIPTURE: ["<data_type_id>"],
        TK_DTYPE_VERITY:    ["<data_type_id>"],
        TK_IDENTIFIER:      ["<data_type_id>"],
        TK_DTYPE_HOLLOW:    [TK_DTYPE_HOLLOW],
    },

    "<rite_after_type>": {
        # genesis () { <main_local_dec_opt> <statement_list> <dismiss_opt> }
        TK_OTHERS_GENESIS: [
            TK_OTHERS_GENESIS,
            TK_SYM_OPPAREN, TK_SYM_CLSPAREN,
            TK_SYM_OPBRACE, "<main_local_dec_opt>", "<statement_list>", "<dismiss_opt>", TK_SYM_CLSBRACE
        ],

        # identifier ( <param_list_opt> ) { <func_local_dec_opt> <statement_list> <dismiss_opt> } <rite_seq>
        TK_IDENTIFIER: [
            TK_IDENTIFIER,
            TK_SYM_OPPAREN, "<param_list_opt>", TK_SYM_CLSPAREN,
            TK_SYM_OPBRACE, "<func_local_dec_opt>", "<statement_list>", "<dismiss_opt>", TK_SYM_CLSBRACE,
            "<rite_seq>"
        ],
    },

    # 4) ORDER MEMBERS
    "<member_list_opt>": {
        TK_DTYPE_TALLY:     ["<member_list>"],
        TK_DTYPE_DIVINE:    ["<member_list>"],
        TK_DTYPE_SIGIL:     ["<member_list>"],
        TK_DTYPE_SCRIPTURE: ["<member_list>"],
        TK_DTYPE_VERITY:    ["<member_list>"],
        TK_IDENTIFIER:      ["<member_list>"],
        TK_SYM_CLSBRACE:    [EPSILON],
    },

    "<member_list>": {
        TK_DTYPE_TALLY:     ["<member>", "<member_list_tail>"],
        TK_DTYPE_DIVINE:    ["<member>", "<member_list_tail>"],
        TK_DTYPE_SIGIL:     ["<member>", "<member_list_tail>"],
        TK_DTYPE_SCRIPTURE: ["<member>", "<member_list_tail>"],
        TK_DTYPE_VERITY:    ["<member>", "<member_list_tail>"],
        TK_IDENTIFIER:      ["<member>", "<member_list_tail>"],
    },

    "<member_list_tail>": {
        TK_DTYPE_TALLY:     ["<member>", "<member_list_tail>"],
        TK_DTYPE_DIVINE:    ["<member>", "<member_list_tail>"],
        TK_DTYPE_SIGIL:     ["<member>", "<member_list_tail>"],
        TK_DTYPE_SCRIPTURE: ["<member>", "<member_list_tail>"],
        TK_DTYPE_VERITY:    ["<member>", "<member_list_tail>"],
        TK_IDENTIFIER:      ["<member>", "<member_list_tail>"],
        TK_SYM_CLSBRACE:    [EPSILON],
    },

    "<member>": {
        # <data_type_id> identifier <array_dims_tail> <member_init_opt> ;
        TK_DTYPE_TALLY:     ["<data_type_id>", TK_IDENTIFIER, "<array_dims_tail>", "<member_init_opt>", TK_SYM_SEMICOL],
        TK_DTYPE_DIVINE:    ["<data_type_id>", TK_IDENTIFIER, "<array_dims_tail>", "<member_init_opt>", TK_SYM_SEMICOL],
        TK_DTYPE_SIGIL:     ["<data_type_id>", TK_IDENTIFIER, "<array_dims_tail>", "<member_init_opt>", TK_SYM_SEMICOL],
        TK_DTYPE_SCRIPTURE: ["<data_type_id>", TK_IDENTIFIER, "<array_dims_tail>", "<member_init_opt>", TK_SYM_SEMICOL],
        TK_DTYPE_VERITY:    ["<data_type_id>", TK_IDENTIFIER, "<array_dims_tail>", "<member_init_opt>", TK_SYM_SEMICOL],
        TK_IDENTIFIER:      ["<data_type_id>", TK_IDENTIFIER, "<array_dims_tail>", "<member_init_opt>", TK_SYM_SEMICOL],
    },

    "<member_init_opt>": {
        TK_OP_ASSIGN:   [TK_OP_ASSIGN, "<member_init_val>"],
        TK_SYM_SEMICOL: [EPSILON],
    },

    "<member_init_val>": {
        TK_SYM_OPBRACE: ["<array_init>"],

        # else <expr>
        TK_OP_NOT:         ["<expr>"],
        TK_OP_TILDE:       ["<expr>"],
        TK_OP_INC:         ["<expr>"],
        TK_OP_DEC:         ["<expr>"],
        TK_SYM_OPPAREN:    ["<expr>"],
        TK_IDENTIFIER:     ["<expr>"],
        TK_OTHERS_VERSEOF: ["<expr>"],
        TK_LIT_INT:        ["<expr>"],
        TK_LIT_DECIMAL:    ["<expr>"],
        TK_LIT_CHAR:       ["<expr>"],
        TK_LIT_STRING:     ["<expr>"],
        TK_OTHERS_HOLY:    ["<expr>"],
        TK_OTHERS_UNHOLY:  ["<expr>"],
    },

    # 5) SACRED INIT LIST
    "<sacred_init_list>": {
        TK_IDENTIFIER: ["<sacred_init>", "<sacred_init_tail>"]
    },

    "<sacred_init_tail>": {
        TK_SYM_COMMA:   [TK_SYM_COMMA, "<sacred_init>", "<sacred_init_tail>"],
        TK_SYM_SEMICOL: [EPSILON],
    },

    "<sacred_init>": {
        TK_IDENTIFIER: [TK_IDENTIFIER, "<sacred_assign_opt>"]
    },

    "<sacred_assign_opt>": {
        TK_OP_ASSIGN:   [TK_OP_ASSIGN, "<const_expr>"],
        TK_SYM_COMMA:   [EPSILON],
        TK_SYM_SEMICOL: [EPSILON],
    },

    # 6) VAR DECL GROUP
    "<var_decl_group>": {
        TK_IDENTIFIER: ["<var_decl_item>", "<var_decl_tail>"]
    },

    "<var_decl_tail>": {
        TK_SYM_COMMA:   [TK_SYM_COMMA, "<var_decl_item>", "<var_decl_tail>"],
        TK_SYM_SEMICOL: [EPSILON],
    },

    "<var_decl_item>": {
        TK_IDENTIFIER: [TK_IDENTIFIER, "<array_dims_tail>", "<var_decl_item_tail>"]
    },

    "<var_decl_item_tail>": {
        TK_OP_ASSIGN:   [TK_OP_ASSIGN, "<var_after_eq>"],
        TK_SYM_COMMA:   [EPSILON],
        TK_SYM_SEMICOL: [EPSILON],
    },

    "<var_after_eq>": {
        TK_SYM_OPBRACE: ["<array_init>"],

        # else <expr>
        TK_OP_NOT:         ["<expr>"],
        TK_OP_TILDE:       ["<expr>"],
        TK_OP_INC:         ["<expr>"],
        TK_OP_DEC:         ["<expr>"],
        TK_SYM_OPPAREN:    ["<expr>"],
        TK_IDENTIFIER:     ["<expr>"],
        TK_OTHERS_VERSEOF: ["<expr>"],
        TK_LIT_INT:        ["<expr>"],
        TK_LIT_DECIMAL:    ["<expr>"],
        TK_LIT_CHAR:       ["<expr>"],
        TK_LIT_STRING:     ["<expr>"],
        TK_OTHERS_HOLY:    ["<expr>"],
        TK_OTHERS_UNHOLY:  ["<expr>"],
    },

    # 7) ARRAYS
    "<array_dims_tail>": {
        TK_SYM_OPBRACK: [TK_SYM_OPBRACK, "<expr>", TK_SYM_CLSBRACK, "<array_dims_tail>"],

        # FOLLOW(array_dims_tail) -> { =, ,, ; }
        TK_OP_ASSIGN:   [EPSILON],
        TK_SYM_COMMA:   [EPSILON],
        TK_SYM_SEMICOL: [EPSILON],
    },

    "<array_init>": {
        TK_SYM_OPBRACE: [TK_SYM_OPBRACE, "<array_vals_opt>", TK_SYM_CLSBRACE]
    },

    "<array_vals_opt>": {
        # <array_vals> | λ
        TK_SYM_OPBRACE:    ["<array_vals>"],
        TK_OP_NOT:         ["<array_vals>"],
        TK_OP_TILDE:       ["<array_vals>"],
        TK_OP_INC:         ["<array_vals>"],
        TK_OP_DEC:         ["<array_vals>"],
        TK_SYM_OPPAREN:    ["<array_vals>"],
        TK_IDENTIFIER:     ["<array_vals>"],
        TK_OTHERS_VERSEOF: ["<array_vals>"],
        TK_LIT_INT:        ["<array_vals>"],
        TK_LIT_DECIMAL:    ["<array_vals>"],
        TK_LIT_CHAR:       ["<array_vals>"],
        TK_LIT_STRING:     ["<array_vals>"],
        TK_OTHERS_HOLY:    ["<array_vals>"],
        TK_OTHERS_UNHOLY:  ["<array_vals>"],
        TK_SYM_CLSBRACE:   [EPSILON],
    },

    "<array_vals>": {
        TK_SYM_OPBRACE:    ["<array_val>", "<array_vals_tail>"],
        TK_OP_NOT:         ["<array_val>", "<array_vals_tail>"],
        TK_OP_TILDE:       ["<array_val>", "<array_vals_tail>"],
        TK_OP_INC:         ["<array_val>", "<array_vals_tail>"],
        TK_OP_DEC:         ["<array_val>", "<array_vals_tail>"],
        TK_SYM_OPPAREN:    ["<array_val>", "<array_vals_tail>"],
        TK_IDENTIFIER:     ["<array_val>", "<array_vals_tail>"],
        TK_OTHERS_VERSEOF: ["<array_val>", "<array_vals_tail>"],
        TK_LIT_INT:        ["<array_val>", "<array_vals_tail>"],
        TK_LIT_DECIMAL:    ["<array_val>", "<array_vals_tail>"],
        TK_LIT_CHAR:       ["<array_val>", "<array_vals_tail>"],
        TK_LIT_STRING:     ["<array_val>", "<array_vals_tail>"],
        TK_OTHERS_HOLY:    ["<array_val>", "<array_vals_tail>"],
        TK_OTHERS_UNHOLY:  ["<array_val>", "<array_vals_tail>"],
    },

    "<array_vals_tail>": {
        TK_SYM_COMMA:    [TK_SYM_COMMA, "<array_val>", "<array_vals_tail>"],
        TK_SYM_CLSBRACE: [EPSILON],
    },

    "<array_val>": {
        # { <array_vals_opt> }  |  <expr>
        TK_SYM_OPBRACE: [TK_SYM_OPBRACE, "<array_vals_opt>", TK_SYM_CLSBRACE],

        TK_OP_NOT:         ["<expr>"],
        TK_OP_TILDE:       ["<expr>"],
        TK_OP_INC:         ["<expr>"],
        TK_OP_DEC:         ["<expr>"],
        TK_SYM_OPPAREN:    ["<expr>"],
        TK_IDENTIFIER:     ["<expr>"],
        TK_OTHERS_VERSEOF: ["<expr>"],
        TK_LIT_INT:        ["<expr>"],
        TK_LIT_DECIMAL:    ["<expr>"],
        TK_LIT_CHAR:       ["<expr>"],
        TK_LIT_STRING:     ["<expr>"],
        TK_OTHERS_HOLY:    ["<expr>"],
        TK_OTHERS_UNHOLY:  ["<expr>"],
    },

    # 8) DATA TYPES
    "<data_type>": {
        TK_DTYPE_TALLY:     [TK_DTYPE_TALLY],
        TK_DTYPE_DIVINE:    [TK_DTYPE_DIVINE],
        TK_DTYPE_SIGIL:     [TK_DTYPE_SIGIL],
        TK_DTYPE_SCRIPTURE: [TK_DTYPE_SCRIPTURE],
        TK_DTYPE_VERITY:    [TK_DTYPE_VERITY],
    },

    "<data_type_id>": {
        TK_DTYPE_TALLY:     ["<data_type>"],
        TK_DTYPE_DIVINE:    ["<data_type>"],
        TK_DTYPE_SIGIL:     ["<data_type>"],
        TK_DTYPE_SCRIPTURE: ["<data_type>"],
        TK_DTYPE_VERITY:    ["<data_type>"],
        TK_IDENTIFIER:      [TK_IDENTIFIER],
    },

    # 9) PARAMS
    "<param_list_opt>": {
        TK_DTYPE_TALLY:     ["<param_list>"],
        TK_DTYPE_DIVINE:    ["<param_list>"],
        TK_DTYPE_SIGIL:     ["<param_list>"],
        TK_DTYPE_SCRIPTURE: ["<param_list>"],
        TK_DTYPE_VERITY:    ["<param_list>"],
        TK_IDENTIFIER:      ["<param_list>"],
        TK_SYM_CLSPAREN:    [EPSILON],
    },

    "<param_list>": {
        TK_DTYPE_TALLY:     ["<param>", "<param_list_tail>"],
        TK_DTYPE_DIVINE:    ["<param>", "<param_list_tail>"],
        TK_DTYPE_SIGIL:     ["<param>", "<param_list_tail>"],
        TK_DTYPE_SCRIPTURE: ["<param>", "<param_list_tail>"],
        TK_DTYPE_VERITY:    ["<param>", "<param_list_tail>"],
        TK_IDENTIFIER:      ["<param>", "<param_list_tail>"],
    },

    "<param_list_tail>": {
        TK_SYM_COMMA:    [TK_SYM_COMMA, "<param>", "<param_list_tail>"],
        TK_SYM_CLSPAREN: [EPSILON],
    },

    "<param>": {
        TK_DTYPE_TALLY:     ["<data_type_id>", TK_IDENTIFIER, "<param_array_tail>"],
        TK_DTYPE_DIVINE:    ["<data_type_id>", TK_IDENTIFIER, "<param_array_tail>"],
        TK_DTYPE_SIGIL:     ["<data_type_id>", TK_IDENTIFIER, "<param_array_tail>"],
        TK_DTYPE_SCRIPTURE: ["<data_type_id>", TK_IDENTIFIER, "<param_array_tail>"],
        TK_DTYPE_VERITY:    ["<data_type_id>", TK_IDENTIFIER, "<param_array_tail>"],
        TK_IDENTIFIER:      ["<data_type_id>", TK_IDENTIFIER, "<param_array_tail>"],
    },

    "<param_array_tail>": {
        TK_SYM_OPBRACK:  [TK_SYM_OPBRACK, TK_SYM_CLSBRACK, "<param_array_tail>"],
        TK_SYM_COMMA:    [EPSILON],
        TK_SYM_CLSPAREN: [EPSILON],
    },

    # 10) LOCAL DECLS
    "<func_local_dec_opt>": {
        TK_SACRED:          ["<func_local_dec>"],
        TK_DTYPE_TALLY:     ["<func_local_dec>"],
        TK_DTYPE_DIVINE:    ["<func_local_dec>"],
        TK_DTYPE_SIGIL:     ["<func_local_dec>"],
        TK_DTYPE_SCRIPTURE: ["<func_local_dec>"],
        TK_DTYPE_VERITY:    ["<func_local_dec>"],
        TK_OTHERS_ORDER:    ["<func_local_dec>"],
        TK_OTHERS_ORDAIN:   ["<func_local_dec>"],
        # else λ
        TK_IO_RECEIVE:      [EPSILON],
        TK_IO_PROCLAIM:     [EPSILON],
        TK_CF_DECREE:       [EPSILON],
        TK_CF_DISCERN:      [EPSILON],
        TK_CF_PROCESSION:   [EPSILON],
        TK_CF_ENDURE:       [EPSILON],
        TK_CF_RITUAL:       [EPSILON],
        TK_CF_DISMISS:      [EPSILON],
        TK_CF_PROCEED:      [EPSILON],
        TK_CF_ABSOLVE:      [EPSILON],
        TK_IDENTIFIER:      [EPSILON],
        TK_OP_INC:          [EPSILON],
        TK_OP_DEC:          [EPSILON],
        TK_SYM_OPPAREN:     [EPSILON],
        TK_SYM_CLSBRACE:    [EPSILON],
    },

    "<func_local_dec>": {
        TK_SACRED:          ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_TALLY:     ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_DIVINE:    ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_SIGIL:     ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_SCRIPTURE: ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_VERITY:    ["<func_local_item>", "<func_local_dec_tail>"],
        TK_OTHERS_ORDER:    ["<func_local_item>", "<func_local_dec_tail>"],
        TK_OTHERS_ORDAIN:   ["<func_local_item>", "<func_local_dec_tail>"],
    },

    "<func_local_dec_tail>": {
        TK_SACRED:          ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_TALLY:     ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_DIVINE:    ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_SIGIL:     ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_SCRIPTURE: ["<func_local_item>", "<func_local_dec_tail>"],
        TK_DTYPE_VERITY:    ["<func_local_item>", "<func_local_dec_tail>"],
        TK_OTHERS_ORDER:    ["<func_local_item>", "<func_local_dec_tail>"],
        TK_OTHERS_ORDAIN:   ["<func_local_item>", "<func_local_dec_tail>"],
        # λ
        TK_IO_RECEIVE:      [EPSILON],
        TK_IO_PROCLAIM:     [EPSILON],
        TK_CF_DECREE:       [EPSILON],
        TK_CF_DISCERN:      [EPSILON],
        TK_CF_PROCESSION:   [EPSILON],
        TK_CF_ENDURE:       [EPSILON],
        TK_CF_RITUAL:       [EPSILON],
        TK_CF_DISMISS:      [EPSILON],
        TK_CF_PROCEED:      [EPSILON],
        TK_CF_ABSOLVE:      [EPSILON],
        TK_IDENTIFIER:      [EPSILON],
        TK_OP_INC:          [EPSILON],
        TK_OP_DEC:          [EPSILON],
        TK_SYM_OPPAREN:     [EPSILON],
        TK_SYM_CLSBRACE:    [EPSILON],
    },

    "<func_local_item>": {
        TK_SACRED:          ["<global_dec_item>"],
        TK_DTYPE_TALLY:     ["<global_dec_item>"],
        TK_DTYPE_DIVINE:    ["<global_dec_item>"],
        TK_DTYPE_SIGIL:     ["<global_dec_item>"],
        TK_DTYPE_SCRIPTURE: ["<global_dec_item>"],
        TK_DTYPE_VERITY:    ["<global_dec_item>"],
        TK_OTHERS_ORDER:    ["<global_dec_item>"],
        TK_OTHERS_ORDAIN:   ["<global_dec_item>"],
    },

    "<main_local_dec_opt>": {
        TK_SACRED:          ["<main_local_dec>"],
        TK_DTYPE_TALLY:     ["<main_local_dec>"],
        TK_DTYPE_DIVINE:    ["<main_local_dec>"],
        TK_DTYPE_SIGIL:     ["<main_local_dec>"],
        TK_DTYPE_SCRIPTURE: ["<main_local_dec>"],
        TK_DTYPE_VERITY:    ["<main_local_dec>"],
        TK_OTHERS_ORDER:    ["<main_local_dec>"],
        TK_OTHERS_ORDAIN:   ["<main_local_dec>"],
        # else λ
        TK_IO_RECEIVE:      [EPSILON],
        TK_IO_PROCLAIM:     [EPSILON],
        TK_CF_DECREE:       [EPSILON],
        TK_CF_DISCERN:      [EPSILON],
        TK_CF_PROCESSION:   [EPSILON],
        TK_CF_ENDURE:       [EPSILON],
        TK_CF_RITUAL:       [EPSILON],
        TK_CF_DISMISS:      [EPSILON],
        TK_CF_PROCEED:      [EPSILON],
        TK_CF_ABSOLVE:      [EPSILON],
        TK_IDENTIFIER:      [EPSILON],
        TK_OP_INC:          [EPSILON],
        TK_OP_DEC:          [EPSILON],
        TK_SYM_OPPAREN:     [EPSILON],
        TK_SYM_CLSBRACE:    [EPSILON],
    },

    "<main_local_dec>": {
        TK_SACRED:          ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_TALLY:     ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_DIVINE:    ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_SIGIL:     ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_SCRIPTURE: ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_VERITY:    ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_OTHERS_ORDER:    ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_OTHERS_ORDAIN:   ["<main_dec_item>", "<main_local_dec_tail>"],
    },

    "<main_local_dec_tail>": {
        TK_SACRED:          ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_TALLY:     ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_DIVINE:    ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_SIGIL:     ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_SCRIPTURE: ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_DTYPE_VERITY:    ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_OTHERS_ORDER:    ["<main_dec_item>", "<main_local_dec_tail>"],
        TK_OTHERS_ORDAIN:   ["<main_dec_item>", "<main_local_dec_tail>"],
        # λ
        TK_IO_RECEIVE:      [EPSILON],
        TK_IO_PROCLAIM:     [EPSILON],
        TK_CF_DECREE:       [EPSILON],
        TK_CF_DISCERN:      [EPSILON],
        TK_CF_PROCESSION:   [EPSILON],
        TK_CF_ENDURE:       [EPSILON],
        TK_CF_RITUAL:       [EPSILON],
        TK_CF_DISMISS:      [EPSILON],
        TK_CF_PROCEED:      [EPSILON],
        TK_CF_ABSOLVE:      [EPSILON],
        TK_IDENTIFIER:      [EPSILON],
        TK_OP_INC:          [EPSILON],
        TK_OP_DEC:          [EPSILON],
        TK_SYM_OPPAREN:     [EPSILON],
        TK_SYM_CLSBRACE:    [EPSILON],
    },

    "<main_dec_item>": {
        TK_SACRED:          ["<func_local_item>"],
        TK_DTYPE_TALLY:     ["<func_local_item>"],
        TK_DTYPE_DIVINE:    ["<func_local_item>"],
        TK_DTYPE_SIGIL:     ["<func_local_item>"],
        TK_DTYPE_SCRIPTURE: ["<func_local_item>"],
        TK_DTYPE_VERITY:    ["<func_local_item>"],
        TK_OTHERS_ORDER:    ["<func_local_item>"],
        TK_OTHERS_ORDAIN:   ["<func_local_item>"],
    },

    # 11) STATEMENTS
    "<statement_list>": {
        # FIRST(<statement>) plus λ when follow is dismiss or }
        TK_DTYPE_TALLY:     ["<statement>", "<statement_list>"],
        TK_DTYPE_DIVINE:    ["<statement>", "<statement_list>"],
        TK_DTYPE_SIGIL:     ["<statement>", "<statement_list>"],
        TK_DTYPE_SCRIPTURE: ["<statement>", "<statement_list>"],
        TK_DTYPE_VERITY:    ["<statement>", "<statement_list>"],

        TK_OTHERS_ORDER:    ["<statement>", "<statement_list>"],
        TK_OTHERS_ORDAIN:   ["<statement>", "<statement_list>"],

        TK_IO_RECEIVE:      ["<statement>", "<statement_list>"],
        TK_IO_PROCLAIM:     ["<statement>", "<statement_list>"],

        TK_CF_DECREE:       ["<statement>", "<statement_list>"],
        TK_CF_DISCERN:      ["<statement>", "<statement_list>"],

        TK_CF_PROCESSION:   ["<statement>", "<statement_list>"],
        TK_CF_ENDURE:       ["<statement>", "<statement_list>"],
        TK_CF_RITUAL:       ["<statement>", "<statement_list>"],

        TK_CF_DISMISS:      ["<statement>", "<statement_list>"],
        TK_CF_PROCEED:      ["<statement>", "<statement_list>"],
        TK_CF_ABSOLVE:      ["<statement>", "<statement_list>"],

        TK_IDENTIFIER:      ["<statement>", "<statement_list>"],
        TK_OP_INC:          ["<statement>", "<statement_list>"],
        TK_OP_DEC:          ["<statement>", "<statement_list>"],
        TK_SYM_OPPAREN:     ["<statement>", "<statement_list>"],

        # λ
        TK_CF_DISMISS:      ["<statement>", "<statement_list>"],  # already above
        TK_SYM_CLSBRACE:    [EPSILON],
    },

    "<statement>": {
        TK_DTYPE_TALLY:     ["<var_dec_stmt>"],
        TK_DTYPE_DIVINE:    ["<var_dec_stmt>"],
        TK_DTYPE_SIGIL:     ["<var_dec_stmt>"],
        TK_DTYPE_SCRIPTURE: ["<var_dec_stmt>"],
        TK_DTYPE_VERITY:    ["<var_dec_stmt>"],
        TK_OTHERS_ORDAIN:   ["<ordain_stmt>"],
        TK_OTHERS_ORDER:    ["<order_stmt>"],
        TK_IO_RECEIVE:      ["<io_stmt>"],
        TK_IO_PROCLAIM:     ["<io_stmt>"],
        TK_CF_DECREE:       ["<cond_stmt>"],
        TK_CF_DISCERN:      ["<cond_stmt>"],
        TK_CF_PROCESSION:   ["<loop_stmt>"],
        TK_CF_ENDURE:       ["<loop_stmt>"],
        TK_CF_RITUAL:       ["<loop_stmt>"],
        TK_CF_DISMISS:      ["<jump_stmt>"],
        TK_CF_PROCEED:      ["<jump_stmt>"],
        TK_CF_ABSOLVE:      ["<jump_stmt>"],
        TK_IDENTIFIER:      [TK_IDENTIFIER, "<stmt_id_tail>"],
        TK_OP_INC:          ["<prefix_incdec_stmt>"],
        TK_OP_DEC:          ["<prefix_incdec_stmt>"],
        TK_SYM_OPPAREN:     ["<paren_postfix_incdec_stmt>"],
    },

    "<prefix_incdec_stmt>": {
        TK_OP_INC: [TK_OP_INC, "<lvalue_core>", TK_SYM_SEMICOL],
        TK_OP_DEC: [TK_OP_DEC, "<lvalue_core>", TK_SYM_SEMICOL],
    },

    "<paren_postfix_incdec_stmt>": {
        TK_SYM_OPPAREN: [TK_SYM_OPPAREN, "<lvalue_core>", TK_SYM_CLSPAREN, "<postfix_inc_opt>", TK_SYM_SEMICOL],
    },

    "<stmt_id_tail>": {
        TK_SYM_OPPAREN: [TK_SYM_OPPAREN, "<arg_list_opt>", TK_SYM_CLSPAREN, "<access_chain_opt>", TK_SYM_SEMICOL],
        TK_SYM_OPBRACK: ["<access_chain_opt>", "<stmt_after_access>"],
        TK_SYM_DOT:     ["<access_chain_opt>", "<stmt_after_access>"],
        TK_OP_ASSIGN:   ["<access_chain_opt>", "<stmt_after_access>"],
        TK_OP_PLUS_EQ:  ["<access_chain_opt>", "<stmt_after_access>"],
        TK_OP_MINUS_EQ: ["<access_chain_opt>", "<stmt_after_access>"],
        TK_OP_MUL_EQ:   ["<access_chain_opt>", "<stmt_after_access>"],
        TK_OP_DIV_EQ:   ["<access_chain_opt>", "<stmt_after_access>"],
        TK_OP_MOD_EQ:   ["<access_chain_opt>", "<stmt_after_access>"],
        TK_OP_POW_EQ:   ["<access_chain_opt>", "<stmt_after_access>"],
        TK_OP_INC:      ["<access_chain_opt>", "<stmt_after_access>"],
        TK_OP_DEC:      ["<access_chain_opt>", "<stmt_after_access>"],
    },

    "<stmt_after_access>": {
        TK_OP_ASSIGN:   ["<assign_op>", "<expr>", TK_SYM_SEMICOL],
        TK_OP_PLUS_EQ:  ["<assign_op>", "<expr>", TK_SYM_SEMICOL],
        TK_OP_MINUS_EQ: ["<assign_op>", "<expr>", TK_SYM_SEMICOL],
        TK_OP_MUL_EQ:   ["<assign_op>", "<expr>", TK_SYM_SEMICOL],
        TK_OP_DIV_EQ:   ["<assign_op>", "<expr>", TK_SYM_SEMICOL],
        TK_OP_MOD_EQ:   ["<assign_op>", "<expr>", TK_SYM_SEMICOL],
        TK_OP_POW_EQ:   ["<assign_op>", "<expr>", TK_SYM_SEMICOL],

        TK_OP_INC:      [TK_OP_INC, TK_SYM_SEMICOL],
        TK_OP_DEC:      [TK_OP_DEC, TK_SYM_SEMICOL],
    },

    "<var_dec_stmt>": {
        TK_DTYPE_TALLY:     ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],
        TK_DTYPE_DIVINE:    ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],
        TK_DTYPE_SIGIL:     ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],
        TK_DTYPE_SCRIPTURE: ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],
        TK_DTYPE_VERITY:    ["<data_type>", "<var_decl_group>", TK_SYM_SEMICOL],
    },

    "<order_stmt>": {
        TK_OTHERS_ORDER: [TK_OTHERS_ORDER, TK_IDENTIFIER, TK_SYM_OPBRACE, "<member_list_opt>", TK_SYM_CLSBRACE, TK_SYM_SEMICOL]
    },

    "<ordain_stmt>": {
        TK_OTHERS_ORDAIN: [TK_OTHERS_ORDAIN, TK_IDENTIFIER, "<ordain_dec_list>", TK_SYM_SEMICOL]
    },

    "<ordain_dec_list>": {
        TK_IDENTIFIER: ["<ordain_dec>", "<ordain_dec_tail>"]
    },

    "<ordain_dec_tail>": {
        TK_SYM_COMMA:   [TK_SYM_COMMA, "<ordain_dec>", "<ordain_dec_tail>"],
        TK_SYM_SEMICOL: [EPSILON],
    },

    "<ordain_dec>": {
        TK_IDENTIFIER: [TK_IDENTIFIER, "<array_dims_tail>", "<ordain_init_opt>"]
    },

    "<ordain_init_opt>": {
        TK_OP_ASSIGN:   [TK_OP_ASSIGN, "<expr>"],
        TK_SYM_COMMA:   [EPSILON],
        TK_SYM_SEMICOL: [EPSILON],
    },

    "<io_stmt>": {
        TK_IO_RECEIVE:  [TK_IO_RECEIVE, TK_SYM_OPPAREN, "<lvalue>", TK_SYM_CLSPAREN, TK_SYM_SEMICOL],
        TK_IO_PROCLAIM: [TK_IO_PROCLAIM, TK_SYM_OPPAREN, "<output_list_opt>", TK_SYM_CLSPAREN, TK_SYM_SEMICOL],
    },

    "<output_list_opt>": {
        TK_OP_NOT:         ["<output_list>"],
        TK_OP_TILDE:       ["<output_list>"],
        TK_OP_INC:         ["<output_list>"],
        TK_OP_DEC:         ["<output_list>"],
        TK_SYM_OPPAREN:    ["<output_list>"],
        TK_IDENTIFIER:     ["<output_list>"],
        TK_OTHERS_VERSEOF: ["<output_list>"],
        TK_LIT_INT:        ["<output_list>"],
        TK_LIT_DECIMAL:    ["<output_list>"],
        TK_LIT_CHAR:       ["<output_list>"],
        TK_LIT_STRING:     ["<output_list>"],
        TK_OTHERS_HOLY:    ["<output_list>"],
        TK_OTHERS_UNHOLY:  ["<output_list>"],
        TK_SYM_CLSPAREN:   [EPSILON],
    },

    "<output_list>": {
        TK_OP_NOT:         ["<expr>", "<output_tail>"],
        TK_OP_TILDE:       ["<expr>", "<output_tail>"],
        TK_OP_INC:         ["<expr>", "<output_tail>"],
        TK_OP_DEC:         ["<expr>", "<output_tail>"],
        TK_SYM_OPPAREN:    ["<expr>", "<output_tail>"],
        TK_IDENTIFIER:     ["<expr>", "<output_tail>"],
        TK_OTHERS_VERSEOF: ["<expr>", "<output_tail>"],
        TK_LIT_INT:        ["<expr>", "<output_tail>"],
        TK_LIT_DECIMAL:    ["<expr>", "<output_tail>"],
        TK_LIT_CHAR:       ["<expr>", "<output_tail>"],
        TK_LIT_STRING:     ["<expr>", "<output_tail>"],
        TK_OTHERS_HOLY:    ["<expr>", "<output_tail>"],
        TK_OTHERS_UNHOLY:  ["<expr>", "<output_tail>"],
    },

    "<output_tail>": {
        TK_SYM_COMMA:    [TK_SYM_COMMA, "<expr>", "<output_tail>"],
        TK_SYM_CLSPAREN: [EPSILON],
    },

    # 12) CONDITIONS
    "<cond_stmt>": {
        TK_CF_DECREE:  ["<decree_chain>"],
        TK_CF_DISCERN: ["<discern_stmt>"],
    },

    "<decree_chain>": {
        TK_CF_DECREE: [
            TK_CF_DECREE, TK_SYM_OPPAREN, "<expr>", TK_SYM_CLSPAREN,
            TK_SYM_OPBRACE, "<statement_list>", TK_SYM_CLSBRACE,
            "<edict_list_opt>", "<absolution_opt>"
        ]
    },

    "<edict_list_opt>": {
        TK_CF_EDICT: ["<edict>", "<edict_list_opt>"],

        TK_CF_ABSOLUTION: [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],

        TK_DTYPE_TALLY:     [EPSILON],
        TK_DTYPE_DIVINE:    [EPSILON],
        TK_DTYPE_SIGIL:     [EPSILON],
        TK_DTYPE_SCRIPTURE: [EPSILON],
        TK_DTYPE_VERITY:    [EPSILON],

        TK_OTHERS_ORDER:    [EPSILON],
        TK_OTHERS_ORDAIN:   [EPSILON],
        TK_IO_RECEIVE:      [EPSILON],
        TK_IO_PROCLAIM:     [EPSILON],
        TK_CF_DECREE:       [EPSILON],
        TK_CF_DISCERN:      [EPSILON],
        TK_CF_PROCESSION:   [EPSILON],
        TK_CF_ENDURE:       [EPSILON],
        TK_CF_RITUAL:       [EPSILON],
        TK_CF_DISMISS:      [EPSILON],
        TK_CF_PROCEED:      [EPSILON],
        TK_CF_ABSOLVE:      [EPSILON],

        TK_IDENTIFIER:      [EPSILON],
        TK_OP_INC:          [EPSILON],
        TK_OP_DEC:          [EPSILON],
        TK_SYM_OPPAREN:     [EPSILON],
    },

    "<edict>": {
        TK_CF_EDICT: [TK_CF_EDICT, TK_SYM_OPPAREN, "<expr>", TK_SYM_CLSPAREN, TK_SYM_OPBRACE, "<statement_list>", TK_SYM_CLSBRACE]
    },

    "<absolution_opt>": {
        TK_CF_ABSOLUTION: [TK_CF_ABSOLUTION, TK_SYM_OPBRACE, "<statement_list>", TK_SYM_CLSBRACE],

        TK_SYM_CLSBRACE: [EPSILON],

        TK_DTYPE_TALLY:     [EPSILON],
        TK_DTYPE_DIVINE:    [EPSILON],
        TK_DTYPE_SIGIL:     [EPSILON],
        TK_DTYPE_SCRIPTURE: [EPSILON],
        TK_DTYPE_VERITY:    [EPSILON],

        TK_OTHERS_ORDER:    [EPSILON],
        TK_OTHERS_ORDAIN:   [EPSILON],
        TK_IO_RECEIVE:      [EPSILON],
        TK_IO_PROCLAIM:     [EPSILON],
        TK_CF_DECREE:       [EPSILON],
        TK_CF_DISCERN:      [EPSILON],
        TK_CF_PROCESSION:   [EPSILON],
        TK_CF_ENDURE:       [EPSILON],
        TK_CF_RITUAL:       [EPSILON],
        TK_CF_DISMISS:      [EPSILON],
        TK_CF_PROCEED:      [EPSILON],
        TK_CF_ABSOLVE:      [EPSILON],

        TK_IDENTIFIER:      [EPSILON],
        TK_OP_INC:          [EPSILON],
        TK_OP_DEC:          [EPSILON],
        TK_SYM_OPPAREN:     [EPSILON],
    },

    "<discern_stmt>": {
        TK_CF_DISCERN: [
            TK_CF_DISCERN, TK_SYM_OPPAREN, "<expr>", TK_SYM_CLSPAREN,
            TK_SYM_OPBRACE, "<verse_list>", "<grace_opt>", TK_SYM_CLSBRACE
        ]
    },

    "<verse_list>": {
        TK_CF_VERSE: [
            TK_CF_VERSE, "<literal_or_identifier>", TK_SYM_COLON,
            "<case_statement_list>", "<verse_end_opt>", "<verse_list>"
        ],
        TK_CF_GRACE:     [EPSILON],
        TK_SYM_CLSBRACE: [EPSILON],
    },

    "<case_statement_list>": {
        TK_DTYPE_TALLY:     ["<statement>", "<case_statement_list>"],
        TK_DTYPE_DIVINE:    ["<statement>", "<case_statement_list>"],
        TK_DTYPE_SIGIL:     ["<statement>", "<case_statement_list>"],
        TK_DTYPE_SCRIPTURE: ["<statement>", "<case_statement_list>"],
        TK_DTYPE_VERITY:    ["<statement>", "<case_statement_list>"],
        TK_OTHERS_ORDER:    ["<statement>", "<case_statement_list>"],
        TK_OTHERS_ORDAIN:   ["<statement>", "<case_statement_list>"],
        TK_IO_RECEIVE:      ["<statement>", "<case_statement_list>"],
        TK_IO_PROCLAIM:     ["<statement>", "<case_statement_list>"],
        TK_CF_DECREE:       ["<statement>", "<case_statement_list>"],
        TK_CF_DISCERN:      ["<statement>", "<case_statement_list>"],
        TK_CF_PROCESSION:   ["<statement>", "<case_statement_list>"],
        TK_CF_ENDURE:       ["<statement>", "<case_statement_list>"],
        TK_CF_RITUAL:       ["<statement>", "<case_statement_list>"],
        TK_CF_DISMISS:      ["<statement>", "<case_statement_list>"],
        TK_CF_PROCEED:      ["<statement>", "<case_statement_list>"],
        TK_IDENTIFIER:      ["<statement>", "<case_statement_list>"],
        TK_OP_INC:          ["<statement>", "<case_statement_list>"],
        TK_OP_DEC:          ["<statement>", "<case_statement_list>"],
        TK_SYM_OPPAREN:     ["<statement>", "<case_statement_list>"],

        TK_CF_ABSOLVE:   [EPSILON],
        TK_CF_FALL:      [EPSILON],
        TK_CF_VERSE:     [EPSILON],
        TK_CF_GRACE:     [EPSILON],
        TK_SYM_CLSBRACE: [EPSILON],
    },

    "<literal_or_identifier>": {
        TK_LIT_INT:       ["<literal>"],
        TK_LIT_DECIMAL:   ["<literal>"],
        TK_LIT_CHAR:      ["<literal>"],
        TK_LIT_STRING:    ["<literal>"],
        TK_OTHERS_HOLY:   ["<literal>"],
        TK_OTHERS_UNHOLY: ["<literal>"],
        TK_IDENTIFIER:    [TK_IDENTIFIER],
    },

    "<verse_end_opt>": {
        TK_CF_ABSOLVE:    ["<verse_end>"],
        TK_CF_FALL:       ["<verse_end>"],
        TK_CF_VERSE:      [EPSILON],
        TK_CF_GRACE:      [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
    },

    "<verse_end>": {
        TK_CF_ABSOLVE: [TK_CF_ABSOLVE, TK_SYM_SEMICOL],
        TK_CF_FALL:    [TK_CF_FALL,    TK_SYM_SEMICOL],
    },

    "<grace_opt>": {
        TK_CF_GRACE:     [TK_CF_GRACE, TK_SYM_COLON, "<case_statement_list>"],
        TK_SYM_CLSBRACE: [EPSILON],
    },

    # 13) LOOPS
    "<loop_stmt>": {
        TK_CF_PROCESSION: ["<procession_stmt>"],
        TK_CF_ENDURE:     ["<endure_stmt>"],
        TK_CF_RITUAL:     ["<ritual_stmt>"],
    },

    "<procession_stmt>": {
        TK_CF_PROCESSION: [
            TK_CF_PROCESSION, TK_SYM_OPPAREN, "<init_opt>", TK_SYM_SEMICOL, "<expr_opt>", TK_SYM_SEMICOL, "<update_opt>", TK_SYM_CLSPAREN,
            TK_SYM_OPBRACE, "<statement_list>", TK_SYM_CLSBRACE
        ]
    },

    "<init_opt>": {
        TK_DTYPE_TALLY:     ["<data_type>", TK_IDENTIFIER, TK_OP_ASSIGN, "<expr>"],
        TK_DTYPE_DIVINE:    ["<data_type>", TK_IDENTIFIER, TK_OP_ASSIGN, "<expr>"],
        TK_DTYPE_SIGIL:     ["<data_type>", TK_IDENTIFIER, TK_OP_ASSIGN, "<expr>"],
        TK_DTYPE_SCRIPTURE: ["<data_type>", TK_IDENTIFIER, TK_OP_ASSIGN, "<expr>"],
        TK_DTYPE_VERITY:    ["<data_type>", TK_IDENTIFIER, TK_OP_ASSIGN, "<expr>"],
        TK_IDENTIFIER:      ["<lvalue>", TK_OP_ASSIGN, "<expr>"],
        TK_SYM_SEMICOL:     [EPSILON],
    },

    "<expr_opt>": {
        # <expr> | λ
        TK_OP_NOT:         ["<expr>"],
        TK_OP_TILDE:       ["<expr>"],
        TK_OP_INC:         ["<expr>"],
        TK_OP_DEC:         ["<expr>"],
        TK_SYM_OPPAREN:    ["<expr>"],
        TK_IDENTIFIER:     ["<expr>"],
        TK_OTHERS_VERSEOF: ["<expr>"],
        TK_LIT_INT:        ["<expr>"],
        TK_LIT_DECIMAL:    ["<expr>"],
        TK_LIT_CHAR:       ["<expr>"],
        TK_LIT_STRING:     ["<expr>"],
        TK_OTHERS_HOLY:    ["<expr>"],
        TK_OTHERS_UNHOLY:  ["<expr>"],
        TK_SYM_SEMICOL:    [EPSILON],
    },

    "<update_opt>": {
        TK_IDENTIFIER:   ["<update_expr>"],
        TK_OP_INC:       ["<update_expr>"],
        TK_OP_DEC:       ["<update_expr>"],
        TK_SYM_OPPAREN:  ["<update_expr>"],
        TK_SYM_CLSPAREN: [EPSILON],
    },

    "<update_expr>": {
        TK_IDENTIFIER:  ["<lvalue>", "<update_tail>"],
        TK_OP_INC:      [TK_OP_INC, "<lvalue_core>"],
        TK_OP_DEC:      [TK_OP_DEC, "<lvalue_core>"],
        TK_SYM_OPPAREN: [TK_SYM_OPPAREN, "<update_expr>", TK_SYM_CLSPAREN],
    },

    "<update_tail>": {
        TK_OP_INC:      [TK_OP_INC],
        TK_OP_DEC:      [TK_OP_DEC],
        TK_OP_ASSIGN:   ["<assign_op>", "<expr>"],
        TK_OP_PLUS_EQ:  ["<assign_op>", "<expr>"],
        TK_OP_MINUS_EQ: ["<assign_op>", "<expr>"],
        TK_OP_MUL_EQ:   ["<assign_op>", "<expr>"],
        TK_OP_DIV_EQ:   ["<assign_op>", "<expr>"],
        TK_OP_MOD_EQ:   ["<assign_op>", "<expr>"],
        TK_OP_POW_EQ:   ["<assign_op>", "<expr>"],
    },

    "<endure_stmt>": {
        TK_CF_ENDURE: [TK_CF_ENDURE, TK_SYM_OPPAREN, "<expr>", TK_SYM_CLSPAREN, TK_SYM_OPBRACE, "<statement_list>", TK_SYM_CLSBRACE]
    },

    "<ritual_stmt>": {
        TK_CF_RITUAL: [TK_CF_RITUAL, TK_SYM_OPBRACE, "<statement_list>", TK_SYM_CLSBRACE, TK_CF_ENDURE, TK_SYM_OPPAREN, "<expr>", TK_SYM_CLSPAREN, TK_SYM_SEMICOL]
    },

    # 14) JUMPS + DISMISS OPT
    "<jump_stmt>": {
        TK_CF_DISMISS: [TK_CF_DISMISS, "<expr_opt>", TK_SYM_SEMICOL],
        TK_CF_PROCEED: [TK_CF_PROCEED, TK_SYM_SEMICOL],
        TK_CF_ABSOLVE: [TK_CF_ABSOLVE, TK_SYM_SEMICOL],
    },

    "<dismiss_opt>": {
        TK_CF_DISMISS:   [TK_CF_DISMISS, "<dismiss_tail>"],
        TK_SYM_CLSBRACE: [EPSILON],
    },

    "<dismiss_tail>": {
        TK_OP_NOT:         ["<expr>", TK_SYM_SEMICOL],
        TK_OP_TILDE:       ["<expr>", TK_SYM_SEMICOL],
        TK_OP_INC:         ["<expr>", TK_SYM_SEMICOL],
        TK_OP_DEC:         ["<expr>", TK_SYM_SEMICOL],
        TK_SYM_OPPAREN:    ["<expr>", TK_SYM_SEMICOL],
        TK_IDENTIFIER:     ["<expr>", TK_SYM_SEMICOL],
        TK_OTHERS_VERSEOF: ["<expr>", TK_SYM_SEMICOL],
        TK_LIT_INT:        ["<expr>", TK_SYM_SEMICOL],
        TK_LIT_DECIMAL:    ["<expr>", TK_SYM_SEMICOL],
        TK_LIT_CHAR:       ["<expr>", TK_SYM_SEMICOL],
        TK_LIT_STRING:     ["<expr>", TK_SYM_SEMICOL],
        TK_OTHERS_HOLY:    ["<expr>", TK_SYM_SEMICOL],
        TK_OTHERS_UNHOLY:  ["<expr>", TK_SYM_SEMICOL],
        TK_SYM_SEMICOL:    [TK_SYM_SEMICOL],
    },

    # 15) LVALUES / ACCESS / ASSIGN OPS
    "<lvalue>": {
        TK_IDENTIFIER: [TK_IDENTIFIER, "<access_chain_opt>"]
    },

    "<lvalue_core>": {
        TK_IDENTIFIER:  [TK_IDENTIFIER, "<access_chain_opt>"],
        TK_SYM_OPPAREN: [TK_SYM_OPPAREN, "<lvalue_core>", TK_SYM_CLSPAREN],
    },

    "<access_chain_opt>": {
        TK_SYM_OPBRACK: ["<access_chain>"],
        TK_SYM_DOT:     ["<access_chain>"],

        TK_OP_ASSIGN:    [EPSILON],
        TK_OP_PLUS_EQ:   [EPSILON],
        TK_OP_MINUS_EQ:  [EPSILON],
        TK_OP_MUL_EQ:    [EPSILON],
        TK_OP_DIV_EQ:    [EPSILON],
        TK_OP_MOD_EQ:    [EPSILON],
        TK_OP_POW_EQ:    [EPSILON],
        TK_OP_INC:       [EPSILON],
        TK_OP_DEC:       [EPSILON],

        TK_OP_AND:       [EPSILON],
        TK_OP_OR:        [EPSILON],

        TK_OP_EQ:        [EPSILON],
        TK_OP_NOT_EQ:    [EPSILON],
        TK_OP_GT:        [EPSILON],
        TK_OP_LT:        [EPSILON],
        TK_OP_GTE:       [EPSILON],
        TK_OP_LTE:       [EPSILON],
        TK_OP_PLUS:      [EPSILON],
        TK_OP_MINUS:     [EPSILON],
        TK_OP_MUL:       [EPSILON],
        TK_OP_DIV:       [EPSILON],
        TK_OP_MOD:       [EPSILON],
        TK_OP_POW:       [EPSILON],

        TK_SYM_CLSPAREN: [EPSILON],
        TK_SYM_SEMICOL:  [EPSILON],
        TK_SYM_COMMA:    [EPSILON],
        TK_SYM_CLSBRACK: [EPSILON],
        TK_SYM_CLSBRACE: [EPSILON],
        TK_SYM_COLON:    [EPSILON],
    },

    "<access_chain>": {
        TK_SYM_OPBRACK: ["<access_step>", "<access_chain_tail>"],
        TK_SYM_DOT:     ["<access_step>", "<access_chain_tail>"],
    },

    "<access_chain_tail>": {
        TK_SYM_OPBRACK: ["<access_step>", "<access_chain_tail>"],
        TK_SYM_DOT:     ["<access_step>", "<access_chain_tail>"],

        TK_OP_ASSIGN:    [EPSILON],
        TK_OP_PLUS_EQ:   [EPSILON],
        TK_OP_MINUS_EQ:  [EPSILON],
        TK_OP_MUL_EQ:    [EPSILON],
        TK_OP_DIV_EQ:    [EPSILON],
        TK_OP_MOD_EQ:    [EPSILON],
        TK_OP_POW_EQ:    [EPSILON],
        TK_OP_INC:       [EPSILON],
        TK_OP_DEC:       [EPSILON],

        TK_OP_AND:       [EPSILON],
        TK_OP_OR:        [EPSILON],

        TK_OP_EQ:        [EPSILON],
        TK_OP_NOT_EQ:    [EPSILON],
        TK_OP_GT:        [EPSILON],
        TK_OP_LT:        [EPSILON],
        TK_OP_GTE:       [EPSILON],
        TK_OP_LTE:       [EPSILON],
        TK_OP_PLUS:      [EPSILON],
        TK_OP_MINUS:     [EPSILON],
        TK_OP_MUL:       [EPSILON],
        TK_OP_DIV:       [EPSILON],
        TK_OP_MOD:       [EPSILON],
        TK_OP_POW:       [EPSILON],

        TK_SYM_CLSPAREN: [EPSILON],
        TK_SYM_SEMICOL:  [EPSILON],
        TK_SYM_COMMA:    [EPSILON],
        TK_SYM_CLSBRACK: [EPSILON],
        TK_SYM_CLSBRACE: [EPSILON],
        TK_SYM_COLON:    [EPSILON],
    },

    "<access_step>": {
        TK_SYM_OPBRACK: [TK_SYM_OPBRACK, "<expr>", TK_SYM_CLSBRACK],
        TK_SYM_DOT:     [TK_SYM_DOT, TK_IDENTIFIER],
    },

    "<assign_op>": {
        TK_OP_ASSIGN:   [TK_OP_ASSIGN],
        TK_OP_PLUS_EQ:  [TK_OP_PLUS_EQ],
        TK_OP_MINUS_EQ: [TK_OP_MINUS_EQ],
        TK_OP_MUL_EQ:   [TK_OP_MUL_EQ],
        TK_OP_DIV_EQ:   [TK_OP_DIV_EQ],
        TK_OP_MOD_EQ:   [TK_OP_MOD_EQ],
        TK_OP_POW_EQ:   [TK_OP_POW_EQ],
    },

    # 16) ARG LIST
    "<arg_list_opt>": {
        TK_OP_NOT:         ["<arg_list>"],
        TK_OP_TILDE:       ["<arg_list>"],
        TK_OP_INC:         ["<arg_list>"],
        TK_OP_DEC:         ["<arg_list>"],
        TK_SYM_OPPAREN:    ["<arg_list>"],
        TK_IDENTIFIER:     ["<arg_list>"],
        TK_OTHERS_VERSEOF: ["<arg_list>"],
        TK_LIT_INT:        ["<arg_list>"],
        TK_LIT_DECIMAL:    ["<arg_list>"],
        TK_LIT_CHAR:       ["<arg_list>"],
        TK_LIT_STRING:     ["<arg_list>"],
        TK_OTHERS_HOLY:    ["<arg_list>"],
        TK_OTHERS_UNHOLY:  ["<arg_list>"],
        TK_SYM_CLSPAREN:   [EPSILON],
    },

    "<arg_list>": {
        TK_OP_NOT:         ["<expr>", "<arg_list_tail>"],
        TK_OP_TILDE:       ["<expr>", "<arg_list_tail>"],
        TK_OP_INC:         ["<expr>", "<arg_list_tail>"],
        TK_OP_DEC:         ["<expr>", "<arg_list_tail>"],
        TK_SYM_OPPAREN:    ["<expr>", "<arg_list_tail>"],
        TK_IDENTIFIER:     ["<expr>", "<arg_list_tail>"],
        TK_OTHERS_VERSEOF: ["<expr>", "<arg_list_tail>"],
        TK_LIT_INT:        ["<expr>", "<arg_list_tail>"],
        TK_LIT_DECIMAL:    ["<expr>", "<arg_list_tail>"],
        TK_LIT_CHAR:       ["<expr>", "<arg_list_tail>"],
        TK_LIT_STRING:     ["<expr>", "<arg_list_tail>"],
        TK_OTHERS_HOLY:    ["<expr>", "<arg_list_tail>"],
        TK_OTHERS_UNHOLY:  ["<expr>", "<arg_list_tail>"],
    },

    "<arg_list_tail>": {
        TK_SYM_COMMA:    [TK_SYM_COMMA, "<expr>", "<arg_list_tail>"],
        TK_SYM_CLSPAREN: [EPSILON],
    },

    # 17) EXPR TREE (aligned names to DOC)
    "<expr>": {
        TK_OP_NOT:         ["<logic_or>"],
        TK_OP_TILDE:       ["<logic_or>"],
        TK_OP_INC:         ["<logic_or>"],
        TK_OP_DEC:         ["<logic_or>"],
        TK_SYM_OPPAREN:    ["<logic_or>"],
        TK_IDENTIFIER:     ["<logic_or>"],
        TK_OTHERS_VERSEOF: ["<logic_or>"],
        TK_LIT_INT:        ["<logic_or>"],
        TK_LIT_DECIMAL:    ["<logic_or>"],
        TK_LIT_CHAR:       ["<logic_or>"],
        TK_LIT_STRING:     ["<logic_or>"],
        TK_OTHERS_HOLY:    ["<logic_or>"],
        TK_OTHERS_UNHOLY:  ["<logic_or>"],
    },

    "<logic_or>": {
        TK_OP_NOT:         ["<logic_and>", "<logic_or_tail>"],
        TK_OP_TILDE:       ["<logic_and>", "<logic_or_tail>"],
        TK_OP_INC:         ["<logic_and>", "<logic_or_tail>"],
        TK_OP_DEC:         ["<logic_and>", "<logic_or_tail>"],
        TK_SYM_OPPAREN:    ["<logic_and>", "<logic_or_tail>"],
        TK_IDENTIFIER:     ["<logic_and>", "<logic_or_tail>"],
        TK_OTHERS_VERSEOF: ["<logic_and>", "<logic_or_tail>"],
        TK_LIT_INT:        ["<logic_and>", "<logic_or_tail>"],
        TK_LIT_DECIMAL:    ["<logic_and>", "<logic_or_tail>"],
        TK_LIT_CHAR:       ["<logic_and>", "<logic_or_tail>"],
        TK_LIT_STRING:     ["<logic_and>", "<logic_or_tail>"],
        TK_OTHERS_HOLY:    ["<logic_and>", "<logic_or_tail>"],
        TK_OTHERS_UNHOLY:  ["<logic_and>", "<logic_or_tail>"],
    },

    "<logic_or_tail>": {
        TK_OP_OR:         [TK_OP_OR, "<logic_and>", "<logic_or_tail>"],
        TK_SYM_CLSBRACK:  [EPSILON],
        TK_SYM_CLSPAREN:  [EPSILON],
        TK_SYM_SEMICOL:   [EPSILON],
        TK_SYM_COMMA:     [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
        TK_SYM_COLON:     [EPSILON],
    },

    "<logic_and>": {
        TK_OP_NOT:         ["<equality>", "<logic_and_tail>"],
        TK_OP_TILDE:       ["<equality>", "<logic_and_tail>"],
        TK_OP_INC:         ["<equality>", "<logic_and_tail>"],
        TK_OP_DEC:         ["<equality>", "<logic_and_tail>"],
        TK_SYM_OPPAREN:    ["<equality>", "<logic_and_tail>"],
        TK_IDENTIFIER:     ["<equality>", "<logic_and_tail>"],
        TK_OTHERS_VERSEOF: ["<equality>", "<logic_and_tail>"],
        TK_LIT_INT:        ["<equality>", "<logic_and_tail>"],
        TK_LIT_DECIMAL:    ["<equality>", "<logic_and_tail>"],
        TK_LIT_CHAR:       ["<equality>", "<logic_and_tail>"],
        TK_LIT_STRING:     ["<equality>", "<logic_and_tail>"],
        TK_OTHERS_HOLY:    ["<equality>", "<logic_and_tail>"],
        TK_OTHERS_UNHOLY:  ["<equality>", "<logic_and_tail>"],
    },

    "<logic_and_tail>": {
        TK_OP_AND:        [TK_OP_AND, "<equality>", "<logic_and_tail>"],
        TK_OP_OR:         [EPSILON],
        TK_SYM_CLSBRACK:  [EPSILON],
        TK_SYM_CLSPAREN:  [EPSILON],
        TK_SYM_SEMICOL:   [EPSILON],
        TK_SYM_COMMA:     [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
        TK_SYM_COLON:     [EPSILON],
    },

    "<equality>": {
        TK_OP_NOT:         ["<relational>", "<eq_op_opt>"],
        TK_OP_TILDE:       ["<relational>", "<eq_op_opt>"],
        TK_OP_INC:         ["<relational>", "<eq_op_opt>"],
        TK_OP_DEC:         ["<relational>", "<eq_op_opt>"],
        TK_SYM_OPPAREN:    ["<relational>", "<eq_op_opt>"],
        TK_IDENTIFIER:     ["<relational>", "<eq_op_opt>"],
        TK_OTHERS_VERSEOF: ["<relational>", "<eq_op_opt>"],
        TK_LIT_INT:        ["<relational>", "<eq_op_opt>"],
        TK_LIT_DECIMAL:    ["<relational>", "<eq_op_opt>"],
        TK_LIT_CHAR:       ["<relational>", "<eq_op_opt>"],
        TK_LIT_STRING:     ["<relational>", "<eq_op_opt>"],
        TK_OTHERS_HOLY:    ["<relational>", "<eq_op_opt>"],
        TK_OTHERS_UNHOLY:  ["<relational>", "<eq_op_opt>"],
    },

    "<eq_op_opt>": {
        TK_OP_EQ:         ["<eq_op>", "<relational>"],
        TK_OP_NOT_EQ:     ["<eq_op>", "<relational>"],
        TK_OP_AND:        [EPSILON],
        TK_OP_OR:         [EPSILON],
        TK_SYM_CLSBRACK:  [EPSILON],
        TK_SYM_CLSPAREN:  [EPSILON],
        TK_SYM_SEMICOL:   [EPSILON],
        TK_SYM_COMMA:     [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
        TK_SYM_COLON:     [EPSILON],
    },

    "<eq_op>": {
        TK_OP_EQ:     [TK_OP_EQ],
        TK_OP_NOT_EQ: [TK_OP_NOT_EQ],
    },

    "<relational>": {
        TK_OP_NOT:         ["<arith_expr>", "<rel_op_opt>"],
        TK_OP_TILDE:       ["<arith_expr>", "<rel_op_opt>"],
        TK_OP_INC:         ["<arith_expr>", "<rel_op_opt>"],
        TK_OP_DEC:         ["<arith_expr>", "<rel_op_opt>"],
        TK_SYM_OPPAREN:    ["<arith_expr>", "<rel_op_opt>"],
        TK_IDENTIFIER:     ["<arith_expr>", "<rel_op_opt>"],
        TK_OTHERS_VERSEOF: ["<arith_expr>", "<rel_op_opt>"],
        TK_LIT_INT:        ["<arith_expr>", "<rel_op_opt>"],
        TK_LIT_DECIMAL:    ["<arith_expr>", "<rel_op_opt>"],
        TK_LIT_CHAR:       ["<arith_expr>", "<rel_op_opt>"],
        TK_LIT_STRING:     ["<arith_expr>", "<rel_op_opt>"],
        TK_OTHERS_HOLY:    ["<arith_expr>", "<rel_op_opt>"],
        TK_OTHERS_UNHOLY:  ["<arith_expr>", "<rel_op_opt>"],
    },

    "<rel_op_opt>": {
        TK_OP_GT:         ["<rel_op>", "<arith_expr>"],
        TK_OP_LT:         ["<rel_op>", "<arith_expr>"],
        TK_OP_GTE:        ["<rel_op>", "<arith_expr>"],
        TK_OP_LTE:        ["<rel_op>", "<arith_expr>"],
        TK_OP_EQ:         [EPSILON],
        TK_OP_NOT_EQ:     [EPSILON],
        TK_OP_AND:        [EPSILON],
        TK_OP_OR:         [EPSILON],
        TK_SYM_CLSBRACK:  [EPSILON],
        TK_SYM_CLSPAREN:  [EPSILON],
        TK_SYM_SEMICOL:   [EPSILON],
        TK_SYM_COMMA:     [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
        TK_SYM_COLON:     [EPSILON],
    },

    "<rel_op>": {
        TK_OP_GT:  [TK_OP_GT],
        TK_OP_LT:  [TK_OP_LT],
        TK_OP_GTE: [TK_OP_GTE],
        TK_OP_LTE: [TK_OP_LTE],
    },

    "<arith_expr>": {
        TK_OP_NOT:         ["<mul_expr>", "<add_sub_tail>"],
        TK_OP_TILDE:       ["<mul_expr>", "<add_sub_tail>"],
        TK_OP_INC:         ["<mul_expr>", "<add_sub_tail>"],
        TK_OP_DEC:         ["<mul_expr>", "<add_sub_tail>"],
        TK_SYM_OPPAREN:    ["<mul_expr>", "<add_sub_tail>"],
        TK_IDENTIFIER:     ["<mul_expr>", "<add_sub_tail>"],
        TK_OTHERS_VERSEOF: ["<mul_expr>", "<add_sub_tail>"],
        TK_LIT_INT:        ["<mul_expr>", "<add_sub_tail>"],
        TK_LIT_DECIMAL:    ["<mul_expr>", "<add_sub_tail>"],
        TK_LIT_CHAR:       ["<mul_expr>", "<add_sub_tail>"],
        TK_LIT_STRING:     ["<mul_expr>", "<add_sub_tail>"],
        TK_OTHERS_HOLY:    ["<mul_expr>", "<add_sub_tail>"],
        TK_OTHERS_UNHOLY:  ["<mul_expr>", "<add_sub_tail>"],
    },

    "<add_sub_tail>": {
        TK_OP_PLUS:   [TK_OP_PLUS, "<mul_expr>", "<add_sub_tail>"],
        TK_OP_MINUS:  [TK_OP_MINUS, "<mul_expr>", "<add_sub_tail>"],
        TK_OP_CONCAT: [TK_OP_CONCAT, "<mul_expr>", "<add_sub_tail>"],

        TK_OP_GT:         [EPSILON],
        TK_OP_LT:         [EPSILON],
        TK_OP_GTE:        [EPSILON],
        TK_OP_LTE:        [EPSILON],
        TK_OP_EQ:         [EPSILON],
        TK_OP_NOT_EQ:     [EPSILON],
        TK_OP_AND:        [EPSILON],
        TK_OP_OR:         [EPSILON],
        TK_SYM_CLSBRACK:  [EPSILON],
        TK_SYM_CLSPAREN:  [EPSILON],
        TK_SYM_SEMICOL:   [EPSILON],
        TK_SYM_COMMA:     [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
        TK_SYM_COLON:     [EPSILON],
    },

    "<mul_expr>": {
        TK_OP_NOT:         ["<pow_expr>", "<mul_tail>"],
        TK_OP_TILDE:       ["<pow_expr>", "<mul_tail>"],
        TK_OP_INC:         ["<pow_expr>", "<mul_tail>"],
        TK_OP_DEC:         ["<pow_expr>", "<mul_tail>"],
        TK_SYM_OPPAREN:    ["<pow_expr>", "<mul_tail>"],
        TK_IDENTIFIER:     ["<pow_expr>", "<mul_tail>"],
        TK_OTHERS_VERSEOF: ["<pow_expr>", "<mul_tail>"],
        TK_LIT_INT:        ["<pow_expr>", "<mul_tail>"],
        TK_LIT_DECIMAL:    ["<pow_expr>", "<mul_tail>"],
        TK_LIT_CHAR:       ["<pow_expr>", "<mul_tail>"],
        TK_LIT_STRING:     ["<pow_expr>", "<mul_tail>"],
        TK_OTHERS_HOLY:    ["<pow_expr>", "<mul_tail>"],
        TK_OTHERS_UNHOLY:  ["<pow_expr>", "<mul_tail>"],
    },

    "<mul_tail>": {
        TK_OP_MUL: [TK_OP_MUL, "<pow_expr>", "<mul_tail>"],
        TK_OP_DIV: [TK_OP_DIV, "<pow_expr>", "<mul_tail>"],
        TK_OP_MOD: [TK_OP_MOD, "<pow_expr>", "<mul_tail>"],

        TK_OP_POW:        [EPSILON],
        TK_OP_PLUS:       [EPSILON],
        TK_OP_MINUS:      [EPSILON],
        TK_OP_CONCAT:     [EPSILON],
        TK_OP_GT:         [EPSILON],
        TK_OP_LT:         [EPSILON],
        TK_OP_GTE:        [EPSILON],
        TK_OP_LTE:        [EPSILON],
        TK_OP_EQ:         [EPSILON],
        TK_OP_NOT_EQ:     [EPSILON],
        TK_OP_AND:        [EPSILON],
        TK_OP_OR:         [EPSILON],
        TK_SYM_CLSBRACK:  [EPSILON],
        TK_SYM_CLSPAREN:  [EPSILON],
        TK_SYM_SEMICOL:   [EPSILON],
        TK_SYM_COMMA:     [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
        TK_SYM_COLON:     [EPSILON],
    },

    "<pow_expr>": {
        TK_OP_NOT:         ["<unary_expr>", "<pow_tail>"],
        TK_OP_TILDE:       ["<unary_expr>", "<pow_tail>"],
        TK_OP_INC:         ["<unary_expr>", "<pow_tail>"],
        TK_OP_DEC:         ["<unary_expr>", "<pow_tail>"],
        TK_SYM_OPPAREN:    ["<unary_expr>", "<pow_tail>"],
        TK_IDENTIFIER:     ["<unary_expr>", "<pow_tail>"],
        TK_OTHERS_VERSEOF: ["<unary_expr>", "<pow_tail>"],
        TK_LIT_INT:        ["<unary_expr>", "<pow_tail>"],
        TK_LIT_DECIMAL:    ["<unary_expr>", "<pow_tail>"],
        TK_LIT_CHAR:       ["<unary_expr>", "<pow_tail>"],
        TK_LIT_STRING:     ["<unary_expr>", "<pow_tail>"],
        TK_OTHERS_HOLY:    ["<unary_expr>", "<pow_tail>"],
        TK_OTHERS_UNHOLY:  ["<unary_expr>", "<pow_tail>"],
    },

    "<pow_tail>": {
        TK_OP_POW: [TK_OP_POW, "<pow_expr>"],

        TK_OP_MUL:        [EPSILON],
        TK_OP_DIV:        [EPSILON],
        TK_OP_MOD:        [EPSILON],
        TK_OP_PLUS:       [EPSILON],
        TK_OP_MINUS:      [EPSILON],
        TK_OP_CONCAT:     [EPSILON],
        TK_OP_GT:         [EPSILON],
        TK_OP_LT:         [EPSILON],
        TK_OP_GTE:        [EPSILON],
        TK_OP_LTE:        [EPSILON],
        TK_OP_EQ:         [EPSILON],
        TK_OP_NOT_EQ:     [EPSILON],
        TK_OP_AND:        [EPSILON],
        TK_OP_OR:         [EPSILON],
        TK_SYM_CLSBRACK:  [EPSILON],
        TK_SYM_CLSPAREN:  [EPSILON],
        TK_SYM_SEMICOL:   [EPSILON],
        TK_SYM_COMMA:     [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
        TK_SYM_COLON:     [EPSILON],
    },

    "<unary_expr>": {
        TK_OP_NOT:   [TK_OP_NOT, "<unary_expr>"],
        TK_OP_TILDE: [TK_OP_TILDE, "<unary_expr>"],

        TK_OP_INC: ["<prefix_unary>"],
        TK_OP_DEC: ["<prefix_unary>"],

        TK_SYM_OPPAREN:    ["<postfix_expr>"],
        TK_IDENTIFIER:     ["<postfix_expr>"],
        TK_OTHERS_VERSEOF: ["<postfix_expr>"],
        TK_LIT_INT:        ["<postfix_expr>"],
        TK_LIT_DECIMAL:    ["<postfix_expr>"],
        TK_LIT_CHAR:       ["<postfix_expr>"],
        TK_LIT_STRING:     ["<postfix_expr>"],
        TK_OTHERS_HOLY:    ["<postfix_expr>"],
        TK_OTHERS_UNHOLY:  ["<postfix_expr>"],
    },

    "<prefix_unary>": {
        TK_OP_INC: [TK_OP_INC, "<lvalue_core>"],
        TK_OP_DEC: [TK_OP_DEC, "<lvalue_core>"],
    },

    "<postfix_expr>": {
        TK_SYM_OPPAREN:    ["<primary>", "<postfix_inc_opt>"],
        TK_IDENTIFIER:     ["<primary>", "<postfix_inc_opt>"],
        TK_OTHERS_VERSEOF: ["<primary>", "<postfix_inc_opt>"],
        TK_LIT_INT:        ["<primary>", "<postfix_inc_opt>"],
        TK_LIT_DECIMAL:    ["<primary>", "<postfix_inc_opt>"],
        TK_LIT_CHAR:       ["<primary>", "<postfix_inc_opt>"],
        TK_LIT_STRING:     ["<primary>", "<postfix_inc_opt>"],
        TK_OTHERS_HOLY:    ["<primary>", "<postfix_inc_opt>"],
        TK_OTHERS_UNHOLY:  ["<primary>", "<postfix_inc_opt>"],
    },

    "<postfix_inc_opt>": {
        TK_OP_INC: [TK_OP_INC],
        TK_OP_DEC: [TK_OP_DEC],

        TK_OP_POW:        [EPSILON],
        TK_OP_MUL:        [EPSILON],
        TK_OP_DIV:        [EPSILON],
        TK_OP_MOD:        [EPSILON],
        TK_OP_PLUS:       [EPSILON],
        TK_OP_MINUS:      [EPSILON],
        TK_OP_CONCAT:     [EPSILON],
        TK_OP_GT:         [EPSILON],
        TK_OP_LT:         [EPSILON],
        TK_OP_GTE:        [EPSILON],
        TK_OP_LTE:        [EPSILON],
        TK_OP_EQ:         [EPSILON],
        TK_OP_NOT_EQ:     [EPSILON],
        TK_OP_AND:        [EPSILON],
        TK_OP_OR:         [EPSILON],
        TK_SYM_CLSBRACK:  [EPSILON],
        TK_SYM_CLSPAREN:  [EPSILON],
        TK_SYM_SEMICOL:   [EPSILON],
        TK_SYM_COMMA:     [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
        TK_SYM_COLON:     [EPSILON],
    },

    "<primary>": {
        TK_LIT_INT:       ["<literal>"],
        TK_LIT_DECIMAL:   ["<literal>"],
        TK_LIT_CHAR:      ["<literal>"],
        TK_LIT_STRING:    ["<literal>"],
        TK_OTHERS_HOLY:   ["<literal>"],
        TK_OTHERS_UNHOLY: ["<literal>"],

        TK_SYM_OPPAREN: [TK_SYM_OPPAREN, "<expr>", TK_SYM_CLSPAREN],
        TK_IDENTIFIER: [TK_IDENTIFIER, "<id_primary_tail>"],
        TK_OTHERS_VERSEOF: [TK_OTHERS_VERSEOF, TK_SYM_OPPAREN, "<expr>", TK_SYM_CLSPAREN],
    },

    "<id_primary_tail>": {
        TK_SYM_OPPAREN: [TK_SYM_OPPAREN, "<arg_list_opt>", TK_SYM_CLSPAREN, "<access_chain_opt>"],

        TK_SYM_OPBRACK: ["<access_chain_opt>"],
        TK_SYM_DOT:     ["<access_chain_opt>"],

        TK_OP_POW:        [EPSILON],
        TK_OP_MUL:        [EPSILON],
        TK_OP_DIV:        [EPSILON],
        TK_OP_MOD:        [EPSILON],
        TK_OP_PLUS:       [EPSILON],
        TK_OP_MINUS:      [EPSILON],
        TK_OP_CONCAT:     [EPSILON],
        TK_OP_GT:         [EPSILON],
        TK_OP_LT:         [EPSILON],
        TK_OP_GTE:        [EPSILON],
        TK_OP_LTE:        [EPSILON],
        TK_OP_EQ:         [EPSILON],
        TK_OP_NOT_EQ:     [EPSILON],
        TK_OP_AND:        [EPSILON],
        TK_OP_OR:         [EPSILON],
        TK_SYM_CLSBRACK:  [EPSILON],
        TK_SYM_CLSPAREN:  [EPSILON],
        TK_SYM_SEMICOL:   [EPSILON],
        TK_SYM_COMMA:     [EPSILON],
        TK_SYM_CLSBRACE:  [EPSILON],
        TK_SYM_COLON:     [EPSILON],
    },

    "<literal>": {
        TK_LIT_INT:     [TK_LIT_INT],
        TK_LIT_DECIMAL: [TK_LIT_DECIMAL],
        TK_LIT_CHAR:    [TK_LIT_CHAR],
        TK_LIT_STRING:  [TK_LIT_STRING],
        TK_OTHERS_HOLY: ["<bool_literal>"],
        TK_OTHERS_UNHOLY: ["<bool_literal>"],
    },

    "<bool_literal>": {
        TK_OTHERS_HOLY:   [TK_OTHERS_HOLY],
        TK_OTHERS_UNHOLY: [TK_OTHERS_UNHOLY],
    },

    # 18) CONST EXPR (DOC IX #239-273)
    "<const_expr>": {
        TK_OTHERS_HOLY:    ["<const_logic_or>"],
        TK_OTHERS_UNHOLY:  ["<const_logic_or>"],
        TK_LIT_INT:        ["<const_logic_or>"],
        TK_LIT_DECIMAL:    ["<const_logic_or>"],
        TK_LIT_CHAR:       ["<const_logic_or>"],
        TK_LIT_STRING:     ["<const_logic_or>"],
        TK_IDENTIFIER:     ["<const_logic_or>"],
        TK_SYM_OPPAREN:    ["<const_logic_or>"],
        TK_OP_NOT:         ["<const_logic_or>"],
        TK_OP_TILDE:       ["<const_logic_or>"],
    },

    "<const_logic_or>": {
        TK_OTHERS_HOLY:    ["<const_logic_and>", "<const_logic_or_tail>"],
        TK_OTHERS_UNHOLY:  ["<const_logic_and>", "<const_logic_or_tail>"],
        TK_LIT_INT:        ["<const_logic_and>", "<const_logic_or_tail>"],
        TK_LIT_DECIMAL:    ["<const_logic_and>", "<const_logic_or_tail>"],
        TK_LIT_CHAR:       ["<const_logic_and>", "<const_logic_or_tail>"],
        TK_LIT_STRING:     ["<const_logic_and>", "<const_logic_or_tail>"],
        TK_IDENTIFIER:     ["<const_logic_and>", "<const_logic_or_tail>"],
        TK_SYM_OPPAREN:    ["<const_logic_and>", "<const_logic_or_tail>"],
        TK_OP_NOT:         ["<const_logic_and>", "<const_logic_or_tail>"],
        TK_OP_TILDE:       ["<const_logic_and>", "<const_logic_or_tail>"],
    },

    "<const_logic_or_tail>": {
        TK_OP_OR:        [TK_OP_OR, "<const_logic_and>", "<const_logic_or_tail>"],
        TK_SYM_COMMA:    [EPSILON],
        TK_SYM_SEMICOL:  [EPSILON],
        TK_SYM_CLSPAREN: [EPSILON],
    },

    "<const_logic_and>": {
        TK_OTHERS_HOLY:    ["<const_equality>", "<const_logic_and_tail>"],
        TK_OTHERS_UNHOLY:  ["<const_equality>", "<const_logic_and_tail>"],
        TK_LIT_INT:        ["<const_equality>", "<const_logic_and_tail>"],
        TK_LIT_DECIMAL:    ["<const_equality>", "<const_logic_and_tail>"],
        TK_LIT_CHAR:       ["<const_equality>", "<const_logic_and_tail>"],
        TK_LIT_STRING:     ["<const_equality>", "<const_logic_and_tail>"],
        TK_IDENTIFIER:     ["<const_equality>", "<const_logic_and_tail>"],
        TK_SYM_OPPAREN:    ["<const_equality>", "<const_logic_and_tail>"],
        TK_OP_NOT:         ["<const_equality>", "<const_logic_and_tail>"],
        TK_OP_TILDE:       ["<const_equality>", "<const_logic_and_tail>"],
    },

    "<const_logic_and_tail>": {
        TK_OP_AND:      [TK_OP_AND, "<const_equality>", "<const_logic_and_tail>"],
        TK_OP_OR:       [EPSILON],
        TK_SYM_COMMA:   [EPSILON],
        TK_SYM_SEMICOL: [EPSILON],
        TK_SYM_CLSPAREN:[EPSILON],
    },

    "<const_equality>": {
        TK_OTHERS_HOLY:    ["<const_relational>", "<const_eq_opt>"],
        TK_OTHERS_UNHOLY:  ["<const_relational>", "<const_eq_opt>"],
        TK_LIT_INT:        ["<const_relational>", "<const_eq_opt>"],
        TK_LIT_DECIMAL:    ["<const_relational>", "<const_eq_opt>"],
        TK_LIT_CHAR:       ["<const_relational>", "<const_eq_opt>"],
        TK_LIT_STRING:     ["<const_relational>", "<const_eq_opt>"],
        TK_IDENTIFIER:     ["<const_relational>", "<const_eq_opt>"],
        TK_SYM_OPPAREN:    ["<const_relational>", "<const_eq_opt>"],
        TK_OP_NOT:         ["<const_relational>", "<const_eq_opt>"],
        TK_OP_TILDE:       ["<const_relational>", "<const_eq_opt>"],
    },

    "<const_eq_opt>": {
        TK_OP_EQ:      [TK_OP_EQ, "<const_relational>"],
        TK_OP_NOT_EQ:  [TK_OP_NOT_EQ, "<const_relational>"],
        TK_OP_AND:     [EPSILON],
        TK_OP_OR:      [EPSILON],
        TK_SYM_COMMA:  [EPSILON],
        TK_SYM_SEMICOL:[EPSILON],
        TK_SYM_CLSPAREN:[EPSILON],
    },

    "<const_relational>": {
        TK_OTHERS_HOLY:    ["<const_add>", "<const_rel_opt>"],
        TK_OTHERS_UNHOLY:  ["<const_add>", "<const_rel_opt>"],
        TK_LIT_INT:        ["<const_add>", "<const_rel_opt>"],
        TK_LIT_DECIMAL:    ["<const_add>", "<const_rel_opt>"],
        TK_LIT_CHAR:       ["<const_add>", "<const_rel_opt>"],
        TK_LIT_STRING:     ["<const_add>", "<const_rel_opt>"],
        TK_IDENTIFIER:     ["<const_add>", "<const_rel_opt>"],
        TK_SYM_OPPAREN:    ["<const_add>", "<const_rel_opt>"],
        TK_OP_NOT:         ["<const_add>", "<const_rel_opt>"],
        TK_OP_TILDE:       ["<const_add>", "<const_rel_opt>"],
    },

    "<const_rel_opt>": {
        TK_OP_LT:      [TK_OP_LT, "<const_add>"],
        TK_OP_LTE:     [TK_OP_LTE, "<const_add>"],
        TK_OP_GT:      [TK_OP_GT, "<const_add>"],
        TK_OP_GTE:     [TK_OP_GTE, "<const_add>"],
        TK_OP_EQ:      [EPSILON],
        TK_OP_NOT_EQ:  [EPSILON],
        TK_OP_AND:     [EPSILON],
        TK_OP_OR:      [EPSILON],
        TK_SYM_COMMA:  [EPSILON],
        TK_SYM_SEMICOL:[EPSILON],
        TK_SYM_CLSPAREN:[EPSILON],
    },

    "<const_add>": {
        TK_OTHERS_HOLY:    ["<const_mul>", "<const_add_tail>"],
        TK_OTHERS_UNHOLY:  ["<const_mul>", "<const_add_tail>"],
        TK_LIT_INT:        ["<const_mul>", "<const_add_tail>"],
        TK_LIT_DECIMAL:    ["<const_mul>", "<const_add_tail>"],
        TK_LIT_CHAR:       ["<const_mul>", "<const_add_tail>"],
        TK_LIT_STRING:     ["<const_mul>", "<const_add_tail>"],
        TK_IDENTIFIER:     ["<const_mul>", "<const_add_tail>"],
        TK_SYM_OPPAREN:    ["<const_mul>", "<const_add_tail>"],
        TK_OP_NOT:         ["<const_mul>", "<const_add_tail>"],
        TK_OP_TILDE:       ["<const_mul>", "<const_add_tail>"],
    },

    "<const_add_tail>": {
        TK_OP_PLUS:    [TK_OP_PLUS, "<const_mul>", "<const_add_tail>"],
        TK_OP_MINUS:   [TK_OP_MINUS, "<const_mul>", "<const_add_tail>"],
        TK_OP_LT:      [EPSILON],
        TK_OP_LTE:     [EPSILON],
        TK_OP_GT:      [EPSILON],
        TK_OP_GTE:     [EPSILON],
        TK_OP_EQ:      [EPSILON],
        TK_OP_NOT_EQ:  [EPSILON],
        TK_OP_AND:     [EPSILON],
        TK_OP_OR:      [EPSILON],
        TK_SYM_COMMA:  [EPSILON],
        TK_SYM_SEMICOL:[EPSILON],
        TK_SYM_CLSPAREN:[EPSILON],
    },

    "<const_mul>": {
        TK_OTHERS_HOLY:    ["<const_pow>", "<const_mul_tail>"],
        TK_OTHERS_UNHOLY:  ["<const_pow>", "<const_mul_tail>"],
        TK_LIT_INT:        ["<const_pow>", "<const_mul_tail>"],
        TK_LIT_DECIMAL:    ["<const_pow>", "<const_mul_tail>"],
        TK_LIT_CHAR:       ["<const_pow>", "<const_mul_tail>"],
        TK_LIT_STRING:     ["<const_pow>", "<const_mul_tail>"],
        TK_IDENTIFIER:     ["<const_pow>", "<const_mul_tail>"],
        TK_SYM_OPPAREN:    ["<const_pow>", "<const_mul_tail>"],
        TK_OP_NOT:         ["<const_pow>", "<const_mul_tail>"],
        TK_OP_TILDE:       ["<const_pow>", "<const_mul_tail>"],
    },

    "<const_mul_tail>": {
        TK_OP_MUL:     [TK_OP_MUL, "<const_pow>", "<const_mul_tail>"],
        TK_OP_DIV:     [TK_OP_DIV, "<const_pow>", "<const_mul_tail>"],
        TK_OP_MOD:     [TK_OP_MOD, "<const_pow>", "<const_mul_tail>"],
        TK_OP_PLUS:    [EPSILON],
        TK_OP_MINUS:   [EPSILON],
        TK_OP_LT:      [EPSILON],
        TK_OP_LTE:     [EPSILON],
        TK_OP_GT:      [EPSILON],
        TK_OP_GTE:     [EPSILON],
        TK_OP_EQ:      [EPSILON],
        TK_OP_NOT_EQ:  [EPSILON],
        TK_OP_AND:     [EPSILON],
        TK_OP_OR:      [EPSILON],
        TK_SYM_COMMA:  [EPSILON],
        TK_SYM_SEMICOL:[EPSILON],
        TK_SYM_CLSPAREN:[EPSILON],
    },

    "<const_pow>": {
        TK_OTHERS_HOLY:    ["<const_unary>", "<const_pow_tail>"],
        TK_OTHERS_UNHOLY:  ["<const_unary>", "<const_pow_tail>"],
        TK_LIT_INT:        ["<const_unary>", "<const_pow_tail>"],
        TK_LIT_DECIMAL:    ["<const_unary>", "<const_pow_tail>"],
        TK_LIT_CHAR:       ["<const_unary>", "<const_pow_tail>"],
        TK_LIT_STRING:     ["<const_unary>", "<const_pow_tail>"],
        TK_IDENTIFIER:     ["<const_unary>", "<const_pow_tail>"],
        TK_SYM_OPPAREN:    ["<const_unary>", "<const_pow_tail>"],
        TK_OP_NOT:         ["<const_unary>", "<const_pow_tail>"],
        TK_OP_TILDE:       ["<const_unary>", "<const_pow_tail>"],
    },

    "<const_pow_tail>": {
        TK_OP_POW:     [TK_OP_POW, "<const_pow>"],
        TK_OP_MUL:     [EPSILON],
        TK_OP_DIV:     [EPSILON],
        TK_OP_MOD:     [EPSILON],
        TK_OP_PLUS:    [EPSILON],
        TK_OP_MINUS:   [EPSILON],
        TK_OP_LT:      [EPSILON],
        TK_OP_LTE:     [EPSILON],
        TK_OP_GT:      [EPSILON],
        TK_OP_GTE:     [EPSILON],
        TK_OP_EQ:      [EPSILON],
        TK_OP_NOT_EQ:  [EPSILON],
        TK_OP_AND:     [EPSILON],
        TK_OP_OR:      [EPSILON],
        TK_SYM_COMMA:  [EPSILON],
        TK_SYM_SEMICOL:[EPSILON],
        TK_SYM_CLSPAREN:[EPSILON],
    },

    "<const_unary>": {
        TK_OP_TILDE: [TK_OP_TILDE, "<const_unary>"],
        TK_OP_NOT:   [TK_OP_NOT, "<const_unary>"],
        # else primary
        TK_OTHERS_HOLY:    ["<const_primary>"],
        TK_OTHERS_UNHOLY:  ["<const_primary>"],
        TK_LIT_INT:        ["<const_primary>"],
        TK_LIT_DECIMAL:    ["<const_primary>"],
        TK_LIT_CHAR:       ["<const_primary>"],
        TK_LIT_STRING:     ["<const_primary>"],
        TK_IDENTIFIER:     ["<const_primary>"],
        TK_SYM_OPPAREN:    ["<const_primary>"],
    },

    "<const_primary>": {
        TK_OTHERS_HOLY:   ["<literal>"],
        TK_OTHERS_UNHOLY: ["<literal>"],
        TK_LIT_INT:       ["<literal>"],
        TK_LIT_DECIMAL:   ["<literal>"],
        TK_LIT_CHAR:      ["<literal>"],
        TK_LIT_STRING:    ["<literal>"],
        TK_IDENTIFIER:    [TK_IDENTIFIER],
        TK_SYM_OPPAREN:   [TK_SYM_OPPAREN, "<const_expr>", TK_SYM_CLSPAREN],
    },
}