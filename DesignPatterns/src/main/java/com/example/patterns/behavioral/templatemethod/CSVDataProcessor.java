package com.example.patterns.behavioral.templatemethod;

/**
 * Template Method Pattern - Concrete Class
 * CSV data processor implementation
 */
public class CSVDataProcessor extends DataProcessor {
    
    @Override
    protected void readData() {
        System.out.println("Reading data from CSV file...");
        System.out.println("CSV data loaded successfully");
    }
    
    @Override
    protected void processRawData() {
        System.out.println("Processing CSV raw data...");
        System.out.println("Parsing CSV columns and rows");
        System.out.println("Handling CSV-specific formatting");
    }
    
    @Override
    protected void transformData() {
        System.out.println("Transforming CSV data...");
        System.out.println("Converting CSV to internal data structure");
        System.out.println("Applying CSV-specific transformations");
    }
    
    @Override
    protected void saveData() {
        System.out.println("Saving processed CSV data...");
        System.out.println("Data saved to database with CSV metadata");
    }
}
