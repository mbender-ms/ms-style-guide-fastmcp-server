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

/github_updates
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

## 📋 Change Tracking with /github_updates

Both versions include a built-in change tracking system that monitors all modifications made by the MCP server during your session.

### How to Use
Simply type `/github_updates` in your GitHub Copilot Chat to get a concise summary of all changes made to your content.

### Output Format
```
**Summary of Changes for Microsoft Style Guide**
**Date:** 2025-08-22
**Changes:**
- Style issue identified: Use 'sign in' instead of 'login' (line 15)
- Style issue identified: Consider using contractions for natural tone (line 23)
- Accessibility improvement: Replace 'guys' with inclusive alternative (line 8)

**Total updates:** 3
```

### What Gets Tracked
- Issues identified during content analysis
- Style violations detected
- Terminology corrections suggested
- Accessibility improvements recommended
- Grammar and readability suggestions

This feature helps you maintain a clear audit trail of all Microsoft Style Guide improvements applied to your documents.

### Example Usage in GitHub Copilot Chat

Here are practical examples of how to use the `/github_updates` tool in your workflow:

#### Basic Usage
```
User: /github_updates
Copilot: **Summary of Changes for Microsoft Style Guide**
**Date:** 2025-08-22
**Changes:**
- Style issue identified: Use 'sign in' instead of 'login' (line 15)
- Style issue identified: Consider using contractions for natural tone (line 23)
- Accessibility improvement: Replace 'guys' with inclusive alternative (line 8)

**Total updates:** 3
```

#### After Analyzing Multiple Documents
```
User: Can you analyze this README file for Microsoft Style Guide compliance?

[After Copilot analyzes the content]

User: Now check this API documentation too.

[After second analysis]

User: /github_updates

Copilot: **Summary of Changes for Microsoft Style Guide**
**Date:** 2025-08-22
**Changes:**
- Style issue identified: Use "email" instead of "e-mail" (line 12)
- Grammar improvement: Convert passive voice to active (line 45)
- Terminology correction: Use "website" instead of "web site" (line 23)
- Voice enhancement: Add contractions for natural tone (line 67)
- Accessibility fix: Replace non-inclusive language (line 89)

**Total updates:** 5
```

#### During Document Review Process
```
User: Please review this technical blog post for Microsoft Style Guide compliance.

[After analysis and suggestions]

User: Great! Now analyze this product announcement draft.

[After second analysis]

User: /github_updates

Copilot: **Summary of Changes for Microsoft Style Guide**
**Date:** 2025-08-22
**Changes:**
- Voice/tone improvement: Use "you're" instead of "you are" (line 8)
- Clarity enhancement: Break long sentence for readability (line 34)
- Terminology standard: Use "Wi-Fi" with proper capitalization (line 19)
- Inclusive language: Replace "guys" with "everyone" (line 52)

**Total updates:** 4
```

#### Empty Session Example
```
User: /github_updates

Copilot: **Summary of Changes for Microsoft Style Guide**
**Date:** 2025-08-22
**Changes:**
- No changes tracked in current session

**Total updates:** 0
```

### Integration with Content Workflow

1. **Draft Review**: Write your content, then ask Copilot to analyze it
2. **Style Analysis**: Let the MCP server identify Microsoft Style Guide issues
3. **Track Changes**: Use `/github_updates` to see all improvements made
4. **Final Review**: Use the summary to ensure all issues were addressed
5. **Documentation**: Include the summary in your content review documentation

## 🛠️ Available MCP Tools

### Offline Version Tools

| Tool | Description | Speed | Accuracy |
|------|-------------|-------|----------|
| `analyze_content` | Pattern-based style analysis | ⚡ Very Fast | ✅ High |
| `get_style_guidelines` | Local guidelines with official links | ⚡ Instant | ✅ High |
| `suggest_improvements` | Local improvement suggestions | ⚡ Very Fast | ✅ High |
| `search_style_guide` | Links to official documentation | ⚡ Instant | ✅ High |
| `github_updates` | Summary of changes made by MCP server | ⚡ Instant | ✅ High |

### Web-Enabled Version Tools

| Tool | Description | Speed | Accuracy |
|------|-------------|-------|----------|
| `analyze_content` | Pattern + live guidance analysis | 🌐 Fast | 🎯 Excellent |
| `get_style_guidelines` | Live guidelines from Microsoft Learn | 🌐 Fast | 🎯 Excellent |
| `suggest_improvements` | Live guidance + local suggestions | 🌐 Fast | 🎯 Excellent |
| `search_style_guide` | Live search of Microsoft documentation | 🌐 Fast | 🎯 Excellent |
| `get_official_guidance` | Fetch specific official guidance | 🌐 Fast | 🎯 Excellent |
| `github_updates` | Summary of changes made by MCP server | ⚡ Instant | 🎯 Excellent |

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

