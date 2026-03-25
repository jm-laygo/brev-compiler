from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

PROJECT_ROOT = next(
    (parent for parent in Path(__file__).resolve().parents if (parent / "backend").is_dir()),
    None,
)

if PROJECT_ROOT and str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.errors import LexicalError, ParserError
from backend.lexer.lexer import Lexer
from backend.parser.predict_set import EPSILON, PREDICT
from backend.tokens import (
    TK_COMMENT,
    TK_COMMENT_BLOCK,
    TK_EOF,
    TK_SYM_NEWLINE,
    TK_SYM_SPACE,
    TK_SYM_TAB,
    TOKEN_DISPLAY_NAMES,
    Token,
)

SKIP_TYPES = {TK_SYM_SPACE, TK_SYM_TAB, TK_SYM_NEWLINE, TK_COMMENT, TK_COMMENT_BLOCK}

EXPR_HELPER_NONTERMINALS = {
    "<expr>",
    "<logic_or>",
    "<logic_or_tail>",
    "<logic_and>",
    "<logic_and_tail>",
    "<equality>",
    "<eq_op_opt>",
    "<relational>",
    "<rel_op_opt>",
    "<arith_expr>",
    "<add_sub_tail>",
    "<mul_expr>",
    "<mul_tail>",
    "<pow_expr>",
    "<pow_tail>",
    "<unary_expr>",
    "<postfix_expr>",
    "<postfix_inc_opt>",
    "<primary>",
    "<literal>",
}

EXPR_CHAIN_START = "<expr>"

MANUAL_SOURCE_CODE = """
    rite tally genesis() {
        tally age = 10;
        dismiss 0;
        }

"""


@dataclass
class ProductionStep:
    step_no: int
    nonterminal: str
    lookahead: str
    lookahead_lexeme: str
    production_no: int
    rhs: Sequence[str]


@dataclass
class MatchStep:
    step_no: int
    terminal: str
    lexeme: str


def _display_token(token_type: str) -> str:
    return TOKEN_DISPLAY_NAMES.get(token_type, token_type)


def _is_nonterminal(symbol: str) -> bool:
    return symbol.startswith("<") and symbol.endswith(">")


def _token_lexeme(token: Token) -> str:
    if token.type == TK_EOF:
        return "<EOF>"
    if token.value is None:
        return ""
    return str(token.value)


def tokenize_for_cfg(source_code: str) -> List[Token]:
    lexer = Lexer(source_code)
    token_list, lexer_errors = lexer.make_tokens()

    if lexer_errors:
        first_error = lexer_errors[0]
        if isinstance(first_error, LexicalError):
            raise first_error
        raise LexicalError(None, str(first_error))

    return [token for token in token_list if token.type not in SKIP_TYPES]


def build_production_numbers() -> Tuple[Dict[Tuple[str, Tuple[str, ...]], int], List[Tuple[int, str, Sequence[str]]]]:
    numbering: Dict[Tuple[str, Tuple[str, ...]], int] = {}
    ordered: List[Tuple[int, str, Sequence[str]]] = []
    next_number = 1

    for nonterminal, predict_row in PREDICT.items():
        for rhs in predict_row.values():
            key = (nonterminal, tuple(rhs))
            if key in numbering:
                continue
            numbering[key] = next_number
            ordered.append((next_number, nonterminal, rhs))
            next_number += 1

    return numbering, ordered


def cfg_trace(tokens: Sequence[Token]) -> Tuple[List[ProductionStep], List[MatchStep]]:
    production_no_by_rule, _ = build_production_numbers()

    stack: List[str] = [TK_EOF, "<program>"]
    token_index = 0
    production_steps: List[ProductionStep] = []
    match_steps: List[MatchStep] = []
    step_counter = 1

    while stack:
        symbol = stack.pop()
        lookahead_token = tokens[token_index] if token_index < len(tokens) else None
        lookahead_type = lookahead_token.type if lookahead_token is not None else None

        if symbol == EPSILON:
            continue

        if _is_nonterminal(symbol):
            predict_row = PREDICT.get(symbol)
            if predict_row is None:
                raise ParserError(lookahead_token, expected=[], details=f"Missing PREDICT row for {symbol}")

            rhs = predict_row.get(lookahead_type)
            if rhs is None:
                raise ParserError(lookahead_token, expected=list(predict_row.keys()))

            production_no = production_no_by_rule[(symbol, tuple(rhs))]
            production_steps.append(
                ProductionStep(
                    step_no=step_counter,
                    nonterminal=symbol,
                    lookahead=lookahead_type,
                    lookahead_lexeme=_token_lexeme(lookahead_token) if lookahead_token is not None else "",
                    production_no=production_no,
                    rhs=rhs,
                )
            )
            step_counter += 1

            for rhs_symbol in reversed(rhs):
                if rhs_symbol != EPSILON:
                    stack.append(rhs_symbol)
            continue

        if lookahead_type != symbol:
            raise ParserError(lookahead_token, expected=[symbol])

        match_steps.append(
            MatchStep(
                step_no=step_counter,
                terminal=symbol,
                lexeme=_token_lexeme(lookahead_token),
            )
        )
        step_counter += 1
        token_index += 1

    if token_index != len(tokens):
        next_token = tokens[token_index]
        raise ParserError(next_token, expected=[TK_EOF], details="Unconsumed tokens remain after CFG simulation")

    return production_steps, match_steps


def simplify_for_professor_mode(production_steps: Sequence[ProductionStep]) -> List[ProductionStep]:
    simplified: List[ProductionStep] = []

    for step in production_steps:
        if list(step.rhs) == [EPSILON]:
            continue

        if step.nonterminal in EXPR_HELPER_NONTERMINALS:
            continue

        simplified.append(step)

    return simplified


