package com.example.patterns;

import com.example.patterns.creational.singleton.DatabaseConnection;
import com.example.patterns.creational.factory.ShapeFactory;
import com.example.patterns.creational.factory.Shape;
import com.example.patterns.creational.builder.House;
import com.example.patterns.creational.builder.Pizza;
import com.example.patterns.creational.abstractfactory.Application;
import com.example.patterns.structural.adapter.AudioPlayer;
import com.example.patterns.structural.bridge.BridgePatternDemo;
import com.example.patterns.structural.composite.CompositePatternDemo;
import com.example.patterns.structural.decorator.DecoratorPatternDemo;
import com.example.patterns.structural.facade.FacadePatternDemo;
import com.example.patterns.structural.flyweight.FlyweightPatternDemo;
import com.example.patterns.structural.proxy.ProxyPatternDemo;
import com.example.patterns.behavioral.observer.WeatherStation;
import com.example.patterns.behavioral.observer.PhoneDisplay;
import com.example.patterns.behavioral.observer.TabletDisplay;
import com.example.patterns.behavioral.strategy.StrategyPatternDemo;
import com.example.patterns.behavioral.command.CommandPatternDemo;
import com.example.patterns.behavioral.state.StatePatternDemo;
import com.example.patterns.behavioral.templatemethod.TemplateMethodPatternDemo;
import com.example.patterns.behavioral.chainofresponsibility.ChainOfResponsibilityPatternDemo;
import com.example.patterns.behavioral.mediator.MediatorPatternDemo;

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
        
        // Bridge Pattern Demo
        demonstrateBridge();
        
        // Composite Pattern Demo
        demonstrateComposite();
        
        // Decorator Pattern Demo
        demonstrateDecorator();
        
        // Facade Pattern Demo
        demonstrateFacade();
        
        // Flyweight Pattern Demo
        demonstrateFlyweight();
        
        // Proxy Pattern Demo
        demonstrateProxy();
          System.out.println("BEHAVIORAL PATTERNS:");
        // Observer Pattern Demo
        demonstrateObserver();
        
        // Strategy Pattern Demo
        demonstrateStrategy();
        
        // Command Pattern Demo
        demonstrateCommand();
        
        // State Pattern Demo
        demonstrateState();
        
        // Template Method Pattern Demo
        demonstrateTemplateMethod();
        
        // Chain of Responsibility Pattern Demo
        demonstrateChainOfResponsibility();
        
        // Mediator Pattern Demo
        demonstrateMediator();        System.out.println("Run individual pattern demos:");
        System.out.println("   java com.example.patterns.creational.prototype.PrototypeDemo");
        System.out.println("   java com.example.patterns.creational.objectpool.ObjectPoolDemo");
        System.out.println("   java com.example.patterns.creational.dependencyinjection.DependencyInjectionDemo");
        System.out.println("   java com.example.patterns.structural.bridge.BridgePatternDemo");
        System.out.println("   java com.example.patterns.structural.composite.CompositePatternDemo");
        System.out.println("   java com.example.patterns.structural.decorator.DecoratorPatternDemo");
        System.out.println("   java com.example.patterns.structural.facade.FacadePatternDemo");
        System.out.println("   java com.example.patterns.structural.flyweight.FlyweightPatternDemo");
        System.out.println("   java com.example.patterns.structural.proxy.ProxyPatternDemo");
        System.out.println("   java com.example.patterns.behavioral.strategy.StrategyPatternDemo");
        System.out.println("   java com.example.patterns.behavioral.command.CommandPatternDemo");
        System.out.println("   java com.example.patterns.behavioral.state.StatePatternDemo");
        System.out.println("   java com.example.patterns.behavioral.templatemethod.TemplateMethodPatternDemo");
        System.out.println("   java com.example.patterns.behavioral.chainofresponsibility.ChainOfResponsibilityPatternDemo");
        System.out.println("   java com.example.patterns.behavioral.mediator.MediatorPatternDemo");
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
    
    private static void demonstrateBridge() {
        System.out.println("--- Bridge Pattern ---");
        BridgePatternDemo.demonstrateBridgePattern();
        System.out.println();
    }
    
    private static void demonstrateComposite() {
        System.out.println("--- Composite Pattern ---");
        CompositePatternDemo.demonstrateCompositePattern();
        System.out.println();
    }
    
    private static void demonstrateDecorator() {
        System.out.println("--- Decorator Pattern ---");
        DecoratorPatternDemo.demonstrateDecoratorPattern();
        System.out.println();
    }
    
    private static void demonstrateFacade() {
        System.out.println("--- Facade Pattern ---");
        FacadePatternDemo.demonstrateFacadePattern();
        System.out.println();
    }
    
    private static void demonstrateFlyweight() {
        System.out.println("--- Flyweight Pattern ---");
        FlyweightPatternDemo.demonstrateFlyweightPattern();
        System.out.println();
    }
    
    private static void demonstrateProxy() {
        System.out.println("--- Proxy Pattern ---");
        ProxyPatternDemo.demonstrateProxyPattern();
        System.out.println();
    }
    
    private static void demonstrateStrategy() {
        System.out.println("--- Strategy Pattern ---");
        StrategyPatternDemo.demonstrateStrategyPattern();
        System.out.println();
    }
    
    private static void demonstrateCommand() {
        System.out.println("--- Command Pattern ---");
        CommandPatternDemo.demonstrateCommandPattern();
        System.out.println();
    }
    
    private static void demonstrateState() {
        System.out.println("--- State Pattern ---");
        StatePatternDemo.demonstrateStatePattern();
        System.out.println();
    }
    
    private static void demonstrateTemplateMethod() {
        System.out.println("--- Template Method Pattern ---");
        TemplateMethodPatternDemo.demonstrateTemplateMethodPattern();
        System.out.println();
    }
    
    private static void demonstrateChainOfResponsibility() {
        System.out.println("--- Chain of Responsibility Pattern ---");
        ChainOfResponsibilityPatternDemo.demonstrateChainOfResponsibilityPattern();
        System.out.println();
    }
    
    private static void demonstrateMediator() {
        System.out.println("--- Mediator Pattern ---");
        MediatorPatternDemo.demonstrateMediatorPattern();
        System.out.println();
    }
}
