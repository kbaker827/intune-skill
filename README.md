# Microsoft Intune Skill for OpenClaw

Manage Microsoft Intune (Endpoint Manager) devices, policies, apps, and compliance via Microsoft Graph API.

## What is OpenClaw?

[OpenClaw](https://github.com/openclaw/openclaw) is an open-source agent framework. This skill extends OpenClaw with Microsoft Intune management capabilities.

## Setup

### 1. Register an Azure AD App

1. Go to [Azure Portal](https://portal.azure.com) → Azure Active Directory → App registrations
2. Click "New registration"
3. Name your app (e.g., "Intune Management")
4. Select "Accounts in this organizational directory only"
5. Click "Register"

### 2. Configure API Permissions

Add these **Application permissions**:
- `DeviceManagementApps.Read.All`
- `DeviceManagementApps.ReadWrite.All`
- `DeviceManagementConfiguration.Read.All`
- `DeviceManagementConfiguration.ReadWrite.All`
- `DeviceManagementManagedDevices.Read.All`
- `DeviceManagementManagedDevices.ReadWrite.All`
- `DeviceManagementServiceConfig.Read.All`
- `User.Read.All`

Click **Grant admin consent** after adding permissions.

### 3. Create Client Secret

1. Go to "Certificates & secrets"
2. Click "New client secret"
3. Add a description and expiration
4. Copy the secret value immediately

### 4. Set Environment Variables

```bash
export INTUNE_TENANT_ID="your-tenant-id"
export INTUNE_CLIENT_ID="your-app-client-id"
export INTUNE_CLIENT_SECRET="your-secret-value"
```

## Usage

### List All Devices
```bash
python3 scripts/intune.py devices list
```

### Get Device Details
```bash
python3 scripts/intune.py devices get --device-id "12345678-1234-1234-1234-123456789012"
```

### Check Compliance
```bash
# List compliance policies
python3 scripts/intune.py compliance list

# Get non-compliant devices
python3 scripts/intune.py compliance states --filter noncompliant
```

### List Apps and Policies
```bash
python3 scripts/intune.py apps list
python3 scripts/intune.py policies list
```

### Device Actions
```bash
# Retire a device
python3 scripts/intune.py devices retire --device-id "DEVICE_ID"

# Remote wipe (destructive!)
python3 scripts/intune.py devices wipe --device-id "DEVICE_ID"
```

## Features

- List managed devices with compliance status
- Get detailed device information
- Check compliance policies and states
- List managed apps
- List configuration policies
- Retire and wipe devices
- User device lookup

## API Reference

See [`references/graph-api-reference.md`](references/graph-api-reference.md) for complete Microsoft Graph API documentation.

## License

MIT
