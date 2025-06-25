package com.example.patterns.structural.decorator;

/**
 * Decorator Pattern - Concrete Decorator
 * Adds milk to coffee
 */
public class MilkDecorator extends CoffeeDecorator {
    
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + ", Milk";
    }
    
    @Override
    public double getCost() {
        return coffee.getCost() + 0.50;
    }
}
