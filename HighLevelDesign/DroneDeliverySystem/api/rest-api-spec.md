# API Design - Drone Delivery System

## Overview
This document outlines the RESTful API design for the drone delivery system, including all endpoints, request/response formats, and authentication mechanisms.

## Base URL
```
Production: https://api.dronedelivery.com/v1
Staging: https://staging-api.dronedelivery.com/v1
Development: http://localhost:8080/v1
```

## Authentication
All APIs use JWT-based authentication with OAuth 2.0 flow.

### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
X-API-Version: 1.0
X-Request-ID: <unique_request_id>
```

## Order Management APIs

### Create Order
Create a new delivery order.

**Endpoint:** `POST /orders`

**Request Body:**
```json
{
  "customer_id": "user_123",
  "pickup_address": {
    "street": "123 Main St",
    "apartment": "Suite 101",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94105",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "special_instructions": "Ring bell at loading dock"
  },
  "delivery_address": {
    "street": "456 Oak Ave",
    "apartment": "Apt 2B",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94102",
    "latitude": 37.7849,
    "longitude": -122.4094,
    "special_instructions": "Leave at door if no answer"
  },
  "package": {
    "weight": 2.5,
    "dimensions": {
      "length": 30,
      "width": 20,
      "height": 15
    },
    "value": 150.00,
    "description": "Electronic device",
    "special_handling": ["fragile", "this_side_up"]
  },
  "delivery_options": {
    "priority": "express",
    "delivery_window": {
      "start": "2025-07-01T14:00:00Z",
      "end": "2025-07-01T16:00:00Z"
    },
    "signature_required": true
  }
}
```

**Response (201 Created):**
```json
{
  "order_id": "ORD-2025-001234",
  "status": "confirmed",
  "estimated_pickup_time": "2025-07-01T11:00:00Z",
  "estimated_delivery_time": "2025-07-01T11:30:00Z",
  "tracking_number": "TRK-789456123",
  "cost": {
    "base_fee": 10.00,
    "distance_fee": 5.00,
    "priority_fee": 3.00,
    "total": 18.00,
    "currency": "USD"
  },
  "created_at": "2025-07-01T10:00:00Z"
}
```

### Get Order Details
Retrieve details of a specific order.

**Endpoint:** `GET /orders/{order_id}`

**Response (200 OK):**
```json
{
  "order_id": "ORD-2025-001234",
  "customer_id": "user_123",
  "status": "in_transit",
  "pickup_address": { /* same as request */ },
  "delivery_address": { /* same as request */ },
  "package": { /* same as request */ },
  "assignment": {
    "drone_id": "DRONE-001",
    "pilot_id": "PILOT-123",
    "assigned_at": "2025-07-01T10:30:00Z"
  },
  "tracking": {
    "current_location": {
      "latitude": 37.7799,
      "longitude": -122.4144,
      "altitude": 120.0
    },
    "status": "en_route_delivery",
    "estimated_arrival": "2025-07-01T11:25:00Z"
  },
  "timeline": {
    "placed": "2025-07-01T10:00:00Z",
    "confirmed": "2025-07-01T10:05:00Z",
    "assigned": "2025-07-01T10:30:00Z",
    "picked_up": "2025-07-01T11:00:00Z",
    "estimated_delivery": "2025-07-01T11:30:00Z"
  },
  "cost": { /* same as response */ }
}
```

### List Orders
Get paginated list of orders for a customer.

**Endpoint:** `GET /orders`

**Query Parameters:**
- `customer_id`: Filter by customer ID
- `status`: Filter by order status
- `from_date`: Filter orders from date
- `to_date`: Filter orders to date
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response (200 OK):**
```json
{
  "orders": [
    { /* order object */ },
    { /* order object */ }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_pages": 5,
    "total_items": 98,
    "has_next": true,
    "has_previous": false
  }
}
```

### Cancel Order
Cancel an existing order.

**Endpoint:** `DELETE /orders/{order_id}`

**Response (200 OK):**
```json
{
  "order_id": "ORD-2025-001234",
  "status": "cancelled",
  "cancelled_at": "2025-07-01T10:45:00Z",
  "refund": {
    "amount": 18.00,
    "currency": "USD",
    "processing_time": "3-5 business days"
  }
}
```

## Real-time Tracking APIs

### Get Real-time Tracking
Get current location and status of delivery.

**Endpoint:** `GET /tracking/{tracking_number}`

**Response (200 OK):**
```json
{
  "tracking_number": "TRK-789456123",
  "order_id": "ORD-2025-001234",
  "status": "in_transit",
  "current_location": {
    "latitude": 37.7799,
    "longitude": -122.4144,
    "altitude": 120.0,
    "address": "Near Golden Gate Park, San Francisco, CA"
  },
  "drone": {
    "drone_id": "DRONE-001",
    "battery_level": 75.5,
    "speed": 35.2,
    "heading": 180.0
  },
  "estimated_arrival": "2025-07-01T11:25:00Z",
  "route": {
    "total_distance": 5.2,
    "remaining_distance": 1.8,
    "progress_percentage": 65.4
  },
  "last_updated": "2025-07-01T11:15:30Z"
}
```

### WebSocket Tracking
Real-time tracking updates via WebSocket.

**Endpoint:** `WSS /tracking/stream/{tracking_number}`

**Message Format:**
```json
{
  "type": "location_update",
  "timestamp": "2025-07-01T11:15:30Z",
  "data": {
    "tracking_number": "TRK-789456123",
    "location": {
      "latitude": 37.7799,
      "longitude": -122.4144,
      "altitude": 120.0
    },
    "battery_level": 75.5,
    "speed": 35.2,
    "estimated_arrival": "2025-07-01T11:25:00Z"
  }
}
```

## Fleet Management APIs

### Get Available Drones
Get list of available drones for assignment.

**Endpoint:** `GET /fleet/drones/available`

**Query Parameters:**
- `min_battery`: Minimum battery level (default: 30)
- `max_distance`: Maximum distance from location in km
- `min_payload`: Minimum payload capacity in kg
- `location`: Reference location (lat,lng)

**Response (200 OK):**
```json
{
  "drones": [
    {
      "drone_id": "DRONE-001",
      "model": "DeliveryDrone-X1",
      "status": "available",
      "location": {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "altitude": 100.0
      },
      "battery_level": 85.5,
      "payload_capacity": 5.0,
      "distance_from_location": 2.3,
      "last_updated": "2025-07-01T11:10:00Z"
    }
  ],
  "total_available": 45,
  "fleet_statistics": {
    "total_drones": 100,
    "available": 45,
    "assigned": 30,
    "in_flight": 20,
    "charging": 3,
    "maintenance": 2
  }
}
```

### Get Drone Details
Get detailed information about a specific drone.

**Endpoint:** `GET /fleet/drones/{drone_id}`

**Response (200 OK):**
```json
{
  "drone_id": "DRONE-001",
  "model": "DeliveryDrone-X1",
  "serial_number": "DX1-2025-001",
  "status": "in_flight",
  "specifications": {
    "max_payload": 5.0,
    "max_range": 25.0,
    "max_speed": 60.0,
    "battery_capacity": 5000,
    "flight_time": 60
  },
  "current_status": {
    "location": {
      "latitude": 37.7799,
      "longitude": -122.4144,
      "altitude": 120.0
    },
    "battery_level": 75.5,
    "speed": 35.2,
    "heading": 180.0,
    "current_payload": 2.5
  },
  "assignment": {
    "order_id": "ORD-2025-001234",
    "assigned_at": "2025-07-01T10:30:00Z",
    "status": "en_route_delivery"
  },
  "maintenance": {
    "last_maintenance": "2025-06-15T08:00:00Z",
    "next_maintenance": "2025-07-15T08:00:00Z",
    "flight_hours": 145.5,
    "cycle_count": 289
  },
  "performance": {
    "total_deliveries": 156,
    "success_rate": 99.4,
    "average_delivery_time": 28.5,
    "energy_efficiency": 12.5
  }
}
```

## Route Optimization APIs

### Calculate Optimal Route
Calculate optimal route for delivery.

**Endpoint:** `POST /routing/optimize`

**Request Body:**
```json
{
  "drone_id": "DRONE-001",
  "pickup_location": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "delivery_location": {
    "latitude": 37.7849,
    "longitude": -122.4094
  },
  "package_weight": 2.5,
  "priority": "express",
  "constraints": {
    "max_flight_time": 30,
    "avoid_weather": true,
    "avoid_no_fly_zones": true
  }
}
```

**Response (200 OK):**
```json
{
  "route_id": "ROUTE-123456",
  "waypoints": [
    {
      "latitude": 37.7749,
      "longitude": -122.4194,
      "altitude": 100.0,
      "sequence": 1,
      "waypoint_type": "pickup"
    },
    {
      "latitude": 37.7780,
      "longitude": -122.4150,
      "altitude": 120.0,
      "sequence": 2,
      "waypoint_type": "waypoint"
    },
    {
      "latitude": 37.7849,
      "longitude": -122.4094,
      "altitude": 100.0,
      "sequence": 3,
      "waypoint_type": "delivery"
    }
  ],
  "route_summary": {
    "total_distance": 5.2,
    "estimated_duration": 28.5,
    "energy_consumption": 125.5,
    "safety_score": 0.95
  },
  "weather_conditions": [
    {
      "location": {
        "latitude": 37.7780,
        "longitude": -122.4150
      },
      "wind_speed": 15.2,
      "visibility": 10.0,
      "conditions": "clear"
    }
  ]
}
```

## Weather Integration APIs

### Get Weather Conditions
Get current weather conditions for a location.

**Endpoint:** `GET /weather/current`

**Query Parameters:**
- `lat`: Latitude
- `lng`: Longitude
- `radius`: Radius in km (default: 1)

**Response (200 OK):**
```json
{
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "conditions": {
    "temperature": 22.5,
    "humidity": 65.0,
    "wind_speed": 15.2,
    "wind_direction": 225.0,
    "visibility": 10.0,
    "precipitation": 0.0,
    "conditions": "clear",
    "flight_safe": true
  },
  "forecast": [
    {
      "time": "2025-07-01T12:00:00Z",
      "wind_speed": 18.5,
      "conditions": "partly_cloudy",
      "flight_safe": true
    }
  ],
  "alerts": [],
  "updated_at": "2025-07-01T11:00:00Z"
}
```

## User Management APIs

### User Registration
Register a new user account.

**Endpoint:** `POST /users/register`

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1-555-123-4567",
  "address": {
    "street": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94105"
  }
}
```

