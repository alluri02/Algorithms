package com.example.patterns.creational.singleton;

/**
 * Singleton Pattern Implementation
 * Ensures a class has only one instance and provides global access to it.
 * 
 * This implementation uses the thread-safe lazy initialization approach.
 */
public class DatabaseConnection {
    // Volatile keyword ensures that multiple threads handle the instance variable correctly
    private static volatile DatabaseConnection instance;
    private String connectionString;
    
    // Private constructor prevents instantiation from other classes
    private DatabaseConnection() {
        // Simulate expensive connection setup
        this.connectionString = "jdbc:mysql://localhost:3306/designpatterns";
        System.out.println("Creating database connection...");
    }
    
    /**
     * Thread-safe method to get the singleton instance
     * Uses double-checked locking pattern for performance optimization
     */
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
    
    public void connect() {
        System.out.println("Connected to database: " + connectionString);
    }
    
    public void disconnect() {
        System.out.println("Disconnected from database");
    }
    
    public String getConnectionString() {
        return connectionString;
    }
}
