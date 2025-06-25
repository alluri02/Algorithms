package com.example.patterns.behavioral.strategy;

/**
 * Strategy Pattern - Context
 * Shopping cart that uses different payment strategies
 */
public class ShoppingCart {
    private PaymentStrategy paymentStrategy;
    
    public void setPaymentStrategy(PaymentStrategy paymentStrategy) {
        this.paymentStrategy = paymentStrategy;
    }
    
    public void processPayment(double amount) {
        if (paymentStrategy == null) {
            System.out.println("No payment method selected!");
            return;
        }
        
        System.out.println("Processing payment of $" + amount);
        paymentStrategy.pay(amount);
    }
}
