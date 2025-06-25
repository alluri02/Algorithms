package com.example.patterns.structural.proxy;

/**
 * Proxy Pattern - Subject interface
 * Common interface for RealSubject and Proxy
 */
public interface Image {
    void display();
    String getFileName();
}
