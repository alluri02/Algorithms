# Behavioral Design Patterns Implementation

This document provides a comprehensive guide to all behavioral design patterns implemented in this project.

## Overview

Behavioral patterns focus on communication between objects and the assignment of responsibilities between objects. They help in defining how objects interact and communicate with each other.

## Implemented Patterns

### 1. Observer Pattern ✅ (Already Implemented)
**Location**: `src/main/java/com/example/patterns/behavioral/observer/`

**Purpose**: Defines a one-to-many dependency between objects so that when one object changes state, all dependents are notified.

### 2. Strategy Pattern
**Location**: `src/main/java/com/example/patterns/behavioral/strategy/`

**Purpose**: Defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime.

**Key Components**:
- `PaymentStrategy` - Strategy interface
- `CreditCardStrategy`, `PayPalStrategy`, `BitcoinStrategy` - Concrete strategies  
- `ShoppingCart` - Context class

**Use Case**: Payment processing with different payment methods that can be switched at runtime.

### 3. Command Pattern
**Location**: `src/main/java/com/example/patterns/behavioral/command/`

**Purpose**: Encapsulates a request as an object, allowing you to parameterize clients with different requests, queue operations, and support undo operations.

**Key Components**:
- `Command` - Command interface
- `LightOnCommand`, `LightOffCommand`, `LightDimCommand` - Concrete commands
- `MacroCommand` - Composite command
- `Light` - Receiver
- `RemoteControl` - Invoker

**Use Case**: Smart home remote control with undo functionality and macro commands.

### 4. State Pattern
**Location**: `src/main/java/com/example/patterns/behavioral/state/`

**Purpose**: Allows an object to alter its behavior when its internal state changes. The object will appear to change its class.

**Key Components**:
- `VendingMachineState` - State interface
- `IdleState`, `HasMoneyState`, `ProductSelectedState`, `OutOfStockState` - Concrete states
- `VendingMachine` - Context

**Use Case**: Vending machine that behaves differently based on its current state (idle, has money, product selected, etc.).

### 5. Template Method Pattern
**Location**: `src/main/java/com/example/patterns/behavioral/templatemethod/`

**Purpose**: Defines the skeleton of an algorithm in a base class, letting subclasses override specific steps without changing the algorithm's structure.

**Key Components**:
- `DataProcessor` - Abstract template class
- `CSVDataProcessor`, `JSONDataProcessor`, `XMLDataProcessor` - Concrete implementations

**Use Case**: Data processing pipeline where the overall process is the same but specific steps vary by data format.

### 6. Chain of Responsibility Pattern
**Location**: `src/main/java/com/example/patterns/behavioral/chainofresponsibility/`

**Purpose**: Passes requests along a chain of handlers until one of them handles the request.

**Key Components**:
- `SupportHandler` - Abstract handler
- `Level1SupportHandler`, `Level2SupportHandler`, `Level3SupportHandler`, `SecurityTeamHandler` - Concrete handlers
- `SupportTicket` - Request object

**Use Case**: Customer support ticket system where tickets are escalated through different support levels.

### 7. Mediator Pattern
**Location**: `src/main/java/com/example/patterns/behavioral/mediator/`

**Purpose**: Defines how a set of objects interact with each other. Promotes loose coupling by preventing objects from referring to each other explicitly.

**Key Components**:
- `ChatMediator` - Mediator interface
- `ChatRoom` - Concrete mediator
- `User` - Abstract colleague
- `RegularUser`, `PremiumUser`, `BotUser` - Concrete colleagues

**Use Case**: Chat room where users communicate through a central mediator rather than directly with each other.

## Pattern Comparisons

### Strategy vs State
- **Strategy**: Focuses on interchangeable algorithms/behaviors
- **State**: Focuses on object behavior changes based on internal state

### Command vs Strategy
- **Command**: Encapsulates requests and supports undo/redo
- **Strategy**: Encapsulates algorithms and focuses on runtime selection

