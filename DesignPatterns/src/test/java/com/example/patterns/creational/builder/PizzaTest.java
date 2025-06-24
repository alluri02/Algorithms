package com.example.patterns.creational.builder;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Pizza Builder Pattern
 */
public class PizzaTest {
    
    @Test
    public void testPlainPizza() {
        Pizza pizza = new Pizza.PizzaBuilder("Medium", "thin crust")
                .build();
        
        assertEquals("Medium", pizza.getSize());
        assertEquals("thin crust", pizza.getCrust());
        assertFalse(pizza.hasCheese());
        assertFalse(pizza.hasPepperoni());
        assertFalse(pizza.hasMushrooms());
    }
    
    @Test
    public void testPizzaWithToppings() {
        Pizza pizza = new Pizza.PizzaBuilder("Large", "thick crust")
                .addCheese()
                .addPepperoni()
                .addMushrooms()
                .build();
        
        assertEquals("Large", pizza.getSize());
        assertEquals("thick crust", pizza.getCrust());
        assertTrue(pizza.hasCheese());
        assertTrue(pizza.hasPepperoni());
        assertTrue(pizza.hasMushrooms());
        assertFalse(pizza.hasOlives());
    }
    
    @Test
    public void testVeggiePizza() {
        Pizza pizza = new Pizza.PizzaBuilder("Small", "thin crust")
                .addCheese()
                .addMushrooms()
                .addOlives()
                .addTomatoes()
                .addOnions()
                .build();
        
        assertTrue(pizza.hasCheese());
        assertTrue(pizza.hasMushrooms());
        assertTrue(pizza.hasOlives());
        assertTrue(pizza.hasTomatoes());
        assertTrue(pizza.hasOnions());
        assertFalse(pizza.hasPepperoni()); // No meat
    }
    
    @Test
    public void testPizzaToString() {
        Pizza pizza = new Pizza.PizzaBuilder("Medium", "stuffed crust")
                .addCheese()
                .addPepperoni()
                .build();
        
        String description = pizza.toString();
        assertTrue(description.contains("Medium"));
        assertTrue(description.contains("stuffed crust"));
        assertTrue(description.contains("cheese"));
        assertTrue(description.contains("pepperoni"));
    }
}
