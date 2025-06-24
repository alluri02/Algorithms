# Design Patterns in Java

A comprehensive collection of Design Pattern implementations in Java following best practices and SOLID principles.

## Project Structure

This project demonstrates the implementation of various design patterns categorized into three main types:

### Creational Patterns
- **Singleton Pattern** - Ensures a class has only one instance
- **Factory Method Pattern** - Creates objects without specifying exact classes
- **Abstract Factory Pattern** - Creates families of related objects
- **Builder Pattern** - Constructs complex objects step by step
- **Prototype Pattern** - Creates objects by cloning existing instances

### Structural Patterns
- **Adapter Pattern** - Allows incompatible interfaces to work together
- **Decorator Pattern** - Adds new functionality to objects dynamically
- **Facade Pattern** - Provides a simplified interface to a complex subsystem
- **Observer Pattern** - Defines a one-to-many dependency between objects
- **Strategy Pattern** - Encapsulates algorithms and makes them interchangeable

### Behavioral Patterns
- **Command Pattern** - Encapsulates requests as objects
- **Iterator Pattern** - Provides a way to access elements sequentially
- **State Pattern** - Allows objects to alter behavior when internal state changes
- **Template Method Pattern** - Defines algorithm skeleton in base class
- **Visitor Pattern** - Separates algorithms from object structure

## Getting Started

### Prerequisites
- Java 17 or higher
- Maven 3.6 or higher

### Building the Project
```bash
mvn clean compile
```

### Running Tests
```bash
mvn test
```

### Running Examples
```bash
mvn exec:java -Dexec.mainClass="com.example.patterns.Main"
```

## Usage Examples

Each pattern includes:
- Implementation classes
- Example usage
- Unit tests
- Documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your pattern implementation
4. Include unit tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
