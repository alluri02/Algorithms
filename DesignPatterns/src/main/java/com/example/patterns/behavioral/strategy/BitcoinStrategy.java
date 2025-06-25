package com.example.patterns.behavioral.strategy;

/**
 * Strategy Pattern - Concrete Strategy
 * Bitcoin payment implementation
 */
public class BitcoinStrategy implements PaymentStrategy {
    private String walletAddress;
    private String privateKey;
    
    public BitcoinStrategy(String walletAddress, String privateKey) {
        this.walletAddress = walletAddress;
        this.privateKey = privateKey;
    }
    
    @Override
    public boolean validatePaymentDetails() {
        // Simple validation logic
        if (walletAddress == null || walletAddress.length() < 26) {
            System.out.println("Invalid wallet address");
            return false;
        }
        if (privateKey == null || privateKey.length() < 32) {
            System.out.println("Invalid private key");
            return false;
        }
        return true;
    }
    
    @Override
    public void pay(double amount) {
        if (validatePaymentDetails()) {
            System.out.println("Paid $" + amount + " using Bitcoin from wallet: " + 
                             walletAddress.substring(0, 8) + "...");
            System.out.println("Transaction processed successfully via Bitcoin network");
        } else {
            System.out.println("Bitcoin payment failed due to invalid wallet details");
        }
    }
}
