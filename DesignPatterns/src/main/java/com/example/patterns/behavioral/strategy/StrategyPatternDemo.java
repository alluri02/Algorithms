package com.example.patterns.behavioral.strategy;

/**
 * Strategy Pattern Demo
 * Demonstrates how to switch algorithms at runtime
 */
public class StrategyPatternDemo {
    
    public static void demonstrateStrategyPattern() {
        System.out.println("=== Strategy Pattern Demo ===");
        
        ShoppingCart cart = new ShoppingCart();
        double amount = 100.50;
        
        System.out.println("\n--- Credit Card Payment ---");
        PaymentStrategy creditCard = new CreditCardStrategy("1234567890123456", "123", "12/25");
        cart.setPaymentStrategy(creditCard);
        cart.processPayment(amount);
        
        System.out.println("\n--- PayPal Payment ---");
        PaymentStrategy paypal = new PayPalStrategy("user@example.com", "password123");
        cart.setPaymentStrategy(paypal);
        cart.processPayment(amount);
        
        System.out.println("\n--- Bitcoin Payment ---");
        PaymentStrategy bitcoin = new BitcoinStrategy("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "L1aW4aubDFB7yfras2S1mN3bqg9nwySY8nkoLove");
        cart.setPaymentStrategy(bitcoin);
        cart.processPayment(amount);
        
        System.out.println("\n--- Invalid Payment Attempts ---");
        PaymentStrategy invalidCard = new CreditCardStrategy("123", "1", "1");
        cart.setPaymentStrategy(invalidCard);
        cart.processPayment(amount);
        
        PaymentStrategy invalidPaypal = new PayPalStrategy("invalid-email", "123");
        cart.setPaymentStrategy(invalidPaypal);
        cart.processPayment(amount);
        
        System.out.println("\nStrategy Pattern allows switching algorithms at runtime!");
    }
    
    public static void main(String[] args) {
        demonstrateStrategyPattern();
    }
}
