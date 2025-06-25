package com.example.patterns.behavioral.strategy;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Strategy Pattern implementation
 */
public class StrategyPatternTest {
    
    private ShoppingCart cart;
    
    @BeforeEach
    void setUp() {
        cart = new ShoppingCart();
    }
    
    @Test
    void testCreditCardPayment() {
        PaymentStrategy creditCard = new CreditCardStrategy("1234567890123456", "123", "12/25");
        cart.setPaymentStrategy(creditCard);
        
        assertTrue(creditCard.validatePaymentDetails());
        assertDoesNotThrow(() -> cart.processPayment(100.0));
    }
    
    @Test
    void testPayPalPayment() {
        PaymentStrategy paypal = new PayPalStrategy("user@example.com", "password123");
        cart.setPaymentStrategy(paypal);
        
        assertTrue(paypal.validatePaymentDetails());
        assertDoesNotThrow(() -> cart.processPayment(50.0));
    }
    
    @Test
    void testBitcoinPayment() {
        PaymentStrategy bitcoin = new BitcoinStrategy("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "L1aW4aubDFB7yfras2S1mN3bqg9nwySY8nkoLove");
        cart.setPaymentStrategy(bitcoin);
        
        assertTrue(bitcoin.validatePaymentDetails());
        assertDoesNotThrow(() -> cart.processPayment(75.0));
    }
    
    @Test
    void testInvalidCreditCard() {
        PaymentStrategy invalidCard = new CreditCardStrategy("123", "1", "1");
        assertFalse(invalidCard.validatePaymentDetails());
    }
    
    @Test
    void testInvalidPayPal() {
        PaymentStrategy invalidPaypal = new PayPalStrategy("invalid-email", "123");
        assertFalse(invalidPaypal.validatePaymentDetails());
    }
    
    @Test
    void testNoPaymentStrategy() {
        // Should handle gracefully when no strategy is set
        assertDoesNotThrow(() -> cart.processPayment(100.0));
    }
    
    @Test
    void testStrategySwitch() {
        PaymentStrategy creditCard = new CreditCardStrategy("1234567890123456", "123", "12/25");
        PaymentStrategy paypal = new PayPalStrategy("user@example.com", "password123");
        
        // Switch between strategies
        cart.setPaymentStrategy(creditCard);
        assertDoesNotThrow(() -> cart.processPayment(100.0));
        
        cart.setPaymentStrategy(paypal);
        assertDoesNotThrow(() -> cart.processPayment(100.0));
    }
}
