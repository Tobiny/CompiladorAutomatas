"""
File Buffer Utility

This module provides buffered file reading capabilities for the compiler.
It reads files in chunks to manage memory efficiently for large source files.
"""

from typing import Generator, Optional
import os


class FileBuffer:
    """
    A file buffer that reads source files in configurable chunks.
    Useful for processing large files without loading everything into memory.
    """
    
    def __init__(self, chunk_size: int = 10):
        """
        Initialize the file buffer.
        
        Args:
            chunk_size: Number of lines to read in each chunk
        """
        self.chunk_size = chunk_size
    
    def load_buffer(self, filename: str) -> Generator[str, None, None]:
        """
        Load file content in chunks.
        
        Args:
            filename: Path to the file to read
            
        Yields:
            String chunks of the file content
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            IOError: If there's an error reading the file
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' not found")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                buffer = []
                line_count = 0
                
                for line in file:
                    buffer.append(line)
                    line_count += 1
                    
                    # Yield chunk when buffer is full or at end of file
                    if line_count == self.chunk_size:
                        yield ''.join(buffer)
                        buffer = []
                        line_count = 0
                
                # Yield remaining lines if any
                if buffer:
                    yield ''.join(buffer)
                    
        except IOError as e:
            raise IOError(f"Error reading file '{filename}': {str(e)}")
    
    def read_entire_file(self, filename: str) -> str:
        """
        Read the entire file content at once.
        
        Args:
            filename: Path to the file to read
            
        Returns:
            Complete file content as string
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            IOError: If there's an error reading the file
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' not found")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            raise IOError(f"Error reading file '{filename}': {str(e)}")
    
    def read_lines(self, filename: str) -> list:
        """
        Read all lines from file as a list.
        
        Args:
            filename: Path to the file to read
            
        Returns:
            List of lines from the file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            IOError: If there's an error reading the file
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' not found")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.readlines()
        except IOError as e:
            raise IOError(f"Error reading file '{filename}': {str(e)}")


def create_file_buffer(chunk_size: int = 10) -> FileBuffer:
    """
    Factory function to create a FileBuffer instance.
    
    Args:
        chunk_size: Number of lines per chunk
        
    Returns:
        FileBuffer instance
    """
    return FileBuffer(chunk_size)


if __name__ == "__main__":
    # Example usage
    buffer = FileBuffer(5)  # 5 lines per chunk
    
    try:
        for chunk in buffer.load_buffer('test.dl'):
            print("Chunk:")
            print(chunk)
            print("-" * 40)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except IOError as e:
        print(f"Error: {e}") 