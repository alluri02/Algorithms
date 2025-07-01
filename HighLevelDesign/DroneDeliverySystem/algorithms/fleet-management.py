# Fleet Management Algorithm - Drone Delivery System

"""
Overview:
The fleet management algorithm optimizes drone utilization, scheduling, and maintenance 
to ensure maximum operational efficiency while maintaining safety standards.

Core Components:
1. Drone State Management
2. Assignment Optimization  
3. Battery Management
4. Maintenance Scheduling
5. Load Balancing
"""

import heapq
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np

class DroneStatus(Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    IN_FLIGHT = "in_flight"
    CHARGING = "charging"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"

class MaintenanceType(Enum):
    ROUTINE = "routine"
    BATTERY = "battery"
    MOTOR = "motor"
    SENSOR = "sensor"
    EMERGENCY = "emergency"

@dataclass
class DroneState:
    drone_id: str
    status: DroneStatus
    battery_level: float  # 0-100
    location: Tuple[float, float, float]  # lat, lng, alt
    payload_capacity: float  # kg
    current_payload: float  # kg
    last_maintenance: datetime
    flight_hours: float
    cycle_count: int
    assigned_order_id: Optional[str] = None
    estimated_available_time: Optional[datetime] = None

@dataclass
class MaintenanceSchedule:
    drone_id: str
    maintenance_type: MaintenanceType
    scheduled_time: datetime
    estimated_duration: timedelta
    priority: int  # 1-10, 10 being highest
    description: str

class FleetManager:
    def __init__(self):
        self.drones: Dict[str, DroneState] = {}
        self.maintenance_queue: List[MaintenanceSchedule] = []
        self.assignment_history: Dict[str, List[Dict]] = {}
        self.performance_metrics: Dict[str, Dict] = {}
        
        # Configuration
        self.max_flight_hours_before_maintenance = 100
        self.min_battery_for_assignment = 30
        self.routine_maintenance_interval = timedelta(days=30)
        
    def register_drone(self, drone_id: str, specifications: Dict):
        """Register a new drone in the fleet"""
        self.drones[drone_id] = DroneState(
            drone_id=drone_id,
            status=DroneStatus.OFFLINE,
            battery_level=100.0,
            location=(0.0, 0.0, 0.0),
            payload_capacity=specifications['max_payload'],
            current_payload=0.0,
            last_maintenance=datetime.now(),
            flight_hours=0.0,
            cycle_count=0
        )
        
        self.performance_metrics[drone_id] = {
            'total_deliveries': 0,
            'success_rate': 100.0,
            'average_delivery_time': 0.0,
            'energy_efficiency': 0.0,
            'maintenance_cost': 0.0
        }
    
    def update_drone_status(self, drone_id: str, status: DroneStatus, 
                           location: Optional[Tuple[float, float, float]] = None,
                           battery_level: Optional[float] = None):
        """Update drone status and location"""
        if drone_id not in self.drones:
            raise ValueError(f"Drone {drone_id} not registered")
            
        drone = self.drones[drone_id]
        drone.status = status
        
        if location:
            drone.location = location
        if battery_level is not None:
            drone.battery_level = battery_level
            
        # Auto-schedule charging if battery is low
        if battery_level and battery_level < 20 and status != DroneStatus.CHARGING:
            self.schedule_charging(drone_id)
    
    def get_available_drones(self, min_battery: float = None, 
                           max_distance_km: float = None,
                           min_payload_capacity: float = None,
                           location: Tuple[float, float] = None) -> List[DroneState]:
        """Get list of available drones matching criteria"""
        available = []
        min_battery = min_battery or self.min_battery_for_assignment
        
        for drone in self.drones.values():
            if drone.status != DroneStatus.AVAILABLE:
                continue
                
            # Battery check
            if drone.battery_level < min_battery:
                continue
                
            # Payload capacity check
            if min_payload_capacity and drone.payload_capacity < min_payload_capacity:
                continue
                
            # Distance check
            if max_distance_km and location:
                distance = self.calculate_distance(
                    (drone.location[0], drone.location[1]), location
                )
                if distance > max_distance_km:
                    continue
                    
            # Maintenance check
            if self.needs_maintenance(drone):
                continue
                
            available.append(drone)
            
        return available
    
    def assign_drone_to_order(self, order_id: str, order_details: Dict) -> Optional[str]:
        """Assign optimal drone to an order"""
        pickup_location = (order_details['pickup_lat'], order_details['pickup_lng'])
        delivery_location = (order_details['delivery_lat'], order_details['delivery_lng'])
        package_weight = order_details['weight']
        priority = order_details.get('priority', 'standard')
        
        # Get available drones
        available_drones = self.get_available_drones(
            min_payload_capacity=package_weight,
            location=pickup_location
        )
        
        if not available_drones:
            return None
            
        # Calculate assignment scores
        drone_scores = []
        for drone in available_drones:
            score = self.calculate_assignment_score(drone, order_details)
            drone_scores.append((score, drone.drone_id))
        
        # Sort by score (lower is better)
        drone_scores.sort()
        best_drone_id = drone_scores[0][1]
        
        # Make assignment
        self.drones[best_drone_id].status = DroneStatus.ASSIGNED
        self.drones[best_drone_id].assigned_order_id = order_id
        self.drones[best_drone_id].current_payload = package_weight
        
        # Estimate availability time
        estimated_duration = self.estimate_delivery_duration(
            self.drones[best_drone_id], pickup_location, delivery_location
        )
        self.drones[best_drone_id].estimated_available_time = \
            datetime.now() + estimated_duration
        
        # Record assignment
        if best_drone_id not in self.assignment_history:
            self.assignment_history[best_drone_id] = []
        self.assignment_history[best_drone_id].append({
            'order_id': order_id,
            'assigned_at': datetime.now(),
            'priority': priority,
            'weight': package_weight
        })
        
        return best_drone_id
    
    def calculate_assignment_score(self, drone: DroneState, order_details: Dict) -> float:
        """Calculate assignment score (lower is better)"""
        pickup_location = (order_details['pickup_lat'], order_details['pickup_lng'])
        delivery_location = (order_details['delivery_lat'], order_details['delivery_lng'])
        
        # Distance factor (40% weight)
        pickup_distance = self.calculate_distance(
            (drone.location[0], drone.location[1]), pickup_location
        )
        delivery_distance = self.calculate_distance(pickup_location, delivery_location)
        total_distance = pickup_distance + delivery_distance
        
        distance_score = total_distance * 0.4
        
        # Battery factor (25% weight)
        battery_score = (100 - drone.battery_level) * 0.25
        
        # Utilization factor (20% weight)
        utilization = order_details['weight'] / drone.payload_capacity
        utilization_score = (1 - utilization) * 0.2
        
        # Performance factor (15% weight)
        performance = self.performance_metrics[drone.drone_id]['success_rate']
        performance_score = (100 - performance) * 0.15
        
        return distance_score + battery_score + utilization_score + performance_score
    
    def complete_delivery(self, drone_id: str, success: bool, 
                         actual_duration: timedelta):
        """Mark delivery as complete and update metrics"""
        if drone_id not in self.drones:
            return
            
        drone = self.drones[drone_id]
        drone.status = DroneStatus.AVAILABLE
        drone.assigned_order_id = None
        drone.current_payload = 0.0
        drone.cycle_count += 1
        
        # Update flight hours (approximate)
        flight_hours = actual_duration.total_seconds() / 3600
        drone.flight_hours += flight_hours
        
        # Update performance metrics
        metrics = self.performance_metrics[drone_id]
        metrics['total_deliveries'] += 1
        
        if success:
            # Update success rate
            total_deliveries = metrics['total_deliveries']
            current_successes = (metrics['success_rate'] / 100) * (total_deliveries - 1)
            new_successes = current_successes + 1
            metrics['success_rate'] = (new_successes / total_deliveries) * 100
        else:
            # Handle failure
            total_deliveries = metrics['total_deliveries']
            current_successes = (metrics['success_rate'] / 100) * (total_deliveries - 1)
            metrics['success_rate'] = (current_successes / total_deliveries) * 100
            
        # Schedule maintenance if needed
        if self.needs_maintenance(drone):
            self.schedule_maintenance(drone_id, MaintenanceType.ROUTINE)
    
    def needs_maintenance(self, drone: DroneState) -> bool:
        """Check if drone needs maintenance"""
        # Flight hours check
        if drone.flight_hours >= self.max_flight_hours_before_maintenance:
            return True
            
        # Time-based check
        time_since_maintenance = datetime.now() - drone.last_maintenance
        if time_since_maintenance >= self.routine_maintenance_interval:
            return True
            
        # Cycle count check
        if drone.cycle_count >= 1000:
            return True
            
        # Battery degradation check
        if drone.battery_level < 85 and drone.status == DroneStatus.AVAILABLE:
            return True
            
        return False
    
    def schedule_maintenance(self, drone_id: str, maintenance_type: MaintenanceType,
                           priority: int = 5):
        """Schedule maintenance for a drone"""
        estimated_duration = {
            MaintenanceType.ROUTINE: timedelta(hours=4),
            MaintenanceType.BATTERY: timedelta(hours=2),
            MaintenanceType.MOTOR: timedelta(hours=6),
            MaintenanceType.SENSOR: timedelta(hours=3),
            MaintenanceType.EMERGENCY: timedelta(hours=8)
        }
        
        maintenance = MaintenanceSchedule(
            drone_id=drone_id,
            maintenance_type=maintenance_type,
            scheduled_time=datetime.now() + timedelta(hours=1),  # Schedule for 1 hour later
            estimated_duration=estimated_duration[maintenance_type],
            priority=priority,
            description=f"{maintenance_type.value} maintenance for {drone_id}"
        )
        
        # Add to priority queue
        heapq.heappush(self.maintenance_queue, 
                      (priority, maintenance.scheduled_time, maintenance))
        
        # Update drone status if emergency
        if maintenance_type == MaintenanceType.EMERGENCY:
            self.drones[drone_id].status = DroneStatus.MAINTENANCE
    
    def schedule_charging(self, drone_id: str):
        """Schedule drone for charging"""
        if drone_id in self.drones:
            self.drones[drone_id].status = DroneStatus.CHARGING
            # Simulate charging completion (would be real-time in actual system)
            charging_time = (100 - self.drones[drone_id].battery_level) * 0.5  # minutes
            self.drones[drone_id].estimated_available_time = \
                datetime.now() + timedelta(minutes=charging_time)
    
    def process_maintenance_queue(self) -> Optional[MaintenanceSchedule]:
        """Process next maintenance in queue"""
        if not self.maintenance_queue:
            return None
            
        priority, scheduled_time, maintenance = heapq.heappop(self.maintenance_queue)
        
        # Check if it's time for maintenance
        if datetime.now() >= scheduled_time:
            drone = self.drones[maintenance.drone_id]
            drone.status = DroneStatus.MAINTENANCE
            drone.last_maintenance = datetime.now()
            return maintenance
        else:
            # Put it back in queue
            heapq.heappush(self.maintenance_queue, (priority, scheduled_time, maintenance))
            return None
    
    def complete_maintenance(self, drone_id: str):
        """Mark maintenance as complete"""
        if drone_id in self.drones:
            drone = self.drones[drone_id]
            drone.status = DroneStatus.AVAILABLE
            drone.battery_level = 100.0  # Assume full charge after maintenance
            drone.flight_hours = 0.0  # Reset flight hours
            drone.cycle_count = 0  # Reset cycle count
    
    def get_fleet_statistics(self) -> Dict:
        """Get fleet performance statistics"""
        total_drones = len(self.drones)
        if total_drones == 0:
            return {}
            
        available_count = sum(1 for d in self.drones.values() 
                             if d.status == DroneStatus.AVAILABLE)
        assigned_count = sum(1 for d in self.drones.values() 
                            if d.status == DroneStatus.ASSIGNED)
        in_flight_count = sum(1 for d in self.drones.values() 
                             if d.status == DroneStatus.IN_FLIGHT)
        charging_count = sum(1 for d in self.drones.values() 
                            if d.status == DroneStatus.CHARGING)
        maintenance_count = sum(1 for d in self.drones.values() 
                               if d.status == DroneStatus.MAINTENANCE)
        
        # Calculate utilization
        active_drones = assigned_count + in_flight_count
        utilization_rate = (active_drones / total_drones) * 100 if total_drones > 0 else 0
        
        # Calculate average battery level
        avg_battery = np.mean([d.battery_level for d in self.drones.values()])
        
        # Calculate fleet performance
        total_deliveries = sum(m['total_deliveries'] for m in self.performance_metrics.values())
        avg_success_rate = np.mean([m['success_rate'] for m in self.performance_metrics.values()])
        
        return {
            'total_drones': total_drones,
            'available': available_count,
            'assigned': assigned_count,
            'in_flight': in_flight_count,
            'charging': charging_count,
            'maintenance': maintenance_count,
            'utilization_rate': utilization_rate,
            'average_battery_level': avg_battery,
            'total_deliveries': total_deliveries,
            'average_success_rate': avg_success_rate,
            'pending_maintenance': len(self.maintenance_queue)
        }
    
    def optimize_fleet_distribution(self, demand_forecast: Dict[str, int]) -> Dict[str, int]:
        """Optimize drone distribution based on demand forecast"""
        # This would implement more sophisticated optimization
        # For now, simple proportional distribution
        
        total_demand = sum(demand_forecast.values())
        available_drones = [d for d in self.drones.values() 
                           if d.status == DroneStatus.AVAILABLE]
        total_available = len(available_drones)
        
        distribution = {}
        for zone, demand in demand_forecast.items():
            if total_demand > 0:
                allocated = int((demand / total_demand) * total_available)
                distribution[zone] = allocated
            else:
                distribution[zone] = 0
                
        return distribution
    
    def calculate_distance(self, coord1: Tuple[float, float], 
                          coord2: Tuple[float, float]) -> float:
        """Calculate distance between two coordinates in km"""
        import math
        
        lat1, lng1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lng2 = math.radians(coord2[0]), math.radians(coord2[1])
        
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        
        return 6371 * c  # Earth's radius in km
    
    def estimate_delivery_duration(self, drone: DroneState, 
                                 pickup: Tuple[float, float],
                                 delivery: Tuple[float, float]) -> timedelta:
        """Estimate total delivery duration"""
        pickup_distance = self.calculate_distance(
            (drone.location[0], drone.location[1]), pickup
        )
        delivery_distance = self.calculate_distance(pickup, delivery)
        total_distance = pickup_distance + delivery_distance
        
        # Assume average speed of 40 km/h including loading/unloading time
        average_speed = 40
        duration_hours = total_distance / average_speed
        
        # Add buffer time for loading/unloading
        buffer_minutes = 10
        
        total_minutes = (duration_hours * 60) + buffer_minutes
        return timedelta(minutes=total_minutes)

# Usage Example
def main():
    fleet_manager = FleetManager()
    
    # Register some drones
    for i in range(5):
        drone_id = f"DRONE-{i+1:03d}"
        specs = {
            'max_payload': 5.0,
            'max_speed': 60,
            'battery_capacity': 5000
        }
        fleet_manager.register_drone(drone_id, specs)
        fleet_manager.update_drone_status(drone_id, DroneStatus.AVAILABLE,
                                        location=(37.7749 + i*0.01, -122.4194 + i*0.01, 100),
                                        battery_level=80 + i*2)
    
    # Simulate order assignment
    order = {
        'pickup_lat': 37.7749,
        'pickup_lng': -122.4194,
        'delivery_lat': 37.7849,
        'delivery_lng': -122.4094,
        'weight': 2.5,
        'priority': 'express'
    }
    
    assigned_drone = fleet_manager.assign_drone_to_order('ORDER-001', order)
    print(f"Assigned drone: {assigned_drone}")
    
    # Get fleet statistics
    stats = fleet_manager.get_fleet_statistics()
    print("Fleet Statistics:", stats)

if __name__ == "__main__":
    main()
