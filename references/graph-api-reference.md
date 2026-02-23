# Microsoft Graph API Reference for Intune

## Authentication

Microsoft Graph uses OAuth 2.0 client credentials flow for app-only access.

### Required Permissions

Register an app in Azure AD and grant these application permissions:

| Permission | Description |
|------------|-------------|
| `DeviceManagementApps.Read.All` | Read apps |
| `DeviceManagementApps.ReadWrite.All` | Read and write apps |
| `DeviceManagementConfiguration.Read.All` | Read device configurations |
| `DeviceManagementConfiguration.ReadWrite.All` | Read and write configurations |
| `DeviceManagementManagedDevices.Read.All` | Read managed devices |
| `DeviceManagementManagedDevices.ReadWrite.All` | Read and write devices |
| `DeviceManagementServiceConfig.Read.All` | Read service configurations |
| `DeviceManagementServiceConfig.ReadWrite.All` | Read and write service config |
| `User.Read.All` | Read user information |

Don't forget to **Grant admin consent** after adding permissions.

### Get Access Token

```
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET
&scope=https://graph.microsoft.com/.default
```

## Base URL

```
https://graph.microsoft.com/v1.0
```

## Device Management Endpoints

### Managed Devices

#### List All Devices
```
GET /deviceManagement/managedDevices
```

#### Get Device Details
```
GET /deviceManagement/managedDevices/{deviceId}
```

#### Retire Device
```
POST /deviceManagement/managedDevices/{deviceId}/retire
```

#### Wipe Device
```
POST /deviceManagement/managedDevices/{deviceId}/wipe
```

#### Delete Device
```
DELETE /deviceManagement/managedDevices/{deviceId}
```

### Compliance Policies

#### List Policies
```
GET /deviceManagement/deviceCompliancePolicies
```

#### Get Policy
```
GET /deviceManagement/deviceCompliancePolicies/{policyId}
```

#### Create Policy
```
POST /deviceManagement/deviceCompliancePolicies
```

### Device Configurations

#### List Configurations
```
GET /deviceManagement/deviceConfigurations
```

#### Get Configuration
```
GET /deviceManagement/deviceConfigurations/{configId}
```

### Mobile Apps

#### List Apps
```
GET /deviceAppManagement/mobileApps
```

#### Get App
```
GET /deviceAppManagement/mobileApps/{appId}
```

#### Assign App
```
POST /deviceAppManagement/mobileApps/{appId}/assign
```

### Users and Devices

#### Get User
```
GET /users/{userId}
```

#### Get User's Devices
```
GET /users/{userId}/managedDevices
```

## Device Properties

### Managed Device Object

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Device ID |
| `deviceName` | String | Device name |
| `userPrincipalName` | String | Primary user's UPN |
| `operatingSystem` | String | OS (Windows, iOS, Android, macOS) |
| `osVersion` | String | OS version |
| `complianceState` | String | compliant, noncompliant, unknown, conflict |
| `lastSyncDateTime` | DateTime | Last check-in |
| `enrolledDateTime` | DateTime | Enrollment date |
| `managedDeviceOwnerType` | String | company, personal |
| `deviceEnrollmentType` | String | Enrollment method |

### Compliance State Values

- `compliant` - Meets all policies
- `noncompliant` - Failed compliance check
- `unknown` - Not yet evaluated
- `conflict` - Policy conflict detected
- `error` - Error during evaluation

## Rate Limits

- Default: 10,000 requests per 10 minutes per app
- Throttling may occur during heavy usage
- Check `Retry-After` header for backoff

## Official Documentation

https://docs.microsoft.com/en-us/graph/api/resources/intune-graph-overview