## � Usage Examples

Here are practical examples showing how to use the Microsoft Style Guide MCP Server with GitHub Copilot Chat for different content scenarios.

### Example 1: Microsoft Learn Documentation Review

**Scenario**: Reviewing Microsoft Learn documentation for both Style Guide and Contributor Guide compliance, handling potential conflicts.

```
User: Analyze this content for Microsoft Style Guide compliance and contributor guide compliance. Call out when the style guide and the contributor guide are in conflict:

"# Configure Azure Functions
This article shows you how to configure Azure Functions in the Azure portal. You will learn how to setup function apps, configure bindings, and manage application settings. Advanced users can utilize the Azure CLI to automate these processes."

Copilot: 📋 Microsoft Style Guide Analysis (Web-Enabled)

⚠️ Good - Multiple improvements needed

📊 **Text Statistics:**
   • Words: 38 | Sentences: 4 | Avg: 9.5 words/sentence

🔍 **Issues Found:** 5
   • Terminology: Use "set up" (verb) instead of "setup" (noun)
   • Voice/Tone: Inconsistent article structure - mix of "you will" and direct commands
   • Style: "shows you how to" is wordy - prefer direct approach
   • Accessibility: "Advanced users" could be more inclusive
   • Structure: Missing H2 headings for Learn docs structure

🔄 **Style Guide vs Contributor Guide Conflicts:**
   • Style Guide: Prefers contractions and natural tone ("you'll learn")
   • Contributor Guide: May prefer formal structure for procedural content
   • Resolution: Use Style Guide preference for better accessibility

🌐 **Live Official Guidance Retrieved:**
   • Voice/Tone: Microsoft's brand voice: above all, simple and human
   • Article Structure: Microsoft Learn contributor guide requirements

User: Check voice and tone of this text

Copilot: 🗣️ **Voice and Tone Analysis**

**Current Assessment:**
• Warm & Relaxed: ⚠️ Partially - lacks contractions
• Crisp & Clear: ✅ Good - clear structure
• Ready to Help: ⚠️ Mixed - some direct, some verbose

**Voice Issues:**
- "shows you how to" → too wordy, use direct approach
- "You will learn" → prefer "Learn how to" or "You'll learn"
- Inconsistent between explanatory and instructional tone

**Recommended Tone Adjustments:**
- More direct: "Configure Azure Functions in the Azure portal"
- Add contractions: "you'll learn" instead of "you will learn"
- Action-oriented: Start with imperative verbs

User: Suggest improvements for this writing

Copilot: ✨ **Improvement Suggestions**

**Revised Version:**
"# Configure Azure Functions
Configure Azure Functions in the Azure portal. Learn how to set up function apps, configure bindings, and manage application settings. You can use the Azure CLI to automate these processes.

## Set up function apps
[Content here]

## Configure bindings  
[Content here]

## Manage application settings
[Content here]"

**Key Changes:**
1. **Terminology**: "set up" (verb) replaces "setup" (noun) - Line 2
2. **Clarity**: Removed wordy "This article shows you how to" - Line 1
3. **Voice**: More direct, action-oriented approach - Line 1
4. **Structure**: Added required H2 headings for Learn docs - Lines 4-8
5. **Accessibility**: "You can use" instead of "Advanced users can utilize" - Line 3

**Style Guide References:**
• Terminology: https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/s/setup-set-up
• Voice & Tone: https://learn.microsoft.com/en-us/style-guide/brand-voice-above-all-simple-human
• Article Structure: https://learn.microsoft.com/en-us/contribute/style-quick-start

User: Show Microsoft Style Guide guidelines for accessibility

Copilot: ♿ **Microsoft Style Guide Accessibility Guidelines**

**Inclusive Language:**
- Avoid "Advanced users" → Use "If you want to automate" or "For automation"
- Replace ability-based assumptions with task-focused language
- Use "people with disabilities" not "disabled people"

**Clear Communication:**
- Write in plain language
- Use short, clear sentences
- Provide alternative text for images
- Structure content with proper headings

**Official Reference:**
https://learn.microsoft.com/en-us/style-guide/bias-free-communication

User: Implement suggestions and I'll review

Copilot: ✅ **Implemented Suggestions - Final Version**

"# Configure Azure Functions
Configure Azure Functions in the Azure portal. Learn how to set up function apps, configure bindings, and manage application settings. Use the Azure CLI to automate these processes.

## Set up function apps
Follow these steps to create and configure your function app.

## Configure bindings
Set up input and output bindings for your functions.

## Manage application settings
Configure environment variables and connection strings."

**Changes Applied:**
✓ Fixed "setup" → "set up" terminology
✓ Removed wordy introduction
✓ Added proper H2 structure for Learn docs
✓ Made language more direct and accessible
✓ Improved voice and tone consistency

User: Provide style guide references for suggestions in chat

Copilot: 📚 **Style Guide References for All Suggestions**

**Terminology Changes:**
• "set up" vs "setup": https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/s/setup-set-up
• Verb/noun distinction: https://learn.microsoft.com/en-us/style-guide/grammar/verbs

**Voice & Tone Improvements:**
• Brand voice principles: https://learn.microsoft.com/en-us/style-guide/brand-voice-above-all-simple-human
• Direct, action-oriented writing: https://learn.microsoft.com/en-us/style-guide/scannable-content/headings
• Conversational tone: https://learn.microsoft.com/en-us/style-guide/brand-voice-above-all-simple-human#warm-and-relaxed

**Accessibility Guidelines:**
• Bias-free communication: https://learn.microsoft.com/en-us/style-guide/bias-free-communication
• Inclusive language: https://learn.microsoft.com/en-us/style-guide/bias-free-communication/writing-that-includes-everyone
• Plain language: https://learn.microsoft.com/en-us/style-guide/scannable-content

**Microsoft Learn Structure:**
• Article formatting: https://learn.microsoft.com/en-us/contribute/style-quick-start
• Heading structure: https://learn.microsoft.com/en-us/contribute/how-to-write-use-markdown#headings
• Content organization: https://learn.microsoft.com/en-us/contribute/content/how-to-structure-your-article

User: Create a pull request description using the tracked changes

Copilot: 📝 **Pull Request Template Generation**

Based on the tracked changes, here's your PR description:

---

## Style Guide Compliance Updates for Azure Functions Documentation

### Summary
Updated Azure Functions configuration documentation to align with Microsoft Style Guide and Learn contributor guidelines.

### Changes Made
- **Terminology**: Fixed "setup" (noun) to "set up" (verb) for proper grammar
- **Voice & Tone**: Removed wordy introduction, made content more direct and action-oriented
- **Structure**: Added proper H2 headings required for Microsoft Learn articles
- **Accessibility**: Replaced "Advanced users" with inclusive "Use the Azure CLI" approach
- **Compliance**: Resolved conflicts between Style Guide and Contributor Guide preferences

### Style Guide References
- [Terminology Standards](https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/s/setup-set-up)
- [Voice & Tone Guidelines](https://learn.microsoft.com/en-us/style-guide/brand-voice-above-all-simple-human)
- [Accessibility Standards](https://learn.microsoft.com/en-us/style-guide/bias-free-communication)

### Testing
- [x] Content reviewed against Microsoft Style Guide
- [x] Structure validated against Microsoft Learn contributor guidelines
- [x] Accessibility improvements verified

User: /github_updates

Copilot: **Summary of Changes for Microsoft Style Guide**
**Date:** 2025-08-22
**Changes:**
- Terminology correction: Use "set up" verb form instead of "setup" (line 2)
- Voice improvement: Remove wordy "This article shows you how to" (line 1)
- Voice enhancement: More direct, action-oriented language (line 1)
- Structure improvement: Added proper H2 headings for Learn docs (lines 4-8)
- Accessibility fix: Replace "Advanced users can utilize" with "Use" (line 3)
- Style guide compliance: Applied Microsoft Learn contributor guide structure
- Reference integration: Provided official style guide URLs for all suggestions
- PR description: Generated pull request description with tracked changes

**Total updates:** 8
```

