# Contributing to Cloud Custodian Documentation

Thank you for your interest in contributing to the Cloud Custodian Documentation project! This guide will help you get started.

## How to Contribute

### Documentation Updates
- **Resource Documentation**: Update or add new AWS resource documentation in the `resourcetype/` directory
- **General Guides**: Improve or add new guides in the `documentation/` directory
- **Examples**: Contribute real-world policy examples and use cases

### Script Improvements
- **Schema Generation**: Enhance the scripts in the `scripts/` directory
- **Automation**: Add new utilities for documentation maintenance
- **Bug Fixes**: Fix issues in existing automation scripts

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/csnayak/cc-documentation.git
   cd cc-documentation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Cloud Custodian** (for schema generation):
   ```bash
   pip install c7n
   ```

## Documentation Standards

### File Naming
- Use lowercase with hyphens: `aws.s3-bucket.md`
- Follow the pattern: `aws.[service-name].md` for AWS resources
- Use descriptive names for general documentation

### Content Structure
- Start with a clear title and description
- Include practical examples
- Add cross-references to related resources
- Follow consistent formatting

### Markdown Guidelines
- Use proper heading hierarchy (H1 for title, H2 for main sections)
- Include code blocks with appropriate syntax highlighting
- Add tables for structured information
- Use bullet points for lists

## Testing Documentation

### Schema Validation
Run the schema generation scripts to ensure accuracy:
```bash
cd scripts
python main.py
```

### Link Checking
Verify that all internal links work correctly before submitting.

## Submission Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Make** your changes
4. **Test** your changes
5. **Commit** with clear messages: `git commit -m "Add documentation for AWS Lambda"`
6. **Push** to your fork: `git push origin feature/your-feature-name`
7. **Submit** a pull request

## Pull Request Guidelines

- Provide a clear description of changes
- Reference any related issues
- Include examples if adding new features
- Ensure documentation is up-to-date
- Follow the existing code style

## Questions or Issues?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Provide detailed information about your environment

## Code of Conduct

Please be respectful and constructive in all interactions. We're here to build better documentation together!

---

Thank you for contributing to the Cloud Custodian community! 🚀
