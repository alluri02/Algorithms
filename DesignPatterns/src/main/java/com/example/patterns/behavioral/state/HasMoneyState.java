package com.example.patterns.behavioral.state;

/**
 * State Pattern - Concrete State
 * Has money state - money inserted, waiting for product selection
 */
public class HasMoneyState implements VendingMachineState {
    
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
        Double price = machine.getProductPrice(product);
        
        if (price == null) {
            System.out.println("Product '" + product + "' not available");
            return;
        }
        
        if (!machine.isProductAvailable(product)) {
            System.out.println("Product '" + product + "' is out of stock");
            machine.setState(machine.getOutOfStockState());
            return;
        }
        
        if (machine.getInsertedMoney() >= price) {
            machine.setSelectedProduct(product);
            System.out.println("Product selected: " + product + " ($" + String.format("%.2f", price) + ")");
            machine.setState(machine.getProductSelectedState());
        } else {
            System.out.println("Insufficient funds. Product costs $" + String.format("%.2f", price) + 
                             ", you have $" + String.format("%.2f", machine.getInsertedMoney()));
        }
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("Please select a product first");
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        double moneyToReturn = machine.getInsertedMoney();
        machine.setInsertedMoney(0.0);
        System.out.println("Money returned: $" + String.format("%.2f", moneyToReturn));
        machine.setState(machine.getIdleState());
    }
    
    @Override
    public String getStateName() {
        return "Has Money";
    }
}
