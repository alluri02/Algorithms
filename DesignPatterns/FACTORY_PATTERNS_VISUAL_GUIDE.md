# Factory vs Abstract Factory - Visual Guide

## **The Main Difference in Pictures**

### **Factory Pattern** 🏭
```
                ShapeFactory
                     |
        ┌─────────────┼─────────────┐
        │             │             │
    [Circle]    [Rectangle]    [Square]
    
• ONE factory
• Creates different SHAPES (same family)
• Simple: Input → Factory → Single Product
```

### **Abstract Factory Pattern** 🏢
```
    WindowsFactory              MacFactory
         |                         |
    ┌────┴────┐               ┌────┴────┐
    |         |               |         |
[WinButton][WinCheckbox]  [MacButton][MacCheckbox]

• MULTIPLE factories  
• Each creates MULTIPLE related products
• Complex: Platform → Factory → Family of Products
```

---

## **Real-World Analogy**

### **Factory Pattern** = **Pizza Restaurant** 🍕
```
Pizza Kitchen (Factory)
├── Input: "Margherita" → Output: Margherita Pizza
├── Input: "Pepperoni"  → Output: Pepperoni Pizza
└── Input: "Veggie"     → Output: Veggie Pizza

ONE kitchen makes different PIZZAS
```

### **Abstract Factory Pattern** = **Restaurant Chain** 🏪
```
McDonald's Kitchen          KFC Kitchen
├── Burger + Fries         ├── Chicken + Coleslaw  
├── Drink + Dessert        ├── Drink + Biscuit
└── (McDonald's Family)    └── (KFC Family)

Each kitchen makes its OWN FAMILY of foods
```

---

## **Code Structure Comparison**

### **Factory Pattern Structure**
```java
// ONE product interface
interface Shape { void draw(); }

// ONE factory
class ShapeFactory {
    Shape getShape(String type) {
        // Creates different shapes
    }
}

// Usage: ONE factory → ONE product
Shape shape = factory.getShape("CIRCLE");
```

### **Abstract Factory Pattern Structure**  
```java
// MULTIPLE product interfaces
interface Button { void render(); }
interface Checkbox { void render(); }

// MULTIPLE factories
interface UIFactory {
    Button createButton();      // Multiple
    Checkbox createCheckbox();  // products
}

// Usage: ONE factory → MULTIPLE related products
UIFactory factory = new WindowsFactory();
Button button = factory.createButton();     // Family
Checkbox checkbox = factory.createCheckbox(); // member
```

---

## **Decision Tree: Which Pattern to Use?**

```
Do you need to create objects?
         │
         ▼
Is it ONE TYPE of object (like shapes)?
         │
    ┌────┴────┐
   YES        NO
    │          │
    ▼          ▼
Use FACTORY    Do you need FAMILIES of related objects?
Pattern              │
                ┌────┴────┐
               YES        NO
                │          │
                ▼          ▼
        Use ABSTRACT    Consider other
        FACTORY         patterns
        Pattern
```

## **Quick Reference**

| Need | Use | Example |
|------|-----|---------|
| Different cars | Factory | `carFactory.getCar("SUV")` |
| Different shapes | Factory | `shapeFactory.getShape("CIRCLE")` |
| Windows UI components | Abstract Factory | `windowsFactory.createButton()` |
| Database families | Abstract Factory | `mysqlFactory.createConnection()` |

## **Memory Trick** 🧠

- **Factory**: **F**actory creates **F**orms (one type)
- **Abstract Factory**: **A**bstract **F**actory creates **A**ll **F**amilies (multiple types)

**Factory** = **Single** responsibility  
**Abstract Factory** = **Multiple** responsibilities
