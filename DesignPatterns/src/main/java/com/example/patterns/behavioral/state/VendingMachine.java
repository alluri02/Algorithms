package com.example.patterns.behavioral.state;

import java.util.HashMap;
import java.util.Map;

/**
 * State Pattern - Context
 * Vending machine that changes behavior based on its state
 */
public class VendingMachine {
    private VendingMachineState currentState;
    private VendingMachineState idleState;
    private VendingMachineState hasMoneyState;
    private VendingMachineState productSelectedState;
    private VendingMachineState outOfStockState;
    
    private double insertedMoney;
    private String selectedProduct;
    private Map<String, Double> productPrices;
    private Map<String, Integer> productStock;
    
    public VendingMachine() {
        // Initialize states
        idleState = new IdleState();
        hasMoneyState = new HasMoneyState();
        productSelectedState = new ProductSelectedState();
        outOfStockState = new OutOfStockState();
        
        // Set initial state
        currentState = idleState;
        
        // Initialize products and prices
        productPrices = new HashMap<>();
        productStock = new HashMap<>();
        
        productPrices.put("Coke", 1.50);
        productPrices.put("Pepsi", 1.50);
        productPrices.put("Water", 1.00);
        productPrices.put("Chips", 2.00);
        
        productStock.put("Coke", 5);
        productStock.put("Pepsi", 3);
        productStock.put("Water", 10);
        productStock.put("Chips", 0); // Out of stock
        
        insertedMoney = 0.0;
        selectedProduct = null;
    }
    
    // State management
    public void setState(VendingMachineState state) {
        this.currentState = state;
        System.out.println("State changed to: " + state.getStateName());
    }
    
    // Public methods that delegate to current state
    public void insertMoney(double amount) {
        currentState.insertMoney(this, amount);
    }
    
    public void selectProduct(String product) {
        currentState.selectProduct(this, product);
    }
    
    public void dispenseProduct() {
        currentState.dispenseProduct(this);
    }
    
    public void returnMoney() {
        currentState.returnMoney(this);
    }
    
    // Getters and setters for state management
    public VendingMachineState getIdleState() { return idleState; }
    public VendingMachineState getHasMoneyState() { return hasMoneyState; }
    public VendingMachineState getProductSelectedState() { return productSelectedState; }
    public VendingMachineState getOutOfStockState() { return outOfStockState; }
    
    public double getInsertedMoney() { return insertedMoney; }
    public void setInsertedMoney(double money) { this.insertedMoney = money; }
    
    public String getSelectedProduct() { return selectedProduct; }
    public void setSelectedProduct(String product) { this.selectedProduct = product; }
    
    public Double getProductPrice(String product) {
        return productPrices.get(product);
    }
    
    public Integer getProductStock(String product) {
        return productStock.getOrDefault(product, 0);
    }
    
    public void decrementStock(String product) {
        int currentStock = productStock.getOrDefault(product, 0);
        if (currentStock > 0) {
            productStock.put(product, currentStock - 1);
        }
    }
    
    public boolean isProductAvailable(String product) {
        return productPrices.containsKey(product) && getProductStock(product) > 0;
    }
    
    public String getCurrentStateName() {
        return currentState.getStateName();
    }
    
    public void displayStatus() {
        System.out.println("--- Vending Machine Status ---");
        System.out.println("Current State: " + currentState.getStateName());
        System.out.println("Inserted Money: $" + String.format("%.2f", insertedMoney));
        System.out.println("Selected Product: " + (selectedProduct != null ? selectedProduct : "None"));
        System.out.println("Available Products:");
        for (Map.Entry<String, Double> entry : productPrices.entrySet()) {
            String product = entry.getKey();
            double price = entry.getValue();
            int stock = getProductStock(product);
            System.out.println("  " + product + ": $" + String.format("%.2f", price) + 
                             " (Stock: " + stock + ")");
        }
        System.out.println("------------------------------");
    }
}
