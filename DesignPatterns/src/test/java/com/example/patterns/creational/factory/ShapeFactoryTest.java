package com.example.patterns.creational.factory;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for ShapeFactory
 */
public class ShapeFactoryTest {
    private ShapeFactory shapeFactory;
    
    @BeforeEach
    public void setUp() {
        shapeFactory = new ShapeFactory();
    }
    
    @Test
    public void testCreateCircle() {
        Shape shape = shapeFactory.getShape("CIRCLE");
        assertNotNull(shape, "Shape should not be null");
        assertTrue(shape instanceof Circle, "Shape should be instance of Circle");
    }
    
    @Test
    public void testCreateRectangle() {
        Shape shape = shapeFactory.getShape("RECTANGLE");
        assertNotNull(shape, "Shape should not be null");
        assertTrue(shape instanceof Rectangle, "Shape should be instance of Rectangle");
    }
    
    @Test
    public void testCreateSquare() {
        Shape shape = shapeFactory.getShape("SQUARE");
        assertNotNull(shape, "Shape should not be null");
        assertTrue(shape instanceof Square, "Shape should be instance of Square");
    }
    
    @Test
    public void testInvalidShapeType() {
        Shape shape = shapeFactory.getShape("TRIANGLE");
        assertNull(shape, "Shape should be null for invalid type");
    }
    
    @Test
    public void testNullShapeType() {
        Shape shape = shapeFactory.getShape(null);
        assertNull(shape, "Shape should be null for null type");
    }
}
