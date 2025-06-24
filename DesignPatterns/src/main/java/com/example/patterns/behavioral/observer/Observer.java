package com.example.patterns.behavioral.observer;

/**
 * Observer interface for the Observer Pattern
 */
public interface Observer {
    void update(float temperature, int humidity, float pressure);
}
