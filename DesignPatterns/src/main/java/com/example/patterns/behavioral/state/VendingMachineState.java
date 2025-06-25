package com.example.patterns.behavioral.state;

/**
 * State Pattern - State interface
 * Defines the interface for concrete states
 */
public interface VendingMachineState {
    void insertMoney(VendingMachine machine, double amount);
    void selectProduct(VendingMachine machine, String product);
    void dispenseProduct(VendingMachine machine);
    void returnMoney(VendingMachine machine);
    String getStateName();
}
