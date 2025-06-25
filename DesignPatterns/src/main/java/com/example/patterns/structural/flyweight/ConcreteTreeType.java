package com.example.patterns.structural.flyweight;

/**
 * Flyweight Pattern - Concrete Flyweight
 * Implements the flyweight interface and stores intrinsic state
 */
public class ConcreteTreeType implements TreeType {
    private String name;
    private String sprite; // Intrinsic state - shared among all trees of this type
    
    public ConcreteTreeType(String name, String sprite) {
        this.name = name;
        this.sprite = sprite;
    }
    
    @Override
    public void render(int x, int y, String color, String size) {
        // Use extrinsic state (x, y, color, size) passed as parameters
        System.out.println("Rendering " + name + " tree:");
        System.out.println("  Position: (" + x + ", " + y + ")");
        System.out.println("  Color: " + color);
        System.out.println("  Size: " + size);
        System.out.println("  Sprite: " + sprite);
        System.out.println();
    }
    
    public String getName() {
        return name;
    }
}
