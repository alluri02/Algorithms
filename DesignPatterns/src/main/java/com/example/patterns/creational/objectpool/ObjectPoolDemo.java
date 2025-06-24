package com.example.patterns.creational.objectpool;

import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Object Pool Pattern - Reuse expensive objects instead of creating new ones
 * 
 * Useful for database connections, thread pools, graphics objects
 */

// Expensive object to pool
class DatabaseConnection {
    private static AtomicInteger connectionCounter = new AtomicInteger(0);
    private final int connectionId;
    private boolean inUse = false;
    
    public DatabaseConnection() {
        this.connectionId = connectionCounter.incrementAndGet();
        // Simulate expensive connection setup
        try {
            Thread.sleep(100); // Simulate connection time
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("Created expensive database connection #" + connectionId);
    }
    
    public void executeQuery(String query) {
        System.out.println("Connection #" + connectionId + " executing: " + query);
    }
    
    public void reset() {
        // Reset connection state for reuse
        System.out.println("Connection #" + connectionId + " reset for reuse");
    }
    
    public boolean isInUse() { return inUse; }
    public void setInUse(boolean inUse) { this.inUse = inUse; }
    public int getConnectionId() { return connectionId; }
}

// Object Pool
class ConnectionPool {
    private final ConcurrentLinkedQueue<DatabaseConnection> pool;
    private final int maxPoolSize;
    private final AtomicInteger currentPoolSize;
    
    public ConnectionPool(int maxSize) {
        this.maxPoolSize = maxSize;
        this.pool = new ConcurrentLinkedQueue<>();
        this.currentPoolSize = new AtomicInteger(0);
        
        // Pre-create some connections
        for (int i = 0; i < Math.min(2, maxSize); i++) {
            pool.offer(createConnection());
        }
    }
    
    public DatabaseConnection borrowConnection() {
        DatabaseConnection connection = pool.poll();
        
        if (connection == null) {
            if (currentPoolSize.get() < maxPoolSize) {
                connection = createConnection();
            } else {
                throw new RuntimeException("Pool exhausted! Max connections: " + maxPoolSize);
            }
        }
        
        connection.setInUse(true);
        System.out.println("Borrowed connection #" + connection.getConnectionId());
        return connection;
    }
    
    public void returnConnection(DatabaseConnection connection) {
        if (connection != null && connection.isInUse()) {
            connection.setInUse(false);
            connection.reset();
            pool.offer(connection);
            System.out.println("Returned connection #" + connection.getConnectionId());
        }
    }
    
    private DatabaseConnection createConnection() {
        currentPoolSize.incrementAndGet();
        return new DatabaseConnection();
    }
    
    public int getPoolSize() {
        return pool.size();
    }
    
    public int getTotalConnections() {
        return currentPoolSize.get();
    }
}

// Demo class
public class ObjectPoolDemo {
    public static void main(String[] args) {
        System.out.println("=== Object Pool Pattern Demo ===");
        
        ConnectionPool pool = new ConnectionPool(3); // Max 3 connections
        
        System.out.println("\n--- Borrowing connections ---");
        DatabaseConnection conn1 = pool.borrowConnection();
        DatabaseConnection conn2 = pool.borrowConnection();
        DatabaseConnection conn3 = pool.borrowConnection();
        
        // Use connections
        System.out.println("\n--- Using connections ---");
        conn1.executeQuery("SELECT * FROM users");
        conn2.executeQuery("SELECT * FROM orders");
        conn3.executeQuery("SELECT * FROM products");
        
        // Return connections
        System.out.println("\n--- Returning connections ---");
        pool.returnConnection(conn1);
        pool.returnConnection(conn2);
        
        // Reuse returned connections
        System.out.println("\n--- Reusing connections ---");
        DatabaseConnection conn4 = pool.borrowConnection(); // Should reuse returned connection
        conn4.executeQuery("SELECT * FROM inventory");
        
        pool.returnConnection(conn3);
        pool.returnConnection(conn4);
        
        System.out.println("\nPool statistics:");
        System.out.println("Available connections: " + pool.getPoolSize());
        System.out.println("Total connections created: " + pool.getTotalConnections());
    }
}
