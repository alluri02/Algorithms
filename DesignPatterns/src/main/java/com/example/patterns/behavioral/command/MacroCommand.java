package com.example.patterns.behavioral.command;

import java.util.ArrayList;
import java.util.List;

/**
 * Command Pattern - Macro Command
 * Executes multiple commands at once
 */
public class MacroCommand implements Command {
    private List<Command> commands;
    
    public MacroCommand(List<Command> commands) {
        this.commands = new ArrayList<>(commands);
    }
    
    @Override
    public void execute() {
        System.out.println("Executing macro command...");
        for (Command command : commands) {
            command.execute();
        }
    }
    
    @Override
    public void undo() {
        System.out.println("Undoing macro command...");
        // Undo in reverse order
        for (int i = commands.size() - 1; i >= 0; i--) {
            commands.get(i).undo();
        }
    }
    
    @Override
    public String getDescription() {
        StringBuilder description = new StringBuilder("Macro: ");
        for (int i = 0; i < commands.size(); i++) {
            description.append(commands.get(i).getDescription());
            if (i < commands.size() - 1) {
                description.append(", ");
            }
        }
        return description.toString();
    }
}
