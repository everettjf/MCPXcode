"""
MCP tools for xctrace command wrappers.
Common xctrace operations for performance profiling and debugging.
"""
import json
import subprocess
from typing import List, Dict, Optional


def list_devices() -> List[Dict]:
    """List available devices for tracing."""
    try:
        result = subprocess.run(['xctrace', 'list', 'devices', '--json'],
                              capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to list devices: {e.stderr}")


def list_templates() -> List[Dict]:
    """List available templates for tracing."""
    try:
        result = subprocess.run(['xctrace', 'list', 'templates', '--json'],
                              capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to list templates: {e.stderr}")


def record(template: str, device_id: str, app_bundle_id: str, 
          output_path: str, time_limit: Optional[int] = None) -> None:
    """
    Record app performance using specified template.
    
    Args:
        template: Name of the template to use
        device_id: UDID of the target device
        app_bundle_id: Bundle ID of the app to record
        output_path: Path to save the trace file
        time_limit: Optional recording time limit in seconds
    """
    cmd = [
        'xctrace', 'record',
        '--template', template,
        '--device', device_id,
        '--target', app_bundle_id,
        '--output', output_path
    ]
    
    if time_limit:
        cmd.extend(['--time-limit', str(time_limit)])
        
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to record trace: {e.stderr}")


def export(trace_path: str, output_path: str, type: str = "json") -> None:
    """
    Export trace data to specified format.
    
    Args:
        trace_path: Path to the trace file
        output_path: Path to save the exported data
        type: Export format (json, html, etc.)
    """
    try:
        subprocess.run([
            'xctrace', 'export',
            '--input', trace_path,
            '--output', output_path,
            '--type', type
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to export trace: {e.stderr}")
