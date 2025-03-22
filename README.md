# MCPXcode

## Introduction

MCPXcode is an open-source implementation of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) for Xcode. It enables seamless integration between Xcode and AI assistants by providing a structured protocol for context exchange and tool execution within the Xcode environment.

Following the MCP specification, this project creates a bridge between Xcode's development environment and AI tools, allowing for enhanced developer workflows through contextual understanding and programmable interactions. It wraps common command-line tools (`xcrun`, `xctrace`) and leverages macOS accessibility features to enable AI-assisted automation of Xcode operations.


**This Project is in Active Development, So May Have Unexpected Issues**


## Installation

```bash

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/everettjf/MCPXcode.git
cd MCPXcode
source .venv/bin/activate
uv add "mcp[cli]"
```

## Config



```json
{
  "mcpServers": {
    "MCPXcode": {
      "command": "uv", # may use full path
      "args": [
        "--directory",
        "<Path>/MCPXcode", # change to your full path
        "run",
        "main.py"
      ]
    }
  }
}
```



## Features

### Current MCP Tool Integrations

- **xcrun Tool Extensions**
  - Context-aware interfaces for common xcrun commands
  - Structured output formatting for AI consumption
  - Semantic error handling and diagnostic reporting

- **xctrace Tool Extensions**
  - Context-enhanced profiling and tracing for iOS/macOS applications
  - Structured performance metrics collection for AI analysis
  - Trace data processing with semantic context

### Planned Extensions

- **Accessibility Tool Extensions**
  - Context-aware UI interactions within Xcode
  - Semantic triggers for build, run, and test operations
  - Structured project navigation capabilities
  - Enhanced context extraction from Xcode UI

- **MCP HTTP Server**
  - Full MCP specification compliance over HTTP
  - Standardized tool execution protocol
  - Context-preserving webhooks for build events
  - Seamless integration with AI-powered CI/CD pipelines

- **MCP Client Libraries**
  - Language-specific SDKs implementing the MCP specification
  - Simplified context exchange between AI assistants and Xcode


## Usage

### MCP CLI Interface

```bash
# Start the MCP server with default settings
mcpxcode serve

# Execute an xcrun tool with context
mcpxcode tool xcrun simctl list --format json

# Execute an xctrace tool with context
mcpxcode tool xctrace record --template 'Time Profiler' --launch com.example.app
```

## Project Roadmap

### Phase 1: MCP Core Implementation (Q2 2025)
- ✅ Basic project structure
- ⬜ Tool extensions for essential xcrun commands with context handling
- ⬜ Tool extensions for basic xctrace functionality with context handling
- ⬜ MCP-compliant CLI interface

### Phase 2: MCP Server Implementation (Q3 2025)
- ⬜ Full MCP specification HTTP server
- ⬜ Context-aware authentication and security
- ⬜ Structured context exchange protocol
- ⬜ Extensible tool registry architecture

### Phase 3: MCP Accessibility Extensions (Q4 2025)
- ⬜ macOS accessibility integration with semantic context
- ⬜ Context-aware Xcode UI automation
- ⬜ Semantic event monitoring and contextual reactions

### Phase 4: Advanced MCP Features (Q1 2026)
- ⬜ MCP-compliant Python client library
- ⬜ Context-aware integration with AI-powered CI/CD tools
- ⬜ Semantic context monitoring dashboard


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.