### Example 2: Blog Post Review

**Scenario**: Reviewing a technical blog post for Microsoft Style Guide compliance.

```
User: Please analyze this blog post draft for Microsoft Style Guide compliance:

"Users can't easily configure the advanced settings in our new AI platform. The user should login first, then navigate to the configuration panel. This process was designed to be user-friendly and was implemented using cutting-edge technology. Guys who are familiar with our previous version will find this update really awesome."

Copilot: 📋 Microsoft Style Guide Analysis

⚠️ Good - Several improvements suggested

📊 **Text Statistics:**
   • Words: 51 | Sentences: 4 | Avg: 12.8 words/sentence

🔍 **Issues Found:** 5
   • Terminology: Use "sign in" instead of "login"
   • Grammar: Convert passive voice to active voice (2 instances)
   • Accessibility: Replace "guys" with inclusive alternative
   • Voice/Tone: Good use of contractions

**Recommended Changes:**
- Line 1: Change "login" to "sign in"
- Line 2: Change "was designed" to active voice
- Line 3: Change "was implemented" to active voice  
- Line 4: Replace "Guys" with "Users" or "People"

User: /github_updates

Copilot: **Summary of Changes for Microsoft Style Guide**
**Date:** 2025-08-22
**Changes:**
- Terminology correction: Use "sign in" instead of "login" (line 1)
- Grammar improvement: Convert passive voice to active (line 2)
- Grammar improvement: Convert passive voice to active (line 3)
- Accessibility fix: Replace non-inclusive "guys" with "users" (line 4)

**Total updates:** 4
```

