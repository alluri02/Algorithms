package com.example.patterns.structural.flyweight;

import java.util.HashMap;
import java.util.Map;

/**
 * Flyweight Pattern - Flyweight Factory
 * Creates and manages flyweight instances
 */
public class TreeTypeFactory {
    private static Map<String, TreeType> treeTypes = new HashMap<>();
    
    public static TreeType getTreeType(String name, String sprite) {
        TreeType treeType = treeTypes.get(name);
        if (treeType == null) {
            System.out.println("Creating new TreeType: " + name);
            treeType = new ConcreteTreeType(name, sprite);
            treeTypes.put(name, treeType);
        } else {
            System.out.println("Reusing existing TreeType: " + name);
        }
        return treeType;
    }
    
    public static int getCreatedTreeTypesCount() {
        return treeTypes.size();
    }
    
    public static void listTreeTypes() {
        System.out.println("Created tree types:");
        for (String key : treeTypes.keySet()) {
            System.out.println("  - " + key);
        }
    }
}
