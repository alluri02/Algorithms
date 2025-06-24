package com.example.patterns.behavioral.observer;

/**
 * PhoneDisplay acts as an Observer that displays weather data on a phone
 */
public class PhoneDisplay implements Observer {
    private float temperature;
    private int humidity;
    private float pressure;
    
    @Override
    public void update(float temperature, int humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;
        display();
    }
    
    public void display() {
        System.out.println("Phone Display: Temperature: " + temperature + "°C, " +
                          "Humidity: " + humidity + "%, " +
                          "Pressure: " + pressure + " hPa");
    }
}