**Response (201 Created):**
```json
{
  "user_id": "user_123",
  "email": "john.doe@example.com",
  "status": "pending_verification",
  "verification_sent": true,
  "created_at": "2025-07-01T10:00:00Z"
}
```

### User Login
Authenticate user and return JWT token.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "user_id": "user_123",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "status": "active"
  }
}
```

## Notification APIs

### Send Notification
Send notification to user (internal API).

**Endpoint:** `POST /notifications/send`

**Request Body:**
```json
{
  "user_id": "user_123",
  "type": "delivery_update",
  "channels": ["push", "sms", "email"],
  "message": {
    "title": "Your order is on the way!",
    "body": "Your package will arrive in approximately 15 minutes.",
    "data": {
      "order_id": "ORD-2025-001234",
      "tracking_number": "TRK-789456123",
      "estimated_arrival": "2025-07-01T11:25:00Z"
    }
  }
}
```

### Get Notification Preferences
Get user's notification preferences.

**Endpoint:** `GET /users/{user_id}/notification-preferences`

**Response (200 OK):**
```json
{
  "user_id": "user_123",
  "preferences": {
    "order_confirmation": {
      "push": true,
      "sms": true,
      "email": true
    },
    "delivery_updates": {
      "push": true,
      "sms": false,
      "email": false
    },
    "promotions": {
      "push": false,
      "sms": false,
      "email": true
    }
  },
  "updated_at": "2025-07-01T10:00:00Z"
}
```

## Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request contains invalid parameters",
    "details": [
      {
        "field": "package.weight",
        "message": "Weight cannot exceed 5.0 kg"
      }
    ],
    "request_id": "req_123456789",
    "timestamp": "2025-07-01T11:00:00Z"
  }
}
```

