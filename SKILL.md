---
name: intune
description: Manage Microsoft Intune devices, policies, apps, and users via Microsoft Graph API. Use when the user wants to list devices, check compliance, deploy apps, manage policies, or query Intune/Endpoint Manager data.
---

# Microsoft Intune

Manage Microsoft Intune (Endpoint Manager) via Microsoft Graph API.

## Quick Start

### Authentication

You need a Microsoft Entra ID app registration with these permissions:
- `DeviceManagementApps.Read.All`
- `DeviceManagementApps.ReadWrite.All`
- `DeviceManagementConfiguration.Read.All`
- `DeviceManagementConfiguration.ReadWrite.All`
- `DeviceManagementManagedDevices.Read.All`
- `DeviceManagementManagedDevices.ReadWrite.All`
- `DeviceManagementServiceConfig.Read.All`
- `DeviceManagementServiceConfig.ReadWrite.All`

Set environment variables:
```bash
export INTUNE_TENANT_ID=your-tenant-id
export INTUNE_CLIENT_ID=your-app-client-id
export INTUNE_CLIENT_SECRET=your-app-secret
```

### List Managed Devices

```bash
python3 scripts/intune.py devices list
```

### Get Device Details

```bash
python3 scripts/intune.py devices get --device-id DEVICE_ID
```

### Check Compliance

```bash
python3 scripts/intune.py compliance list
```

## Common Commands

| Command | Description |
|---------|-------------|
| `devices list` | List all managed devices |
| `devices get` | Get device details |
| `devices wipe` | Remote wipe device |
| `devices retire` | Retire device |
| `compliance list` | List compliance policies |
| `compliance states` | Get device compliance states |
| `apps list` | List managed apps |
| `policies list` | List configuration policies |
| `users devices` | List devices for a user |

## Resources

### scripts/
- `intune.py` - CLI tool for Intune management

### references/
- `graph-api-reference.md` - Microsoft Graph API documentation for Intune

## Examples

### List all devices
```bash
python3 scripts/intune.py devices list
```

### Get specific device
```bash
python3 scripts/intune.py devices get --device-id "12345678-1234-1234-1234-123456789012"
```

### List non-compliant devices
```bash
python3 scripts/intune.py compliance states --filter noncompliant
```

### Retire a device
```bash
python3 scripts/intune.py devices retire --device-id "12345678-1234-1234-1234-123456789012"
```
