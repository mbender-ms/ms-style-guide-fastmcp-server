#!/usr/bin/env python3
"""
Microsoft Style Guide MCP Server - FastMCP Cross-Platform Version

A simplified, cross-platform MCP server using FastMCP for analyzing content 
against the official Microsoft Writing Style Guide.

This version provides the same functionality as the original but with:
- Simplified setup and dependencies
- Cross-platform compatibility
- Automatic VS Code integration
- Built-in Copilot Chat support
- Microsoft Style Guide Document Reviewer prompt
"""

import asyncio
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try FastMCP first, fall back to basic implementation
try:
    from fastmcp import FastMCP
    MCP_AVAILABLE = True
    logger.info("FastMCP library detected - enhanced functionality available")
except ImportError:
    try:
        # Try regular MCP
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        from mcp.types import TextContent, CallToolResult, ListToolsResult, Tool, Resource, Prompt
        MCP_AVAILABLE = True
        logger.info("Standard MCP library detected")
    except ImportError:
        MCP_AVAILABLE = False
        logger.info("No MCP library found - using development mode")

class MicrosoftStyleGuideAnalyzer:
    """Core analyzer for Microsoft Style Guide compliance."""
    
    def __init__(self):
        """Initialize the analyzer with pattern matching capabilities."""
        self.style_guide_base_url = "https://learn.microsoft.com/en-us/style-guide"
        
        # Change tracking for github_updates tool
        self.change_history = []
        
        # Core style patterns
        self.patterns = {
            "contractions": r"\b(it's|you're|we're|don't|can't|won't|let's|you'll|we'll)\b",
            "passive_voice": r"\b(is|are|was|were|been|be)\s+\w*ed\b",
            "long_sentences": r"[.!?]+\s*[A-Z][^.!?]{100,}[.!?]",
            "gendered_pronouns": r"\b(he|him|his|she|her|hers)\b",
            "non_inclusive_terms": r"\b(guys|mankind|blacklist|whitelist|master|slave|crazy|insane|lame)\b",
            "you_addressing": r"\byou\b",
            "second_person_avoid": r"\b(the user|users|one should|people should)\b"
        }
        
        # Microsoft terminology standards
        self.terminology_standards = {
            "AI": {"correct": "AI", "avoid": ["A.I."], "note": "No periods"},
            "email": {"correct": "email", "avoid": ["e-mail"], "note": "One word"},
            "website": {"correct": "website", "avoid": ["web site"], "note": "One word"},
            "sign_in": {"correct": "sign in (verb), sign-in (noun)", "avoid": ["login", "log in"], "note": "Microsoft standard"},
            "setup": {"correct": "set up (verb), setup (noun)", "avoid": ["setup (verb)"], "note": "Context dependent"},
            "wifi": {"correct": "Wi-Fi", "avoid": ["WiFi", "wifi"], "note": "Hyphenated, both caps"}
        }

    def analyze_content(self, text: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Analyze text content against Microsoft Style Guide principles."""
        issues = []
        suggestions = []
        
        # Basic statistics
        words = text.split()
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        word_count = len(words)
        sentence_count = len(sentences)
        avg_words_per_sentence = round(word_count / max(1, sentence_count), 1)
        
        # Voice and tone analysis
        if analysis_type in ["comprehensive", "voice_tone"]:
            contractions = len(re.findall(self.patterns["contractions"], text, re.IGNORECASE))
            you_usage = len(re.findall(self.patterns["you_addressing"], text, re.IGNORECASE))
            
            if contractions > 0:
                suggestions.append({
                    "type": "positive",
                    "message": f"Good use of contractions ({contractions} found) - supports warm, natural tone",
                    "principle": "warm_and_relaxed"
                })
            else:
                issues.append({
                    "type": "voice_tone",
                    "severity": "info",
                    "message": "Consider using contractions (it's, you're, we'll) for a more natural tone",
                    "principle": "warm_and_relaxed"
                })
            
            if you_usage > 0:
                suggestions.append({
                    "type": "positive",
                    "message": f"Good use of 'you' ({you_usage} instances) - directly engages readers",
                    "principle": "ready_to_help"
                })
        
        # Grammar analysis
        if analysis_type in ["comprehensive", "grammar"]:
            # Passive voice
            passive_matches = list(re.finditer(self.patterns["passive_voice"], text, re.IGNORECASE))
            for match in passive_matches:
                issues.append({
                    "type": "grammar",
                    "severity": "warning",
                    "position": match.start(),
                    "text": match.group(),
                    "message": "Consider using active voice for clarity",
                    "principle": "crisp_and_clear"
                })
            
            # Long sentences
            long_sentences = list(re.finditer(self.patterns["long_sentences"], text))
            for match in long_sentences:
                issues.append({
                    "type": "grammar",
                    "severity": "info",
                    "position": match.start(),
                    "message": "Long sentence detected - consider breaking into shorter sentences",
                    "principle": "crisp_and_clear"
                })
        
        # Terminology analysis
        if analysis_type in ["comprehensive", "terminology"]:
            for term, standard in self.terminology_standards.items():
                for avoid_term in standard["avoid"]:
                    if avoid_term.lower() in text.lower():
                        issues.append({
                            "type": "terminology",
                            "severity": "warning",
                            "text": avoid_term,
                            "message": f"Use '{standard['correct']}' instead of '{avoid_term}'",
                            "note": standard["note"]
                        })
        
        # Accessibility analysis
        if analysis_type in ["comprehensive", "accessibility"]:
            # Non-inclusive language
            non_inclusive_matches = list(re.finditer(self.patterns["non_inclusive_terms"], text, re.IGNORECASE))
            for match in non_inclusive_matches:
                issues.append({
                    "type": "accessibility",
                    "severity": "error",
                    "position": match.start(),
                    "text": match.group(),
                    "message": f"'{match.group()}' may not be inclusive - consider alternatives",
                    "principle": "bias_free_communication"
                })
            
            # Gendered pronouns
            gendered_matches = list(re.finditer(self.patterns["gendered_pronouns"], text, re.IGNORECASE))
            for match in gendered_matches:
                issues.append({
                    "type": "accessibility",
                    "severity": "warning",
                    "position": match.start(),
                    "text": match.group(),
                    "message": "Consider gender-neutral alternatives",
                    "principle": "bias_free_communication"
                })
        
        # Generate overall assessment
        total_issues = len(issues)
        if total_issues == 0:
            status = "✅ Excellent"
            assessment = "Content follows Microsoft Style Guide principles well"
        elif total_issues <= 2:
            status = "⚠️ Good"
            assessment = "Minor style improvements suggested"
        else:
            status = "❌ Needs Work"
            assessment = "Multiple style issues detected"
        
        return {
            "status": status,
            "assessment": assessment,
            "statistics": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_words_per_sentence": avg_words_per_sentence
            },
            "issues": issues,
            "suggestions": suggestions,
            "total_issues": total_issues,
            "analysis_type": analysis_type,
            "style_guide_url": self.style_guide_base_url
        }

    def review_document(self, document_text: str, document_type: str = "general", 
                       target_audience: str = "general", review_focus: str = "all") -> Dict[str, Any]:
        """Comprehensive document review using Microsoft Style Guide criteria."""
        
        # Perform comprehensive analysis
        analysis = self.analyze_content(document_text, "comprehensive")
        
        # Calculate quality scores
        quality_scores = self._calculate_quality_scores(analysis, document_text)
        
        # Generate detailed review sections
        voice_tone_review = self._review_voice_tone(analysis, document_text)
        clarity_review = self._review_clarity(analysis, document_text)
        structure_review = self._review_structure(document_text, document_type)
        ux_review = self._review_user_experience(document_text, target_audience)
        compliance_review = self._review_compliance(analysis)
        
        # Generate improvement recommendations
        recommendations = self._generate_recommendations(analysis, quality_scores)
        
        # Create rewrite examples
        rewrite_examples = self._generate_rewrite_examples(analysis, document_text)
        
        # Calculate overall score
        overall_score = round(sum(quality_scores.values()) / len(quality_scores), 1)
        
        return {
            "document_info": {
                "type": document_type,
                "audience": target_audience,
                "focus": review_focus,
                "word_count": analysis["statistics"]["word_count"],
                "sentence_count": analysis["statistics"]["sentence_count"]
            },
            "executive_summary": {
                "overall_score": overall_score,
                "quality_level": self._get_quality_level(overall_score),
                "key_strengths": self._identify_strengths(analysis, quality_scores),
                "critical_issues": self._identify_critical_issues(analysis),
                "next_steps": self._generate_next_steps(overall_score, analysis)
            },
            "detailed_analysis": {
                "voice_tone": voice_tone_review,
                "clarity": clarity_review,
                "structure": structure_review,
                "user_experience": ux_review,
                "compliance": compliance_review
            },
            "recommendations": recommendations,
            "rewrite_examples": rewrite_examples,
            "quality_scores": quality_scores,
            "style_guide_url": self.style_guide_base_url
        }

    def _calculate_quality_scores(self, analysis: Dict, document_text: str) -> Dict[str, float]:
        """Calculate quality scores for different aspects."""
        
        # Voice & Tone Score (0-10)
        contractions = len(re.findall(self.patterns["contractions"], document_text, re.IGNORECASE))
        you_usage = len(re.findall(self.patterns["you_addressing"], document_text, re.IGNORECASE))
        voice_issues = len([i for i in analysis["issues"] if i["type"] == "voice_tone"])
        
        voice_score = 10.0
        voice_score -= voice_issues * 2.0
        voice_score += min(contractions * 0.5, 2.0)  # Bonus for contractions
        voice_score += min(you_usage * 0.2, 1.0)     # Bonus for 'you' usage
        voice_score = max(0, min(10, voice_score))
        
        # Clarity Score (0-10)
        avg_sentence_length = analysis["statistics"]["avg_words_per_sentence"]
        clarity_issues = len([i for i in analysis["issues"] if i["type"] == "grammar"])
        
        clarity_score = 10.0
        clarity_score -= clarity_issues * 1.5
        if avg_sentence_length > 25:
            clarity_score -= (avg_sentence_length - 25) * 0.1
        clarity_score = max(0, min(10, clarity_score))
        
        # Accessibility Score (0-10)
        accessibility_issues = len([i for i in analysis["issues"] if i["type"] == "accessibility"])
        
        accessibility_score = 10.0
        accessibility_score -= accessibility_issues * 3.0  # Heavy penalty for accessibility issues
        accessibility_score = max(0, min(10, accessibility_score))
        
        # Compliance Score (0-10)
        terminology_issues = len([i for i in analysis["issues"] if i["type"] == "terminology"])
        
        compliance_score = 10.0
        compliance_score -= terminology_issues * 2.0
        compliance_score = max(0, min(10, compliance_score))
        
        return {
            "voice_tone": voice_score,
            "clarity": clarity_score,
            "accessibility": accessibility_score,
            "compliance": compliance_score
        }

    def _review_voice_tone(self, analysis: Dict, document_text: str) -> Dict[str, Any]:
        """Review voice and tone aspects."""
        voice_issues = [i for i in analysis["issues"] if i["type"] == "voice_tone"]
        
        # Check for Microsoft's three voice principles
        contractions_count = len(re.findall(self.patterns["contractions"], document_text, re.IGNORECASE))
        you_count = len(re.findall(self.patterns["you_addressing"], document_text, re.IGNORECASE))
        
        warm_relaxed = "✅ Good" if contractions_count > 0 else "❌ Missing contractions"
        crisp_clear = "✅ Good" if analysis["statistics"]["avg_words_per_sentence"] <= 25 else "⚠️ Sentences too long"
        ready_help = "✅ Good" if you_count > 0 else "⚠️ Limited direct address"
        
        return {
            "warm_and_relaxed": warm_relaxed,
            "crisp_and_clear": crisp_clear,
            "ready_to_help": ready_help,
            "issues": voice_issues,
            "contractions_found": contractions_count,
            "direct_address_count": you_count
        }

    def _review_clarity(self, analysis: Dict, document_text: str) -> Dict[str, Any]:
        """Review clarity aspects."""
        clarity_issues = [i for i in analysis["issues"] if i["type"] == "grammar"]
        
        # Check readability factors
        passive_voice_count = len(re.findall(self.patterns["passive_voice"], document_text, re.IGNORECASE))
        long_sentences = len(re.findall(self.patterns["long_sentences"], document_text))
        
        return {
            "passive_voice_instances": passive_voice_count,
            "long_sentences": long_sentences,
            "avg_sentence_length": analysis["statistics"]["avg_words_per_sentence"],
            "clarity_issues": clarity_issues,
            "readability_level": "Good" if passive_voice_count <= 2 and long_sentences == 0 else "Needs Improvement"
        }

    def _review_structure(self, document_text: str, document_type: str) -> Dict[str, Any]:
        """Review document structure."""
        
        # Basic structure analysis
        paragraphs = [p.strip() for p in document_text.split('\n\n') if p.strip()]
        headings = len(re.findall(r'^#+\s', document_text, re.MULTILINE))
        lists = len(re.findall(r'^\s*[-*+]\s', document_text, re.MULTILINE))
        
        # Structure assessment based on document type
        structure_quality = "Good"
        if document_type in ["tutorial", "user_guide"] and headings < 3:
            structure_quality = "Needs more headings for navigation"
        elif len(paragraphs) > 10 and headings < 2:
            structure_quality = "Long content needs better organization"
        
        return {
            "paragraph_count": len(paragraphs),
            "heading_count": headings,
            "list_count": lists,
            "structure_quality": structure_quality,
            "organization_score": min(10, headings * 2 + lists * 0.5)
        }

    def _review_user_experience(self, document_text: str, target_audience: str) -> Dict[str, Any]:
        """Review user experience aspects."""
        
        # Check for user-friendly elements
        action_verbs = len(re.findall(r'\b(click|select|choose|enter|type|navigate|open|close)\b', document_text, re.IGNORECASE))
        error_prevention = len(re.findall(r'\b(note|important|warning|tip|caution)\b', document_text, re.IGNORECASE))
        examples = len(re.findall(r'\b(example|for instance|such as)\b', document_text, re.IGNORECASE))
        
        # UX quality assessment
        ux_score = 0
        ux_score += min(action_verbs * 0.5, 3)
        ux_score += min(error_prevention * 1, 3)
        ux_score += min(examples * 1, 2)
        
        return {
            "action_oriented_language": action_verbs,
            "error_prevention_elements": error_prevention,
            "examples_provided": examples,
            "ux_score": min(10, ux_score),
            "audience_appropriateness": "Appropriate" if target_audience != "expert" or examples > 0 else "May need more examples"
        }

    def _review_compliance(self, analysis: Dict) -> Dict[str, Any]:
        """Review Microsoft Style Guide compliance."""
        
        terminology_issues = [i for i in analysis["issues"] if i["type"] == "terminology"]
        accessibility_issues = [i for i in analysis["issues"] if i["type"] == "accessibility"]
        
        compliance_level = "Excellent"
        if len(terminology_issues) > 0 or len(accessibility_issues) > 0:
            compliance_level = "Needs Improvement"
        elif len(analysis["issues"]) > 3:
            compliance_level = "Partially Compliant"
        
        return {
            "terminology_compliance": len(terminology_issues) == 0,
            "accessibility_compliance": len(accessibility_issues) == 0,
            "overall_compliance": compliance_level,
            "compliance_issues": terminology_issues + accessibility_issues
        }

    def _generate_recommendations(self, analysis: Dict, quality_scores: Dict) -> Dict[str, List[str]]:
        """Generate prioritized improvement recommendations."""
        
        high_priority = []
        medium_priority = []
        low_priority = []
        
        # High priority (accessibility and critical issues)
        accessibility_issues = [i for i in analysis["issues"] if i["type"] == "accessibility" and i["severity"] == "error"]
        if accessibility_issues:
            high_priority.append("Fix inclusive language violations - these are critical for Microsoft standards")
        
        if quality_scores["accessibility"] < 7:
            high_priority.append("Address accessibility concerns immediately")
        
        # Medium priority (voice, tone, major clarity issues)
        if quality_scores["voice_tone"] < 7:
            medium_priority.append("Improve voice and tone to match Microsoft's warm, conversational style")
        
        if quality_scores["clarity"] < 7:
            medium_priority.append("Simplify complex sentences and reduce passive voice usage")
        
        if analysis["statistics"]["avg_words_per_sentence"] > 25:
            medium_priority.append("Break down long sentences for better readability")
        
        # Low priority (minor improvements)
        if quality_scores["compliance"] < 9:
            low_priority.append("Update terminology to match Microsoft standards")
        
        if len(re.findall(r"\b(it's|you're|we're|don't|can't|won't)\b", str(analysis), re.IGNORECASE)) == 0:
            low_priority.append("Add contractions to make tone more natural and conversational")
        
        return {
            "high_priority": high_priority or ["No critical issues found"],
            "medium_priority": medium_priority or ["Minor style improvements available"],
            "low_priority": low_priority or ["Content meets Microsoft standards well"]
        }

    def _generate_rewrite_examples(self, analysis: Dict, document_text: str) -> List[Dict[str, str]]:
        """Generate before/after rewrite examples."""
        
        examples = []
        
        # Find passive voice examples
        passive_matches = list(re.finditer(self.patterns["passive_voice"], document_text, re.IGNORECASE))
        if passive_matches:
            match = passive_matches[0]
            sentence_start = max(0, document_text.rfind('.', 0, match.start()) + 1)
            sentence_end = document_text.find('.', match.end())
            if sentence_end == -1:
                sentence_end = len(document_text)
            
            original = document_text[sentence_start:sentence_end].strip()
            improved = re.sub(r'\b(is|are|was|were|been|be)\s+(\w+ed)\b', 
                            lambda m: f"the system {m.group(2).replace('ed', 's')}" if m.group(1) in ['is', 'are'] 
                            else f"we {m.group(2).replace('ed', '')}", original, flags=re.IGNORECASE)
            
            examples.append({
                "category": "Active Voice",
                "before": original,
                "after": improved,
                "explanation": "Changed from passive to active voice for clarity and directness"
            })
        
        # Find non-inclusive language examples
        non_inclusive_matches = list(re.finditer(self.patterns["non_inclusive_terms"], document_text, re.IGNORECASE))
        if non_inclusive_matches:
            match = non_inclusive_matches[0]
            original_word = match.group()
            
            replacements = {
                "guys": "everyone", "mankind": "humanity", "blacklist": "block list",
                "whitelist": "allow list", "master": "primary", "slave": "secondary"
            }
            
            replacement = replacements.get(original_word.lower(), "inclusive alternative")
            
            examples.append({
                "category": "Inclusive Language",
                "before": f"...{original_word}...",
                "after": f"...{replacement}...",
                "explanation": f"Replaced '{original_word}' with more inclusive language"
            })
        
        # Add contractions example if none found
        if not re.search(self.patterns["contractions"], document_text, re.IGNORECASE):
            examples.append({
                "category": "Natural Tone",
                "before": "You cannot access this feature.",
                "after": "You can't access this feature.",
                "explanation": "Added contractions for a more natural, conversational tone"
            })
        
        return examples[:3]  # Limit to 3 examples

    def _get_quality_level(self, score: float) -> str:
        """Convert numeric score to quality level."""
        if score >= 9:
            return "Excellent"
        elif score >= 7:
            return "Good"
        elif score >= 5:
            return "Needs Improvement"
        else:
            return "Requires Major Revision"

    def _identify_strengths(self, analysis: Dict, quality_scores: Dict) -> List[str]:
        """Identify key strengths in the content."""
        strengths = []
        
        if quality_scores["voice_tone"] >= 8:
            strengths.append("Strong Microsoft voice and tone compliance")
        
        if quality_scores["accessibility"] >= 9:
            strengths.append("Excellent inclusive language usage")
        
        if analysis["statistics"]["avg_words_per_sentence"] <= 20:
            strengths.append("Good sentence length for readability")
        
        if len(analysis["suggestions"]) > 0:
            strengths.append("Uses engaging, direct language effectively")
        
        return strengths[:3] or ["Content follows basic writing principles"]

    def _identify_critical_issues(self, analysis: Dict) -> List[str]:
        """Identify critical issues that need immediate attention."""
        critical = []
        
        accessibility_errors = [i for i in analysis["issues"] if i["type"] == "accessibility" and i["severity"] == "error"]
        if accessibility_errors:
            critical.append(f"Accessibility violations: {len(accessibility_errors)} instances of non-inclusive language")
        
        if analysis["statistics"]["avg_words_per_sentence"] > 30:
            critical.append("Sentences are too long - will significantly impact readability")
        
        passive_voice_count = len([i for i in analysis["issues"] if "passive" in i.get("message", "")])
        if passive_voice_count > 5:
            critical.append("Excessive passive voice usage affects clarity")
        
        return critical[:3] or ["No critical issues identified"]

    def _generate_next_steps(self, score: float, analysis: Dict) -> List[str]:
        """Generate recommended next steps based on review."""
        if score >= 8:
            return ["Content is ready for publication", "Consider final proofreading pass"]
        elif score >= 6:
            return ["Address medium-priority recommendations", "Review with stakeholders", "One more revision recommended"]
        else:
            return ["Major revision needed", "Focus on high-priority issues first", "Consider restructuring content"]

    def get_style_guidelines(self, category: str = "all") -> Dict[str, Any]:
        """Get Microsoft Style Guide guidelines for a specific category."""
        guidelines = {
            "category": category,
            "base_url": self.style_guide_base_url,
            "principles": {}
        }
        
        if category in ["voice", "all"]:
            guidelines["principles"]["voice_and_tone"] = {
                "warm_and_relaxed": [
                    "Use contractions (it's, you're, we'll)",
                    "Write like you speak - natural, conversational",
                    "Be friendly and approachable"
                ],
                "crisp_and_clear": [
                    "Be direct and scannable",
                    "Keep sentences under 25 words",
                    "Use simple, clear language"
                ],
                "ready_to_help": [
                    "Use action-oriented language",
                    "Address readers as 'you'",
                    "Be supportive and encouraging"
                ]
            }
        
        if category in ["grammar", "all"]:
            guidelines["principles"]["grammar"] = {
                "active_voice": "Use active voice for clarity and engagement",
                "sentence_structure": "Keep sentences short and parallel",
                "imperative_mood": "Use for instructions (Click, Choose, Select)"
            }
        
        if category in ["terminology", "all"]:
            guidelines["principles"]["terminology"] = self.terminology_standards
        
        if category in ["accessibility", "all"]:
            guidelines["principles"]["accessibility"] = {
                "inclusive_language": [
                    "Use 'everyone' instead of 'guys'",
                    "Use 'allow list' instead of 'whitelist'",
                    "Use 'primary/secondary' instead of 'master/slave'"
                ],
                "people_first": "Use 'people with disabilities' not 'disabled people'",
                "gender_neutral": "Avoid gendered pronouns in generic references"
            }
        
        return guidelines

    def suggest_improvements(self, text: str, focus_area: str = "all") -> Dict[str, Any]:
        """Generate specific improvement suggestions for the text."""
        analysis = self.analyze_content(text, "comprehensive")
        improvements = []
        
        for issue in analysis["issues"]:
            if focus_area == "all" or issue["type"] == focus_area:
                improvement = {
                    "issue": issue["message"],
                    "suggestion": self._get_improvement_suggestion(issue),
                    "type": issue["type"],
                    "severity": issue["severity"]
                }
                improvements.append(improvement)
        
        # Add general improvements
        if analysis["statistics"]["avg_words_per_sentence"] > 25:
            improvements.append({
                "issue": "Average sentence length is high",
                "suggestion": "Break long sentences into shorter, clearer ones",
                "type": "grammar",
                "severity": "info"
            })
        
        return {
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "total_improvements": len(improvements),
            "improvements": improvements,
            "focus_area": focus_area,
            "style_guide_url": f"{self.style_guide_base_url}/top-10-tips-style-voice"
        }
    
    def _get_improvement_suggestion(self, issue: Dict[str, Any]) -> str:
        """Generate specific improvement suggestion based on issue type."""
        issue_type = issue["type"]
        
        if issue_type == "voice_tone":
            return "Use more contractions and direct language to sound natural and friendly"
        elif issue_type == "grammar" and "passive" in issue["message"]:
            return f"Change '{issue.get('text', '')}' to active voice"
        elif issue_type == "terminology":
            return f"Replace with Microsoft-approved term as noted"
        elif issue_type == "accessibility":
            return f"Use inclusive alternative for '{issue.get('text', '')}'"
        else:
            return "Follow Microsoft Style Guide recommendations"
    
    def track_change(self, file_path: str, line_number: int, change_description: str):
        """Track a change made to a document for the github_updates summary."""
        from datetime import datetime
        
        change_entry = {
            "timestamp": datetime.now(),
            "file_path": file_path,
            "line_number": line_number,
            "description": change_description
        }
        self.change_history.append(change_entry)
    
    def get_github_updates_summary(self) -> Dict[str, Any]:
        """Generate a concise summary of all changes made by the MCP Server."""
        from datetime import datetime
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        total_updates = len(self.change_history)
        
        # Format changes for display
        formatted_changes = []
        for change in self.change_history:
            change_text = f"- {change['description']}"
            if change['line_number'] > 0:
                change_text += f" (line {change['line_number']})"
            formatted_changes.append(change_text)
        
        # If no changes tracked, provide a default message
        if not formatted_changes:
            formatted_changes = ["- No changes tracked in current session"]
        
        summary_text = f"""**Summary of Changes for Microsoft Style Guide**
**Date:** {current_date}
**Changes:**
{chr(10).join(formatted_changes)}

**Total updates:** {total_updates}

📋 **For Pull Request:**
Copy the summary above to include in your pull request description. This provides reviewers with a clear audit trail of all Microsoft Style Guide improvements made during your session."""
        
        return {
            "summary": summary_text,
            "date": current_date,
            "total_updates": total_updates,
            "changes": self.change_history,
            "formatted_summary": summary_text,
            "pr_instructions": "Copy the summary above to include in your pull request description."
        }

# Initialize the analyzer
analyzer = MicrosoftStyleGuideAnalyzer()

# FastMCP Server Implementation
if MCP_AVAILABLE:
    try:
        # Try FastMCP first
        app = FastMCP("Microsoft Style Guide")
        
        @app.tool()
        def analyze_content(text: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
            """Analyze content against Microsoft Style Guide principles."""
            if not text.strip():
                return {"error": "No text provided for analysis"}
            
            result = analyzer.analyze_content(text, analysis_type)
            
            # Track changes/issues found for github_updates summary
            if result['issues']:
                for issue in result['issues']:
                    line_num = issue.get('position', 0) // 50 + 1  # Rough estimate of line number
                    change_desc = f"Style issue identified: {issue['message']}"
                    analyzer.track_change("content_analysis", line_num, change_desc)
            
            # Format for display
            summary = f"""📋 Microsoft Style Guide Analysis

{result['status']} - {result['assessment']}

📊 **Text Statistics:**
   • Words: {result['statistics']['word_count']}
   • Sentences: {result['statistics']['sentence_count']}
   • Avg words/sentence: {result['statistics']['avg_words_per_sentence']}

🔍 **Issues Found:** {result['total_issues']}"""
            
            if result['issues']:
                issues_by_type = {}
                for issue in result['issues']:
                    issue_type = issue['type']
                    if issue_type not in issues_by_type:
                        issues_by_type[issue_type] = []
                    issues_by_type[issue_type].append(issue)
                
                for issue_type, issues_list in issues_by_type.items():
                    summary += f"\n   • {issue_type.replace('_', ' ').title()}: {len(issues_list)}"
            
            if result['suggestions']:
                summary += f"\n\n✅ **Positive Elements:** {len(result['suggestions'])}"
            
            summary += f"\n\n🌐 **Official Guidelines:** {result['style_guide_url']}"
            
            return {"summary": summary, "detailed": result}
        
        @app.tool()
        def microsoft_document_reviewer(document_text: str, document_type: str = "general", 
                                      target_audience: str = "general", review_focus: str = "all") -> Dict[str, Any]:
            """Comprehensive document review using Microsoft Style Guide criteria for technical writers."""
            if not document_text.strip():
                return {"error": "No document text provided for review"}
            
            review = analyzer.review_document(document_text, document_type, target_audience, review_focus)
            
            # Format comprehensive review for display
            summary = f"""📋 Microsoft Style Guide Document Review

## Executive Summary
**Overall Quality Score:** {review['executive_summary']['overall_score']}/10 ({review['executive_summary']['quality_level']})
**Document Type:** {review['document_info']['type'].title()}
**Target Audience:** {review['document_info']['audience'].title()}
**Word Count:** {review['document_info']['word_count']}

### Key Strengths
{chr(10).join(f"✅ {strength}" for strength in review['executive_summary']['key_strengths'])}

### Critical Issues
{chr(10).join(f"🔴 {issue}" for issue in review['executive_summary']['critical_issues'])}

### Recommended Next Steps
{chr(10).join(f"📌 {step}" for step in review['executive_summary']['next_steps'])}

## Quality Scores
**Voice & Tone:** {review['quality_scores']['voice_tone']}/10
**Clarity:** {review['quality_scores']['clarity']}/10  
**Accessibility:** {review['quality_scores']['accessibility']}/10
**Compliance:** {review['quality_scores']['compliance']}/10

## Voice & Tone Assessment
**Warm & Relaxed:** {review['detailed_analysis']['voice_tone']['warm_and_relaxed']}
**Crisp & Clear:** {review['detailed_analysis']['voice_tone']['crisp_and_clear']}
**Ready to Help:** {review['detailed_analysis']['voice_tone']['ready_to_help']}
- Contractions found: {review['detailed_analysis']['voice_tone']['contractions_found']}
- Direct address count: {review['detailed_analysis']['voice_tone']['direct_address_count']}

## Clarity Analysis
**Readability Level:** {review['detailed_analysis']['clarity']['readability_level']}
- Average sentence length: {review['detailed_analysis']['clarity']['avg_sentence_length']} words
- Passive voice instances: {review['detailed_analysis']['clarity']['passive_voice_instances']}
- Long sentences: {review['detailed_analysis']['clarity']['long_sentences']}

## User Experience Review
**UX Score:** {review['detailed_analysis']['user_experience']['ux_score']}/10
- Action-oriented language: {review['detailed_analysis']['user_experience']['action_oriented_language']} instances
- Error prevention elements: {review['detailed_analysis']['user_experience']['error_prevention_elements']}
- Examples provided: {review['detailed_analysis']['user_experience']['examples_provided']}
- Audience appropriateness: {review['detailed_analysis']['user_experience']['audience_appropriateness']}

## Improvement Recommendations

### High Priority
{chr(10).join(f"🔴 {rec}" for rec in review['recommendations']['high_priority'])}

### Medium Priority  
{chr(10).join(f"⚠️ {rec}" for rec in review['recommendations']['medium_priority'])}

### Low Priority
{chr(10).join(f"ℹ️ {rec}" for rec in review['recommendations']['low_priority'])}

## Rewrite Examples"""

            # Add rewrite examples
            for i, example in enumerate(review['rewrite_examples'], 1):
                summary += f"""

### {i}. {example['category']}
**Before:** {example['before']}
**After:** {example['after']}
**Why:** {example['explanation']}"""

            summary += f"""

## Microsoft Style Guide Resources
📚 **Official Guide:** {review['style_guide_url']}
📖 **Voice & Tone:** {review['style_guide_url']}/brand-voice-above-all-simple-human
🔍 **Word List:** {review['style_guide_url']}/a-z-word-list-term-collections
♿ **Accessibility:** {review['style_guide_url']}/bias-free-communication"""

            return {"formatted_review": summary, "detailed_data": review}
        
        @app.tool()
        def get_style_guidelines(category: str = "all") -> Dict[str, Any]:
            """Get Microsoft Style Guide guidelines for a specific category."""
            guidelines = analyzer.get_style_guidelines(category)
            
            # Format for display
            response = f"""📚 Microsoft Writing Style Guide - {category.title()} Guidelines

🌐 **Official Documentation:** {guidelines['base_url']}

"""
            
            for principle_name, principle_data in guidelines['principles'].items():
                response += f"## {principle_name.replace('_', ' ').title()}\n\n"
                
                if isinstance(principle_data, dict):
                    for key, value in principle_data.items():
                        response += f"**{key.replace('_', ' ').title()}:**\n"
                        if isinstance(value, list):
                            for item in value:
                                response += f"• {item}\n"
                        else:
                            response += f"• {value}\n"
                        response += "\n"
                elif isinstance(principle_data, str):
                    response += f"• {principle_data}\n\n"
            
            return {"formatted": response, "data": guidelines}
        
        @app.tool()
        def suggest_improvements(text: str, focus_area: str = "all") -> Dict[str, Any]:
            """Get improvement suggestions for content."""
            if not text.strip():
                return {"error": "No text provided for improvement suggestions"}
            
            improvements = analyzer.suggest_improvements(text, focus_area)
            
            # Format for display
            response = f"""💡 Microsoft Style Guide Improvement Suggestions

**Text:** "{improvements['text_preview']}"
**Focus Area:** {focus_area.replace('_', ' ').title()}
**Total Improvements:** {improvements['total_improvements']}

"""
            
            if improvements['improvements']:
                response += "**Specific Improvements:**\n"
                for i, improvement in enumerate(improvements['improvements'], 1):
                    severity_icon = "🔴" if improvement['severity'] == "error" else "⚠️" if improvement['severity'] == "warning" else "ℹ️"
                    response += f"{i}. {severity_icon} **{improvement['type'].replace('_', ' ').title()}:** {improvement['suggestion']}\n"
                response += "\n"
            else:
                response += "✅ **No improvements needed** - content follows Microsoft Style Guide well!\n\n"
            
            response += f"📚 **Reference:** {improvements['style_guide_url']}"
            
            return {"formatted": response, "data": improvements}
        
        @app.tool()
        def search_style_guide(query: str) -> Dict[str, Any]:
            """Search Microsoft Style Guide for specific guidance."""
            if not query.strip():
                return {"error": "No search query provided"}
            
            # Provide search guidance and relevant URLs
            search_url = f"{analyzer.style_guide_base_url}/?search={query.replace(' ', '%20')}"
            
            response = f"""🔍 Microsoft Style Guide Search

**Query:** "{query}"

**Search URL:** {search_url}

**Key Resources:**
• Voice & Tone: {analyzer.style_guide_base_url}/brand-voice-above-all-simple-human
• Writing Tips: {analyzer.style_guide_base_url}/global-communications/writing-tips
• Bias-Free Communication: {analyzer.style_guide_base_url}/bias-free-communication
• A-Z Word List: {analyzer.style_guide_base_url}/a-z-word-list-term-collections
• Top 10 Tips: {analyzer.style_guide_base_url}/top-10-tips-style-voice

💡 **Tip:** Visit the search URL above for the most current guidance on your query.
"""
            
            return {"formatted": response, "search_url": search_url, "query": query}

        # Add prompt support if FastMCP supports it
        if hasattr(app, 'prompt'):
            @app.prompt()
            def microsoft_style_guide_reviewer():
                """Microsoft Style Guide Document Reviewer - Comprehensive review prompt for technical writers."""
                return {
                    "name": "microsoft_document_reviewer", 
                    "description": "Performs comprehensive document review using Microsoft Style Guide criteria, providing detailed feedback on voice, clarity, structure, and user experience for technical writers.",
                    "arguments": [
                        {
                            "name": "document_text",
                            "description": "The document content to review",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "document_type", 
                            "description": "Type of document (api_docs, user_guide, tutorial, troubleshooting, general)",
                            "required": False,
                            "type": "string",
                            "default": "general"
                        },
                        {
                            "name": "target_audience",
                            "description": "Intended audience (developer, end_user, admin, mixed, general)", 
                            "required": False,
                            "type": "string",
                            "default": "general"
                        },
                        {
                            "name": "review_focus",
                            "description": "Specific areas to emphasize (voice_tone, structure, clarity, accessibility, all)",
                            "required": False, 
                            "type": "string",
                            "default": "all"
                        }
                    ],
                    "template": """You are a senior technical writing editor specializing in Microsoft Style Guide compliance. Review the provided document and provide comprehensive feedback using these evaluation criteria:

## Document Context
- **Type**: {{document_type}}
- **Audience**: {{target_audience}}  
- **Focus Areas**: {{review_focus}}

## Review Framework

### 1. Microsoft Voice & Tone Assessment
- **Warm and Relaxed**: Does the content use contractions and natural language?
- **Crisp and Clear**: Is the content direct, scannable, and concise?
- **Ready to Help**: Does it use action-oriented, supportive language?

### 2. Technical Writing Quality
- **Clarity**: Are complex concepts explained clearly?
- **Completeness**: Does it cover all necessary information?
- **Accuracy**: Is technical information precise and current?
- **Structure**: Is information logically organized?

### 3. User Experience Evaluation
- **Task Success**: Can users complete their goals with this content?
- **Cognitive Load**: Is the information digestible?
- **Error Prevention**: Does it help users avoid common mistakes?
- **Accessibility**: Is it inclusive and barrier-free?

### 4. Content Standards Compliance
- **Terminology**: Follows Microsoft terminology standards
- **Grammar**: Uses active voice, proper sentence structure
- **Formatting**: Consistent with Microsoft documentation patterns
- **Cross-references**: Links and references are accurate

## Required Output Format

### Executive Summary
- Overall quality score (1-10)
- Key strengths (2-3 points)
- Critical issues (2-3 points)
- Recommended next steps

### Detailed Analysis
**Voice & Tone Issues**: [Specific examples with suggestions]
**Clarity Problems**: [Areas needing simplification or explanation]
**Structural Concerns**: [Organization and flow issues]
**User Experience Gaps**: [Where users might struggle]
**Compliance Issues**: [Microsoft Style Guide violations]

### Improvement Recommendations
**High Priority**: [Critical fixes needed immediately]
**Medium Priority**: [Important improvements for next revision]
**Low Priority**: [Nice-to-have enhancements]

### Rewrite Examples
Provide 2-3 "before/after" examples showing how to improve problematic sections using Microsoft Style Guide principles.

Please review this document: {{document_text}}"""
                }
    
    except NameError:
        # FastMCP not available, use standard MCP
        logger.info("FastMCP not available, using standard MCP implementation")
        MCP_AVAILABLE = False

# Fallback for when MCP is not available
if not MCP_AVAILABLE:
    class MockApp:
        def __init__(self, name):
            self.name = name
            self.tools = {}
        
        def tool(self):
            def decorator(func):
                self.tools[func.__name__] = func
                return func
            return decorator
        
        async def run_stdio(self):
            print(f"Mock MCP server '{self.name}' running in development mode")
            print("Available tools:", list(self.tools.keys()))
            # Simple test
            if "analyze_content" in self.tools:
                result = self.tools["analyze_content"]("Hello, you can easily set up your account!")
                print("Test analysis:", result)
    
    app = MockApp("Microsoft Style Guide")
    
    # Add the same tools but as regular functions
    @app.tool()
    def analyze_content(text: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Analyze content against Microsoft Style Guide principles."""
        if not text.strip():
            return {"error": "No text provided for analysis"}
        return analyzer.analyze_content(text, analysis_type)
    
    @app.tool()
    def microsoft_document_reviewer(document_text: str, document_type: str = "general", 
                                  target_audience: str = "general", review_focus: str = "all") -> Dict[str, Any]:
        """Comprehensive document review using Microsoft Style Guide criteria."""
        if not document_text.strip():
            return {"error": "No document text provided for review"}
        return analyzer.review_document(document_text, document_type, target_audience, review_focus)
    
    @app.tool()
    def get_style_guidelines(category: str = "all") -> Dict[str, Any]:
        """Get Microsoft Style Guide guidelines."""
        return analyzer.get_style_guidelines(category)
    
    @app.tool()
    def suggest_improvements(text: str, focus_area: str = "all") -> Dict[str, Any]:
        """Get improvement suggestions."""
        if not text.strip():
            return {"error": "No text provided"}
        return analyzer.suggest_improvements(text, focus_area)
    
    @app.tool()
    def search_style_guide(query: str) -> Dict[str, Any]:
        """Search Microsoft Style Guide."""
        if not query.strip():
            return {"error": "No query provided"}
        return {"query": query, "url": f"{analyzer.style_guide_base_url}/?search={query}"}
    
    @app.tool()
    def github_updates() -> Dict[str, Any]:
        """Generate a concise summary of all changes made by the MCP Server to articles.
        Call this tool with '/github_updates' in the chat to get a summary of changes."""
        return analyzer.get_github_updates_summary()

async def main():
    """Run the MCP server."""
    parser = argparse.ArgumentParser(description="Microsoft Style Guide MCP Server - FastMCP Version")
    parser.add_argument("--version", action="version", version="microsoft-style-guide-fastmcp 1.0.0")
    parser.add_argument("--test", action="store_true", help="Run a quick test")
    
    args = parser.parse_args()
    
    if args.test:
        # Run a quick test - use analyzer directly to avoid FastMCP tool wrapper issues
        test_text = "You can easily configure the settings to suit your needs."
        result = analyzer.analyze_content(test_text)
        print("Test Result:", json.dumps(result, indent=2))
        
        # Test document reviewer
        review_result = analyzer.review_document(test_text, "tutorial", "developer")
        print("\nDocument Review Test:", json.dumps(review_result, indent=2))
        return
    
    logger.info("Starting Microsoft Style Guide MCP Server (FastMCP)")
    
    try:
        if hasattr(app, 'run_stdio_async'):
            # FastMCP
            await app.run_stdio_async()
        elif hasattr(app, 'run_stdio'):
            # Standard MCP
            await app.run_stdio()
        else:
            # Mock implementation
            await app.run_stdio()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())