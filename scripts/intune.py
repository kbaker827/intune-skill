#!/usr/bin/env python3
"""
Microsoft Intune CLI - Manage devices, policies, and apps via Microsoft Graph API.

Usage:
    python3 intune.py devices list
    python3 intune.py devices get --device-id DEVICE_ID
    python3 intune.py compliance list

Environment variables:
    INTUNE_TENANT_ID - Azure AD tenant ID
    INTUNE_CLIENT_ID - App registration client ID
    INTUNE_CLIENT_SECRET - App registration client secret
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from typing import Optional

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

def get_access_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    """Get OAuth2 access token from Microsoft."""
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }).encode('utf-8')
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('access_token')
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"Authentication error: HTTP {e.code}", file=sys.stderr)
        if error_body:
            print(f"Response: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error getting token: {e}", file=sys.stderr)
        sys.exit(1)


def graph_request(endpoint: str, token: str, method: str = "GET", data: dict = None) -> dict:
    """Make a Microsoft Graph API request."""
    url = f"{GRAPH_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        if data:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method=method
            )
        else:
            req = urllib.request.Request(url, headers=headers, method=method)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"API error: HTTP {e.code} - {e.reason}", file=sys.stderr)
        if error_body:
            try:
                error_json = json.loads(error_body)
                print(f"Details: {json.dumps(error_json, indent=2)}", file=sys.stderr)
            except:
                print(f"Response: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_devices(token: str):
    """List all managed devices."""
    data = graph_request("/deviceManagement/managedDevices", token)
    devices = data.get('value', [])
    
    if not devices:
        print("No managed devices found.")
        return
    
    print(f"Found {len(devices)} managed device(s):\n")
    for device in devices:
        print(f"Device: {device.get('deviceName', 'Unknown')}")
        print(f"  ID: {device.get('id', 'N/A')}")
        print(f"  User: {device.get('userPrincipalName', 'N/A')}")
        print(f"  OS: {device.get('operatingSystem', 'N/A')} {device.get('osVersion', '')}")
        print(f"  Compliance: {device.get('complianceState', 'N/A')}")
        print(f"  Last Sync: {device.get('lastSyncDateTime', 'N/A')}")
        print(f"  Enrolled: {device.get('enrolledDateTime', 'N/A')}")
        print()


def get_device(token: str, device_id: str):
    """Get detailed device information."""
    device = graph_request(f"/deviceManagement/managedDevices/{device_id}", token)
    
    print(f"Device Details:\n")
    print(json.dumps(device, indent=2))


def retire_device(token: str, device_id: str):
    """Retire a managed device."""
    endpoint = f"/deviceManagement/managedDevices/{device_id}/retire"
    graph_request(endpoint, token, method="POST")
    print(f"Device {device_id} retired successfully")


def wipe_device(token: str, device_id: str):
    """Remote wipe a managed device."""
    endpoint = f"/deviceManagement/managedDevices/{device_id}/wipe"
    graph_request(endpoint, token, method="POST")
    print(f"Remote wipe initiated for device {device_id}")


def list_compliance_policies(token: str):
    """List compliance policies."""
    data = graph_request("/deviceManagement/deviceCompliancePolicies", token)
    policies = data.get('value', [])
    
    if not policies:
        print("No compliance policies found.")
        return
    
    print(f"Found {len(policies)} compliance policy(ies):\n")
    for policy in policies:
        print(f"Policy: {policy.get('displayName', 'Unknown')}")
        print(f"  ID: {policy.get('id', 'N/A')}")
        print(f"  Platform: {policy.get('@odata.type', 'N/A').split('.')[-1]}")
        print(f"  Created: {policy.get('createdDateTime', 'N/A')}")
        print()


def get_compliance_states(token: str, filter_state: Optional[str] = None):
    """Get device compliance states."""
    data = graph_request("/deviceManagement/managedDevices", token)
    devices = data.get('value', [])
    
    if filter_state:
        devices = [d for d in devices if d.get('complianceState', '').lower() == filter_state.lower()]
    
    if not devices:
        print(f"No devices found" + (f" with compliance state '{filter_state}'" if filter_state else ""))
        return
    
    print(f"Compliance Status:\n")
    for device in devices:
        print(f"{device.get('deviceName', 'Unknown')}: {device.get('complianceState', 'N/A')}")


def list_apps(token: str):
    """List managed apps."""
    data = graph_request("/deviceAppManagement/mobileApps", token)
    apps = data.get('value', [])
    
    if not apps:
        print("No managed apps found.")
        return
    
    print(f"Found {len(apps)} managed app(s):\n")
    for app in apps:
        print(f"App: {app.get('displayName', 'Unknown')}")
        print(f"  ID: {app.get('id', 'N/A')}")
        print(f"  Type: {app.get('@odata.type', 'N/A').split('.')[-1]}")
        print(f"  Publisher: {app.get('publisher', 'N/A')}")
        print()


def list_policies(token: str):
    """List device configuration policies."""
    data = graph_request("/deviceManagement/deviceConfigurations", token)
    policies = data.get('value', [])
    
    if not policies:
        print("No configuration policies found.")
        return
    
    print(f"Found {len(policies)} configuration policy(ies):\n")
    for policy in policies:
        print(f"Policy: {policy.get('displayName', 'Unknown')}")
        print(f"  ID: {policy.get('id', 'N/A')}")
        print(f"  Platform: {policy.get('@odata.type', 'N/A').split('.')[-1]}")
        print()


def list_user_devices(token: str, user_id: str):
    """List devices for a specific user."""
    # Get user first to find their ID if email provided
    if '@' in user_id:
        user_data = graph_request(f"/users/{user_id}", token)
        user_id = user_data.get('id')
    
    data = graph_request(f"/users/{user_id}/managedDevices", token)
    devices = data.get('value', [])
    
    if not devices:
        print(f"No managed devices found for user.")
        return
    
    print(f"Found {len(devices)} device(s):\n")
    for device in devices:
        print(f"Device: {device.get('deviceName', 'Unknown')}")
        print(f"  ID: {device.get('id', 'N/A')}")
        print(f"  Compliance: {device.get('complianceState', 'N/A')}")
        print()


def main():
    parser = argparse.ArgumentParser(description='Microsoft Intune CLI')
    parser.add_argument('--tenant-id', help='Azure AD tenant ID (or set INTUNE_TENANT_ID)')
    parser.add_argument('--client-id', help='App client ID (or set INTUNE_CLIENT_ID)')
    parser.add_argument('--client-secret', help='App client secret (or set INTUNE_CLIENT_SECRET)')
    
    subparsers = parser.add_subparsers(dest='category', help='Category')
    
    # Devices
    devices_parser = subparsers.add_parser('devices', help='Device management')
    devices_sub = devices_parser.add_subparsers(dest='command')
    
    devices_sub.add_parser('list', help='List all devices')
    
    get_parser = devices_sub.add_parser('get', help='Get device details')
    get_parser.add_argument('--device-id', '-d', required=True, help='Device ID')
    
    retire_parser = devices_sub.add_parser('retire', help='Retire device')
    retire_parser.add_argument('--device-id', '-d', required=True, help='Device ID')
    
    wipe_parser = devices_sub.add_parser('wipe', help='Remote wipe device')
    wipe_parser.add_argument('--device-id', '-d', required=True, help='Device ID')
    
    # Compliance
    compliance_parser = subparsers.add_parser('compliance', help='Compliance management')
    compliance_sub = compliance_parser.add_subparsers(dest='command')
    compliance_sub.add_parser('list', help='List compliance policies')
    
    states_parser = compliance_sub.add_parser('states', help='Get compliance states')
    states_parser.add_argument('--filter', '-f', choices=['compliant', 'noncompliant', 'unknown', 'conflict'],
                               help='Filter by compliance state')
    
    # Apps
    apps_parser = subparsers.add_parser('apps', help='App management')
    apps_sub = apps_parser.add_subparsers(dest='command')
    apps_sub.add_parser('list', help='List managed apps')
    
    # Policies
    policies_parser = subparsers.add_parser('policies', help='Policy management')
    policies_sub = policies_parser.add_subparsers(dest='command')
    policies_sub.add_parser('list', help='List configuration policies')
    
    # Users
    users_parser = subparsers.add_parser('users', help='User management')
    users_sub = users_parser.add_subparsers(dest='command')
    
    user_devices_parser = users_sub.add_parser('devices', help='List user devices')
    user_devices_parser.add_argument('--user-id', '-u', required=True, help='User ID or email')
    
    args = parser.parse_args()
    
    if not args.category:
        parser.print_help()
        sys.exit(1)
    
    # Get credentials
    tenant_id = args.tenant_id or os.environ.get('INTUNE_TENANT_ID')
    client_id = args.client_id or os.environ.get('INTUNE_CLIENT_ID')
    client_secret = args.client_secret or os.environ.get('INTUNE_CLIENT_SECRET')
    
    if not all([tenant_id, client_id, client_secret]):
        print("Error: Missing credentials.", file=sys.stderr)
        print("Set environment variables:", file=sys.stderr)
        print("  INTUNE_TENANT_ID, INTUNE_CLIENT_ID, INTUNE_CLIENT_SECRET", file=sys.stderr)
        print("\nOr use command-line arguments:", file=sys.stderr)
        print("  --tenant-id, --client-id, --client-secret", file=sys.stderr)
        sys.exit(1)
    
    # Get access token
    token = get_access_token(tenant_id, client_id, client_secret)
    
    # Execute command
    if args.category == 'devices':
        if args.command == 'list':
            list_devices(token)
        elif args.command == 'get':
            get_device(token, args.device_id)
        elif args.command == 'retire':
            retire_device(token, args.device_id)
        elif args.command == 'wipe':
            wipe_device(token, args.device_id)
    elif args.category == 'compliance':
        if args.command == 'list':
            list_compliance_policies(token)
        elif args.command == 'states':
            get_compliance_states(token, args.filter)
    elif args.category == 'apps':
        if args.command == 'list':
            list_apps(token)
    elif args.category == 'policies':
        if args.command == 'list':
            list_policies(token)
    elif args.category == 'users':
        if args.command == 'devices':
            list_user_devices(token, args.user_id)


if __name__ == '__main__':
    main()
