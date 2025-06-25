package com.example.patterns.structural.decorator;

/**
 * Decorator Pattern Demo
 * Demonstrates how to add behavior to objects dynamically
 */
public class DecoratorPatternDemo {
    
    public static void demonstrateDecoratorPattern() {
        System.out.println("=== Decorator Pattern Demo ===");
        
        // Start with simple coffee
        Coffee coffee = new SimpleCoffee();
        System.out.println("Basic order: " + coffee.getDescription() + " - $" + coffee.getCost());
        
        // Add milk
        coffee = new MilkDecorator(coffee);
        System.out.println("With milk: " + coffee.getDescription() + " - $" + coffee.getCost());
        
        // Add sugar
        coffee = new SugarDecorator(coffee);
        System.out.println("With sugar: " + coffee.getDescription() + " - $" + coffee.getCost());
        
        // Add vanilla
        coffee = new VanillaDecorator(coffee);
        System.out.println("With vanilla: " + coffee.getDescription() + " - $" + coffee.getCost());
        
        System.out.println("\n--- Different Combinations ---");
        
        // Different combination
        Coffee specialCoffee = new VanillaDecorator(
            new MilkDecorator(
                new SimpleCoffee()
            )
        );
        System.out.println("Special combo: " + specialCoffee.getDescription() + " - $" + specialCoffee.getCost());
        
        // Triple milk (showing multiple decorators of same type)
        Coffee extraMilky = new MilkDecorator(
            new MilkDecorator(
                new MilkDecorator(
                    new SimpleCoffee()
                )
            )
        );
        System.out.println("Triple milk: " + extraMilky.getDescription() + " - $" + extraMilky.getCost());
        
        System.out.println("\nDecorator Pattern allows us to add features dynamically without changing the original object!");
    }
    
    public static void main(String[] args) {
        demonstrateDecoratorPattern();
    }
}
