# Duck Language Specification

## Overview

Duck Language (DL) is a simple, statically-typed programming language designed for educational purposes. It supports basic programming constructs including variables, arithmetic operations, control flow, and I/O operations.

## Lexical Elements

### Keywords

```
main      - Program entry point (reserved)
int       - Integer data type
boolean   - Boolean data type  
str       - String data type
if        - Conditional statement
else      - Alternative branch (reserved)
while     - Loop statement
read      - Input operation
print     - Output operation
True      - Boolean literal
False     - Boolean literal
```

### Identifiers

Identifiers must start with a letter and can contain letters and digits.

```
identifier ::= letter (letter | digit)*
letter     ::= 'a'..'z' | 'A'..'Z'  
digit      ::= '0'..'9'
```

Examples: `x`, `variable1`, `myVar`, `counter`

### Literals

#### Integer Literals
```
integer_literal ::= digit+
```
Examples: `42`, `0`, `256`

#### Boolean Literals
```
boolean_literal ::= 'True' | 'False'
```

#### String Literals
```
string_literal ::= '"' character* '"'
character      ::= any_character_except_quote
```
Examples: `"Hello, World!"`, `"Duck Language"`

### Operators

#### Arithmetic Operators
- `+` - Addition
- `-` - Subtraction  
- `*` - Multiplication
- `/` - Division

#### Comparison Operators
- `==` - Equal to
- `!=` - Not equal to
- `<`  - Less than
- `>`  - Greater than
- `<=` - Less than or equal to (reserved)
- `>=` - Greater than or equal to (reserved)

#### Logical Operators
- `&&` - Logical AND
- `||` - Logical OR (represented as `/&` in source)
- `!`  - Logical NOT

#### Assignment Operator
- `=` - Assignment

### Delimiters
- `(` `)` - Parentheses for grouping expressions and function calls
- `{` `}` - Braces for code blocks
- `;` - Statement terminator
- `,` - Parameter separator (reserved)

### Comments
- `//` - Single-line comment
- `/* */` - Multi-line comment

## Grammar

### Program Structure
```
program ::= declaration*

declaration ::= variable_declaration
              | assignment_statement  
              | control_statement
              | io_statement
```

### Variable Declarations
```
variable_declaration ::= type identifier ';'
                       | type identifier '=' expression ';'

type ::= 'int' | 'boolean' | 'str'
```

Examples:
```duck
int x;
int y = 42;
boolean flag = True;
str message = "Hello";
```

### Expressions
```
expression ::= logical_or_expression

logical_or_expression ::= logical_and_expression ('||' logical_and_expression)*

logical_and_expression ::= equality_expression ('&&' equality_expression)*

equality_expression ::= relational_expression (('==' | '!=') relational_expression)*

relational_expression ::= additive_expression (('<' | '>') additive_expression)*

additive_expression ::= multiplicative_expression (('+' | '-') multiplicative_expression)*

multiplicative_expression ::= unary_expression (('*' | '/') unary_expression)*

unary_expression ::= '!' unary_expression
                   | primary_expression

primary_expression ::= identifier
                     | integer_literal
                     | boolean_literal
                     | string_literal
                     | '(' expression ')'
```

### Statements

#### Assignment Statement
```
assignment_statement ::= identifier '=' expression ';'
```

#### Control Statements
```
if_statement ::= 'if' '(' expression ')' '{' statement* '}'

while_statement ::= 'while' '(' expression ')' '{' statement* '}'
```

#### I/O Statements
```
print_statement ::= 'print' '(' print_argument ('+ print_argument)* ')' ';'
print_argument  ::= expression | string_literal

read_statement ::= 'read' '(' identifier ')' ';'
```

## Type System

### Data Types

1. **int**: 16-bit signed integers (-32,768 to 32,767)
2. **boolean**: Boolean values (True or False)
3. **str**: String literals (read-only)

### Type Compatibility

- Arithmetic operations (`+`, `-`, `*`, `/`) are only valid for integer types
- Comparison operations can be used with same types
- Logical operations are only valid for boolean types
- String concatenation uses the `+` operator

### Type Checking Rules

1. Variables must be declared before use
2. Assignment requires type compatibility
3. Arithmetic expressions must use numeric types
4. Boolean expressions must use boolean types
5. String operations are limited to concatenation and display

## Scoping Rules

- All variables have global scope
- Variable names must be unique within the program
- Variables must be declared before first use

## Semantic Rules

### Variable Declaration
- A variable can only be declared once
- Variables can be declared with or without initialization
- Uninitialized variables have default values:
  - `int`: 0
  - `boolean`: False
  - `str`: empty string

### Expressions
- All operands in arithmetic expressions must be integers
- Boolean expressions can use logical operators
- Parentheses override default operator precedence

### Control Flow
- Condition expressions in `if` and `while` statements must evaluate to boolean
- Code blocks are delimited by braces `{}`

### I/O Operations
- `print()` can output variables, literals, and concatenated expressions
- `read()` can only read into previously declared variables
- Reading into a variable marks it as "requires input"

## Operator Precedence

From highest to lowest precedence:

1. `()` - Parentheses
2. `!` - Logical NOT
3. `*`, `/` - Multiplication, Division
4. `+`, `-` - Addition, Subtraction  
5. `<`, `>` - Relational operators
6. `==`, `!=` - Equality operators
7. `&&` - Logical AND
8. `||` - Logical OR
9. `=` - Assignment

## Error Handling

### Compile-time Errors
- Syntax errors (malformed statements)
- Undeclared variables
- Type mismatches
- Unbalanced parentheses or braces
- Duplicate variable declarations

### Runtime Considerations
- Division by zero (undefined behavior)
- Integer overflow (undefined behavior)

## Example Program

```duck
// Calculate factorial iteratively
int n = 5;
int factorial = 1;
int i = 1;

print("Calculating factorial of " + n);

while(i <= n) {
    factorial = factorial * i;
    i = i + 1;
}

print("Result: " + factorial);
```

## Reserved for Future Extensions

- `else` clause for if statements
- `<=`, `>=` comparison operators
- Function definitions and calls
- Arrays and data structures
- `main()` function entry point
- Local variable scoping 