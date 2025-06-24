package com.example.patterns.creational.factory;

/**
 * Factory Pattern Implementation
 * Creates objects without specifying the exact class to create
 */
public class ShapeFactory {
    
    /**
     * Factory method to create Shape objects based on the given type
     * @param shapeType the type of shape to create
     * @return Shape object or null if type is not recognized
     */
    public Shape getShape(String shapeType) {
        if (shapeType == null) {
            return null;
        }
        
        switch (shapeType.toUpperCase()) {
            case "CIRCLE":
                return new Circle();
            case "RECTANGLE":
                return new Rectangle();
            case "SQUARE":
                return new Square();
            default:
                System.out.println("Unknown shape type: " + shapeType);
                return null;
        }
    }
}
