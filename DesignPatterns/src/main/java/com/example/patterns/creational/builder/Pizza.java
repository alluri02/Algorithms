package com.example.patterns.creational.builder;

/**
 * Pizza class demonstrating a simple and intuitive Builder Pattern
 * This example is easier to understand than the Computer example
 */
public class Pizza {
    // Pizza properties
    private final String size;
    private final String crust;
    private final boolean hasCheese;
    private final boolean hasPepperoni;
    private final boolean hasMushrooms;
    private final boolean hasOlives;
    private final boolean hasTomatoes;
    private final boolean hasOnions;
    
    // Private constructor - only Builder can create Pizza
    private Pizza(PizzaBuilder builder) {
        this.size = builder.size;
        this.crust = builder.crust;
        this.hasCheese = builder.hasCheese;
        this.hasPepperoni = builder.hasPepperoni;
        this.hasMushrooms = builder.hasMushrooms;
        this.hasOlives = builder.hasOlives;
        this.hasTomatoes = builder.hasTomatoes;
        this.hasOnions = builder.hasOnions;
    }
    
    // Getters
    public String getSize() { return size; }
    public String getCrust() { return crust; }
    public boolean hasCheese() { return hasCheese; }
    public boolean hasPepperoni() { return hasPepperoni; }
    public boolean hasMushrooms() { return hasMushrooms; }
    public boolean hasOlives() { return hasOlives; }
    public boolean hasTomatoes() { return hasTomatoes; }
    public boolean hasOnions() { return hasOnions; }
    
    @Override
    public String toString() {
        StringBuilder description = new StringBuilder();
        description.append(size).append(" ").append(crust).append(" pizza");
        
        if (hasCheese || hasPepperoni || hasMushrooms || hasOlives || hasTomatoes || hasOnions) {
            description.append(" with:");
            if (hasCheese) description.append(" cheese");
            if (hasPepperoni) description.append(" pepperoni");
            if (hasMushrooms) description.append(" mushrooms");
            if (hasOlives) description.append(" olives");
            if (hasTomatoes) description.append(" tomatoes");
            if (hasOnions) description.append(" onions");
        }
        
        return description.toString();
    }
    
    /**
     * Simple and intuitive Pizza Builder
     * Each method clearly states what it does
     */
    public static class PizzaBuilder {
        // Required fields
        private String size;
        private String crust;
        
        // Optional toppings - default to false
        private boolean hasCheese = false;
        private boolean hasPepperoni = false;
        private boolean hasMushrooms = false;
        private boolean hasOlives = false;
        private boolean hasTomatoes = false;
        private boolean hasOnions = false;
        
        // Start building with size and crust (required)
        public PizzaBuilder(String size, String crust) {
            this.size = size;
            this.crust = crust;
        }
        
        // Simple methods to add toppings
        public PizzaBuilder addCheese() {
            this.hasCheese = true;
            return this;
        }
        
        public PizzaBuilder addPepperoni() {
            this.hasPepperoni = true;
            return this;
        }
        
        public PizzaBuilder addMushrooms() {
            this.hasMushrooms = true;
            return this;
        }
        
        public PizzaBuilder addOlives() {
            this.hasOlives = true;
            return this;
        }
        
        public PizzaBuilder addTomatoes() {
            this.hasTomatoes = true;
            return this;
        }
        
        public PizzaBuilder addOnions() {
            this.hasOnions = true;
            return this;
        }
        
        // Build the final pizza
        public Pizza build() {
            return new Pizza(this);
        }
    }
}
