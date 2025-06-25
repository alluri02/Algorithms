# Structural Design Patterns Implementation

This document provides a comprehensive guide to all structural design patterns implemented in this project.

## Overview

Structural patterns deal with object composition. They help ensure that if one part of a system changes, the entire structure of the system doesn't need to change along with it.

## Implemented Patterns

### 1. Adapter Pattern
**Location**: `src/main/java/com/example/patterns/structural/adapter/`

**Purpose**: Allows incompatible interfaces to work together by providing a wrapper that converts one interface to another.

**Key Components**:
- `MediaPlayer` - Target interface
- `AdvancedMediaPlayer` - Adaptee interface  
- `MediaAdapter` - Adapter class
- `AudioPlayer` - Client class

**Use Case**: Playing different audio formats (MP3, MP4, VLC) through a unified interface.

### 2. Bridge Pattern
**Location**: `src/main/java/com/example/patterns/structural/bridge/`

**Purpose**: Separates an abstraction from its implementation, allowing both to vary independently.

**Key Components**:
- `Device` - Implementation interface
- `Television`, `Radio` - Concrete implementations
- `RemoteControl` - Abstraction
- `AdvancedRemoteControl` - Refined abstraction

**Use Case**: Remote controls that can work with different types of devices.

### 3. Composite Pattern
**Location**: `src/main/java/com/example/patterns/structural/composite/`

**Purpose**: Composes objects into tree structures to represent part-whole hierarchies, allowing clients to treat individual objects and compositions uniformly.

**Key Components**:
- `FileSystemComponent` - Component interface
- `File` - Leaf component
- `Directory` - Composite component

**Use Case**: File system where directories can contain files and other directories.

### 4. Decorator Pattern
**Location**: `src/main/java/com/example/patterns/structural/decorator/`

**Purpose**: Adds new functionality to objects dynamically without altering their structure.

**Key Components**:
- `Coffee` - Component interface
- `SimpleCoffee` - Concrete component
- `CoffeeDecorator` - Base decorator
- `MilkDecorator`, `SugarDecorator`, `VanillaDecorator` - Concrete decorators

**Use Case**: Adding various ingredients to coffee orders.

### 5. Facade Pattern
**Location**: `src/main/java/com/example/patterns/structural/facade/`

**Purpose**: Provides a simplified interface to a complex subsystem.

**Key Components**:
- `CPU`, `Memory`, `HardDrive` - Subsystem classes
- `ComputerFacade` - Facade class

**Use Case**: Simplified computer startup/shutdown operations hiding complex subsystem interactions.

### 6. Flyweight Pattern
**Location**: `src/main/java/com/example/patterns/structural/flyweight/`

**Purpose**: Minimizes memory usage by sharing efficiently among similar objects.

**Key Components**:
- `TreeType` - Flyweight interface
- `ConcreteTreeType` - Concrete flyweight (intrinsic state)
- `Tree` - Context (extrinsic state)
- `TreeTypeFactory` - Flyweight factory
- `Forest` - Client

**Use Case**: Rendering many trees in a forest game efficiently.

### 7. Proxy Pattern
**Location**: `src/main/java/com/example/patterns/structural/proxy/`

**Purpose**: Provides a placeholder or surrogate for another object to control access to it.

**Key Components**:
- `Image`, `Document` - Subject interfaces
- `RealImage`, `RealDocument` - Real subjects
- `ImageProxy`, `DocumentProxy` - Proxy classes

**Use Cases**: 
- Virtual Proxy: Lazy loading of expensive resources (images)
- Protection Proxy: Access control based on user permissions (documents)

## Pattern Comparisons

### Adapter vs Bridge
- **Adapter**: Makes incompatible interfaces work together (after classes are designed)
- **Bridge**: Separates abstraction from implementation (planned from the beginning)

### Composite vs Decorator
- **Composite**: Focuses on tree structures and part-whole relationships
- **Decorator**: Focuses on adding responsibilities to objects

### Facade vs Adapter
- **Facade**: Simplifies a complex interface
- **Adapter**: Makes incompatible interfaces compatible

### Flyweight vs Singleton
- **Flyweight**: Manages multiple instances efficiently by sharing state
- **Singleton**: Ensures only one instance exists

### Proxy vs Decorator
- **Proxy**: Controls access to an object (same interface)
- **Decorator**: Adds new behavior to an object

## Running the Examples

### Individual Pattern Demos
```bash
# Bridge Pattern
java com.example.patterns.structural.bridge.BridgePatternDemo

# Composite Pattern  
java com.example.patterns.structural.composite.CompositePatternDemo

# Decorator Pattern
java com.example.patterns.structural.decorator.DecoratorPatternDemo

# Facade Pattern
java com.example.patterns.structural.facade.FacadePatternDemo

# Flyweight Pattern
java com.example.patterns.structural.flyweight.FlyweightPatternDemo

# Proxy Pattern
java com.example.patterns.structural.proxy.ProxyPatternDemo
```

### All Patterns Demo
```bash
java com.example.patterns.Main
```

### Running Tests
```bash
mvn test -Dtest="**/structural/**/*Test"
```

## Benefits of Structural Patterns

1. **Flexibility**: Easy to change implementations without affecting clients
2. **Reusability**: Components can be combined in different ways
3. **Maintainability**: Clear separation of concerns
4. **Performance**: Optimizations like lazy loading and object sharing
5. **Simplicity**: Complex operations hidden behind simple interfaces

## When to Use Each Pattern

### Adapter
- When you need to use an existing class with an incompatible interface
- When working with legacy code or third-party libraries

### Bridge
- When you want to avoid permanent binding between abstraction and implementation
- When both abstractions and implementations should be extensible

### Composite
- When you want to represent part-whole hierarchies
- When you want clients to treat individual objects and compositions uniformly

### Decorator
- When you want to add responsibilities to objects dynamically
- When extension by subclassing is impractical

### Facade
- When you want to provide a simple interface to a complex subsystem
- When there are many dependencies between clients and implementation classes

### Flyweight
- When you need to use a large number of similar objects
- When memory usage is a concern

### Proxy
- When you need lazy loading, access control, caching, or logging
- When you want to add functionality without changing the original object

## Common Implementation Pitfalls

1. **Adapter**: Don't confuse with Bridge pattern
2. **Bridge**: Avoid tight coupling between abstraction and implementation
3. **Composite**: Ensure proper handling of parent-child relationships
4. **Decorator**: Be careful with the order of decorators
5. **Facade**: Don't make the facade too complex
6. **Flyweight**: Properly separate intrinsic and extrinsic state
7. **Proxy**: Ensure proxy implements the same interface as the real object
