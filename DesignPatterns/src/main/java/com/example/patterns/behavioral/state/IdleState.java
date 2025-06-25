package com.example.patterns.behavioral.state;

/**
 * State Pattern - Concrete State
 * Idle state - waiting for money insertion
 */
public class IdleState implements VendingMachineState {
    
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        if (amount > 0) {
            machine.setInsertedMoney(amount);
            System.out.println("Money inserted: $" + String.format("%.2f", amount));
            machine.setState(machine.getHasMoneyState());
        } else {
            System.out.println("Please insert a valid amount of money");
        }
    }
    
    @Override
    public void selectProduct(VendingMachine machine, String product) {
        System.out.println("Please insert money first");
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("Please insert money and select a product first");
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        System.out.println("No money to return");
    }
    
    @Override
    public String getStateName() {
        return "Idle";
    }
}
