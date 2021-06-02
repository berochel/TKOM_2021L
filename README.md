# TKOM

#### libraries used:

- objbrowser
- argparse

#### tokenize text from file:

python -m lexer.main --file_path <PATH>

#### print with additional info:

python -m lexer.main -v

#### change default (64) identifier size:

python -m lexer.main --ident_length 64

#### change default (256) string size:

python -m lexer.main --ident_length 256

#### parser:

python -m my_parser.main --file_path <PATH>

#### change default (64) identifier size:

python -m my_parser.main --ident_length 64

#### change default (256) string size:

python -m my_parser.main --ident_length 256

#### interpreter:

python -m my_interpreter.main --file_path <PATH>

#### change default (64) identifier size:

python -m my_interpreter.main --ident_length 64

#### change default (256) string size:

python -m my_interpreter.main --ident_length 256
