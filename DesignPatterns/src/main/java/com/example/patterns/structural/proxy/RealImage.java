package com.example.patterns.structural.proxy;

/**
 * Proxy Pattern - Real Subject
 * The actual object that performs the expensive operations
 */
public class RealImage implements Image {
    private String fileName;
    
    public RealImage(String fileName) {
        this.fileName = fileName;
        loadFromDisk();
    }
    
    private void loadFromDisk() {
        System.out.println("Loading image from disk: " + fileName);
        // Simulate expensive loading operation
        try {
            Thread.sleep(1000); // Simulate loading delay
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("Image loaded successfully: " + fileName);
    }
    
    @Override
    public void display() {
        System.out.println("Displaying image: " + fileName);
    }
    
    @Override
    public String getFileName() {
        return fileName;
    }
}
