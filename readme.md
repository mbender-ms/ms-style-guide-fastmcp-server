# Microsoft Style Guide FastMCP Server

A streamlined, cross-platform MCP server for analyzing content against the **Microsoft Writing Style Guide** using the FastMCP framework. Choose between **Offline** and **Web-Enabled** versions based on your needs.

## 🚀 Quick Start (One Command)

```bash
# Clone or download this repository
git clone https://github.com/asudbring/ms-style-guide-fastmcp-server.git
cd ms-style-guide-fastmcp-server

# Interactive setup (choose your version)
python fastmcp_setup.py

# OR Auto setup with specific version
python fastmcp_setup.py --offline    # Fast, reliable, works offline
python fastmcp_setup.py --web        # Live content from Microsoft Learn
```

**That's it!** The setup script will:
- ✅ Let you choose between Offline or Web-Enabled versions
- ✅ Install FastMCP and version-specific dependencies
- ✅ Configure VS Code global `mcp.json`
- ✅ Set up Copilot Chat integration
- ✅ Create test files and documentation
- ✅ Test server functionality

## 🎯 Choose Your Version

### 📊 Version Comparison

| Feature | Offline Version | Web-Enabled Version |
|---------|-----------------|---------------------|
| **Setup** | Fastest, minimal dependencies | Quick, requires `aiohttp` |
| **Speed** | ⚡ Very fast (local analysis) | 🌐 Fast (with web requests) |
| **Internet** | ❌ Not required | ✅ Required for full features |
| **Content** | Local patterns + official links | Live content from Microsoft Learn |
| **Accuracy** | High (local patterns) | Highest (official guidance) |
| **Reliability** | Very high (offline) | High (depends on internet) |
| **Up-to-date** | Static rules | Always current |
| **Use Case** | Fast checking, offline work | Detailed guidance, online work |

### 🤔 Which Version Should I Choose?

**Choose Offline Version if:**
- ✅ You want the fastest possible analysis
- ✅ You work in environments without reliable internet
- ✅ You need consistent performance
- ✅ You primarily need pattern-based checking
- ✅ Security policies restrict web access

**Choose Web-Enabled Version if:**
- ✅ You want the most accurate, up-to-date guidance
- ✅ You have reliable internet connection
- ✅ You need official examples and live content
- ✅ You want real-time search capabilities
- ✅ You're creating content that needs official validation

## 📁 Project Structure

```
ms-style-guide-fastmcp-server/
├── fastmcp_style_server.py         # Offline FastMCP server
├── fastmcp_style_server_web.py     # Web-enabled FastMCP server  
├── fastmcp_setup.py                # Intelligent setup script
├── mcp.json                        # VS Code MCP configuration
├── copilot_usage.md                # Usage examples and documentation
├── requirements.txt                # Python dependencies
└── readme.md                       # This file
```

## 🎯 Microsoft Style Guide Analysis

Both versions analyze content based on Microsoft's core principles:

### Voice and Tone
- **Warm and Relaxed**: Use contractions, natural language
- **Crisp and Clear**: Direct, scannable content
- **Ready to Help**: Action-oriented, supportive language

### Analysis Types
- `comprehensive` - Complete style analysis (default)
- `voice_tone` - Voice and tone compliance
- `grammar` - Grammar and style patterns
- `terminology` - Microsoft terminology standards
- `accessibility` - Inclusive language checking

### Version-Specific Features

#### Offline Version Features
- ⚡ **Lightning Fast**: Instant local analysis
- 💾 **No Dependencies**: Works completely offline
- 🔒 **Secure**: No external web requests
- 📋 **Pattern-Based**: Comprehensive regex pattern matching
- 🔗 **Official Links**: Direct links to Microsoft Style Guide

#### Web-Enabled Version Features
- 🌐 **Live Content**: Fetches real content from Microsoft Learn
- 📊 **Current Examples**: Always up-to-date official examples
- 🔍 **Live Search**: Real-time search of Microsoft Style Guide
- 📖 **Official Guidance**: Fetches specific guidance for detected issues
- ⚡ **Smart Caching**: Caches web content for performance

## 💬 GitHub Copilot Chat Integration

### Version-Aware Commands

Both versions support the same natural language commands, but provide different levels of detail:

