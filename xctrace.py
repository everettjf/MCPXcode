"""
MCP tools for xctrace command wrappers.
Common xctrace operations for performance profiling and debugging.
"""
import json
import subprocess
import os
from typing import List, Dict, Optional, Union, Any


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


def record_with_options(template: str, device_id: str, app_bundle_id: str, 
                       output_path: str, time_limit: Optional[int] = None,
                       template_options: Optional[Dict[str, str]] = None,
                       launch_args: Optional[List[str]] = None,
                       env_vars: Optional[Dict[str, str]] = None) -> None:
    """
    Advanced record with additional options for template, launch args, and env vars.
    
    Args:
        template: Name of the template to use
        device_id: UDID of the target device
        app_bundle_id: Bundle ID of the app to record
        output_path: Path to save the trace file
        time_limit: Optional recording time limit in seconds
        template_options: Optional template-specific options
        launch_args: Optional launch arguments for the app
        env_vars: Optional environment variables for the app
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
        
    # Add template options
    if template_options:
        for key, value in template_options.items():
            cmd.extend(['--template-option', f"{key}={value}"])
    
    # Add launch arguments
    if launch_args:
        cmd.extend(['--launch-args', ' '.join(launch_args)])
    
    # Add environment variables
    if env_vars:
        for key, value in env_vars.items():
            cmd.extend(['--setenv', f"{key}={value}"])
            
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to record trace: {e.stderr}")


def attach(pid: int, template: str, output_path: str, time_limit: Optional[int] = None) -> None:
    """
    Attach to a running process for tracing.
    
    Args:
        pid: Process ID to attach to
        template: Name of the template to use
        output_path: Path to save the trace file
        time_limit: Optional recording time limit in seconds
    """
    cmd = [
        'xctrace', 'attach',
        '--pid', str(pid),
        '--template', template,
        '--output', output_path
    ]
    
    if time_limit:
        cmd.extend(['--time-limit', str(time_limit)])
        
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to attach tracer: {e.stderr}")


def diagnose_archive(archive_path: str, output_dir: str) -> None:
    """
    Diagnose a trace archive.
    
    Args:
        archive_path: Path to the trace archive
        output_dir: Directory to save the diagnosis results
    """
    try:
        subprocess.run([
            'xctrace', 'diagnose',
            '--input', archive_path,
            '--output', output_dir
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to diagnose archive: {e.stderr}")


def document_template(template: str, output_path: str) -> None:
    """
    Generate documentation for a template.
    
    Args:
        template: Name of the template to document
        output_path: Path to save the documentation
    """
    try:
        result = subprocess.run([
            'xctrace', 'document-template',
            '--template', template
        ], capture_output=True, text=True, check=True)
        
        # Write documentation to file
        with open(output_path, 'w') as f:
            f.write(result.stdout)
            
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to document template: {e.stderr}")
    except IOError as e:
        raise Exception(f"Failed to write documentation: {str(e)}")


def analyze_trace(trace_path: str, output_dir: str) -> None:
    """
    Analyze a trace file and generate performance reports.
    
    Args:
        trace_path: Path to the trace file
        output_dir: Directory to save analysis reports
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        subprocess.run([
            'xctrace', 'analyze',
            '--input', trace_path,
            '--output', output_dir
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to analyze trace: {e.stderr}")


def compare_traces(base_trace: str, comparison_trace: str, output_path: str) -> None:
    """
    Compare two trace files and generate a comparison report.
    
    Args:
        base_trace: Path to the base trace file
        comparison_trace: Path to the comparison trace file
        output_path: Path to save the comparison report
    """
    try:
        subprocess.run([
            'xctrace', 'compare',
            '--base', base_trace,
            '--compare', comparison_trace,
            '--output', output_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to compare traces: {e.stderr}")
