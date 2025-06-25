package com.example.patterns.behavioral.strategy;

/**
 * Strategy Pattern - Concrete Strategy
 * Credit Card payment implementation
 */
public class CreditCardStrategy implements PaymentStrategy {
    private String cardNumber;
    private String cvv;
    private String expiryDate;
    
    public CreditCardStrategy(String cardNumber, String cvv, String expiryDate) {
        this.cardNumber = cardNumber;
        this.cvv = cvv;
        this.expiryDate = expiryDate;
    }
    
    @Override
    public boolean validatePaymentDetails() {
        // Simple validation logic
        if (cardNumber == null || cardNumber.length() != 16) {
            System.out.println("Invalid card number");
            return false;
        }
        if (cvv == null || cvv.length() != 3) {
            System.out.println("Invalid CVV");
            return false;
        }
        if (expiryDate == null || expiryDate.length() != 5) {
            System.out.println("Invalid expiry date");
            return false;
        }
        return true;
    }
    
    @Override
    public void pay(double amount) {
        if (validatePaymentDetails()) {
            System.out.println("Paid $" + amount + " using Credit Card ending in " + 
                             cardNumber.substring(12));
            System.out.println("Transaction processed successfully via Credit Card");
        } else {
            System.out.println("Credit Card payment failed due to invalid details");
        }
    }
}
