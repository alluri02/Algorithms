package com.example.patterns.structural.decorator;

/**
 * Decorator Pattern - Component interface
 * Base interface for objects that can be decorated
 */
public interface Coffee {
    String getDescription();
    double getCost();
}
