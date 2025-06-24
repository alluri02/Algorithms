package com.example.patterns.behavioral.observer;

import java.util.ArrayList;
import java.util.List;

/**
 * WeatherStation acts as the Subject in the Observer Pattern
 * It maintains weather data and notifies all registered observers when data changes
 */
public class WeatherStation implements Subject {
    private List<Observer> observers;
    private float temperature;
    private int humidity;
    private float pressure;
    
    public WeatherStation() {
        observers = new ArrayList<>();
    }
    
    @Override
    public void addObserver(Observer observer) {
        observers.add(observer);
        System.out.println("Observer added to weather station");
    }
    
    @Override
    public void removeObserver(Observer observer) {
        observers.remove(observer);
        System.out.println("Observer removed from weather station");
    }
    
    @Override
    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(temperature, humidity, pressure);
        }
    }
    
    /**
     * Sets new weather data and notifies all observers
     */
    public void setWeatherData(float temperature, int humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;
        
        System.out.println("\nWeather Station: New weather data received!");
        notifyObservers();
    }
    
    // Getters
    public float getTemperature() { return temperature; }
    public int getHumidity() { return humidity; }
    public float getPressure() { return pressure; }
}
