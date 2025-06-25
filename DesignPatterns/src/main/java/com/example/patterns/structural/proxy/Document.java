package com.example.patterns.structural.proxy;

/**
 * Another example - Protection Proxy
 * Controls access based on user permissions
 */
public interface Document {
    void read();
    void write(String content);
}
