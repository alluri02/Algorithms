package com.example.patterns.creational.abstractfactory;

/**
 * Abstract Factory Pattern - Creates families of related objects
 * 
 * This example creates different UI components for different operating systems
 */

// Abstract products
interface Button {
    void render();
    void click();
}

interface Checkbox {
    void render();
    void toggle();
}

// Windows implementations
class WindowsButton implements Button {
    @Override
    public void render() {
        System.out.println("Rendering Windows-style button");
    }
    
    @Override
    public void click() {
        System.out.println("Windows button clicked!");
    }
}

class WindowsCheckbox implements Checkbox {
    @Override
    public void render() {
        System.out.println("Rendering Windows-style checkbox");
    }
    
    @Override
    public void toggle() {
        System.out.println("Windows checkbox toggled!");
    }
}

// Mac implementations
class MacButton implements Button {
    @Override
    public void render() {
        System.out.println("Rendering Mac-style button");
    }
    
    @Override
    public void click() {
        System.out.println("Mac button clicked!");
    }
}

class MacCheckbox implements Checkbox {
    @Override
    public void render() {
        System.out.println("Rendering Mac-style checkbox");
    }
    
    @Override
    public void toggle() {
        System.out.println("Mac checkbox toggled!");
    }
}

// Abstract Factory
interface UIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

// Concrete Factories
class WindowsFactory implements UIFactory {
    @Override
    public Button createButton() {
        return new WindowsButton();
    }
    
    @Override
    public Checkbox createCheckbox() {
        return new WindowsCheckbox();
    }
}

class MacFactory implements UIFactory {
    @Override
    public Button createButton() {
        return new MacButton();
    }
    
    @Override
    public Checkbox createCheckbox() {
        return new MacCheckbox();
    }
}

// Client code
public class Application {
    private UIFactory factory;
    private Button button;
    private Checkbox checkbox;
    
    public Application(UIFactory factory) {
        this.factory = factory;
    }
    
    public void createUI() {
        button = factory.createButton();
        checkbox = factory.createCheckbox();
    }
    
    public void render() {
        button.render();
        checkbox.render();
    }
    
    public void interact() {
        button.click();
        checkbox.toggle();
    }
    
    // Factory method to get appropriate factory
    public static UIFactory getFactory(String osType) {
        if (osType.equalsIgnoreCase("Windows")) {
            return new WindowsFactory();
        } else if (osType.equalsIgnoreCase("Mac")) {
            return new MacFactory();
        }
        throw new IllegalArgumentException("Unknown OS type: " + osType);
    }
}
