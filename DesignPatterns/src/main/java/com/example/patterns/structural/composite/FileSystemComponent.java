package com.example.patterns.structural.composite;

/**
 * Composite Pattern - Component interface
 * Defines operations for both leaf and composite objects
 */
public interface FileSystemComponent {
    void showDetails();
    long getSize();
    String getName();
}
