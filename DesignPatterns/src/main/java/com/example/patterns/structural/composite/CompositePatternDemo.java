package com.example.patterns.structural.composite;

/**
 * Composite Pattern Demo
 * Demonstrates how to treat individual objects and compositions uniformly
 */
public class CompositePatternDemo {
    
    public static void demonstrateCompositePattern() {
        System.out.println("=== Composite Pattern Demo ===");
        
        // Create files
        File file1 = new File("document.txt", 1024);
        File file2 = new File("image.jpg", 2048);
        File file3 = new File("video.mp4", 10240);
        File file4 = new File("readme.md", 512);
        
        // Create directories
        Directory documents = new Directory("Documents");
        Directory media = new Directory("Media");
        Directory root = new Directory("Root");
        
        // Build directory structure
        documents.addComponent(file1);
        documents.addComponent(file4);
        
        media.addComponent(file2);
        media.addComponent(file3);
        
        root.addComponent(documents);
        root.addComponent(media);
        
        // Display the entire structure
        System.out.println("\n--- File System Structure ---");
        root.showDetails();
        
        // Demonstrate treating leaf and composite uniformly
        System.out.println("\n--- Individual Component Details ---");
        System.out.println("Single file:");
        file1.showDetails();
        
        System.out.println("\nSingle directory:");
        documents.showDetails();
        
        System.out.println("\nComposite Pattern allows us to treat individual files and directories uniformly!");
    }
    
    public static void main(String[] args) {
        demonstrateCompositePattern();
    }
}
