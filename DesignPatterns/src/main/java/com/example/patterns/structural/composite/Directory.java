package com.example.patterns.structural.composite;

import java.util.ArrayList;
import java.util.List;

/**
 * Composite Pattern - Composite
 * Represents a directory that can contain files and other directories
 */
public class Directory implements FileSystemComponent {
    private String name;
    private List<FileSystemComponent> components = new ArrayList<>();

    public Directory(String name) {
        this.name = name;
    }

    public void addComponent(FileSystemComponent component) {
        components.add(component);
    }

    public void removeComponent(FileSystemComponent component) {
        components.remove(component);
    }

    @Override
    public void showDetails() {
        System.out.println("Directory: " + name + " (Total Size: " + getSize() + " bytes)");
        for (FileSystemComponent component : components) {
            System.out.print("  ");
            component.showDetails();
        }
    }

    @Override
    public long getSize() {
        long totalSize = 0;
        for (FileSystemComponent component : components) {
            totalSize += component.getSize();
        }
        return totalSize;
    }

    @Override
    public String getName() {
        return name;
    }

    public List<FileSystemComponent> getComponents() {
        return new ArrayList<>(components);
    }
}
