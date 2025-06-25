package com.example.patterns.structural.decorator;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Decorator Pattern implementation
 */
public class DecoratorPatternTest {
    
    private Coffee simpleCoffee;
    
    @BeforeEach
    void setUp() {
        simpleCoffee = new SimpleCoffee();
    }
    
    @Test
    void testSimpleCoffee() {
        assertEquals("Simple Coffee", simpleCoffee.getDescription());
        assertEquals(2.00, simpleCoffee.getCost(), 0.01);
    }
    
    @Test
    void testSingleDecorator() {
        Coffee coffeeWithMilk = new MilkDecorator(simpleCoffee);
        assertEquals("Simple Coffee, Milk", coffeeWithMilk.getDescription());
        assertEquals(2.50, coffeeWithMilk.getCost(), 0.01);
        
        Coffee coffeeWithSugar = new SugarDecorator(simpleCoffee);
        assertEquals("Simple Coffee, Sugar", coffeeWithSugar.getDescription());
        assertEquals(2.25, coffeeWithSugar.getCost(), 0.01);
        
        Coffee coffeeWithVanilla = new VanillaDecorator(simpleCoffee);
        assertEquals("Simple Coffee, Vanilla", coffeeWithVanilla.getDescription());
        assertEquals(2.75, coffeeWithVanilla.getCost(), 0.01);
    }
    
    @Test
    void testMultipleDecorators() {
        Coffee decoratedCoffee = new VanillaDecorator(
            new SugarDecorator(
                new MilkDecorator(simpleCoffee)
            )
        );
        
        assertEquals("Simple Coffee, Milk, Sugar, Vanilla", decoratedCoffee.getDescription());
        assertEquals(3.50, decoratedCoffee.getCost(), 0.01); // 2.00 + 0.50 + 0.25 + 0.75
    }
    
    @Test
    void testSameDecoratorMultipleTimes() {
        Coffee doubleMilkCoffee = new MilkDecorator(
            new MilkDecorator(simpleCoffee)
        );
        
        assertEquals("Simple Coffee, Milk, Milk", doubleMilkCoffee.getDescription());
        assertEquals(3.00, doubleMilkCoffee.getCost(), 0.01); // 2.00 + 0.50 + 0.50
    }
    
    @Test
    void testDecoratorOrder() {
        Coffee coffee1 = new SugarDecorator(new MilkDecorator(simpleCoffee));
        Coffee coffee2 = new MilkDecorator(new SugarDecorator(simpleCoffee));
        
        // Same cost regardless of order
        assertEquals(coffee1.getCost(), coffee2.getCost(), 0.01);
        
        // Different description based on order
        assertEquals("Simple Coffee, Milk, Sugar", coffee1.getDescription());
        assertEquals("Simple Coffee, Sugar, Milk", coffee2.getDescription());
    }
}
