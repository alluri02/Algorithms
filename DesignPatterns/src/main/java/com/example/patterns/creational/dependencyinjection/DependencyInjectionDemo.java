package com.example.patterns.creational.dependencyinjection;

/**
 * Dependency Injection Pattern - Inject dependencies from outside
 * 
 * Instead of creating dependencies inside a class, inject them from outside
 * This makes code more testable and flexible
 */

// Dependencies (services)
interface EmailService {
    void sendEmail(String to, String message);
}

interface LoggingService {
    void log(String message);
}

interface DatabaseService {
    void saveUser(String username);
    String getUser(String username);
}

// Concrete implementations
class GmailService implements EmailService {
    @Override
    public void sendEmail(String to, String message) {
        System.out.println("Gmail: Sending email to " + to + " - " + message);
    }
}

class OutlookService implements EmailService {
    @Override
    public void sendEmail(String to, String message) {
        System.out.println("Outlook: Sending email to " + to + " - " + message);
    }
}

class ConsoleLogger implements LoggingService {
    @Override
    public void log(String message) {
        System.out.println("LOG: " + message);
    }
}

class FileLogger implements LoggingService {
    @Override
    public void log(String message) {
        System.out.println("FILE_LOG: " + message + " (saved to file)");
    }
}

class MySQLDatabase implements DatabaseService {
    @Override
    public void saveUser(String username) {
        System.out.println("MySQL: Saved user " + username);
    }
    
    @Override
    public String getUser(String username) {
        return "MySQL: Retrieved user " + username;
    }
}

class PostgreSQLDatabase implements DatabaseService {
    @Override
    public void saveUser(String username) {
        System.out.println("PostgreSQL: Saved user " + username);
    }
    
    @Override
    public String getUser(String username) {
        return "PostgreSQL: Retrieved user " + username;
    }
}

// Client class that depends on services
class UserService {
    private final EmailService emailService;
    private final LoggingService loggingService;
    private final DatabaseService databaseService;
    
    // Constructor Injection - dependencies injected through constructor
    public UserService(EmailService emailService, 
                      LoggingService loggingService, 
                      DatabaseService databaseService) {
        this.emailService = emailService;
        this.loggingService = loggingService;
        this.databaseService = databaseService;
    }
    
    public void registerUser(String username, String email) {
        loggingService.log("Starting user registration for: " + username);
        
        // Save to database
        databaseService.saveUser(username);
        
        // Send welcome email
        emailService.sendEmail(email, "Welcome " + username + "!");
        
        loggingService.log("User registration completed for: " + username);
    }
    
    public void getUserInfo(String username) {
        loggingService.log("Retrieving user info for: " + username);
        String userInfo = databaseService.getUser(username);
        System.out.println(userInfo);
    }
}

// Simple Dependency Injection Container
class DIContainer {
    public static UserService createUserService(String config) {
        EmailService emailService;
        LoggingService loggingService;
        DatabaseService databaseService;
        
        // Configure based on environment
        switch (config.toLowerCase()) {
            case "production":
                emailService = new OutlookService();
                loggingService = new FileLogger();
                databaseService = new PostgreSQLDatabase();
                break;
            case "development":
                emailService = new GmailService();
                loggingService = new ConsoleLogger();
                databaseService = new MySQLDatabase();
                break;
            default:
                throw new IllegalArgumentException("Unknown config: " + config);
        }
        
        return new UserService(emailService, loggingService, databaseService);
    }
}

// Demo class
public class DependencyInjectionDemo {
    public static void main(String[] args) {
        System.out.println("=== Dependency Injection Pattern Demo ===");
        
        // Development environment
        System.out.println("\n--- Development Environment ---");
        UserService devUserService = DIContainer.createUserService("development");
        devUserService.registerUser("john_doe", "john@example.com");
        devUserService.getUserInfo("john_doe");
        
        // Production environment
        System.out.println("\n--- Production Environment ---");
        UserService prodUserService = DIContainer.createUserService("production");
        prodUserService.registerUser("jane_smith", "jane@company.com");
        prodUserService.getUserInfo("jane_smith");
        
        // Manual injection for testing
        System.out.println("\n--- Manual Injection (Testing) ---");
        UserService testUserService = new UserService(
            new GmailService(),
            new ConsoleLogger(),
            new MySQLDatabase()
        );
        testUserService.registerUser("test_user", "test@test.com");
    }
}
