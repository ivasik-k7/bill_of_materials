# Objective:
# The objective of this technical
# task is to create a Python tool that parses various platform
# dependency files, extracts relevant information about dependencies,
# and generates a Software Bill of Materials (SBOM) summary document

# The tool should support parsing dependency files from different platforms such as Python's requirements.txt, pyproject.toml, etc
# Extract relevant information such as package names, versions, descriptions, licenses, and any other metadata available in the dependency files.

# Generate a Software Bill of Materials (SBOM) summary document based on the parsed dependency information.

# The SBOM document should be generated in a standardized format such as JSON, XML, or CSV.
# Each entry in the SBOM should represent a dependency with all relevant information
# Implement appropriate error handling mechanisms for cases such as invalid file paths, unsupported file formats, or parsing errors.
# Provide informative error messages to aid troubleshooting and debugging.
# Write unit tests to ensure the correctness of the parsing and SBOM generation functionality.
# Provide clear and concise documentation for how to use the tool, including installation instructions and usage examples.

# Additional Considerations:

# Efficiency: Optimize the parsing and generation process for large dependency files to ensure reasonable performance.
# Extensibility: Design the tool in a modular and extensible way to easily add support for parsing new dependency file formats in the future.
# Compatibility: Ensure compatibility with different Python versions and environments.

# Submission:

# Provide the Python script/tool, unit tests, and documentation in a well-structured format.
# Include any necessary dependencies and installation instructions.


from app.parser import ParserContext

if __name__ == "__main__":
    with ParserContext("examples/requirements.txt") as parser:
        data = parser.parse()
