package com.example.patterns.behavioral.state;

/**
 * State Pattern - Concrete State
 * Product selected state - ready to dispense product
 */
public class ProductSelectedState implements VendingMachineState {
    
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        if (amount > 0) {
            double totalMoney = machine.getInsertedMoney() + amount;
            machine.setInsertedMoney(totalMoney);
            System.out.println("Additional money inserted: $" + String.format("%.2f", amount));
            System.out.println("Total money: $" + String.format("%.2f", totalMoney));
        } else {
            System.out.println("Please insert a valid amount of money");
        }
    }
    
    @Override
    public void selectProduct(VendingMachine machine, String product) {
        System.out.println("Product already selected: " + machine.getSelectedProduct());
        System.out.println("Please dispense the current product or return money to select a different product");
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        String product = machine.getSelectedProduct();
        Double price = machine.getProductPrice(product);
        
        if (product == null || price == null) {
            System.out.println("Error: No product selected");
            machine.setState(machine.getHasMoneyState());
            return;
        }
        
        // Check stock again (in case it changed)
        if (!machine.isProductAvailable(product)) {
            System.out.println("Sorry, " + product + " is now out of stock");
            machine.setState(machine.getOutOfStockState());
            return;
        }
        
        // Dispense product
        System.out.println("Dispensing " + product + "...");
        machine.decrementStock(product);
        
        // Calculate change
        double change = machine.getInsertedMoney() - price;
        if (change > 0) {
            System.out.println("Your change: $" + String.format("%.2f", change));
        }
        
        // Reset machine
        machine.setInsertedMoney(0.0);
        machine.setSelectedProduct(null);
        machine.setState(machine.getIdleState());
        
        System.out.println("Thank you for your purchase!");
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        double moneyToReturn = machine.getInsertedMoney();
        machine.setInsertedMoney(0.0);
        machine.setSelectedProduct(null);
        System.out.println("Transaction cancelled. Money returned: $" + String.format("%.2f", moneyToReturn));
        machine.setState(machine.getIdleState());
    }
    
    @Override
    public String getStateName() {
        return "Product Selected";
    }
}