def collapse_expression_chains(production_steps: Sequence[ProductionStep]) -> List[ProductionStep]:
    collapsed: List[ProductionStep] = []
    i = 0

    while i < len(production_steps):
        step = production_steps[i]

        if step.nonterminal == EXPR_CHAIN_START and list(step.rhs) == ["<logic_or>"]:
            j = i + 1
            while j < len(production_steps) and production_steps[j].nonterminal in EXPR_HELPER_NONTERMINALS:
                j += 1

            token_desc = _display_token(step.lookahead)
            summary_rhs = ["...", "<primary>", "<literal>", token_desc]

            collapsed.append(
                ProductionStep(
                    step_no=step.step_no,
                    nonterminal=step.nonterminal,
                    lookahead=step.lookahead,
                    lookahead_lexeme=step.lookahead_lexeme,
                    production_no=step.production_no,
                    rhs=summary_rhs,
                )
            )
            i = j
            continue

        collapsed.append(step)
        i += 1

    return collapsed


def format_trace(production_steps: Sequence[ProductionStep]) -> str:
    def build_table(headers: Sequence[str], rows: Sequence[Sequence[str]], max_width_by_col: Sequence[int]) -> str:
        widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = min(max(widths[i], len(cell)), max_width_by_col[i])

        def border() -> str:
            return "+" + "+".join("-" * (width + 2) for width in widths) + "+"

        def render_row(cells: Sequence[str]) -> List[str]:
            wrapped_cells = []
            for i, cell in enumerate(cells):
                wrapped = textwrap.wrap(cell, width=widths[i], break_long_words=True, break_on_hyphens=False)
                wrapped_cells.append(wrapped or [""])

            row_height = max(len(cell_lines) for cell_lines in wrapped_cells)
            output_lines: List[str] = []

            for line_index in range(row_height):
                line_cells = []
                for col_index in range(len(cells)):
                    cell_lines = wrapped_cells[col_index]
                    part = cell_lines[line_index] if line_index < len(cell_lines) else ""
                    line_cells.append(part.ljust(widths[col_index]))
                output_lines.append("| " + " | ".join(line_cells) + " |")

            return output_lines

        lines: List[str] = [border()]
        lines.extend(render_row(headers))
        lines.append(border())
        for row in rows:
            lines.extend(render_row(row))
        lines.append(border())
        return "\n".join(lines)

    production_rows = []
    for visible_step_no, step in enumerate(production_steps, start=1):
        token_cell = _display_token(step.lookahead)
        if step.lookahead_lexeme and step.lookahead_lexeme != "<EOF>":
            token_cell = f"{token_cell} ({step.lookahead_lexeme})"

        production_rows.append(
            [
                str(visible_step_no),
                str(step.production_no),
                step.nonterminal,
                f"{step.production_no} {step.nonterminal} -> {' '.join(step.rhs)}",
                token_cell,
            ]
        )

    lines: List[str] = ["CFG step-by-step derivation", ""]
    lines.append(
        build_table(
            ["Step", "Production #", "Non-terminal", "Production Rule", "Terminal / Token"],
            production_rows,
            [5, 12, 18, 40, 22],
        )
    )
    return "\n".join(lines)


def read_source(args: argparse.Namespace) -> str:
    if args.file:
        with open(args.file, "r", encoding="utf-8") as source_file:
            return source_file.read()

    if args.stdin:
        if not sys.stdin.isatty():
            return sys.stdin.read()
        print("Paste Brev program. End input with Ctrl+Z then Enter (Windows) or Ctrl+D (Unix).")
        return sys.stdin.read()

    if MANUAL_SOURCE_CODE.strip():
        return MANUAL_SOURCE_CODE

    if not sys.stdin.isatty():
        return sys.stdin.read()

    print("Paste Brev program. End input with Ctrl+Z then Enter (Windows) or Ctrl+D (Unix).")
    return sys.stdin.read()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Simulate LL(1) CFG expansion for Brev source and print production mapping trace."
    )
    parser.add_argument("-f", "--file", help="Path to a Brev source file. If omitted, reads from stdin.")
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Force reading source from stdin, ignoring MANUAL_SOURCE_CODE.",
    )
    parser.add_argument(
        "--show-productions",
        action="store_true",
        help="Print the grammar's production number mapping before the trace.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Show shortened output (hides lambda and expression-helper expansions).",
    )
    parser.add_argument(
        "--no-collapse-expr",
        action="store_true",
        help="Disable expression-chain collapsing and show each expression helper production explicitly.",
    )
    args = parser.parse_args()

    try:
        source_code = read_source(args)
        tokens = tokenize_for_cfg(source_code)
        production_steps, _ = cfg_trace(tokens)

        if args.compact:
            production_steps = simplify_for_professor_mode(production_steps)

        if not args.no_collapse_expr:
            production_steps = collapse_expression_chains(production_steps)

        if args.show_productions:
            _, ordered = build_production_numbers()
            print("Production number map")
            print("=" * 72)
            for number, nonterminal, rhs in ordered:
                print(f"P#{number:03} | {nonterminal} -> {' '.join(rhs)}")
            print("=" * 72)

        print(format_trace(production_steps))
        return 0

    except (LexicalError, ParserError) as parse_error:
        if hasattr(parse_error, "as_string"):
            print(parse_error.as_string(), file=sys.stderr)
        else:
            print(str(parse_error), file=sys.stderr)
        return 1
    except Exception as generic_error:
        print(f"CFG trace failed: {generic_error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
