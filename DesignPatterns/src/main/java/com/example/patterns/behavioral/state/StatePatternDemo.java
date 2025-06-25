package com.example.patterns.behavioral.state;

/**
 * State Pattern Demo
 * Demonstrates how object behavior changes based on its internal state
 */
public class StatePatternDemo {
    
    public static void demonstrateStatePattern() {
        System.out.println("=== State Pattern Demo ===");
        
        VendingMachine machine = new VendingMachine();
        machine.displayStatus();
        
        System.out.println("\n--- Scenario 1: Successful Purchase ---");
        System.out.println("Current state: " + machine.getCurrentStateName());
        
        // Try to select product without money
        machine.selectProduct("Coke");
        
        // Insert money
        machine.insertMoney(2.00);
        
        // Select product
        machine.selectProduct("Coke");
        
        // Dispense product
        machine.dispenseProduct();
        
        System.out.println("\n--- Scenario 2: Insufficient Funds ---");
        machine.insertMoney(1.00);
        machine.selectProduct("Chips"); // Costs $2.00
        
        // Add more money
        machine.insertMoney(1.50);
        machine.selectProduct("Chips");
        machine.dispenseProduct();
        
        System.out.println("\n--- Scenario 3: Out of Stock ---");
        machine.insertMoney(2.00);
        machine.selectProduct("Chips"); // Should be out of stock now
        
        // Try to dispense
        machine.dispenseProduct();
        
        // Select different product
        machine.selectProduct("Water");
        machine.dispenseProduct();
        
        System.out.println("\n--- Scenario 4: Money Return ---");
        machine.insertMoney(5.00);
        machine.selectProduct("Pepsi");
        machine.returnMoney(); // Cancel transaction
        
        System.out.println("\n--- Final Machine Status ---");
        machine.displayStatus();
        
        System.out.println("\nState Pattern allows objects to change behavior when their internal state changes!");
    }
    
    public static void main(String[] args) {
        demonstrateStatePattern();
    }
}
