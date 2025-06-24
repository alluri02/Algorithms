# Complete Guide to Creational Design Patterns

## Overview

Creational patterns deal with **object creation mechanisms**, trying to create objects in a manner suitable to the situation. These patterns make object creation more flexible and provide solutions to control object creation.

## ✅ All 7 Creational Patterns Implemented

### 1. **Singleton Pattern** 🔄
**Purpose**: Ensure a class has only one instance and provide global access to it.

**When to use**:
- Database connections
- Logging services
- Configuration managers
- Thread pools

**Example**:
```java
DatabaseConnection db1 = DatabaseConnection.getInstance();
DatabaseConnection db2 = DatabaseConnection.getInstance();
// db1 == db2 (same instance)
```

**Key Features**:
- Thread-safe implementation
- Lazy initialization
- Double-checked locking

---

### 2. **Factory Method Pattern** 🏭
**Purpose**: Create objects without specifying the exact class to create.

**When to use**:
- When you don't know exact types beforehand
- When object creation is complex
- When you want to centralize creation logic

**Example**:
```java
ShapeFactory factory = new ShapeFactory();
Shape circle = factory.getShape("CIRCLE");
Shape rectangle = factory.getShape("RECTANGLE");
```

**Key Features**:
- Encapsulates object creation
- Easy to extend with new types
- Follows Open/Closed Principle

---

### 3. **Builder Pattern** 🏗️
**Purpose**: Construct complex objects step by step with optional parameters.

**When to use**:
- Objects with many optional parameters
- Complex object construction
- When you want immutable objects

**Example**:
```java
House house = new House.HouseBuilder(3, 2)
    .withGarage()
    .withPool()
    .withRoof("tile")
    .build();
```

**Key Features**:
- Fluent API (method chaining)
- Handles optional parameters elegantly
- Creates immutable objects

---

### 4. **Abstract Factory Pattern** 🏢
**Purpose**: Create families of related objects without specifying their concrete classes.

**When to use**:
- Creating UI components for different platforms
- Database drivers for different databases
- Cross-platform applications

**Example**:
```java
UIFactory windowsFactory = Application.getFactory("Windows");
Button button = windowsFactory.createButton();
Checkbox checkbox = windowsFactory.createCheckbox();
```

**Key Features**:
- Creates families of related objects
- Platform/environment specific creation
- Ensures compatibility between products

---

### 5. **Prototype Pattern** 🔬
**Purpose**: Create objects by cloning existing instances instead of creating new ones.

**When to use**:
- Object creation is expensive (database queries, network calls)
- You need many similar objects with slight variations
- Dynamic object creation at runtime

**Example**:
```java
ShapeCache cache = new ShapeCache();
Shape circle1 = cache.getShape("circle");  // Clone from cache
Shape circle2 = cache.getShape("circle");  // Another clone
// circle1 != circle2 (different instances)
```

**Key Features**:
- Avoids expensive object creation
- Clone instead of create
- Registry/cache of prototypes

---

### 6. **Object Pool Pattern** 🏊‍♂️
**Purpose**: Reuse expensive objects instead of creating new ones every time.

**When to use**:
- Database connections
- Thread pools
- Graphics objects
- Network connections

**Example**:
```java
ConnectionPool pool = new ConnectionPool(5);
DatabaseConnection conn = pool.borrowConnection();
conn.executeQuery("SELECT * FROM users");
pool.returnConnection(conn);  // Return for reuse
```

**Key Features**:
- Manages expensive object lifecycle
- Performance optimization
- Resource limitation

---

### 7. **Dependency Injection Pattern** 💉
**Purpose**: Inject dependencies from outside instead of creating them inside the class.

**When to use**:
- Making code testable
- Loose coupling between classes
- Configuration-based object creation
- Framework development

**Example**:
```java
// Dependencies injected through constructor
UserService service = new UserService(
    emailService,     // Injected
    loggingService,   // Injected
    databaseService   // Injected
);
```

**Key Features**:
- Loose coupling
- Easy testing (mock dependencies)
- Configuration flexibility

---

## Pattern Comparison

| Pattern | Complexity | Use Case | Key Benefit |
|---------|------------|----------|-------------|
| **Singleton** | Simple | One instance only | Global access |
| **Factory** | Simple | Unknown types | Centralized creation |
| **Builder** | Medium | Complex objects | Optional parameters |
| **Abstract Factory** | Medium | Related families | Platform independence |
| **Prototype** | Medium | Expensive creation | Clone vs create |
| **Object Pool** | Medium | Resource management | Reuse expensive objects |
| **Dependency Injection** | Medium | Loose coupling | Testable code |

## When to Use Each Pattern

### 🚀 **For Performance**:
- **Object Pool**: Reuse expensive objects
- **Prototype**: Clone instead of create
- **Singleton**: One expensive instance

### 🔧 **For Flexibility**:
- **Factory**: Easy to add new types
- **Abstract Factory**: Platform independence
- **Dependency Injection**: Configurable dependencies

### 📝 **For Complex Construction**:
- **Builder**: Many optional parameters
- **Factory**: Centralized creation logic

### 🧪 **For Testing**:
- **Dependency Injection**: Mock dependencies
- **Factory**: Test different implementations

## Project Structure

```
creational/
├── singleton/
│   └── DatabaseConnection.java          # Singleton Pattern
├── factory/
│   ├── Shape.java                        # Factory Pattern
│   ├── Circle.java, Rectangle.java, Square.java
│   └── ShapeFactory.java
├── builder/
│   ├── House.java                        # Simple Builder
│   ├── Pizza.java                        # Intuitive Builder
│   └── Computer.java                     # Complex Builder
├── abstractfactory/
│   └── Application.java                  # Abstract Factory Pattern
├── prototype/
│   └── PrototypeDemo.java               # Prototype Pattern
├── objectpool/
│   └── ObjectPoolDemo.java              # Object Pool Pattern
└── dependencyinjection/
    └── DependencyInjectionDemo.java     # Dependency Injection Pattern
```

## Running the Examples

### All Patterns Demo:
```bash
java -cp target/classes com.example.patterns.Main
```

### Individual Pattern Demos:
```bash
# Prototype Pattern
java -cp target/classes com.example.patterns.creational.prototype.PrototypeDemo

# Object Pool Pattern
java -cp target/classes com.example.patterns.creational.objectpool.ObjectPoolDemo

# Dependency Injection Pattern
java -cp target/classes com.example.patterns.creational.dependencyinjection.DependencyInjectionDemo

# Builder Pattern Comprehensive Demo
java -cp target/classes com.example.patterns.creational.builder.BuilderPatternDemo
```

## Key Takeaways

1. **Creational patterns solve object creation problems**
2. **Each pattern has specific use cases**
3. **Choose based on your needs**: performance, flexibility, testing, etc.
4. **Patterns can be combined**: Factory + Singleton, Builder + Prototype, etc.
5. **Start simple**: Don't over-engineer, use patterns when they add value

## Next Steps

- Learn **Structural Patterns** (Adapter, Decorator, Facade, etc.)
- Learn **Behavioral Patterns** (Observer, Strategy, Command, etc.)
- Practice implementing these patterns in real projects
- Understand when NOT to use patterns (avoid over-engineering)

The goal is to have the right tool for the right job! 🛠️
