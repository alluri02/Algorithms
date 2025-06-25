package com.example.patterns.structural.proxy;

/**
 * Real Subject for protection proxy example
 */
public class RealDocument implements Document {
    private String title;
    private String content;
    
    public RealDocument(String title) {
        this.title = title;
        this.content = "Initial content of " + title;
    }
    
    @Override
    public void read() {
        System.out.println("Reading document: " + title);
        System.out.println("Content: " + content);
    }
    
    @Override
    public void write(String content) {
        System.out.println("Writing to document: " + title);
        this.content = content;
        System.out.println("Document updated successfully");
    }
}
