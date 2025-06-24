package com.example.patterns.creational.builder;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Computer Builder Pattern
 */
public class ComputerTest {
    
    @Test
    public void testBasicComputerCreation() {
        Computer computer = new Computer.ComputerBuilder("Intel i5", "16GB")
                .build();
        
        assertEquals("Intel i5", computer.getCpu());
        assertEquals("16GB", computer.getRam());
        assertEquals("500GB HDD", computer.getStorage()); // Default value
        assertEquals("Integrated", computer.getGraphicsCard()); // Default value
        assertFalse(computer.hasWifi()); // Default value
        assertFalse(computer.hasBluetooth()); // Default value
    }
    
    @Test
    public void testFullComputerCreation() {
        Computer computer = new Computer.ComputerBuilder("Intel i9", "32GB")
                .storage("1TB SSD")
                .graphicsCard("RTX 4090")
                .motherboard("ASUS ROG")
                .powerSupply("1000W")
                .hasWifi(true)
                .hasBluetooth(true)
                .build();
        
        assertEquals("Intel i9", computer.getCpu());
        assertEquals("32GB", computer.getRam());
        assertEquals("1TB SSD", computer.getStorage());
        assertEquals("RTX 4090", computer.getGraphicsCard());
        assertEquals("ASUS ROG", computer.getMotherboard());
        assertEquals("1000W", computer.getPowerSupply());
        assertTrue(computer.hasWifi());
        assertTrue(computer.hasBluetooth());
    }
    
    @Test
    public void testBuilderChaining() {
        Computer computer = new Computer.ComputerBuilder("AMD Ryzen 7", "16GB")
                .storage("512GB SSD")
                .hasWifi(true)
                .build();
        
        assertEquals("AMD Ryzen 7", computer.getCpu());
        assertEquals("16GB", computer.getRam());
        assertEquals("512GB SSD", computer.getStorage());
        assertTrue(computer.hasWifi());
        assertFalse(computer.hasBluetooth()); // Not set, should be default
    }
    
    @Test
    public void testToString() {
        Computer computer = new Computer.ComputerBuilder("Intel i7", "16GB")
                .storage("1TB HDD")
                .build();
        
        String computerString = computer.toString();
        assertTrue(computerString.contains("Intel i7"));
        assertTrue(computerString.contains("16GB"));
        assertTrue(computerString.contains("1TB HDD"));
    }
}
