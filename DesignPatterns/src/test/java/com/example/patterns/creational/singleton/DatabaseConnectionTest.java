package com.example.patterns.creational.singleton;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for DatabaseConnection Singleton
 */
public class DatabaseConnectionTest {
    
    @Test
    public void testSingletonInstance() {
        DatabaseConnection instance1 = DatabaseConnection.getInstance();
        DatabaseConnection instance2 = DatabaseConnection.getInstance();
        
        assertSame(instance1, instance2, "Both instances should be the same object");
    }
    
    @Test
    public void testConnectionString() {
        DatabaseConnection instance = DatabaseConnection.getInstance();
        String connectionString = instance.getConnectionString();
        
        assertNotNull(connectionString, "Connection string should not be null");
        assertTrue(connectionString.contains("jdbc:mysql"), "Connection string should contain jdbc:mysql");
    }
}
