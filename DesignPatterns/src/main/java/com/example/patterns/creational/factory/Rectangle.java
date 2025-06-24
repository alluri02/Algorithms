package com.example.patterns.creational.factory;

/**
 * Rectangle implementation of Shape
 */
public class Rectangle implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing a Rectangle");
    }
}
