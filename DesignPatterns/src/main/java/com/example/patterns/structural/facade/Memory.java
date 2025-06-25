package com.example.patterns.structural.facade;

/**
 * Facade Pattern - Subsystem class
 * Memory operations
 */
public class Memory {
    
    public void load(long position, byte[] data) {
        System.out.println("Memory: Loading data at position " + position);
    }
    
    public void clear() {
        System.out.println("Memory: Clearing memory");
    }
}
