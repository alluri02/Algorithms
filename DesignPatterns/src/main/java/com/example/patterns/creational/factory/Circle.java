package com.example.patterns.creational.factory;

/**
 * Circle implementation of Shape
 */
public class Circle implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing a Circle");
    }
}
