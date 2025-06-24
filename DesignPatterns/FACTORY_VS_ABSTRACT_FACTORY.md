# Factory vs Abstract Factory Pattern - Complete Comparison

## **Key Difference in One Sentence**

- **Factory Pattern**: Creates **ONE TYPE** of object (different shapes)
- **Abstract Factory Pattern**: Creates **FAMILIES** of related objects (Windows UI family vs Mac UI family)

---

## **1. Factory Pattern (Simple Factory)**

### **Purpose**: Create objects of the same family/type
### **Creates**: Single products of different variations

```java
// Factory Pattern Example
ShapeFactory factory = new ShapeFactory();

Shape circle = factory.getShape("CIRCLE");      // Creates Circle
Shape rectangle = factory.getShape("RECTANGLE"); // Creates Rectangle  
Shape square = factory.getShape("SQUARE");       // Creates Square

// All products are SHAPES (same family)
```

### **Structure**:
```
ShapeFactory
├── creates Circle
├── creates Rectangle  
└── creates Square

(All are Shapes - SINGLE product family)
```

---

## **2. Abstract Factory Pattern**

### **Purpose**: Create families of related objects
### **Creates**: Multiple products that work together

```java
// Abstract Factory Pattern Example
UIFactory windowsFactory = Application.getFactory("Windows");
UIFactory macFactory = Application.getFactory("Mac");

// Windows Family
Button winButton = windowsFactory.createButton();     // Windows Button
Checkbox winCheckbox = windowsFactory.createCheckbox(); // Windows Checkbox

// Mac Family  
Button macButton = macFactory.createButton();         // Mac Button
Checkbox macCheckbox = macFactory.createCheckbox();   // Mac Checkbox

// Each factory creates MULTIPLE related products
```

### **Structure**:
```
WindowsFactory                    MacFactory
├── creates WindowsButton    VS   ├── creates MacButton
└── creates WindowsCheckbox       └── creates MacCheckbox

(Each factory creates a FAMILY of related products)
```

---

## **Visual Comparison**

### **Factory Pattern** 🏭
```
Input: "CIRCLE"     →  ShapeFactory  →  Output: Circle
Input: "RECTANGLE"  →  ShapeFactory  →  Output: Rectangle
Input: "SQUARE"     →  ShapeFactory  →  Output: Square

ONE factory creates ONE type of product (different shapes)
```

### **Abstract Factory Pattern** 🏢
```
WindowsFactory  →  Button + Checkbox + Textbox (Windows family)
MacFactory      →  Button + Checkbox + Textbox (Mac family)  
LinuxFactory    →  Button + Checkbox + Textbox (Linux family)

MULTIPLE factories, each creates MULTIPLE related products
```

---

## **Detailed Comparison Table**

| Aspect | Factory Pattern | Abstract Factory Pattern |
|--------|----------------|-------------------------|
| **Creates** | Single product type | Multiple product families |
| **Complexity** | Simple | More complex |
| **Products** | Circle, Rectangle, Square | Windows UI, Mac UI families |
| **Factories** | One factory | Multiple factories |
| **Use Case** | Different variations of same thing | Different platforms/environments |
| **Example** | Shape creator | UI component creator |
| **Coupling** | Low | Very low (families are isolated) |

---

## **Real-World Examples**

### **Factory Pattern Examples**:
- **Car Factory**: Creates different car models (SUV, Sedan, Hatchback)
- **Pizza Factory**: Creates different pizzas (Margherita, Pepperoni, Veggie)
- **Logger Factory**: Creates different loggers (File, Console, Database)

### **Abstract Factory Examples**:
- **UI Framework**: Windows UI vs Mac UI vs Linux UI
- **Database Factory**: MySQL family vs PostgreSQL family vs Oracle family
- **Game Engine**: 2D graphics family vs 3D graphics family

---

## **Code Comparison**

### **Factory Pattern Code**:
```java
// ONE interface, ONE factory
interface Shape { void draw(); }

class ShapeFactory {
    public Shape getShape(String type) {
        switch(type) {
            case "CIRCLE": return new Circle();
            case "RECTANGLE": return new Rectangle();
            // Creates different SHAPES
        }
    }
}

// Usage
Shape circle = factory.getShape("CIRCLE");
```

