package com.example.patterns.creational.prototype;

/**
 * Prototype Pattern - Create objects by cloning existing instances
 * 
 * Useful when creating objects is expensive (database queries, network calls)
 */

// Prototype interface
interface Cloneable {
    Object clone();
}

// Abstract prototype
abstract class Shape implements Cloneable {
    protected String color;
    protected int x, y;
    
    public Shape() {}
    
    public Shape(Shape target) {
        if (target != null) {
            this.color = target.color;
            this.x = target.x;
            this.y = target.y;
        }
    }
    
    public abstract Shape clone();
    public abstract void draw();
    
    // Getters and setters
    public String getColor() { return color; }
    public void setColor(String color) { this.color = color; }
    public int getX() { return x; }
    public void setX(int x) { this.x = x; }
    public int getY() { return y; }
    public void setY(int y) { this.y = y; }
}

// Concrete prototypes
class Circle extends Shape {
    private int radius;
    
    public Circle() {}
    
    public Circle(Circle target) {
        super(target);
        if (target != null) {
            this.radius = target.radius;
        }
    }
    
    @Override
    public Shape clone() {
        return new Circle(this);
    }
    
    @Override
    public void draw() {
        System.out.println("Drawing Circle: color=" + color + 
                          ", position=(" + x + "," + y + "), radius=" + radius);
    }
    
    public int getRadius() { return radius; }
    public void setRadius(int radius) { this.radius = radius; }
}

class Rectangle extends Shape {
    private int width, height;
    
    public Rectangle() {}
    
    public Rectangle(Rectangle target) {
        super(target);
        if (target != null) {
            this.width = target.width;
            this.height = target.height;
        }
    }
    
    @Override
    public Shape clone() {
        return new Rectangle(this);
    }
    
    @Override
    public void draw() {
        System.out.println("Drawing Rectangle: color=" + color + 
                          ", position=(" + x + "," + y + "), size=" + width + "x" + height);
    }
    
    public int getWidth() { return width; }
    public void setWidth(int width) { this.width = width; }
    public int getHeight() { return height; }
    public void setHeight(int height) { this.height = height; }
}

// Prototype registry/cache
class ShapeCache {
    private java.util.Map<String, Shape> cache = new java.util.HashMap<>();
    
    public ShapeCache() {
        loadCache();
    }
    
    public Shape getShape(String shapeId) {
        Shape cachedShape = cache.get(shapeId);
        return (Shape) cachedShape.clone();
    }
    
    // Load initial prototypes
    private void loadCache() {
        Circle circle = new Circle();
        circle.setColor("Red");
        circle.setX(10);
        circle.setY(20);
        circle.setRadius(15);
        cache.put("circle", circle);
        
        Rectangle rectangle = new Rectangle();
        rectangle.setColor("Blue");
        rectangle.setX(30);
        rectangle.setY(40);
        rectangle.setWidth(50);
        rectangle.setHeight(25);
        cache.put("rectangle", rectangle);
    }
}

// Demo class
public class PrototypeDemo {
    public static void main(String[] args) {
        ShapeCache cache = new ShapeCache();
        
        System.out.println("=== Prototype Pattern Demo ===");
        
        // Clone shapes from cache
        Shape clonedCircle1 = cache.getShape("circle");
        Shape clonedCircle2 = cache.getShape("circle");
        Shape clonedRectangle = cache.getShape("rectangle");
        
        // Modify cloned objects
        clonedCircle2.setColor("Green");
        clonedCircle2.setX(100);
        
        // Draw all shapes
        System.out.println("Original prototypes:");
        clonedCircle1.draw();
        clonedRectangle.draw();
        
        System.out.println("\nModified clones:");
        clonedCircle2.draw();
        
        System.out.println("\nObjects are different instances: " + 
                          (clonedCircle1 != clonedCircle2));
    }
}
