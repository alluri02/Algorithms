package com.example.patterns.behavioral.observer;

/**
 * Subject interface for the Observer Pattern
 */
public interface Subject {
    void addObserver(Observer observer);
    void removeObserver(Observer observer);
    void notifyObservers();
}