### **Abstract Factory Pattern Code**:
```java
// MULTIPLE interfaces for MULTIPLE products
interface Button { void render(); }
interface Checkbox { void render(); }

// MULTIPLE factories for MULTIPLE families
interface UIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

class WindowsFactory implements UIFactory {
    public Button createButton() { return new WindowsButton(); }
    public Checkbox createCheckbox() { return new WindowsCheckbox(); }
}

class MacFactory implements UIFactory {
    public Button createButton() { return new MacButton(); }
    public Checkbox createCheckbox() { return new MacCheckbox(); }
}

// Usage
UIFactory factory = new WindowsFactory();
Button button = factory.createButton();       // Windows style
Checkbox checkbox = factory.createCheckbox(); // Windows style
```

---

## **When to Use Which?**

### **Use Factory Pattern When**:
✅ You need to create different variations of the **same type**  
✅ You want to centralize object creation logic  
✅ You don't know the exact type until runtime  
✅ Simple object creation

**Example**: Creating different shapes, different car types, different loggers

### **Use Abstract Factory Pattern When**:
✅ You need to create **families of related objects**  
✅ You want to ensure objects in a family work together  
✅ You support multiple platforms/environments  
✅ Complex object creation with dependencies

**Example**: Cross-platform UI, different database drivers, different rendering engines

---

## **Common Mistakes**

### **❌ Wrong: Using Abstract Factory for single products**
```java
// Don't use Abstract Factory just to create shapes
ShapeFactory factory = new CircleFactory(); // Overkill!
Shape circle = factory.createShape();
```

### **❌ Wrong: Using Factory for families**
```java
// Factory can't guarantee UI consistency
Button button = shapeFactory.getShape("WINDOWS_BUTTON"); // Wrong!
Checkbox checkbox = shapeFactory.getShape("MAC_CHECKBOX"); // Inconsistent!
```

### **✅ Correct Usage**:
```java
// Factory for single product type
Shape circle = shapeFactory.getShape("CIRCLE");

// Abstract Factory for product families  
UIFactory windowsFactory = new WindowsFactory();
Button button = windowsFactory.createButton();     // Consistent
Checkbox checkbox = windowsFactory.createCheckbox(); // family
```

---

## **Evolution from Factory to Abstract Factory**

### **Step 1: Simple Factory**
```java
class ShapeFactory {
    Shape getShape(String type) { /* creates shapes */ }
}
```

### **Step 2: Factory Method**
```java
abstract class ShapeFactory {
    abstract Shape createShape();
}
class CircleFactory extends ShapeFactory { /* creates circles */ }
```

### **Step 3: Abstract Factory**
```java
interface UIFactory {
    Button createButton();
    Checkbox createCheckbox();
    // Creates FAMILY of related objects
}
```

---

## **Memory Aids**

### **Factory Pattern** 🏭
- **"One factory, many products of SAME TYPE"**
- Think: Car factory making different car models
- Simple: Input → Factory → Single Product

### **Abstract Factory Pattern** 🏢  
- **"Many factories, each making FAMILIES of products"**
- Think: Different OS making their own UI families
- Complex: Platform → Factory → Family of Products

---

## **Testing the Examples**

Run these to see the difference:

```bash
# Factory Pattern (single products)
java -cp target/classes com.example.patterns.Main
# Look at "Factory Pattern" section

# Abstract Factory Pattern (product families)  
java -cp target/classes com.example.patterns.Main
# Look at "Abstract Factory Pattern" section
```

---

## **Summary**

| | Factory | Abstract Factory |
|---|---------|------------------|
| **What** | Creates objects | Creates object families |
| **How many** | One product type | Multiple product types |
| **Complexity** | Simple | Complex |
| **Goal** | Centralize creation | Ensure family consistency |
| **Use when** | Different variations | Different platforms |

**Remember**: Factory creates **one thing in different ways**, Abstract Factory creates **many related things together**! 🎯
