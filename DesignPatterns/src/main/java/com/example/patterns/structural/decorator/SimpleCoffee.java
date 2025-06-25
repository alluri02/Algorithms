package com.example.patterns.structural.decorator;

/**
 * Decorator Pattern - Concrete Component
 * Basic coffee implementation
 */
public class SimpleCoffee implements Coffee {
    
    @Override
    public String getDescription() {
        return "Simple Coffee";
    }
    
    @Override
    public double getCost() {
        return 2.00;
    }
}
