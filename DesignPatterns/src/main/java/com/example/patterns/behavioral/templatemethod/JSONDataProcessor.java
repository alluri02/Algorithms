package com.example.patterns.behavioral.templatemethod;

/**
 * Template Method Pattern - Concrete Class
 * JSON data processor implementation
 */
public class JSONDataProcessor extends DataProcessor {
    
    @Override
    protected void readData() {
        System.out.println("Reading data from JSON file...");
        System.out.println("JSON data loaded successfully");
    }
    
    @Override
    protected void processRawData() {
        System.out.println("Processing JSON raw data...");
        System.out.println("Parsing JSON objects and arrays");
        System.out.println("Handling nested JSON structures");
    }
    
    @Override
    protected void transformData() {
        System.out.println("Transforming JSON data...");
        System.out.println("Converting JSON to internal data structure");
        System.out.println("Flattening nested JSON objects");
    }
    
    @Override
    protected void saveData() {
        System.out.println("Saving processed JSON data...");
        System.out.println("Data saved to database with JSON schema information");
    }
    
    // Override hook method
    @Override
    protected boolean shouldValidateData() {
        return true; // JSON always needs validation
    }
    
    // Override validation for JSON-specific checks
    @Override
    protected void validateData() {
        System.out.println("Performing JSON-specific validation...");
        System.out.println("Checking JSON schema compliance");
        System.out.println("Validating required JSON fields");
        System.out.println("JSON validation passed");
    }
}
