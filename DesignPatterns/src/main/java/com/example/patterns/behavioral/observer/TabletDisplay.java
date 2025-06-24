package com.example.patterns.behavioral.observer;

/**
 * TabletDisplay acts as an Observer that displays weather data on a tablet
 */
public class TabletDisplay implements Observer {
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
        System.out.println("Tablet Display: Current conditions - " + temperature + "°C " +
                          "and " + humidity + "% humidity " +
                          "(Pressure: " + pressure + " hPa)");
    }
}