### Error Codes
- `INVALID_REQUEST` (400): Request validation failed
- `UNAUTHORIZED` (401): Authentication required
- `FORBIDDEN` (403): Insufficient permissions
- `NOT_FOUND` (404): Resource not found
- `CONFLICT` (409): Resource conflict
- `RATE_LIMITED` (429): Too many requests
- `INTERNAL_ERROR` (500): Internal server error
- `SERVICE_UNAVAILABLE` (503): Service temporarily unavailable

## Rate Limiting

All APIs are rate limited based on user tier:

### Rate Limits by Endpoint
- **Order APIs**: 100 requests/minute per user
- **Tracking APIs**: 1000 requests/minute per user
- **Fleet APIs**: 50 requests/minute per admin
- **Auth APIs**: 10 requests/minute per IP

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1625097600
```

## API Versioning

APIs are versioned using URL path versioning:
- Current version: `/v1/`
- Deprecated versions supported for 12 months
- Breaking changes require new version
- Non-breaking changes deployed to existing version

## Webhook APIs

### Configure Webhooks
Configure webhook endpoints for order updates.

**Endpoint:** `POST /webhooks`

**Request Body:**
```json
{
  "url": "https://your-app.com/webhooks/drone-delivery",
  "events": ["order.created", "order.updated", "delivery.completed"],
  "secret": "webhook_secret_key"
}
```

### Webhook Payload Example
```json
{
  "event": "delivery.completed",
  "timestamp": "2025-07-01T11:30:00Z",
  "data": {
    "order_id": "ORD-2025-001234",
    "status": "delivered",
    "delivered_at": "2025-07-01T11:28:45Z",
    "delivery_confirmation": {
      "signature": "John Doe",
      "photo_url": "https://cdn.example.com/delivery-photos/123.jpg"
    }
  },
  "signature": "sha256=..."
}
```
