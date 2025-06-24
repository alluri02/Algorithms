package com.example.patterns.creational.builder;

/**
 * Comprehensive Builder Pattern Demo
 * Shows three different examples from simple to complex
 */
public class BuilderPatternDemo {
    
    public static void main(String[] args) {
        System.out.println("=== Builder Pattern Examples ===\n");
        
        demonstrateHouseBuilder();
        demonstratePizzaBuilder();
        demonstrateComputerBuilder();
    }
    
    /**
     * Simplest Builder example - House
     * Perfect for understanding the basic concept
     */
    private static void demonstrateHouseBuilder() {
        System.out.println("--- Simple House Builder ---");
        
        // Build a basic house
        House basicHouse = new House.HouseBuilder(3, 2)
                .build();
        System.out.println("Basic house: " + basicHouse);
        
        // Build a luxury house step by step
        House luxuryHouse = new House.HouseBuilder(5, 3)
                .withGarage()
                .withGarden()
                .withPool()
                .withRoof("tile")
                .build();
        System.out.println("Luxury house: " + luxuryHouse);
        
        // Build a custom house
        House customHouse = new House.HouseBuilder(4, 2)
                .withGarden()
                .withRoof("metal")
                .build();
        System.out.println("Custom house: " + customHouse);
        
        System.out.println();
    }
    
    /**
     * Intuitive Builder example - Pizza
     * Shows how to add optional features
     */
    private static void demonstratePizzaBuilder() {
        System.out.println("--- Pizza Builder ---");
        
        // Plain pizza
        Pizza plainPizza = new Pizza.PizzaBuilder("Medium", "thin crust")
                .build();
        System.out.println("Plain pizza: " + plainPizza);
        
        // Vegetarian pizza
        Pizza veggiePizza = new Pizza.PizzaBuilder("Large", "thick crust")
                .addCheese()
                .addMushrooms()
                .addOlives()
                .addTomatoes()
                .addOnions()
                .build();
        System.out.println("Veggie pizza: " + veggiePizza);
        
        // Meat lover's pizza
        Pizza meatPizza = new Pizza.PizzaBuilder("Large", "stuffed crust")
                .addCheese()
                .addPepperoni()
                .build();
        System.out.println("Meat pizza: " + meatPizza);
        
        System.out.println();
    }
    
    /**
     * Complex Builder example - Computer
     * Shows handling of many optional parameters
     */
    private static void demonstrateComputerBuilder() {
        System.out.println("--- Computer Builder ---");
        
        // Office computer
        Computer officeComputer = new Computer.ComputerBuilder("Intel i5", "8GB")
                .build();
        System.out.println("Office computer: " + officeComputer);
        
        // Gaming computer
        Computer gamingComputer = new Computer.ComputerBuilder("Intel i9", "32GB")
                .storage("2TB NVMe SSD")
                .graphicsCard("RTX 4090")
                .motherboard("ASUS ROG Strix")
                .powerSupply("1000W Gold")
                .hasWifi(true)
                .hasBluetooth(true)
                .build();
        System.out.println("Gaming computer: " + gamingComputer);
        
        System.out.println();
    }
}
