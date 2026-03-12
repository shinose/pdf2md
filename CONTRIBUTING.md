# Contributing to PDF2MD

Thank you for your interest in contributing to the PDF to Markdown Converter! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Git
- Basic understanding of Python, PDF processing, and Markdown

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/pdf2md.git
   cd pdf2md
   ```

2. **Set Up Development Environment**
   ```bash
   # Install dependencies
   ./setup.sh
   
   # Create a virtual environment (recommended)
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ./setup.sh
   ```

3. **Verify Setup**
   ```bash
   # Run tests to ensure everything works
   python3 test_converter.py
   
   # Create test PDF for development
   python3 create_test_pdf.py
   ```

## 📋 Development Workflow

### 1. Create a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### 2. Make Changes

- Follow the existing code style
- Add comments for complex logic
- Update documentation as needed
- Add tests for new functionality

### 3. Test Your Changes

```bash
# Run the test suite
python3 test_converter.py

# Test both GUI and CLI versions
python3 pdf2md_cli.py test_document.pdf
python3 pdf2md.py  # If you have a display

# Test edge cases and error conditions
```

### 4. Commit Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add feature: description of changes"
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create a pull request on GitHub
```

## 🎯 Contribution Areas

### Code Contributions

**GUI Improvements:**
- Enhanced user interface
- Better error handling
- Additional features (drag-and-drop, recent files, etc.)

**CLI Enhancements:**
- New command-line options
- Batch processing improvements
- Better progress reporting

**Core Functionality:**
- Improved PDF processing
- Better OCR integration
- Enhanced Markdown formatting
- Support for more PDF features

**Testing:**
- Additional test cases
- Better error simulation
- Performance tests

### Documentation Contributions

- Improve README.md
- Add code comments
- Create tutorials
- Update API documentation
- Add examples

### Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Operating system
   - Installed package versions

2. **Steps to Reproduce**
   - Clear, step-by-step instructions
   - Sample PDF file (if applicable)
   - Expected vs. actual behavior

3. **Error Messages**
   - Full error traceback
   - Any relevant logs

4. **Additional Context**
   - Things you've tried
   - Related issues

## 📝 Code Style Guidelines

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings for functions and classes

### Example Code Style

```python
def extract_text_from_pdf(pdf_path: str, ocr_enabled: bool = True) -> str:
    """
    Extract text from PDF file with optional OCR support.
    
    Args:
        pdf_path: Path to the PDF file
        ocr_enabled: Whether to use OCR for image text extraction
        
    Returns:
        Extracted text as HTML string
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If PDF file is corrupted
    """
    # Implementation here
    pass
```

### Documentation Style

- Use clear, concise language
- Include code examples
- Add emojis for better readability (as seen in README)
- Use proper markdown formatting

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
python3 test_converter.py

# Test specific functionality
python3 -c "
from pdf2md import PDF2MarkdownConverter
# Test specific features here
"
```

### Writing Tests

- Test both success and failure cases
- Include edge cases
- Test with different PDF types
- Mock external dependencies when appropriate

### Test File Structure

```python
def test_feature_name():
    """Test description"""
    # Arrange
    setup_code()
    
    # Act
    result = function_to_test()
    
    # Assert
    assert expected_result == result
```

## 🔧 Common Development Tasks

### Adding New CLI Options

1. Update `argparse` in `pdf2md_cli.py`
2. Add parameter handling
3. Update help text
4. Add tests

### Adding GUI Features

1. Modify `pdf2md.py` GUI class
2. Ensure cross-platform compatibility
3. Add error handling
4. Test with and without display

### Improving PDF Processing

1. Modify core processing logic in both files
2. Ensure backward compatibility
3. Add comprehensive tests
4. Update documentation

## 📦 Release Process

### Version Bumping

- Update version in README.md
- Update version history
- Tag the release

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated
- [ ] Release tagged on GitHub

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the community

### Communication

- Use clear, descriptive commit messages
- Explain the "why" behind changes
- Ask questions when unsure
- Share knowledge and help others

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Commit history
- Special thanks in documentation

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check existing documentation first
- **Code Comments**: Read code comments for implementation details

## 🔄 Review Process

### Pull Request Review

All pull requests go through review:

1. **Automated Checks**
   - Tests must pass
   - Code style checks
   - Documentation updates

2. **Manual Review**
   - Code quality assessment
   - Feature completeness
   - Documentation accuracy
   - Performance considerations

### Merge Requirements

- At least one approval from maintainers
- All discussions resolved
- Tests passing
- Documentation updated

---

Thank you for contributing to PDF2MD! Your contributions help make this project better for everyone. 🎉
