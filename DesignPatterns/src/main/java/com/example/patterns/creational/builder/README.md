# Builder Pattern - Easy to Understand Guide

## What is the Builder Pattern?

The Builder Pattern is used when you want to create objects that have many optional parts or configurations. Instead of having constructors with many parameters, you build the object step by step.

## Why Use Builder Pattern?

### Problems it solves:
1. **Too many constructor parameters** - Hard to remember the order
2. **Optional parameters** - You don't always need every feature
3. **Readable code** - Clear what each part does

### Before Builder Pattern (Bad):
```java
// Confusing constructor with many parameters
House house = new House(5, 3, true, false, true, "tile", true);
// What do these booleans mean? Hard to read!
```

### After Builder Pattern (Good):
```java
// Clear and readable
House house = new House.HouseBuilder(5, 3)
    .withGarage()
    .withPool()
    .withRoof("tile")
    .build();
// Easy to understand what each feature does!
```

## Simple Examples

### 1. House Builder (Simplest)
```java
// Basic house - just required info
House basicHouse = new House.HouseBuilder(3, 2)
    .build();

// Fancy house - add optional features
House fancyHouse = new House.HouseBuilder(5, 3)
    .withGarage()    // Add garage
    .withGarden()    // Add garden
    .withPool()      // Add pool
    .withRoof("tile") // Change roof type
    .build();
```

### 2. Pizza Builder (More Features)
```java
// Plain pizza
Pizza plain = new Pizza.PizzaBuilder("Medium", "thin crust")
    .build();

// Loaded pizza
Pizza loaded = new Pizza.PizzaBuilder("Large", "thick crust")
    .addCheese()     // Add cheese
    .addPepperoni()  // Add pepperoni
    .addMushrooms()  // Add mushrooms
    .addOlives()     // Add olives
    .build();
```

## How Builder Pattern Works

### Step 1: Main Class (Private Constructor)
```java
public class House {
    private final int rooms;
    private final boolean hasGarage;
    
    // Private - only Builder can create House
    private House(HouseBuilder builder) {
        this.rooms = builder.rooms;
        this.hasGarage = builder.hasGarage;
    }
}
```

### Step 2: Builder Class (Inside Main Class)
```java
public static class HouseBuilder {
    private int rooms;           // Required
    private boolean hasGarage = false;  // Optional, default false
    
    // Constructor for required fields
    public HouseBuilder(int rooms) {
        this.rooms = rooms;
    }
    
    // Method to add garage
    public HouseBuilder withGarage() {
        this.hasGarage = true;
        return this;  // Return 'this' for chaining
    }
    
    // Build the final house
    public House build() {
        return new House(this);
    }
}
```

### Step 3: Using the Builder
```java
House house = new House.HouseBuilder(3)  // Required: 3 rooms
    .withGarage()                         // Optional: add garage
    .build();                             // Create the house
```

## Key Benefits

### 1. **Readable Code**
- Each method clearly states what it does
- No confusing parameter positions
- Self-documenting

### 2. **Flexible Construction**
- Add only the features you want
- Skip optional features easily
- Different combinations possible

### 3. **Method Chaining**
- Fluent interface: `.withGarage().withPool().build()`
- Reads like natural language
- Easy to write and understand

### 4. **Immutable Objects**
- Once built, object cannot be changed
- Thread-safe
- Prevents bugs from accidental changes

## Common Patterns

### Required vs Optional
```java
// Required parameters in constructor
new House.HouseBuilder(rooms, bathrooms)  // Must provide

// Optional features as methods
.withGarage()     // Optional
.withPool()       // Optional
```

### Boolean Features
```java
// Instead of: setHasGarage(true)
.withGarage()     // Clearer intent

// Instead of: setHasPool(false)
// Just don't call .withPool()
```

### Configuration Features
```java
// Setting specific values
.withRoof("tile")           // Set roof type
.withSize("Large")          // Set size
.withCrust("thick crust")   // Set crust type
```

## When to Use Builder Pattern

### ✅ Good for:
- Objects with many optional parameters
- Complex object construction
- When you want immutable objects
- When parameter order is confusing

### ❌ Not needed for:
- Simple objects with few parameters
- Objects that change frequently after creation
- When all parameters are usually required

## Real-World Examples

- **StringBuilder** in Java
- **Pizza ordering** systems
- **Computer configuration** builders
- **House/Building** design
- **HTTP request** builders
- **Database query** builders

## Tips for Good Builder Design

1. **Required parameters** → Constructor
2. **Optional parameters** → Builder methods
3. **Return 'this'** for method chaining
4. **Clear method names** (withGarage, addCheese)
5. **build() method** creates final object
6. **Private constructor** in main class

## Running the Examples

```bash
# Compile and run the comprehensive demo
javac -d target/classes src/main/java/com/example/patterns/creational/builder/*.java
java -cp target/classes com.example.patterns.creational.builder.BuilderPatternDemo
```

The Builder Pattern makes complex object creation simple and readable!
