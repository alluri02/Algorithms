package com.example.patterns.structural.flyweight;

/**
 * Flyweight Pattern - Context
 * Stores extrinsic state and maintains a reference to flyweight
 */
public class Tree {
    private int x, y;
    private String color;
    private String size;
    private TreeType treeType; // Reference to flyweight
    
    public Tree(int x, int y, String color, String size, TreeType treeType) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.size = size;
        this.treeType = treeType;
    }
    
    public void render() {
        treeType.render(x, y, color, size);
    }
    
    // Getters
    public int getX() { return x; }
    public int getY() { return y; }
    public String getColor() { return color; }
    public String getSize() { return size; }
}