### Chain of Responsibility vs Mediator
- **Chain of Responsibility**: Linear chain where one handler processes the request
- **Mediator**: Central hub that coordinates communication between multiple objects

### Template Method vs Strategy
- **Template Method**: Fixed algorithm structure with customizable steps
- **Strategy**: Completely interchangeable algorithms

### Observer vs Mediator
- **Observer**: One-to-many communication (publisher-subscriber)
- **Mediator**: Many-to-many communication through central coordinator

## Running the Examples

### Individual Pattern Demos
```bash
# Strategy Pattern
java -cp "src/main/java" com.example.patterns.behavioral.strategy.StrategyPatternDemo

# Command Pattern
java -cp "src/main/java" com.example.patterns.behavioral.command.CommandPatternDemo

# State Pattern
java -cp "src/main/java" com.example.patterns.behavioral.state.StatePatternDemo

# Template Method Pattern
java -cp "src/main/java" com.example.patterns.behavioral.templatemethod.TemplateMethodPatternDemo

# Chain of Responsibility Pattern
java -cp "src/main/java" com.example.patterns.behavioral.chainofresponsibility.ChainOfResponsibilityPatternDemo

# Mediator Pattern
java -cp "src/main/java" com.example.patterns.behavioral.mediator.MediatorPatternDemo
```

### All Patterns Demo
```bash
java -cp "src/main/java" com.example.patterns.Main
```

### Running Tests
```bash
mvn test -Dtest="**/behavioral/**/*Test"
```

## Benefits of Behavioral Patterns

1. **Loose Coupling**: Objects interact without being tightly coupled
2. **Flexibility**: Easy to add new behaviors or modify existing ones
3. **Reusability**: Behaviors can be reused across different contexts
4. **Maintainability**: Clear separation of concerns
5. **Extensibility**: New patterns can be added without modifying existing code

## When to Use Each Pattern

### Observer
- When changes to one object require updating multiple dependent objects
- When you want to notify multiple objects without making them tightly coupled

### Strategy
- When you have multiple ways to perform a task
- When you want to switch algorithms at runtime
- When you want to avoid conditional statements for algorithm selection

### Command
- When you want to parameterize objects with operations
- When you need to queue, log, or undo operations
- When you want to decouple invoker from receiver

### State
- When an object's behavior depends on its state
- When you have complex conditional logic based on object state
- When state transitions need to be explicit and controlled

### Template Method
- When you have an algorithm with fixed structure but variable steps
- When you want to avoid code duplication in similar algorithms
- When you want to control the algorithm structure while allowing customization

### Chain of Responsibility
- When you want to decouple request senders from receivers
- When multiple objects can handle a request
- When you want to pass requests through a chain until one handles it

### Mediator
- When you have complex communication between multiple objects
- When you want to reduce dependencies between communicating objects
- When you want to centralize complex communications and control logic

## Common Implementation Pitfalls

1. **Observer**: Avoid memory leaks by properly removing observers
2. **Strategy**: Don't confuse with State pattern
3. **Command**: Be careful with command history management
4. **State**: Ensure proper state transition validation
5. **Template Method**: Keep template method final to prevent override
6. **Chain of Responsibility**: Ensure the chain doesn't become too long
7. **Mediator**: Avoid making the mediator too complex

## Real-World Applications

- **Observer**: Model-View-Controller (MVC) architectures, Event systems
- **Strategy**: Payment gateways, Sorting algorithms, Data compression
- **Command**: GUI buttons, Macro recording, Transaction processing
- **State**: Game character behavior, Network protocols, UI workflows
- **Template Method**: Data processing pipelines, Web frameworks
- **Chain of Responsibility**: Exception handling, Request processing
- **Mediator**: Chat applications, Air traffic control, GUI components

## Best Practices

1. **Choose the right pattern** for your specific use case
2. **Keep interfaces simple** and focused
3. **Document the communication flow** clearly
4. **Test behavioral interactions** thoroughly
5. **Consider performance implications** of pattern overhead
6. **Use composition over inheritance** where appropriate
7. **Implement proper error handling** for edge cases