#### Basic Commands (Both Versions)
```
analyze this content for Microsoft Style Guide compliance:
"Welcome to our new product! You can easily configure the settings."

check voice and tone of this text:
"Users can configure settings through the interface."

suggest improvements for this writing:
"Users should use the functionality to optimize performance."

show Microsoft Style Guide guidelines for accessibility
```

#### Web-Enhanced Commands (Web Version Only)
```
search the Microsoft Style Guide for "active voice examples"
get live guidance on "inclusive language best practices"
fetch current Microsoft terminology standards
find official examples for "contractions in technical writing"
```

### Command Responses by Version

#### Offline Version Response
```
📋 Microsoft Style Guide Analysis

✅ Good - Minor improvements suggested

📊 Text Statistics:
   • Words: 32 | Sentences: 2 | Avg: 16.0 words/sentence

🔍 Issues Found: 2
   • Voice/Tone: Use more contractions for natural tone
   • Terminology: Use "sign in" instead of "login"

🌐 Official Guidelines: https://learn.microsoft.com/en-us/style-guide
💾 Offline Analysis: Fast local pattern matching
```

#### Web Version Response
```
📋 Microsoft Style Guide Analysis (Web-Enabled)

✅ Good - Minor improvements suggested

📊 Text Statistics:
   • Words: 32 | Sentences: 2 | Avg: 16.0 words/sentence

🔍 Issues Found: 2
   • Voice/Tone: Use more contractions for natural tone
   • Terminology: Use "sign in" instead of "login"

🌐 Live Official Guidance Retrieved:
   • Voice/Tone: Microsoft's brand voice: above all, simple and human
     https://learn.microsoft.com/en-us/style-guide/brand-voice-above-all-simple-human
   • Terminology: A-Z word list and term collections
     https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections

⚡ Web-Enabled: Live guidance from Microsoft Learn
```

## 🛠️ Available MCP Tools

### Offline Version Tools

| Tool | Description | Speed | Accuracy |
|------|-------------|-------|----------|
| `analyze_content` | Pattern-based style analysis | ⚡ Very Fast | ✅ High |
| `get_style_guidelines` | Local guidelines with official links | ⚡ Instant | ✅ High |
| `suggest_improvements` | Local improvement suggestions | ⚡ Very Fast | ✅ High |
| `search_style_guide` | Links to official documentation | ⚡ Instant | ✅ High |

### Web-Enabled Version Tools

| Tool | Description | Speed | Accuracy |
|------|-------------|-------|----------|
| `analyze_content` | Pattern + live guidance analysis | 🌐 Fast | 🎯 Excellent |
| `get_style_guidelines` | Live guidelines from Microsoft Learn | 🌐 Fast | 🎯 Excellent |
| `suggest_improvements` | Live guidance + local suggestions | 🌐 Fast | 🎯 Excellent |
| `search_style_guide` | Live search of Microsoft documentation | 🌐 Fast | 🎯 Excellent |
| `get_official_guidance` | Fetch specific official guidance | 🌐 Fast | 🎯 Excellent |

## 🔧 Setup Options

### Interactive Setup (Recommended)
```bash
python fastmcp_setup.py
# Choose your version during setup
# Get explanations of each version's benefits
```

### Command Line Setup
```bash
# Force specific versions
python fastmcp_setup.py --offline    # Fast, reliable offline version
python fastmcp_setup.py --web        # Live content web version  
python fastmcp_setup.py --auto       # Auto-select offline version

# Special options
python fastmcp_setup.py --copilot    # Focus on Copilot Chat integration
```

### Manual Configuration (If Needed)

#### For Offline Version
Create `%APPDATA%\Code\User\mcp.json` (Windows) or equivalent:

```json
{
  "servers": {
    "microsoft-style-guide": {
      "command": "python",
      "args": ["path/to/fastmcp_style_server.py"],
      "env": {"PYTHONPATH": "path/to/project"},
      "initializationOptions": {
        "name": "Microsoft Style Guide (Offline)",
        "server_type": "fastmcp_offline"
      }
    }
  }
}
```

#### For Web-Enabled Version
```json
{
  "servers": {
    "microsoft-style-guide": {
      "command": "python", 
      "args": ["path/to/fastmcp_style_server_web.py"],
      "env": {"PYTHONPATH": "path/to/project"},
      "initializationOptions": {
        "name": "Microsoft Style Guide (Web)",
        "server_type": "fastmcp_web",
        "capabilities": {"web_enabled": true}
      }
    }
  }
}
```

