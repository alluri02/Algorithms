package com.example.patterns.structural.proxy;

/**
 * Protection Proxy - controls access based on user permissions
 */
public class DocumentProxy implements Document {
    private RealDocument realDocument;
    private String title;
    private String userRole;
    
    public DocumentProxy(String title, String userRole) {
        this.title = title;
        this.userRole = userRole;
    }
    
    @Override
    public void read() {
        // Anyone can read
        System.out.println("Proxy: Checking read permissions for " + userRole);
        if (realDocument == null) {
            realDocument = new RealDocument(title);
        }
        realDocument.read();
    }
    
    @Override
    public void write(String content) {
        System.out.println("Proxy: Checking write permissions for " + userRole);
        if (!"admin".equals(userRole) && !"editor".equals(userRole)) {
            System.out.println("Access denied: " + userRole + " cannot write to document");
            return;
        }
        
        if (realDocument == null) {
            realDocument = new RealDocument(title);
        }
        realDocument.write(content);
    }
}
