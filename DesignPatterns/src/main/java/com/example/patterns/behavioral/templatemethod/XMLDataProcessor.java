package com.example.patterns.behavioral.templatemethod;

/**
 * Template Method Pattern - Concrete Class
 * XML data processor implementation
 */
public class XMLDataProcessor extends DataProcessor {
    
    @Override
    protected void readData() {
        System.out.println("Reading data from XML file...");
        System.out.println("XML data loaded successfully");
    }
    
    @Override
    protected void processRawData() {
        System.out.println("Processing XML raw data...");
        System.out.println("Parsing XML elements and attributes");
        System.out.println("Handling XML namespaces");
    }
    
    @Override
    protected void transformData() {
        System.out.println("Transforming XML data...");
        System.out.println("Converting XML to internal data structure");
        System.out.println("Resolving XML references and includes");
    }
    
    @Override
    protected void saveData() {
        System.out.println("Saving processed XML data...");
        System.out.println("Data saved to database with XML schema validation");
    }
    
    // Override hook method - XML has built-in validation
    @Override
    protected boolean shouldValidateData() {
        return false; // XML schema validation is sufficient
    }
}
