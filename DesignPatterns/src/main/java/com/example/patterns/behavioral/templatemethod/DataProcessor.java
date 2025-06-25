package com.example.patterns.behavioral.templatemethod;

/**
 * Template Method Pattern - Abstract Class
 * Defines the skeleton of data processing algorithm
 */
public abstract class DataProcessor {
    
    // Template method - defines the algorithm structure
    public final void processData() {
        System.out.println("=== Data Processing Started ===");
        
        readData();
        processRawData();
        
        if (shouldValidateData()) {
            validateData();
        }
        
        transformData();
        saveData();
        
        System.out.println("=== Data Processing Completed ===\n");
    }
    
    // Abstract methods - must be implemented by subclasses
    protected abstract void readData();
    protected abstract void processRawData();
    protected abstract void transformData();
    protected abstract void saveData();
    
    // Hook method - subclasses can override if needed
    protected boolean shouldValidateData() {
        return true; // Default behavior
    }
    
    // Concrete method with default implementation
    protected void validateData() {
        System.out.println("Validating data integrity...");
        System.out.println("Data validation passed");
    }
}
