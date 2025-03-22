from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
import json
import subprocess
from xctrace import list_devices as xctrace_list_devices
from xctrace import list_templates, record, export
mcp = FastMCP("MCPXcode")

@mcp.tool()
async def get_mcpxcode() -> str:
    """Print Summary of MCPXcode
    """
    return "Hello MCPXcode :) MCPXcode is MCP server for Xcode."


@mcp.tool()
async def list_devices() -> dict[str, Any]:
    """List all available simulator devices.
    
    Returns:
        Dict[str, Any]: JSON response containing all available devices
    """
    try:
        result = subprocess.run(
            ["xcrun", "simctl", "list", "devices", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to list devices: {e.stderr}")

@mcp.tool()
async def boot_device(device_id: str) -> str:
    """Boot a simulator device.
    
    Args:
        device_id (str): The UDID of the simulator device to boot
        
    Returns:
        str: Success message if the device was booted
    """
    try:
        subprocess.run(
            ["xcrun", "simctl", "boot", device_id],
            capture_output=True,
            text=True,
            check=True
        )
        return f"Successfully booted device {device_id}"
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to boot device: {e.stderr}")

@mcp.tool()
async def shutdown_device(device_id: str) -> str:
    """Shutdown a simulator device.
    
    Args:
        device_id (str): The UDID of the simulator device to shutdown
        
    Returns:
        str: Success message if the device was shutdown
    """
    try:
        subprocess.run(
            ["xcrun", "simctl", "shutdown", device_id],
            capture_output=True,
            text=True,
            check=True
        )
        return f"Successfully shutdown device {device_id}"
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to shutdown device: {e.stderr}")

@mcp.tool()
async def install_app(device_id: str, app_path: str) -> str:
    """Install an app on a simulator device.
    
    Args:
        device_id (str): The UDID of the simulator device
        app_path (str): Path to the .app bundle to install
        
    Returns:
        str: Success message if the app was installed
    """
    try:
        subprocess.run(
            ["xcrun", "simctl", "install", device_id, app_path],
            capture_output=True,
            text=True,
            check=True
        )
        return f"Successfully installed app at {app_path} on device {device_id}"
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to install app: {e.stderr}")

@mcp.tool()
async def launch_app(device_id: str, bundle_id: str) -> str:
    """Launch an app on a simulator device.
    
    Args:
        device_id (str): The UDID of the simulator device
        bundle_id (str): Bundle identifier of the app to launch
        
    Returns:
        str: Success message if the app was launched
    """
    try:
        subprocess.run(
            ["xcrun", "simctl", "launch", device_id, bundle_id],
            capture_output=True,
            text=True,
            check=True
        )
        return f"Successfully launched app {bundle_id} on device {device_id}"
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to launch app: {e.stderr}")


@mcp.tool()
async def get_sdk_path() -> str:
    """Get the path of the current SDK.
    
    Returns:
        str: Path to the current SDK
    """
    try:
        result = subprocess.run(
            ["xcrun", "--show-sdk-path"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to get SDK path: {e.stderr}")

@mcp.tool()
async def get_sdk_version() -> str:
    """Get the version of the current SDK.
    
    Returns:
        str: Version of the current SDK
    """
    try:
        result = subprocess.run(
            ["xcrun", "--show-sdk-version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to get SDK version: {e.stderr}")

@mcp.tool()
async def get_sdk_platform_path() -> str:
    """Get the platform path of the current SDK.
    
    Returns:
        str: Platform path of the current SDK
    """
    try:
        result = subprocess.run(
            ["xcrun", "--show-sdk-platform-path"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to get SDK platform path: {e.stderr}")

@mcp.tool()
async def find_developer_tool(tool_name: str) -> str:
    """Find the path of a developer tool.
    
    Args:
        tool_name (str): Name of the developer tool to find
        
    Returns:
        str: Full path to the developer tool
    """
    try:
        result = subprocess.run(
            ["xcrun", "-f", tool_name],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to find tool {tool_name}: {e.stderr}")

@mcp.tool()
async def run_tool_with_sdk(tool_name: str, sdk_name: str, *args: str) -> str:
    """Run a developer tool with a specific SDK.
    
    Args:
        tool_name (str): Name of the developer tool to run
        sdk_name (str): Name of the SDK to use (e.g., 'iphoneos', 'macosx')
        *args: Additional arguments to pass to the tool
        
    Returns:
        str: Output from the tool
    """
    try:
        cmd = ["xcrun", "--sdk", sdk_name, tool_name] + list(args)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to run {tool_name} with SDK {sdk_name}: {e.stderr}")

@mcp.tool()
async def xctrace_devices() -> List[Dict]:
    """List available devices for tracing using xctrace."""
    return xctrace_list_devices()

@mcp.tool()
async def xctrace_templates() -> List[Dict]:
    """List available templates for tracing using xctrace."""
    return list_templates()

@mcp.tool()
async def xctrace_record(template: str, device_id: str, app_bundle_id: str, 
                      output_path: str, time_limit: Optional[int] = None) -> str:
    """Record app performance using xctrace.
    
    Args:
        template: Name of the template to use
        device_id: UDID of the target device
        app_bundle_id: Bundle ID of the app to record
        output_path: Path to save the trace file
        time_limit: Optional recording time limit in seconds
    """
    record(template, device_id, app_bundle_id, output_path, time_limit)
    return f"Successfully recorded trace to {output_path}"

@mcp.tool()
async def xctrace_export(trace_path: str, output_path: str, type: str = "json") -> str:
    """Export trace data to specified format.
    
    Args:
        trace_path: Path to the trace file
        output_path: Path to save the exported data
        type: Export format (json, html, etc.)
    """
    export(trace_path, output_path, type)
    return f"Successfully exported trace to {output_path}"

if __name__ == "__main__":
    mcp.run(transport='stdio')