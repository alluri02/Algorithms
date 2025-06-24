# Design Patterns Implementation Guide

## Project Overview

This Java project demonstrates the implementation of various design patterns. Each pattern is implemented with best practices and includes comprehensive examples and unit tests.

## Project Structure

```
DesignPatterns/
├── src/
│   ├── main/java/com/example/patterns/
│   │   ├── Main.java                           # Demo application
│   │   ├── creational/
│   │   │   ├── singleton/
│   │   │   │   └── DatabaseConnection.java     # Singleton Pattern
│   │   │   ├── factory/
│   │   │   │   ├── Shape.java                  # Factory Pattern Interface
│   │   │   │   ├── Circle.java                 # Concrete Shape
│   │   │   │   ├── Rectangle.java              # Concrete Shape
│   │   │   │   ├── Square.java                 # Concrete Shape
│   │   │   │   └── ShapeFactory.java           # Factory Implementation
│   │   │   └── builder/
│   │   │       └── Computer.java               # Builder Pattern
│   │   ├── structural/
│   │   │   └── adapter/
│   │   │       ├── MediaPlayer.java            # Target Interface
│   │   │       ├── AdvancedMediaPlayer.java    # Adaptee Interface
│   │   │       ├── VlcPlayer.java              # Concrete Adaptee
│   │   │       ├── Mp4Player.java              # Concrete Adaptee
│   │   │       ├── MediaAdapter.java           # Adapter Implementation
│   │   │       └── AudioPlayer.java            # Client Class
│   │   └── behavioral/
│   │       └── observer/
│   │           ├── Observer.java               # Observer Interface
│   │           ├── Subject.java                # Subject Interface
│   │           ├── WeatherStation.java         # Concrete Subject
│   │           ├── PhoneDisplay.java           # Concrete Observer
│   │           └── TabletDisplay.java          # Concrete Observer
│   └── test/java/com/example/patterns/
│       ├── creational/
│       │   ├── singleton/
│       │   │   └── DatabaseConnectionTest.java
│       │   ├── factory/
│       │   │   └── ShapeFactoryTest.java
│       │   └── builder/
│       │       └── ComputerTest.java
├── target/                                     # Compiled classes
├── .vscode/                                    # VS Code configuration
├── pom.xml                                     # Maven configuration
├── run.bat                                     # Windows batch script
├── run.ps1                                     # PowerShell script
├── .gitignore                                  # Git ignore rules
└── README.md                                   # Project documentation
```

## Design Patterns Implemented

### 1. Singleton Pattern
**Location**: `src/main/java/com/example/patterns/creational/singleton/`

**Purpose**: Ensures a class has only one instance and provides global access to it.

**Key Features**:
- Thread-safe implementation using double-checked locking
- Lazy initialization for performance
- Demonstrates database connection scenario

**Usage**:
```java
DatabaseConnection db = DatabaseConnection.getInstance();
db.connect();
```

### 2. Factory Pattern
**Location**: `src/main/java/com/example/patterns/creational/factory/`

**Purpose**: Creates objects without specifying the exact class to create.

**Key Features**:
- Encapsulates object creation logic
- Easy to extend with new shapes
- Follows Open/Closed Principle

**Usage**:
```java
ShapeFactory factory = new ShapeFactory();
Shape circle = factory.getShape("CIRCLE");
circle.draw();
```

### 3. Builder Pattern
**Location**: `src/main/java/com/example/patterns/creational/builder/`

**Purpose**: Constructs complex objects step by step with optional parameters.

**Key Features**:
- Handles complex object construction
- Method chaining for fluent API
- Separates construction from representation

**Usage**:
```java
Computer computer = new Computer.ComputerBuilder("Intel i7", "16GB")
    .storage("1TB SSD")
    .graphicsCard("RTX 4070")
    .hasWifi(true)
    .build();
```

### 4. Adapter Pattern
**Location**: `src/main/java/com/example/patterns/structural/adapter/`

**Purpose**: Allows incompatible interfaces to work together.

**Key Features**:
- Enables legacy code integration
- Converts one interface to another
- Promotes code reuse

