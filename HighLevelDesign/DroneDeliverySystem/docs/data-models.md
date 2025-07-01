# Data Models - Drone Delivery System

## Core Entities

### 1. User
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'suspended', 'deleted') DEFAULT 'active'
);
```

### 2. Address
```sql
CREATE TABLE addresses (
    address_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    street_address VARCHAR(255) NOT NULL,
    apartment VARCHAR(50),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_delivery_safe BOOLEAN DEFAULT TRUE,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Order
```sql
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    pickup_address_id UUID REFERENCES addresses(address_id),
    delivery_address_id UUID REFERENCES addresses(address_id),
    package_weight DECIMAL(5, 2) NOT NULL, -- in kg
    package_dimensions JSON, -- {length, width, height}
    priority ENUM('standard', 'express', 'emergency') DEFAULT 'standard',
    special_handling JSON, -- fragile, temperature_sensitive, etc.
    estimated_delivery_time TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    total_cost DECIMAL(10, 2),
    status ENUM('placed', 'confirmed', 'assigned', 'in_transit', 'delivered', 'cancelled', 'failed') DEFAULT 'placed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Drone
```sql
CREATE TABLE drones (
    drone_id UUID PRIMARY KEY,
    model VARCHAR(100) NOT NULL,
    serial_number VARCHAR(100) UNIQUE NOT NULL,
    max_payload DECIMAL(5, 2) NOT NULL, -- in kg
    max_range DECIMAL(8, 2) NOT NULL, -- in km
    battery_capacity DECIMAL(8, 2) NOT NULL, -- in mAh
    current_battery_level DECIMAL(5, 2) DEFAULT 100.0, -- percentage
    status ENUM('available', 'assigned', 'in_flight', 'maintenance', 'charging', 'offline') DEFAULT 'offline',
    last_maintenance_date TIMESTAMP,
    next_maintenance_due TIMESTAMP,
    home_base_id UUID REFERENCES drone_bases(base_id),
    current_latitude DECIMAL(10, 8),
    current_longitude DECIMAL(11, 8),
    current_altitude DECIMAL(8, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Drone Base
```sql
CREATE TABLE drone_bases (
    base_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address_id UUID REFERENCES addresses(address_id),
    capacity INTEGER NOT NULL, -- max drones
    charging_stations INTEGER NOT NULL,
    operational_hours JSON, -- {start_time, end_time, days}
    manager_contact JSON, -- contact information
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Delivery Assignment
```sql
CREATE TABLE delivery_assignments (
    assignment_id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders(order_id),
    drone_id UUID REFERENCES drones(drone_id),
    pilot_id UUID REFERENCES pilots(pilot_id), -- for supervised flights
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_pickup_time TIMESTAMP,
    estimated_delivery_time TIMESTAMP,
    actual_pickup_time TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    route JSON, -- flight path coordinates
    status ENUM('assigned', 'en_route_pickup', 'picked_up', 'en_route_delivery', 'delivered', 'returned', 'failed') DEFAULT 'assigned'
);
```

### 7. Flight Path
```sql
CREATE TABLE flight_paths (
    path_id UUID PRIMARY KEY,
    assignment_id UUID REFERENCES delivery_assignments(assignment_id),
    waypoints JSON NOT NULL, -- array of {lat, lng, altitude, timestamp}
    estimated_duration INTEGER, -- in minutes
    actual_duration INTEGER, -- in minutes
    distance DECIMAL(8, 2), -- in km
    weather_conditions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 8. Real-time Tracking
```sql
CREATE TABLE drone_tracking (
    tracking_id UUID PRIMARY KEY,
    drone_id UUID REFERENCES drones(drone_id),
    assignment_id UUID REFERENCES delivery_assignments(assignment_id),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    altitude DECIMAL(8, 2) NOT NULL,
    speed DECIMAL(6, 2), -- in km/h
    heading DECIMAL(5, 2), -- degrees
    battery_level DECIMAL(5, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_drone_timestamp (drone_id, timestamp),
    INDEX idx_assignment_timestamp (assignment_id, timestamp)
);
```

### 9. Weather Data
```sql
CREATE TABLE weather_data (
    weather_id UUID PRIMARY KEY,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    temperature DECIMAL(5, 2), -- in Celsius
    humidity DECIMAL(5, 2), -- percentage
    wind_speed DECIMAL(6, 2), -- in km/h
    wind_direction DECIMAL(5, 2), -- degrees
    visibility DECIMAL(6, 2), -- in km
    precipitation DECIMAL(6, 2), -- in mm
    conditions VARCHAR(100), -- clear, cloudy, rainy, etc.
    flight_safe BOOLEAN DEFAULT TRUE,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_location_time (latitude, longitude, recorded_at)
);
```

### 10. Maintenance Records
```sql
CREATE TABLE maintenance_records (
    maintenance_id UUID PRIMARY KEY,
    drone_id UUID REFERENCES drones(drone_id),
    maintenance_type ENUM('routine', 'repair', 'upgrade', 'inspection') NOT NULL,
    description TEXT,
    technician_id UUID,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    cost DECIMAL(10, 2),
    parts_replaced JSON, -- array of part information
    next_maintenance_due TIMESTAMP,
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled') DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## NoSQL Document Models (MongoDB)

### Order Document
```javascript
{
  "_id": ObjectId("..."),
  "orderNumber": "ORD-2025-001234",
  "customer": {
    "userId": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  },
  "pickup": {
    "address": {
      "street": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "zipCode": "94105",
      "coordinates": {
        "lat": 37.7749,
        "lng": -122.4194
      }
    },
    "contactPerson": "Store Manager",
    "instructions": "Ring bell at loading dock"
  },
  "delivery": {
    "address": {
      "street": "456 Oak Ave",
      "apartment": "Apt 2B",
      "city": "San Francisco",
      "state": "CA",
      "zipCode": "94102",
      "coordinates": {
        "lat": 37.7849,
        "lng": -122.4094
      }
    },
    "contactPerson": "Jane Smith",
    "instructions": "Leave at door if no answer",
    "deliveryWindow": {
      "start": "2025-07-01T14:00:00Z",
      "end": "2025-07-01T16:00:00Z"
    }
  },
  "package": {
    "weight": 2.5,
    "dimensions": {
      "length": 30,
      "width": 20,
      "height": 15
    },
    "specialHandling": ["fragile", "this_side_up"],
    "value": 150.00,
    "description": "Electronic device"
  },
  "pricing": {
    "baseFee": 10.00,
    "distanceFee": 5.00,
    "priorityFee": 3.00,
    "total": 18.00,
    "currency": "USD"
  },
  "status": "assigned",
  "timeline": {
    "placed": "2025-07-01T10:00:00Z",
    "confirmed": "2025-07-01T10:05:00Z",
    "assigned": "2025-07-01T10:30:00Z",
    "estimatedPickup": "2025-07-01T11:00:00Z",
    "estimatedDelivery": "2025-07-01T11:30:00Z"
  },
  "assignment": {
    "droneId": "drone-uuid",
    "assignmentId": "assignment-uuid",
    "pilotId": "pilot-uuid"
  },
  "createdAt": "2025-07-01T10:00:00Z",
  "updatedAt": "2025-07-01T10:30:00Z"
}
```

### Drone Status Document
```javascript
{
  "_id": ObjectId("..."),
  "droneId": "DRONE-001",
  "model": "DeliveryDrone-X1",
  "serialNumber": "DX1-2025-001",
  "specifications": {
    "maxPayload": 5.0,
    "maxRange": 25.0,
    "maxSpeed": 50.0,
    "batteryCapacity": 5000,
    "flightTime": 60
  },
  "currentStatus": {
    "status": "in_flight",
    "location": {
      "lat": 37.7749,
      "lng": -122.4194,
      "altitude": 120.0
    },
    "battery": 75.5,
    "speed": 35.2,
    "heading": 180.0,
    "lastUpdate": "2025-07-01T11:15:30Z"
  },
  "currentAssignment": {
    "orderId": "order-uuid",
    "assignmentId": "assignment-uuid",
    "status": "en_route_delivery",
    "estimatedArrival": "2025-07-01T11:30:00Z"
  },
  "homeBase": {
    "baseId": "base-uuid",
    "name": "SF Downtown Hub",
    "coordinates": {
      "lat": 37.7849,
      "lng": -122.4094
    }
  },
  "maintenance": {
    "lastMaintenance": "2025-06-15T08:00:00Z",
    "nextMaintenance": "2025-07-15T08:00:00Z",
    "flightHours": 145.5,
    "cycleCount": 289
  },
  "createdAt": "2025-01-01T00:00:00Z",
  "updatedAt": "2025-07-01T11:15:30Z"
}
```

## Time-Series Data (InfluxDB)

### Drone Telemetry
```
measurement: drone_telemetry
tags:
  - drone_id
  - assignment_id
  - base_id
fields:
  - latitude (float)
  - longitude (float)
  - altitude (float)
  - speed (float)
  - heading (float)
  - battery_level (float)
  - temperature (float)
  - vibration (float)
timestamp: 2025-07-01T11:15:30Z
```

### System Metrics
```
measurement: system_performance
tags:
  - service_name
  - instance_id
  - region
fields:
  - cpu_usage (float)
  - memory_usage (float)
  - request_count (integer)
  - response_time (float)
  - error_rate (float)
timestamp: 2025-07-01T11:15:30Z
```

## Data Relationships

### Entity Relationship Overview
- User (1) -> (N) Orders
- User (1) -> (N) Addresses
- Order (1) -> (1) Pickup Address
- Order (1) -> (1) Delivery Address
- Order (1) -> (1) Delivery Assignment
- Delivery Assignment (N) -> (1) Drone
- Drone (N) -> (1) Drone Base
- Delivery Assignment (1) -> (N) Flight Paths
- Drone (1) -> (N) Tracking Records
- Drone (1) -> (N) Maintenance Records

## Data Partitioning Strategy

### Horizontal Partitioning (Sharding)
- **Geographic Sharding**: Partition data by geographic regions
- **Time-based Sharding**: Partition historical data by time periods
- **Hash-based Sharding**: Distribute data using consistent hashing

### Vertical Partitioning
- Separate frequently accessed from rarely accessed columns
- Move large JSON/TEXT fields to separate tables
- Create read replicas for analytics workloads

## Caching Strategy

### Redis Cache Layers
```
Level 1: User sessions and authentication tokens
Level 2: Active orders and drone status
Level 3: Route calculations and weather data
Level 4: Static reference data (addresses, drone specs)
```

### Cache Keys Pattern
```
user:profile:{user_id}
order:active:{order_id}
drone:status:{drone_id}
route:cache:{origin_lat}:{origin_lng}:{dest_lat}:{dest_lng}
weather:current:{lat}:{lng}
```

## Data Consistency

### ACID Properties
- **Atomicity**: Use database transactions for critical operations
- **Consistency**: Enforce referential integrity constraints
- **Isolation**: Use appropriate isolation levels
- **Durability**: Regular backups and replication

### Eventual Consistency
- Non-critical data can be eventually consistent
- Use event sourcing for audit trails
- Implement compensation patterns for distributed transactions
