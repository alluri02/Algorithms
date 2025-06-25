package com.example.patterns.behavioral.strategy;

/**
 * Strategy Pattern - Strategy interface
 * Defines the algorithm interface
 */
public interface PaymentStrategy {
    void pay(double amount);
    boolean validatePaymentDetails();
}
