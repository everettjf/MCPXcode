"""
MCP tools for xcrun command wrappers.
Common xcrun operations for Xcode development.
"""
import json
import subprocess
from typing import List, Dict, Optional, Union, Any


def xcodebuild_list_sdks() -> List[Dict]:
    """List all available SDKs."""
    try:
        result = subprocess.run(['xcrun', 'xcodebuild', '-showsdks', '-json'],
                              capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to list SDKs: {e.stderr}")


def xcodebuild_list_schemes(project_path: str) -> List[str]:
    """List all schemes in a project.
    
    Args:
        project_path: Path to .xcodeproj or .xcworkspace
    """
    try:
        result = subprocess.run(['xcrun', 'xcodebuild', '-list', '-project', project_path, '-json'],
                              capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return data.get('project', {}).get('schemes', [])
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to list schemes: {e.stderr}")


def xcodebuild_build(project_path: str, scheme: str, configuration: str = "Debug", 
                   sdk: str = "iphonesimulator", destination: Optional[str] = None) -> str:
    """Build an Xcode project.
    
    Args:
        project_path: Path to .xcodeproj or .xcworkspace
        scheme: Scheme to build
        configuration: Build configuration (Debug, Release)
        sdk: SDK to build for
        destination: Optional destination specifier (e.g. 'platform=iOS Simulator,name=iPhone 14')
    """
    cmd = [
        'xcrun', 'xcodebuild',
        '-project', project_path,
        '-scheme', scheme,
        '-configuration', configuration,
        '-sdk', sdk
    ]
    
    if destination:
        cmd.extend(['-destination', destination])
        
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Build failed: {e.stderr}")


def altool_validate_app(app_path: str, username: str, password_keychain_item: str) -> str:
    """Validate an app before submission to App Store.
    
    Args:
        app_path: Path to .ipa file
        username: App Store Connect username
        password_keychain_item: Keychain item containing password
    """
    try:
        result = subprocess.run([
            'xcrun', 'altool', '--validate-app',
            '-f', app_path,
            '-u', username,
            '-p', f"@keychain:{password_keychain_item}"
        ], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"App validation failed: {e.stderr}")


def altool_upload_app(app_path: str, username: str, password_keychain_item: str) -> str:
    """Upload an app to App Store.
    
    Args:
        app_path: Path to .ipa file
        username: App Store Connect username
        password_keychain_item: Keychain item containing password
    """
    try:
        result = subprocess.run([
            'xcrun', 'altool', '--upload-app',
            '-f', app_path,
            '-u', username,
            '-p', f"@keychain:{password_keychain_item}"
        ], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"App upload failed: {e.stderr}")


def swift_symbols(binary_path: str) -> List[str]:
    """Extract Swift symbols from a binary.
    
    Args:
        binary_path: Path to binary file
    """
    try:
        result = subprocess.run(['xcrun', 'swift-demangle', binary_path],
                              capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to extract symbols: {e.stderr}")


def otool_headers(binary_path: str) -> List[str]:
    """Show Mach-O headers of a binary.
    
    Args:
        binary_path: Path to binary file
    """
    try:
        result = subprocess.run(['xcrun', 'otool', '-h', binary_path],
                              capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to show headers: {e.stderr}")


def otool_libraries(binary_path: str) -> List[str]:
    """Show linked libraries of a binary.
    
    Args:
        binary_path: Path to binary file
    """
    try:
        result = subprocess.run(['xcrun', 'otool', '-L', binary_path],
                              capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to show linked libraries: {e.stderr}")


def nm_symbols(binary_path: str) -> List[str]:
    """Show symbols in a binary.
    
    Args:
        binary_path: Path to binary file
    """
    try:
        result = subprocess.run(['xcrun', 'nm', binary_path],
                              capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to show symbols: {e.stderr}")
