package com.example.patterns.creational.builder;

/**
 * House class demonstrating the simplest possible Builder Pattern
 * Perfect for beginners to understand the concept
 */
public class House {
    // Basic house properties
    private final int rooms;
    private final int bathrooms;
    private final boolean hasGarage;
    private final boolean hasGarden;
    private final boolean hasPool;
    private final String roofType;
    
    // Private constructor
    private House(HouseBuilder builder) {
        this.rooms = builder.rooms;
        this.bathrooms = builder.bathrooms;
        this.hasGarage = builder.hasGarage;
        this.hasGarden = builder.hasGarden;
        this.hasPool = builder.hasPool;
        this.roofType = builder.roofType;
    }
    
    // Simple getters
    public int getRooms() { return rooms; }
    public int getBathrooms() { return bathrooms; }
    public boolean hasGarage() { return hasGarage; }
    public boolean hasGarden() { return hasGarden; }
    public boolean hasPool() { return hasPool; }
    public String getRoofType() { return roofType; }
    
    @Override
    public String toString() {
        StringBuilder description = new StringBuilder();
        description.append("House with ").append(rooms).append(" rooms and ").append(bathrooms).append(" bathrooms");
        
        if (hasGarage) description.append(", garage");
        if (hasGarden) description.append(", garden");
        if (hasPool) description.append(", pool");
        description.append(", ").append(roofType).append(" roof");
        
        return description.toString();
    }
    
    /**
     * Super simple House Builder
     * Easy to read and understand
     */
    public static class HouseBuilder {
        // Required basic info
        private int rooms;
        private int bathrooms;
        
        // Optional features - start with defaults
        private boolean hasGarage = false;
        private boolean hasGarden = false;
        private boolean hasPool = false;
        private String roofType = "flat";
        
        // Constructor with required info only
        public HouseBuilder(int rooms, int bathrooms) {
            this.rooms = rooms;
            this.bathrooms = bathrooms;
        }
        
        // Add garage
        public HouseBuilder withGarage() {
            this.hasGarage = true;
            return this;
        }
        
        // Add garden
        public HouseBuilder withGarden() {
            this.hasGarden = true;
            return this;
        }
        
        // Add pool
        public HouseBuilder withPool() {
            this.hasPool = true;
            return this;
        }
        
        // Set roof type
        public HouseBuilder withRoof(String roofType) {
            this.roofType = roofType;
            return this;
        }
        
        // Build the house
        public House build() {
            return new House(this);
        }
    }
}
