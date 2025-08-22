#!/usr/bin/env python3
"""
Microsoft Style Guide MCP Server Auto-Updater

This script can update the MCP server from a GitHub repository.
Can be run standalone or integrated as an MCP tool.
"""

import asyncio
import json
import logging
import os
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import subprocess
import hashlib

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    import urllib.request
    import urllib.parse
    import urllib.error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServerUpdater:
    """Handles updating the MCP server from GitHub repository."""
    
    def __init__(self, 
                 repo_owner: Optional[str] = None,
                 repo_name: Optional[str] = None,
                 current_version: Optional[str] = None,
                 config_file: str = "update_config.json"):
        """Initialize the updater.
        
        Args:
            repo_owner: GitHub repository owner
            repo_name: GitHub repository name  
            current_version: Current version of the MCP server
            config_file: Path to configuration file
        """
        # Load configuration from file
        self.config = self._load_config(config_file)
        
        # Use provided values or fall back to config, then defaults
        self.repo_owner = repo_owner or self.config.get("repository", {}).get("owner", "asudbring")
        self.repo_name = repo_name or self.config.get("repository", {}).get("name", "ms-style-guide-fastmcp-server")
        self.current_version = current_version or self._detect_current_version()
        self.github_api_base = "https://api.github.com"
        self.repo_api_url = f"{self.github_api_base}/repos/{self.repo_owner}/{self.repo_name}"
        self.session = None
        
        # Files to update (can be configured)
        self.update_files = [
            "fastmcp_style_server.py",
            "fastmcp_style_server_web.py", 
            "copilot_integration.py",
            "requirements.txt",
            "fastmcp_setup.py",
            "readme.md"
        ]
        
        # Files to preserve during update
        self.preserve_files = [
            ".vscode/settings.json",
            "vscode_mcp_config.json",
            "mcp_manifest.json",
            "test_document.md",
            "copilot_integration.py"
        ]
        
        # Backup directory
        self.backup_dir = Path("backups")
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"Config file not found: {config_file}, using defaults")
                return {}
        except Exception as e:
            logger.error(f"Error loading config file {config_file}: {e}")
            return {}
    
    def _detect_current_version(self) -> str:
        """Detect current version from .mcp_version, CHANGELOG.md, git tags, or fallback."""
        try:
            # Try to read from version file first
            version_file = Path(".mcp_version")
            if version_file.exists():
                with open(version_file, 'r') as f:
                    version = f.read().strip()
                    if version:
                        return version
        except Exception:
            pass

        try:
            # Try to read version from top of CHANGELOG.md (first non-empty line)
            changelog_file = Path("CHANGELOG.md")
            if changelog_file.exists():
                with open(changelog_file, 'r', encoding='utf-8') as f:
                    # Read a few lines to find the first meaningful line
                    for _ in range(20):
                        line = f.readline()
                        if not line:
                            break
                        line = line.strip()
                        if not line:
                            continue
                        # Accept patterns like "1.0", "v1.0", "Version: 1.0", "## [1.0] - YYYY-MM-DD"
                        try:
                            import re
                            m = re.search(r'v?(\d+\.\d+(?:\.\d+)?)', line)
                            if m:
                                return m.group(1)
                        except Exception:
                            # If regex fails for any reason, continue to next line
                            continue
        except Exception:
            pass

        try:
            # Try to get version from git tag
            result = subprocess.run(
                ["git", "describe", "--tags", "--exact-match", "HEAD"],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            if result.returncode == 0:
                return result.stdout.strip().lstrip("v")
        except Exception:
            pass

        try:
            # Try to get current commit hash as fallback
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            if result.returncode == 0:
                return f"git-{result.stdout.strip()}"
        except Exception:
            pass

        # Default fallback
        return "1.0.0"
    
    async def get_session(self):
        """Get or create HTTP session."""
        if AIOHTTP_AVAILABLE:
            if self.session is None:
                timeout = aiohttp.ClientTimeout(total=30)
                self.session = aiohttp.ClientSession(timeout=timeout)
            return self.session
        return None
    
    async def close_session(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def check_for_updates(self) -> Dict[str, Any]:
        """Check if updates are available from GitHub."""
        try:
            # First try to get latest release info
            releases_url = f"{self.repo_api_url}/releases/latest"
            
            if AIOHTTP_AVAILABLE:
                session = await self.get_session()
                if session:
                    async with session.get(releases_url) as response:
                        if response.status == 200:
                            release_data = await response.json()
                            latest_version = release_data.get("tag_name", "").lstrip("v")
                            release_notes = release_data.get("body", "")
                            published_at = release_data.get("published_at", "")
                            download_url = release_data.get("zipball_url", "")
                            
                            # Compare versions (simple string comparison for now)
                            update_available = latest_version != self.current_version
                            
                            return {
                                "update_available": update_available,
                                "current_version": self.current_version,
                                "latest_version": latest_version,
                                "release_notes": release_notes,
                                "published_at": published_at,
                                "download_url": download_url,
                                "release_data": release_data,
                                "update_method": "release"
                            }
                        elif response.status == 404:
                            # No releases available, try to get latest commit from main branch
                            return await self._check_latest_commit()
                        else:
                            raise Exception(f"GitHub API error: {response.status}")
                else:
                    raise Exception("HTTP session not available")
            else:
                # Fallback to urllib
                try:
                    with urllib.request.urlopen(releases_url) as response:
                        release_data = json.loads(response.read().decode())
                        latest_version = release_data.get("tag_name", "").lstrip("v")
                        release_notes = release_data.get("body", "")
                        published_at = release_data.get("published_at", "")
                        download_url = release_data.get("zipball_url", "")
                        
                        # Compare versions (simple string comparison for now)
                        update_available = latest_version != self.current_version
                        
                        return {
                            "update_available": update_available,
                            "current_version": self.current_version,
                            "latest_version": latest_version,
                            "release_notes": release_notes,
                            "published_at": published_at,
                            "download_url": download_url,
                            "release_data": release_data,
                            "update_method": "release"
                        }
                except urllib.error.HTTPError as e:
                    if e.code == 404:
                        # No releases available, try to get latest commit from main branch
                        return await self._check_latest_commit()
                    else:
                        raise Exception(f"GitHub API error: {e.code}")
            
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return {
                "update_available": False,
                "error": str(e),
                "current_version": self.current_version
            }
    
    async def _check_latest_commit(self) -> Dict[str, Any]:
        """Check latest commit from main branch when no releases are available."""
        try:
            branch = self.config.get("repository", {}).get("branch", "main")
            commits_url = f"{self.repo_api_url}/commits/{branch}"
            
            if AIOHTTP_AVAILABLE:
                session = await self.get_session()
                if session:
                    async with session.get(commits_url) as response:
                        if response.status == 200:
                            commit_data = await response.json()
                        else:
                            raise Exception(f"GitHub API error: {response.status}")
                else:
                    raise Exception("HTTP session not available")
            else:
                # Fallback to urllib
                with urllib.request.urlopen(commits_url) as response:
                    commit_data = json.loads(response.read().decode())
            
            latest_commit = commit_data.get("sha", "")[:7]  # Short commit hash
            commit_message = commit_data.get("commit", {}).get("message", "")
            commit_date = commit_data.get("commit", {}).get("committer", {}).get("date", "")
            download_url = f"https://github.com/{self.repo_owner}/{self.repo_name}/archive/{branch}.zip"
            
            # Compare with current version
            current_commit = self.current_version.replace("git-", "") if self.current_version.startswith("git-") else ""
            update_available = latest_commit != current_commit and latest_commit != ""
            
            return {
                "update_available": update_available,
                "current_version": self.current_version,
                "latest_version": f"git-{latest_commit}",
                "release_notes": f"Latest commit: {commit_message}",
                "published_at": commit_date,
                "download_url": download_url,
                "commit_data": commit_data,
                "update_method": "commit"
            }
            
        except Exception as e:
            logger.error(f"Error checking latest commit: {e}")
            return {
                "update_available": False,
                "error": str(e),
                "current_version": self.current_version
            }
    
    async def download_update(self, download_url: str, target_path: Path) -> bool:
        """Download update from GitHub."""
        try:
            logger.info(f"Downloading update from: {download_url}")
            
            if AIOHTTP_AVAILABLE:
                session = await self.get_session()
                if session:
                    async with session.get(download_url) as response:
                        if response.status == 200:
                            with open(target_path, 'wb') as f:
                                async for chunk in response.content.iter_chunked(8192):
                                    f.write(chunk)
                        else:
                            raise Exception(f"Download failed: {response.status}")
                else:
                    raise Exception("HTTP session not available")
            else:
                # Fallback to urllib
                urllib.request.urlretrieve(download_url, target_path)
            
            logger.info(f"Download completed: {target_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading update: {e}")
            return False
    
    def create_backup(self) -> str:
        """Create backup of current installation."""
        try:
            # Create backup directory with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}"
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Backup current files
            current_dir = Path.cwd()
            for file_pattern in self.update_files + self.preserve_files:
                source_path = current_dir / file_pattern
                if source_path.exists():
                    if source_path.is_file():
                        dest_path = backup_path / file_pattern
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_path, dest_path)
                    elif source_path.is_dir():
                        dest_path = backup_path / file_pattern
                        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
            
            # Save backup metadata
            backup_info = {
                "timestamp": timestamp,
                "version": self.current_version,
                "files": self.update_files + self.preserve_files,
                "backup_path": str(backup_path)
            }
            
            with open(backup_path / "backup_info.json", "w") as f:
                json.dump(backup_info, f, indent=2)
            
            logger.info(f"Backup created: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            raise
    
    def extract_and_apply_update(self, zip_path: Path, backup_path: str, update_info: Dict[str, Any]) -> bool:
        """Extract downloaded update and apply changes."""
        try:
            # Extract to temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Extract zip file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                # Find the extracted directory (GitHub zips have a root directory)
                extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
                if not extracted_dirs:
                    raise Exception("No directories found in downloaded zip")
                
                source_dir = extracted_dirs[0]
                current_dir = Path.cwd()
                
                # Update files
                updated_files = []
                for file_name in self.update_files:
                    source_file = source_dir / file_name
                    dest_file = current_dir / file_name
                    
                    if source_file.exists():
                        # Verify file integrity (basic check)
                        if source_file.stat().st_size > 0:
                            # Create backup of existing file if it exists
                            if dest_file.exists():
                                backup_file = Path(backup_path) / file_name
                                backup_file.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(dest_file, backup_file)
                            
                            # Copy new file
                            shutil.copy2(source_file, dest_file)
                            updated_files.append(file_name)
                            logger.info(f"Updated: {file_name}")
                        else:
                            logger.warning(f"Skipped empty file: {file_name}")
                    else:
                        logger.warning(f"File not found in update: {file_name}")
                
                # Update requirements if changed
                requirements_file = current_dir / "requirements.txt"
                if requirements_file.exists() and "requirements.txt" in updated_files:
                    logger.info("Requirements.txt updated - you may need to reinstall dependencies")
                
                # Update version tracking if this was a commit-based update
                if update_info.get("update_method") == "commit":
                    version_file = current_dir / ".mcp_version"
                    with open(version_file, "w") as f:
                        f.write(update_info.get("latest_version", ""))
                
                logger.info(f"Update applied successfully. Updated {len(updated_files)} files.")
                return True
                
        except Exception as e:
            logger.error(f"Error applying update: {e}")
            # Restore from backup on failure
            self.restore_backup(backup_path)
            return False
    
    def restore_backup(self, backup_path: str) -> bool:
        """Restore from backup."""
        try:
            backup_dir = Path(backup_path)
            current_dir = Path.cwd()
            
            if not backup_dir.exists():
                logger.error(f"Backup directory not found: {backup_path}")
                return False
            
            # Restore files
            for file_pattern in self.update_files + self.preserve_files:
                backup_file = backup_dir / file_pattern
                dest_file = current_dir / file_pattern
                
                if backup_file.exists():
                    if backup_file.is_file():
                        shutil.copy2(backup_file, dest_file)
                    elif backup_file.is_dir():
                        if dest_file.exists():
                            shutil.rmtree(dest_file)
                        shutil.copytree(backup_file, dest_file)
                    logger.info(f"Restored: {file_pattern}")
            
            logger.info("Backup restored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False
    
    async def perform_update(self, force: bool = False) -> Dict[str, Any]:
        """Perform complete update process."""
        try:
            # Check for updates
            logger.info("Checking for updates...")
            update_info = await self.check_for_updates()
            
            if not update_info.get("update_available") and not force:
                return {
                    "success": True,
                    "action": "no_update_needed",
                    "message": f"Already on latest version: {self.current_version}",
                    "update_info": update_info
                }
            
            if update_info.get("error"):
                return {
                    "success": False,
                    "action": "check_failed",
                    "error": update_info["error"]
                }
            
            download_url = update_info.get("download_url")
            if not download_url:
                return {
                    "success": False,
                    "action": "no_download_url",
                    "error": "No download URL available"
                }
            
            # Create backup
            logger.info("Creating backup...")
            backup_path = self.create_backup()
            
            # Download update
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = Path(temp_dir) / "update.zip"
                
                if not await self.download_update(download_url, zip_path):
                    return {
                        "success": False,
                        "action": "download_failed", 
                        "error": "Failed to download update"
                    }
                
                # Apply update
                logger.info("Applying update...")
                if self.extract_and_apply_update(zip_path, backup_path, update_info):
                    # Update version info if available
                    new_version = update_info.get("latest_version", "unknown")
                    
                    return {
                        "success": True,
                        "action": "updated",
                        "message": f"Successfully updated from {self.current_version} to {new_version}",
                        "previous_version": self.current_version,
                        "new_version": new_version,
                        "backup_path": backup_path,
                        "restart_required": True
                    }
                else:
                    return {
                        "success": False,
                        "action": "update_failed",
                        "error": "Failed to apply update - restored from backup",
                        "backup_path": backup_path
                    }
                    
        except Exception as e:
            logger.error(f"Error during update: {e}")
            return {
                "success": False,
                "action": "update_error",
                "error": str(e)
            }
    
    def get_update_status(self) -> Dict[str, Any]:
        """Get current update status and version info."""
        return {
            "current_version": self.current_version,
            "repo_owner": self.repo_owner,
            "repo_name": self.repo_name,
            "github_url": f"https://github.com/{self.repo_owner}/{self.repo_name}",
            "update_files": self.update_files,
            "preserve_files": self.preserve_files,
            "backup_dir": str(self.backup_dir)
        }

class UpdateCommand:
    """Command-line interface for the updater."""
    
    def __init__(self):
        self.updater = MCPServerUpdater()
    
    async def run_update_check(self):
        """Check for updates and display information."""
        print("🔍 Checking for Microsoft Style Guide MCP Server updates...")
        
        update_info = await self.updater.check_for_updates()
        
        if update_info.get("error"):
            print(f"❌ Error checking for updates: {update_info['error']}")
            return False
        
        current_version = update_info.get("current_version", "unknown")
        latest_version = update_info.get("latest_version", "unknown")
        
        print(f"📊 Current version: {current_version}")
        print(f"📊 Latest version: {latest_version}")
        
        if update_info.get("update_available"):
            print("✅ Update available!")
            
            release_notes = update_info.get("release_notes", "")
            if release_notes:
                print(f"\n📝 Release Notes:\n{release_notes[:500]}...")
            
            published_at = update_info.get("published_at", "")
            if published_at:
                print(f"📅 Published: {published_at}")
            
            return True
        else:
            print("✅ You are running the latest version")
            return False
    
    async def run_update(self, force: bool = False):
        """Perform the update."""
        print("🚀 Starting Microsoft Style Guide MCP Server update...")
        
        result = await self.updater.perform_update(force=force)
        
        if result["success"]:
            if result["action"] == "no_update_needed":
                print(f"✅ {result['message']}")
            elif result["action"] == "updated":
                print(f"✅ {result['message']}")
                print(f"💾 Backup created at: {result['backup_path']}")
                if result.get("restart_required"):
                    print("⚠️  Restart required: Please restart VS Code and the MCP server")
        else:
            print(f"❌ Update failed: {result.get('error', 'Unknown error')}")
            if result.get("backup_path"):
                print(f"💾 Backup available at: {result['backup_path']}")
        
        return result["success"]
    
    async def run_status(self):
        """Display update status information."""
        status = self.updater.get_update_status()
        
        print("📊 Microsoft Style Guide MCP Server Update Status")
        print("=" * 50)
        print(f"Current Version: {status['current_version']}")
        print(f"Repository: {status['github_url']}")
        print(f"Update Files: {', '.join(status['update_files'])}")
        print(f"Backup Directory: {status['backup_dir']}")

async def main():
    """Main entry point for the updater."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Microsoft Style Guide MCP Server Updater",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mcp_updater.py check           # Check for updates
  python mcp_updater.py update          # Update if available
  python mcp_updater.py update --force  # Force update
  python mcp_updater.py status          # Show status
  python mcp_updater.py restore backup_20241201_143022  # Restore backup
        """
    )
    
    parser.add_argument(
        "action",
        choices=["check", "update", "status", "restore"],
        help="Action to perform"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update even if no new version detected"
    )
    parser.add_argument(
        "--repo-owner",
        default="asudbring",
        help="GitHub repository owner (default: asudbring)"
    )
    parser.add_argument(
        "--repo-name", 
        default="ms-style-guide-fastmcp-server",
        help="GitHub repository name (default: ms-style-guide-fastmcp-server)"
    )
    parser.add_argument(
        "--backup-path",
        help="Backup path for restore action"
    )
    
    args = parser.parse_args()
    
    # Create updater with custom repo if specified
    updater = MCPServerUpdater(
        repo_owner=args.repo_owner,
        repo_name=args.repo_name
    )
    
    command = UpdateCommand()
    command.updater = updater
    
    try:
        if args.action == "check":
            await command.run_update_check()
        
        elif args.action == "update":
            await command.run_update(force=args.force)
        
        elif args.action == "status":
            await command.run_status()
        
        elif args.action == "restore":
            if not args.backup_path:
                print("❌ Error: --backup-path required for restore action")
                return 1
            
            success = updater.restore_backup(args.backup_path)
            if success:
                print(f"✅ Restored from backup: {args.backup_path}")
            else:
                print(f"❌ Failed to restore from backup: {args.backup_path}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Update interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    finally:
        await updater.close_session()

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)