### Example 3: API Documentation Review

**Scenario**: Ensuring API documentation follows Microsoft Style Guide standards.

```
User: Check this API documentation for Microsoft Style Guide compliance:

"This API allows developers to access user data. You cannot retrieve sensitive information without proper authentication. The system will return an error if the request is malformed. Users should provide their credentials via the login endpoint."

Copilot: 📋 Microsoft Style Guide Analysis (Web-Enabled)

✅ Good - Minor improvements suggested

📊 **Text Statistics:**
   • Words: 38 | Sentences: 4 | Avg: 9.5 words/sentence

🔍 **Issues Found:** 2
   • Terminology: Use "sign-in" instead of "login" for noun form
   • Voice/Tone: Consider more contractions for natural tone

🌐 **Live Official Guidance Retrieved:**
   • Terminology: A-Z word list and term collections
     https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections

**Improvements:**
- Replace "login endpoint" with "sign-in endpoint"
- Consider "can't retrieve" instead of "cannot retrieve"

User: Now check this error message documentation too:

"An error occurred while processing your request. The application cannot complete this action. Please contact support if the issue persists."

User: /github_updates

Copilot: **Summary of Changes for Microsoft Style Guide**
**Date:** 2025-08-22
**Changes:**
- Terminology correction: Use "sign-in endpoint" instead of "login endpoint" (line 4)
- Voice improvement: Add contractions for natural tone (line 2)
- Voice improvement: Use "can't complete" instead of "cannot complete" (line 1)

**Total updates:** 3
```

### Example 4: README File Enhancement

**Scenario**: Improving a project README for better accessibility and tone.

```
User: Help me improve this README section:

"# Project Setup
Users should follow these steps to setup the application. Developers cannot access advanced features until they complete the authentication process. This guide will help guys get started quickly."

Copilot: 📋 Microsoft Style Guide Analysis

⚠️ Needs improvement - Multiple issues found

📊 **Text Statistics:**
   • Words: 31 | Sentences: 3 | Avg: 10.3 words/sentence

🔍 **Issues Found:** 4
   • Terminology: Use "set up" (verb) instead of "setup" (noun)
   • Voice/Tone: Add contractions for natural tone
   • Accessibility: Replace "guys" with inclusive language
   • Grammar: Consider active voice alternatives

**Suggested Rewrite:**
"# Project Setup
Follow these steps to set up the application. You can't access advanced features until you complete the authentication process. This guide helps everyone get started quickly."

User: /github_updates

Copilot: **Summary of Changes for Microsoft Style Guide**
**Date:** 2025-08-22
**Changes:**
- Terminology fix: Use "set up" verb form instead of "setup" (line 2)
- Voice enhancement: Add "can't" contraction for natural tone (line 3)
- Accessibility improvement: Replace "guys" with "everyone" (line 4)
- Voice improvement: Direct address using "you" (line 3)

**Total updates:** 4
```

## 🔧 Calling Specific Tools

### Using analyze_content
```
User: @workspace analyze this content for Microsoft Style Guide compliance:
"Content to analyze here..."
```

### Using get_style_guidelines  
```
User: Show me Microsoft Style Guide guidelines for accessibility
User: Get style guidelines for voice and tone
User: What are the Microsoft terminology standards?
```

### Using suggest_improvements
```
User: Suggest improvements for this writing:
"Text that needs improvement..."
User: Focus on voice and tone improvements for this content
```

### Using search_style_guide (Web Version)
```
User: Search the Microsoft Style Guide for "active voice examples"
User: Find guidance on "inclusive language best practices"
User: Look up "contractions in technical writing"
```

### Using github_updates
```
User: /github_updates
User: Show me a summary of all changes made this session
User: What style improvements have been tracked?
```

### Using get_official_guidance (Web Version)
```
User: Get official Microsoft guidance on "bias-free communication"
User: Fetch live examples of "warm and relaxed" tone
User: Show current Microsoft standards for "technical writing"
```

## �🐛 Troubleshooting

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

- [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [VS Code MCP Integration](https://code.visualstudio.com/)

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with FastMCP for better technical writing** ✨