## 🧪 Testing Your Setup

### 1. Test the Server
```bash
# Test offline version
python fastmcp_style_server.py --test

# Test web version  
python fastmcp_style_server_web.py --test
```

### 2. Test in VS Code
1. Open a markdown file for testing
2. Use Copilot Chat: `@workspace analyze this document`
3. Check that MCP tools appear in Command Palette
4. Verify correct version is running in MCP server list

## 📊 Performance Comparison

### Speed Benchmarks

| Operation | Offline Version | Web Version |
|-----------|----------------|-------------|
| **Server Startup** | ~0.5 seconds | ~1.0 seconds |
| **Simple Analysis** | ~0.1 seconds | ~0.3 seconds |
| **Complex Analysis** | ~0.2 seconds | ~0.8 seconds |
| **Guidelines Retrieval** | ~0.05 seconds | ~0.5 seconds |
| **Search Operations** | ~0.05 seconds | ~1.0 seconds |

### Resource Usage

| Resource | Offline Version | Web Version |
|----------|----------------|-------------|
| **Memory** | ~20MB | ~35MB |
| **CPU** | Very Low | Low |
| **Network** | None | Moderate |
| **Storage** | ~2MB | ~2MB + cache |

## 🎯 Use Case Recommendations

### Choose Offline Version For:

**Content Development**
- ✅ Draft writing and quick style checks
- ✅ Code comment analysis
- ✅ README file improvements
- ✅ Batch processing multiple files

**Environments**
- ✅ Secure/air-gapped environments
- ✅ Unreliable internet connections
- ✅ Performance-critical workflows
- ✅ CI/CD pipelines

**Teams**
- ✅ Large teams needing consistent performance
- ✅ Junior developers learning style guidelines
- ✅ Automated quality checks

### Choose Web Version For:

**Content Publishing**
- ✅ Final review before publication
- ✅ Marketing copy validation
- ✅ Official documentation
- ✅ Customer-facing content

**Environments**
- ✅ Stable internet connections
- ✅ Content teams needing latest guidance
- ✅ Editorial workflows
- ✅ Style guide research

**Teams**
- ✅ Content creators and technical writers
- ✅ Marketing teams
- ✅ Documentation teams
- ✅ Style guide maintainers

## 🐛 Troubleshooting

### Server Not Appearing in VS Code
1. Check that `mcp.json` exists in VS Code User directory
2. Restart VS Code completely (close all windows)
3. Verify MCP extension is installed and enabled
4. Check VS Code Developer Console for MCP errors

### Python Path Issues
```bash
# Check Python executable
which python
python --version

# Update mcp.json with absolute paths if needed
```

### Dependencies Missing
```bash
# Reinstall dependencies
pip install fastmcp
# OR
pip install mcp

# Test server directly
python fastmcp_style_server.py --test
```

### Copilot Chat Isn't Working
1. Ensure GitHub Copilot Chat extension is installed
2. Verify MCP server is running and accessible
3. Check VS Code Developer Console for MCP errors

##  Advanced Usage

### Custom Analysis Types
```python
# In your own scripts
from fastmcp_style_server import analyzer

result = analyzer.analyze_content("Your text", "voice_tone")
guidelines = analyzer.get_style_guidelines("accessibility")
```

### Batch Processing
```python
# Analyze multiple files using the server directly
from fastmcp_style_server import analyzer

for file in ["README.md", "docs/guide.md"]:
    with open(file, 'r') as f:
        content = f.read()
        result = analyzer.analyze_content(content)
        print(f"{file}: {result}")
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Check Style Guide Compliance
  run: |
    python fastmcp_style_server.py --test
    # Add your analysis workflow here
```
## 📝 Change Log

For a detailed list of changes, please refer to the [CHANGELOG.md](CHANGELOG.md) file.

## 🤝 Contributing

1. Fork this repository
2. Make changes to FastMCP server or setup
3. Test with `python fastmcp_setup.py --auto`
4. Submit pull request

## 📚 References

- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [VS Code MCP Integration](https://code.visualstudio.com/)

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with FastMCP for better technical writing** ✨
