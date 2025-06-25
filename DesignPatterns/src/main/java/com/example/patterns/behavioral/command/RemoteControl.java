package com.example.patterns.behavioral.command;

import java.util.Stack;

/**
 * Command Pattern - Invoker
 * Remote control that can execute and undo commands
 */
public class RemoteControl {
    private Command[] onCommands;
    private Command[] offCommands;
    private Stack<Command> commandHistory;
    
    public RemoteControl(int slots) {
        onCommands = new Command[slots];
        offCommands = new Command[slots];
        commandHistory = new Stack<>();
        
        // Initialize with null commands
        Command noCommand = new NoCommand();
        for (int i = 0; i < slots; i++) {
            onCommands[i] = noCommand;
            offCommands[i] = noCommand;
        }
    }
    
    public void setCommand(int slot, Command onCommand, Command offCommand) {
        if (slot >= 0 && slot < onCommands.length) {
            onCommands[slot] = onCommand;
            offCommands[slot] = offCommand;
        }
    }
    
    public void onButtonPressed(int slot) {
        if (slot >= 0 && slot < onCommands.length) {
            System.out.println("Executing: " + onCommands[slot].getDescription());
            onCommands[slot].execute();
            commandHistory.push(onCommands[slot]);
        }
    }
    
    public void offButtonPressed(int slot) {
        if (slot >= 0 && slot < offCommands.length) {
            System.out.println("Executing: " + offCommands[slot].getDescription());
            offCommands[slot].execute();
            commandHistory.push(offCommands[slot]);
        }
    }
    
    public void undoButtonPressed() {
        if (!commandHistory.isEmpty()) {
            Command lastCommand = commandHistory.pop();
            System.out.println("Undoing: " + lastCommand.getDescription());
            lastCommand.undo();
        } else {
            System.out.println("No commands to undo");
        }
    }
    
    public void executeCustomCommand(Command command) {
        System.out.println("Executing custom: " + command.getDescription());
        command.execute();
        commandHistory.push(command);
    }
    
    @Override
    public String toString() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("\n------ Remote Control ------\n");
        for (int i = 0; i < onCommands.length; i++) {
            stringBuilder.append("[slot ").append(i).append("] ");
            stringBuilder.append(onCommands[i].getDescription()).append("  |  ");
            stringBuilder.append(offCommands[i].getDescription()).append("\n");
        }
        return stringBuilder.toString();
    }
    
    // Null Object Pattern implementation
    private static class NoCommand implements Command {
        @Override
        public void execute() {
            System.out.println("No command assigned");
        }
        
        @Override
        public void undo() {
            System.out.println("No command to undo");
        }
        
        @Override
        public String getDescription() {
            return "No Command";
        }
    }
}
