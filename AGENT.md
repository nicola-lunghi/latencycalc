# AI Agent Documentation for latencycalc

This document outlines the capabilities and workflows that the AI assistant can perform with this codebase.

## Project Overview

**latencycalc** is a Python tool for measuring audio interface latency using ASIO drivers. It provides CLI commands to list audio devices and measure input/output latency.

## AI Agent Capabilities

### 🔧 **Bug Investigation & Fixes**
- **Windows Console Issues**: Can diagnose and fix Click library Windows console errors (OSError: Windows error 6)
- **Import Issues**: Can resolve module import and packaging problems
- **Error Reproduction**: Can create minimal reproduction cases for bugs

### 📦 **Package Management**
- **Entry Points**: Can configure and fix Python package entry points
- **Dependencies**: Can manage Python dependencies and virtual environments
- **Installation**: Can troubleshoot pip installation issues

### 🐛 **Bug Reporting**
- **Issue Reproduction**: Can create minimal test cases to reproduce bugs
- **Bug Report Writing**: Can draft comprehensive bug reports with all necessary details
- **Environment Analysis**: Can gather system information for bug reports

### 🧹 **Code Cleanup**
- **Redundant Code Removal**: Can identify and remove duplicate code (e.g., double monkey patching)
- **File Organization**: Can reorganize files for better project structure
- **Git Management**: Can stage, commit, and manage version control

### 🏗️ **Project Setup**
- **Development Environment**: Can set up development environments with proper tooling
- **Code Quality**: Uses Ruff for fast Python linting and formatting (`ruff check` and `ruff format`)
- **CI/CD**: Can configure linting, formatting, and testing tools
- **Documentation**: Can update README and other documentation files

## Recent Work Examples

### Windows Console Fix
- **Issue**: Click library causing `OSError: Windows error 6` in Windows terminals
- **Solution**: Added monkey patch in entry point to disable problematic Windows console handling
- **Files Modified**: `src/latencycalc_entry.py`, `pyproject.toml`, `src/latencycalc.py`

### Package Structure Improvements
- **Issue**: Entry point configuration issues
- **Solution**: Moved entry point to separate file with proper imports
- **Result**: Clean separation of concerns and reliable package installation

## Workflow Patterns

### Bug Investigation Process
1. **Reproduce**: Create minimal reproduction case
2. **Analyze**: Examine error traces and identify root cause
3. **Fix**: Implement solution with proper error handling
4. **Test**: Verify fix works across different scenarios
5. **Document**: Create comprehensive bug report if upstream issue

### Code Cleanup Process
1. **Audit**: Review codebase for issues (duplicates, organization)
2. **Plan**: Identify necessary changes without breaking functionality
3. **Execute**: Make changes incrementally with testing
4. **Verify**: Ensure all functionality still works
5. **Commit**: Create clean, descriptive commits

## Communication Style

- **Clear Explanations**: Provides step-by-step reasoning for all actions
- **Code Comments**: Explains complex code changes thoroughly
- **Testing**: Always verifies changes work before proceeding
- **Documentation**: Updates relevant docs when making structural changes

## Limitations

- **Windows Development Environment**: This project is developed on Windows systems, so terminal commands use PowerShell syntax (e.g., `Remove-Item` instead of `rm`, `Get-ChildItem` instead of `ls`)
- Cannot execute code that requires physical audio hardware
- Cannot test on non-Windows platforms for Windows-specific issues
- Cannot access external services or APIs without explicit permission
- Cannot make changes that would break existing functionality without verification

## Contact

This AI agent is designed to assist with development, debugging, and maintenance of the latencycalc project. For complex architectural decisions or external integrations, human developer review is recommended.
