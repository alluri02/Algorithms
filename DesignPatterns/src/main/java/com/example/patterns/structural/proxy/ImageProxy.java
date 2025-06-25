package com.example.patterns.structural.proxy;

/**
 * Proxy Pattern - Proxy
 * Controls access to the real subject and provides lazy loading
 */
public class ImageProxy implements Image {
    private String fileName;
    private RealImage realImage;
    
    public ImageProxy(String fileName) {
        this.fileName = fileName;
    }
    
    @Override
    public void display() {
        // Lazy loading - create real image only when needed
        if (realImage == null) {
            System.out.println("Proxy: First access - creating real image");
            realImage = new RealImage(fileName);
        } else {
            System.out.println("Proxy: Using cached image");
        }
        realImage.display();
    }
    
    @Override
    public String getFileName() {
        return fileName;
    }
    
    public boolean isLoaded() {
        return realImage != null;
    }
}
