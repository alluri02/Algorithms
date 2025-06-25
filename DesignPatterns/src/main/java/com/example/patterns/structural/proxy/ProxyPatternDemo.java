package com.example.patterns.structural.proxy;

/**
 * Proxy Pattern Demo
 * Demonstrates lazy loading and protection proxy patterns
 */
public class ProxyPatternDemo {
    
    public static void demonstrateProxyPattern() {
        System.out.println("=== Proxy Pattern Demo ===");
        
        // Virtual Proxy Example (Lazy Loading)
        System.out.println("\n--- Virtual Proxy (Lazy Loading) ---");
          // Create proxies for images (no loading yet)
        Image image1 = new ImageProxy("photo1.jpg");
        Image image2 = new ImageProxy("photo2.jpg");
        
        System.out.println("Images created (not loaded yet)");
        
        // First access - loads the image
        System.out.println("\nFirst display of image1:");
        image1.display();
        
        // Second access - uses cached image
        System.out.println("\nSecond display of image1:");
        image1.display();
        
        // Display other images
        System.out.println("\nDisplaying image2:");
        image2.display();
        
        // Protection Proxy Example
        System.out.println("\n--- Protection Proxy (Access Control) ---");
        
        // Different user roles
        Document adminDoc = new DocumentProxy("confidential.txt", "admin");
        Document editorDoc = new DocumentProxy("article.txt", "editor");
        Document userDoc = new DocumentProxy("public.txt", "user");
        
        System.out.println("\nAdmin accessing document:");
        adminDoc.read();
        adminDoc.write("Admin updated content");
        
        System.out.println("\nEditor accessing document:");
        editorDoc.read();
        editorDoc.write("Editor updated content");
        
        System.out.println("\nUser accessing document:");
        userDoc.read();
        userDoc.write("User trying to update content"); // Should be denied
        
        System.out.println("\nProxy Pattern provides controlled access to objects!");
    }
    
    public static void main(String[] args) {
        demonstrateProxyPattern();
    }
}
