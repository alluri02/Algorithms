package com.example.patterns.structural.composite;

/**
 * Composite Pattern - Leaf
 * Represents a file in the file system
 */
public class File implements FileSystemComponent {
    private String name;
    private long size;

    public File(String name, long size) {
        this.name = name;
        this.size = size;
    }

    @Override
    public void showDetails() {
        System.out.println("File: " + name + " (Size: " + size + " bytes)");
    }

    @Override
    public long getSize() {
        return size;
    }

    @Override
    public String getName() {
        return name;
    }
}
