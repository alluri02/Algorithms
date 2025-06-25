package com.example.patterns.structural.flyweight;

/**
 * Flyweight Pattern Demo
 * Demonstrates how to minimize memory usage by sharing common data
 */
public class FlyweightPatternDemo {
    
    public static void demonstrateFlyweightPattern() {
        System.out.println("=== Flyweight Pattern Demo ===");
        
        Forest forest = new Forest();
        
        // Plant many trees of different types
        System.out.println("\n--- Planting Trees ---");
        
        // Oak trees
        forest.plantTree(10, 20, "Oak", "Green", "Large", "oak_sprite.png");
        forest.plantTree(30, 40, "Oak", "Dark Green", "Medium", "oak_sprite.png");
        forest.plantTree(50, 60, "Oak", "Light Green", "Large", "oak_sprite.png");
        
        // Pine trees
        forest.plantTree(15, 25, "Pine", "Dark Green", "Tall", "pine_sprite.png");
        forest.plantTree(35, 45, "Pine", "Green", "Medium", "pine_sprite.png");
        
        // Birch trees
        forest.plantTree(20, 30, "Birch", "Yellow", "Small", "birch_sprite.png");
        forest.plantTree(40, 50, "Birch", "Light Yellow", "Medium", "birch_sprite.png");
        
        // More Oak trees (should reuse existing flyweight)
        forest.plantTree(70, 80, "Oak", "Autumn Orange", "Large", "oak_sprite.png");
        forest.plantTree(90, 100, "Oak", "Brown", "Small", "oak_sprite.png");
        
        System.out.println("\n--- Forest Status ---");
        TreeTypeFactory.listTreeTypes();
        
        // Render the forest
        System.out.println();
        forest.render();
        
        System.out.println("\n--- Memory Efficiency ---");
        System.out.println("We created " + forest.getTreeCount() + " trees but only " + 
                          TreeTypeFactory.getCreatedTreeTypesCount() + " flyweight objects!");
        System.out.println("Flyweight Pattern saves memory by sharing intrinsic state between objects!");
    }
    
    public static void main(String[] args) {
        demonstrateFlyweightPattern();
    }
}
