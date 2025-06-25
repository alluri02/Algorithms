package com.example.patterns.behavioral.strategy;

/**
 * Strategy Pattern - Concrete Strategy
 * PayPal payment implementation
 */
public class PayPalStrategy implements PaymentStrategy {
    private String email;
    private String password;
    
    public PayPalStrategy(String email, String password) {
        this.email = email;
        this.password = password;
    }
    
    @Override
    public boolean validatePaymentDetails() {
        // Simple validation logic
        if (email == null || !email.contains("@")) {
            System.out.println("Invalid email address");
            return false;
        }
        if (password == null || password.length() < 6) {
            System.out.println("Invalid password");
            return false;
        }
        return true;
    }
    
    @Override
    public void pay(double amount) {
        if (validatePaymentDetails()) {
            System.out.println("Paid $" + amount + " using PayPal account: " + email);
            System.out.println("Transaction processed successfully via PayPal");
        } else {
            System.out.println("PayPal payment failed due to invalid credentials");
        }
    }
}
