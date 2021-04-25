# TKOM

#### tokenize text from file:
python -m lexer.main --file_path <PATH>
#### tokenize text from stdin:
python -m lexer.main --input_type stdin
#### print with additional info:
python -m lexer.main -v
#### change default (64) identifier size:
python -m lexer.main -ident_length 64
#### change default (256) string size:
python -m lexer.main -ident_length 256
