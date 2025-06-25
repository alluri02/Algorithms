package com.example.patterns.structural.flyweight;

import java.util.ArrayList;
import java.util.List;

/**
 * Flyweight Pattern - Client
 * Forest that manages many trees efficiently using flyweights
 */
public class Forest {
    private List<Tree> trees = new ArrayList<>();
    
    public void plantTree(int x, int y, String name, String color, String size, String sprite) {
        TreeType treeType = TreeTypeFactory.getTreeType(name, sprite);
        Tree tree = new Tree(x, y, color, size, treeType);
        trees.add(tree);
    }
    
    public void render() {
        System.out.println("=== Rendering Forest ===");
        for (Tree tree : trees) {
            tree.render();
        }
        System.out.println("Total trees: " + trees.size());
        System.out.println("Total tree types (flyweights): " + TreeTypeFactory.getCreatedTreeTypesCount());
    }
    
    public int getTreeCount() {
        return trees.size();
    }
}
