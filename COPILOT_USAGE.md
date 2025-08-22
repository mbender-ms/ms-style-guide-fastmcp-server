# GitHub Copilot Chat Integration Examples
## Server Version: Web-Enabled FastMCP Server

## In VS Code Copilot Chat, you can use these commands:

### Content Analysis
```
@workspace analyze this content for Microsoft Style Guide compliance:
"Welcome to our new product! You can easily configure the settings to meet your needs."
```

### Voice and Tone Check
```
@workspace check voice and tone of this text:
"The configuration of settings can be accomplished by the user through the interface."
```

### Improvement Suggestions
```
@workspace suggest improvements for this writing:
"Users should utilize the functionality to facilitate optimal performance."
```

### Style Guidelines
```
@workspace show Microsoft Style Guide guidelines for voice and tone
```


### Live Search (Web Version Only)
```
@workspace search the Microsoft Style Guide for "active voice examples"
@workspace find guidance on "inclusive language best practices"
```

### Live Official Guidance
```
@workspace get official Microsoft guidance on terminology standards
@workspace fetch latest voice and tone guidelines from Microsoft Learn
```


## Direct Script Usage

```bash
# Analyze content
python copilot_integration.py analyze "Your content here"

# Get improvements  
python copilot_integration.py improve "Text to improve"

# Get guidelines
python copilot_integration.py guidelines voice

# Live search (web version)
python copilot_integration.py search "active voice"
```

## Server Version: Web-Enabled FastMCP Server

🌐 **Web Features**: Live content from Microsoft Learn, always up-to-date guidance

## MCP Tools Available in VS Code

Once the MCP server is running, these tools are available:
- `analyze_content` - Comprehensive style analysis
- `get_style_guidelines` - Retrieve specific guidelines
- `suggest_improvements` - Get improvement suggestions
- `search_style_guide` - Search official documentation(live)
- `get_official_guidance` - Get live official guidance (web version)
