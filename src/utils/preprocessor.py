"""
Source Code Preprocessor

This module handles preprocessing of source code files, including:
- Comment removal (single-line # and multi-line /* */)
- Whitespace normalization
- Line numbering
- Bracket balance validation
- Empty line removal
"""

import re
from typing import Dict, List, Tuple


class SourcePreprocessor:
    """Preprocesses source code files for compilation."""
    
    def __init__(self):
        self.bracket_stack = []
        self.line_count = 1
        
    def remove_comments(self, source_code: str) -> str:
        """
        Remove comments from source code while preserving strings.
        
        Args:
            source_code: The source code string
            
        Returns:
            Source code with comments removed
        """
        # Pattern captures strings in quotes (group 1) or comments (group 2)
        pattern = r'(\".*?\"|\'.*?\')|(/\*.*?\*/|#[^\r\n]*$)'
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
        
        def comment_replacer(match):
            """Replace comments with empty string, preserve strings."""
            if match.group(2) is not None:
                # This is a comment, remove it
                return ""
            else:
                # This is a string, preserve it
                return match.group(1)
                
        return regex.sub(comment_replacer, source_code)
    
    def validate_brackets(self, line: str) -> bool:
        """
        Validate bracket balance for a single line.
        
        Args:
            line: Source code line
            
        Returns:
            True if brackets are balanced so far
        """
        opening_brackets = re.findall(r'{', line)
        closing_brackets = re.findall(r'}', line)
        
        # Add opening brackets to stack
        for _ in opening_brackets:
            self.bracket_stack.append('{')
            
        # Remove closing brackets from stack
        for _ in closing_brackets:
            try:
                self.bracket_stack.pop()
            except IndexError:
                print("Error: Unbalanced brackets detected.")
                return False
                
        return True
    
    def normalize_line(self, line: str) -> str:
        """
        Normalize a line by removing extra whitespace.
        
        Args:
            line: Source code line
            
        Returns:
            Normalized line
        """
        # Remove leading whitespace and normalize multiple spaces
        normalized = line.lstrip(' ')
        normalized = " ".join(normalized.split())
        return normalized
    
    def remove_empty_lines(self, line_dict: Dict[int, str]) -> Dict[int, str]:
        """
        Remove empty lines from the line dictionary.
        
        Args:
            line_dict: Dictionary mapping line numbers to content
            
        Returns:
            Dictionary with empty lines removed
        """
        return {k: v for k, v in line_dict.items() if v.strip()}
    
    def preprocess_file(self, filename: str) -> bool:
        """
        Preprocess a source file and save the result.
        
        Args:
            filename: Input filename (without extension)
            
        Returns:
            True if preprocessing was successful
        """
        try:
            # Read source file
            with open(f"{filename}", "r", encoding='utf-8') as file:
                source_code = file.read()
            
            # Reset state
            self.bracket_stack = []
            self.line_count = 1
            
            # Remove comments
            source_code = self.remove_comments(source_code)
            
            # Process line by line
            line_dict = {}
            
            for line in source_code.split("\n"):
                # Normalize line
                normalized_line = self.normalize_line(line)
                line_dict[self.line_count] = normalized_line
                
                # Validate brackets
                if not self.validate_brackets(line):
                    return False
                    
                self.line_count += 1
            
            # Check final bracket balance
            if len(self.bracket_stack) > 0:
                print("Error: Unbalanced brackets - missing closing brackets.")
                return False
            
            # Remove empty lines
            line_dict = self.remove_empty_lines(line_dict)
            
            # Generate output
            output_lines = []
            for line_num in sorted(line_dict.keys()):
                if line_dict[line_num]:  # Only add non-empty lines
                    output_lines.append(f"{line_num}: {line_dict[line_num]}")
            
            # Write preprocessed file
            output_filename = f"{filename}d"  # Add 'd' suffix for 'debugged'
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write('\n'.join(output_lines))
            
            print(f"Preprocessing completed successfully. Output: {output_filename}")
            return True
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return False
        except Exception as e:
            print(f"Error during preprocessing: {str(e)}")
            return False


def preprocess_source(filename: str) -> bool:
    """
    Convenience function to preprocess a source file.
    
    Args:
        filename: Source file to preprocess
        
    Returns:
        True if successful
    """
    preprocessor = SourcePreprocessor()
    return preprocessor.preprocess_file(filename)


if __name__ == "__main__":
    # Example usage
    preprocess_source('test.dl') 