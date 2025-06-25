package com.example.patterns.behavioral.command;

/**
 * Command Pattern - Command interface
 * Defines the execute method for all commands
 */
public interface Command {
    void execute();
    void undo();
    String getDescription();
}
