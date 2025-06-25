package com.example.patterns.behavioral.templatemethod;

/**
 * Template Method Pattern Demo
 * Demonstrates how template method defines algorithm structure while allowing customization
 */
public class TemplateMethodPatternDemo {
    
    public static void demonstrateTemplateMethodPattern() {
        System.out.println("=== Template Method Pattern Demo ===");
        
        System.out.println("\n--- Processing CSV Data ---");
        DataProcessor csvProcessor = new CSVDataProcessor();
        csvProcessor.processData();
        
        System.out.println("--- Processing JSON Data ---");
        DataProcessor jsonProcessor = new JSONDataProcessor();
        jsonProcessor.processData();
        
        System.out.println("--- Processing XML Data ---");
        DataProcessor xmlProcessor = new XMLDataProcessor();
        xmlProcessor.processData();
        
        // Demonstrate that we can't override the template method
        System.out.println("--- Template Method Benefits ---");
        System.out.println("✓ Algorithm structure is fixed and cannot be changed");
        System.out.println("✓ Each processor implements specific steps differently");
        System.out.println("✓ Hook methods allow optional customization");
        System.out.println("✓ Common functionality is reused (validation)");
        
        System.out.println("\nTemplate Method Pattern defines algorithm skeleton while letting subclasses customize specific steps!");
    }
    
    public static void main(String[] args) {
        demonstrateTemplateMethodPattern();
    }
}
