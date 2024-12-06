import pytest
from input_validator.validators import (
    validate_sql_injection,
    validate_xss,
    validate_path_traversal,
    validate_command_injection,
    validate_nosql_injection
)

def test_validate_sql_injection():
    # Valid query
    assert validate_sql_injection("SELECT * FROM users") == "SELECT * FROM users"
    
    # SQL Injection patterns
    with pytest.raises(ValueError, match="Potential SQL Injection detected."):
        validate_sql_injection("SELECT * FROM users; DROP TABLE users;")
    with pytest.raises(ValueError, match="Potential SQL Injection detected."):
        validate_sql_injection("SELECT * FROM users WHERE id = 1 OR 1=1")

def test_validate_xss():
    # Valid input
    assert validate_xss("Hello, World!") == "Hello, World!"
    
    # XSS patterns
    with pytest.raises(ValueError, match="Potential XSS detected."):
        validate_xss("<script>alert('XSS')</script>")

def test_validate_path_traversal():
    # Valid path
    assert validate_path_traversal("safe/path") == "safe/path"
    
    # Path Traversal patterns
    with pytest.raises(ValueError, match="Potential Path Traversal detected."):
        validate_path_traversal("../etc/passwd")
    with pytest.raises(ValueError, match="Potential Path Traversal detected."):
        validate_path_traversal("/etc/passwd")

def test_validate_command_injection():
    # Valid command
    assert validate_command_injection("ls -l") == "ls -l"
    
    # Command Injection patterns
    with pytest.raises(ValueError, match="Potential Command Injection detected."):
        validate_command_injection("ls -l; rm -rf /")

def test_validate_nosql_injection():
    # Valid input
    assert validate_nosql_injection("{ 'name': 'John' }") == "{ 'name': 'John' }"
    
    # NoSQL Injection patterns
    with pytest.raises(ValueError, match="Potential NoSQL Injection detected."):
        validate_nosql_injection("{ '$where': 'this.credits < 100' }")
