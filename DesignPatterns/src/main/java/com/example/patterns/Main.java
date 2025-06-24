package com.example.patterns;

import com.example.patterns.creational.singleton.DatabaseConnection;
import com.example.patterns.creational.factory.ShapeFactory;
import com.example.patterns.creational.factory.Shape;
import com.example.patterns.creational.builder.House;
import com.example.patterns.creational.builder.Pizza;
import com.example.patterns.creational.abstractfactory.Application;
import com.example.patterns.structural.adapter.AudioPlayer;
import com.example.patterns.behavioral.observer.WeatherStation;
import com.example.patterns.behavioral.observer.PhoneDisplay;
import com.example.patterns.behavioral.observer.TabletDisplay;

/**
 * Main class demonstrating various design patterns
 */
public class Main {    public static void main(String[] args) {
        System.out.println("=== Design Patterns Demo ===\n");
        
        System.out.println("CREATIONAL PATTERNS:");
        // Singleton Pattern Demo
        demonstrateSingleton();
        
        // Factory Pattern Demo
        demonstrateFactory();
        
        // Builder Pattern Demo
        demonstrateBuilder();
        
        // Abstract Factory Pattern Demo
        demonstrateAbstractFactory();
        
        System.out.println("STRUCTURAL PATTERNS:");
        // Adapter Pattern Demo
        demonstrateAdapter();
        
        System.out.println("BEHAVIORAL PATTERNS:");
        // Observer Pattern Demo
        demonstrateObserver();
        
        System.out.println("Run individual pattern demos:");
        System.out.println("   java com.example.patterns.creational.prototype.PrototypeDemo");
        System.out.println("   java com.example.patterns.creational.objectpool.ObjectPoolDemo");
        System.out.println("   java com.example.patterns.creational.dependencyinjection.DependencyInjectionDemo");
    }
    
    private static void demonstrateSingleton() {
        System.out.println("--- Singleton Pattern ---");
        DatabaseConnection db1 = DatabaseConnection.getInstance();
        DatabaseConnection db2 = DatabaseConnection.getInstance();
        
        System.out.println("db1 == db2: " + (db1 == db2));
        db1.connect();
        System.out.println();
    }
      private static void demonstrateFactory() {
        System.out.println("--- Factory Pattern ---");
        ShapeFactory shapeFactory = new ShapeFactory();
        
        Shape circle = shapeFactory.getShape("CIRCLE");
        Shape rectangle = shapeFactory.getShape("RECTANGLE");
        Shape square = shapeFactory.getShape("SQUARE");
        
        circle.draw();
        rectangle.draw();
        square.draw();
        System.out.println();
    }
      private static void demonstrateBuilder() {
        System.out.println("--- Builder Pattern ---");
        
        // Simple House Builder
        House basicHouse = new House.HouseBuilder(3, 2)
                .build();
        System.out.println("Basic house: " + basicHouse);
        
        House luxuryHouse = new House.HouseBuilder(5, 3)
                .withGarage()
                .withGarden()
                .withPool()
                .withRoof("tile")
                .build();
        System.out.println("Luxury house: " + luxuryHouse);
        
        // Pizza Builder
        Pizza veggiePizza = new Pizza.PizzaBuilder("Large", "thick crust")
                .addCheese()
                .addMushrooms()
                .addOlives()
                .addTomatoes()
                .build();
        System.out.println("Veggie pizza: " + veggiePizza);
        
        System.out.println();
    }
    
    private static void demonstrateAdapter() {
        System.out.println("--- Adapter Pattern ---");
        AudioPlayer player = new AudioPlayer();
        
        player.play("mp3", "song.mp3");
        player.play("mp4", "video.mp4");
        player.play("vlc", "movie.vlc");
        player.play("avi", "movie.avi");
        System.out.println();
    }
    
    private static void demonstrateObserver() {
        System.out.println("--- Observer Pattern ---");
        WeatherStation weatherStation = new WeatherStation();
        
        PhoneDisplay phoneDisplay = new PhoneDisplay();
        TabletDisplay tabletDisplay = new TabletDisplay();
        
        weatherStation.addObserver(phoneDisplay);
        weatherStation.addObserver(tabletDisplay);
        
        weatherStation.setWeatherData(25.5f, 65, 1013.2f);
        weatherStation.setWeatherData(27.3f, 70, 1012.5f);
        System.out.println();
    }
    
    private static void demonstrateAbstractFactory() {
        System.out.println("--- Abstract Factory Pattern ---");
        
        // Create Windows application
        Application windowsApp = new Application(Application.getFactory("Windows"));
        windowsApp.createUI();
        System.out.println("Windows UI:");
        windowsApp.render();
        windowsApp.interact();
        
        // Create Mac application
        Application macApp = new Application(Application.getFactory("Mac"));
        macApp.createUI();
        System.out.println("\nMac UI:");
        macApp.render();
        macApp.interact();
        
        System.out.println();
    }
}
