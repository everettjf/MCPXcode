from typing import Any
from mcp.server.fastmcp import FastMCP

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


if __name__ == "__main__":
    mcp.run(transport='stdio')