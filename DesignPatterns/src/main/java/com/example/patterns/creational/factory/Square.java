package com.example.patterns.creational.factory;

/**
 * Square implementation of Shape
 */
public class Square implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing a Square");
    }
}