**Usage**:
```java
AudioPlayer player = new AudioPlayer();
player.play("mp4", "movie.mp4"); // Uses adapter internally
```

### 5. Observer Pattern
**Location**: `src/main/java/com/example/patterns/behavioral/observer/`

**Purpose**: Defines a one-to-many dependency between objects.

**Key Features**:
- Loose coupling between subject and observers
- Dynamic subscription/unsubscription
- Broadcast communication

**Usage**:
```java
WeatherStation station = new WeatherStation();
PhoneDisplay phone = new PhoneDisplay();
station.addObserver(phone);
station.setWeatherData(25.0f, 60, 1013.2f);
```

## Building and Running

### Prerequisites
- Java 11 or higher
- Maven (optional, for dependency management)

### Quick Start

#### Option 1: Using Batch Script (Windows)
```cmd
run.bat
```

#### Option 2: Using PowerShell Script
```powershell
.\run.ps1
```

#### Option 3: Manual Compilation
```cmd
# Create target directory
mkdir target\classes

# Compile all Java files
javac -d target\classes -cp src\main\java src\main\java\com\example\patterns\**\*.java

# Run the demo
java -cp target\classes com.example.patterns.Main
```

#### Option 4: Using Maven (if available)
```cmd
mvn clean compile exec:java -Dexec.mainClass="com.example.patterns.Main"
```

## Testing

### Running Unit Tests (Manual)
```cmd
# Compile test files
javac -d target\test-classes -cp "target\classes;junit-jupiter-api-5.9.2.jar" src\test\java\**\*.java

# Run tests (requires JUnit setup)
java -cp "target\test-classes;target\classes;junit-platform-console-standalone.jar" org.junit.platform.console.ConsoleLauncher --scan-classpath
```

### Running Tests with Maven
```cmd
mvn test
```

## Design Principles Demonstrated

1. **Single Responsibility Principle**: Each class has one reason to change
2. **Open/Closed Principle**: Classes are open for extension, closed for modification
3. **Dependency Inversion**: Depend on abstractions, not concretions
4. **Composition over Inheritance**: Favor object composition over class inheritance

## Best Practices Implemented

- **Thread Safety**: Proper synchronization in Singleton pattern
- **Immutability**: Builder pattern creates immutable objects
- **Interface Segregation**: Small, focused interfaces
- **Loose Coupling**: Observer pattern demonstrates loose coupling
- **Encapsulation**: Private constructors and controlled access

## Extension Points

### Adding New Patterns
1. Create appropriate package under `creational`, `structural`, or `behavioral`
2. Implement the pattern following existing conventions
3. Add demonstration in `Main.java`
4. Create comprehensive unit tests
5. Update this documentation

### Adding New Shapes (Factory Pattern)
1. Implement the `Shape` interface
2. Add case in `ShapeFactory.getShape()` method
3. Add test cases

### Adding New Media Types (Adapter Pattern)
1. Create new player implementing `AdvancedMediaPlayer`
2. Update `MediaAdapter` to handle new type
3. Test the integration

## Common Issues and Solutions

### Issue: "mvn command not found"
**Solution**: Maven is not installed. Use manual compilation with `javac` and `java` commands.

### Issue: Compilation errors about missing classes
**Solution**: Ensure all dependencies are compiled first. Use the provided scripts for proper compilation order.

### Issue: Class path issues
**Solution**: Make sure the `-cp` parameter includes all necessary directories.

## Performance Considerations

- **Singleton**: Lazy initialization reduces startup time
- **Factory**: Object creation is centralized and can be optimized
- **Observer**: Use weak references for large observer lists
- **Builder**: Consider object pooling for frequently created objects

## Security Considerations

- **Singleton**: Be aware of reflection attacks
- **Factory**: Validate input parameters
- **Observer**: Prevent memory leaks with proper cleanup

## Contributing

1. Follow existing code structure and naming conventions
2. Include comprehensive unit tests
3. Update documentation for new patterns
4. Ensure thread safety where applicable
5. Follow Java coding standards

## Further Reading

- "Design Patterns: Elements of Reusable Object-Oriented Software" by Gang of Four
- "Head First Design Patterns" by Freeman & Freeman
- "Effective Java" by Joshua Bloch
