package com.example.patterns.creational.builder;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for House Builder Pattern
 */
public class HouseTest {
    
    @Test
    public void testBasicHouse() {
        House house = new House.HouseBuilder(3, 2)
                .build();
        
        assertEquals(3, house.getRooms());
        assertEquals(2, house.getBathrooms());
        assertFalse(house.hasGarage());
        assertFalse(house.hasGarden());
        assertFalse(house.hasPool());
        assertEquals("flat", house.getRoofType()); // Default
    }
    
    @Test
    public void testLuxuryHouse() {
        House house = new House.HouseBuilder(5, 3)
                .withGarage()
                .withGarden()
                .withPool()
                .withRoof("tile")
                .build();
        
        assertEquals(5, house.getRooms());
        assertEquals(3, house.getBathrooms());
        assertTrue(house.hasGarage());
        assertTrue(house.hasGarden());
        assertTrue(house.hasPool());
        assertEquals("tile", house.getRoofType());
    }
    
    @Test
    public void testPartialFeatures() {
        House house = new House.HouseBuilder(4, 2)
                .withGarden()
                .withRoof("metal")
                .build();
        
        assertEquals(4, house.getRooms());
        assertEquals(2, house.getBathrooms());
        assertFalse(house.hasGarage());
        assertTrue(house.hasGarden());
        assertFalse(house.hasPool());
        assertEquals("metal", house.getRoofType());
    }
    
    @Test
    public void testHouseToString() {
        House house = new House.HouseBuilder(3, 2)
                .withGarage()
                .withRoof("tile")
                .build();
        
        String description = house.toString();
        assertTrue(description.contains("3 rooms"));
        assertTrue(description.contains("2 bathrooms"));
        assertTrue(description.contains("garage"));
        assertTrue(description.contains("tile roof"));
    }
}
