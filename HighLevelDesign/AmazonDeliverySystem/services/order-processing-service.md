# Order Processing Service Implementation

## Overview

The Order Processing Service is the core orchestrator for Amazon's order lifecycle, handling order placement, validation, pricing, and coordination with downstream services. Built on microservices architecture with event-driven patterns for scalability and reliability.

## Table of Contents

1. [Service Architecture](#service-architecture)
2. [API Specifications](#api-specifications)
3. [Data Models](#data-models)
4. [Business Logic Implementation](#business-logic)
5. [Integration Patterns](#integration-patterns)
6. [Performance Optimization](#performance-optimization)
7. [Testing Strategy](#testing-strategy)

---

## Service Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Order Processing Service                 │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Order API   │  │ Validation   │  │   Pricing       │  │
│  │   Gateway     │  │   Engine     │  │   Engine        │  │
│  └───────────────┘  └──────────────┘  └─────────────────┘  │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Order       │  │ Inventory    │  │   Payment       │  │
│  │ Orchestrator  │  │ Integration  │  │ Integration     │  │
│  └───────────────┘  └──────────────┘  └─────────────────┘  │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Event       │  │    Order     │  │   Audit &       │  │
│  │  Publisher    │  │   Storage    │  │   Logging       │  │
│  └───────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

```yaml
# Order Processing Service Technology Stack
technology_stack:
  runtime: "Java 17 with Spring Boot 3.0"
  framework: "Spring WebFlux (Reactive)"
  database: 
    primary: "DynamoDB (orders, order_items)"
    cache: "Redis (session, pricing cache)"
    search: "Elasticsearch (order search)"
  messaging: "Apache Kafka"
  monitoring: "Micrometer + DataDog"
  deployment: "Kubernetes with Helm charts"
  
service_configuration:
  replicas: 50  # per region
  cpu_limit: "2000m"
  memory_limit: "4Gi"
  jvm_options: "-Xmx3g -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
```

---

## API Specifications

### Order Management APIs

#### Create Order

```yaml
# POST /api/v1/orders
create_order:
  summary: "Create new order with validation and pricing"
  request_body:
    customer_id: "string (required)"
    items:
      - product_id: "string (required)"
        quantity: "integer (required, min: 1, max: 999)"
        seller_id: "string (required)"
    shipping_address:
      line1: "string (required)"
      line2: "string (optional)"
      city: "string (required)"
      state: "string (required)"
      postal_code: "string (required)"
      country: "string (required)"
    payment_method:
      type: "enum [credit_card, debit_card, gift_card, amazon_pay]"
      token: "string (required for card payments)"
    delivery_preferences:
      speed: "enum [same_day, next_day, two_day, standard]"
      time_window: "object (optional)"
      special_instructions: "string (optional)"
      
  response:
    order_id: "string"
    order_status: "enum [pending, confirmed, processing]"
    estimated_total: "decimal"
    estimated_delivery_date: "iso8601_datetime"
    estimated_delivery_window: "object"
    
  error_responses:
    400: "Invalid request data"
    402: "Payment declined"
    409: "Inventory unavailable"
    429: "Rate limit exceeded"
    500: "Internal server error"
```

#### Order Status Management

```yaml
# GET /api/v1/orders/{orderId}
get_order:
  summary: "Retrieve order details and current status"
  path_parameters:
    orderId: "string (required)"
  query_parameters:
    include_items: "boolean (default: true)"
    include_tracking: "boolean (default: true)"
    
  response:
    order_id: "string"
    customer_id: "string"
    order_status: "enum"
    created_at: "iso8601_datetime"
    updated_at: "iso8601_datetime"
    items: "array of order_item objects"
    shipping_address: "address object"
    billing_address: "address object"
    payment_details: "payment object (masked)"
    order_totals: "pricing breakdown object"
    delivery_information: "delivery tracking object"

# PUT /api/v1/orders/{orderId}
update_order:
  summary: "Update order details (limited modifications allowed)"
  allowed_modifications:
    - "shipping_address (if order not shipped)"
    - "delivery_preferences (if order not shipped)"
    - "payment_method (if payment not processed)"
    
# DELETE /api/v1/orders/{orderId}
cancel_order:
  summary: "Cancel order and initiate refund if applicable"
  business_rules:
    - "Orders can be cancelled before shipping"
    - "Partial cancellations allowed for multi-item orders"
    - "Automatic refund initiation for paid orders"
```

---

## Data Models

### Core Order Domain Models

```java
// Order Aggregate Root
@Entity
@Table(name = "orders")
public class Order {
    @Id
    private String orderId;
    
    @Column(nullable = false)
    private String customerId;
    
    @Enumerated(EnumType.STRING)
    private OrderStatus status;
    
    @Embedded
    private OrderTotals totals;
    
    @Embedded
    private ShippingAddress shippingAddress;
    
    @Embedded
    private BillingAddress billingAddress;
    
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, fetch = FetchType.EAGER)
    private List<OrderItem> items;
    
    @Embedded
    private DeliveryPreferences deliveryPreferences;
    
    @Embedded
    private PaymentInformation paymentInformation;
    
    @Column(name = "created_at", nullable = false)
    private Instant createdAt;
    
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
    
    @Version
    private Long version;  // Optimistic locking
    
    // Business methods
    public void addItem(OrderItem item) {
        validateItemAddition(item);
        this.items.add(item);
        item.setOrder(this);
        updateTotals();
    }
    
    public void removeItem(String productId) {
        this.items.removeIf(item -> item.getProductId().equals(productId));
        updateTotals();
    }
    
    public void updateStatus(OrderStatus newStatus) {
        validateStatusTransition(this.status, newStatus);
        this.status = newStatus;
        this.updatedAt = Instant.now();
    }
    
    private void validateStatusTransition(OrderStatus current, OrderStatus target) {
        // Implement business rules for valid status transitions
    }
    
    private void updateTotals() {
        // Recalculate order totals based on items
    }
}

// Order Item Value Object
@Entity
@Table(name = "order_items")
public class OrderItem {
    @Id
    private String orderItemId;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id")
    private Order order;
    
    @Column(nullable = false)
    private String productId;
    
    @Column(nullable = false)
    private String sellerId;
    
    @Column(nullable = false)
    private Integer quantity;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal unitPrice;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal totalPrice;
    
    @Embedded
    private ProductDetails productDetails;
    
    // Calculated methods
    public BigDecimal calculateLineTotal() {
        return unitPrice.multiply(BigDecimal.valueOf(quantity));
    }
}

// Order Status Enum
public enum OrderStatus {
    PENDING("Order received, awaiting validation"),
    CONFIRMED("Order validated and confirmed"),
    PAYMENT_PROCESSING("Payment being processed"),
    PAYMENT_FAILED("Payment processing failed"),
    PROCESSING("Order being prepared for fulfillment"),
    SHIPPED("Order shipped to customer"),
    DELIVERED("Order delivered successfully"),
    CANCELLED("Order cancelled"),
    RETURNED("Order returned by customer");
    
    private final String description;
    
    OrderStatus(String description) {
        this.description = description;
    }
}
```

---

## Business Logic Implementation

### Order Processing Workflow

```java
@Service
@Transactional
public class OrderProcessingService {
    
    private final OrderRepository orderRepository;
    private final InventoryService inventoryService;
    private final PricingService pricingService;
    private final PaymentService paymentService;
    private final EventPublisher eventPublisher;
    private final OrderValidator orderValidator;
    
    public OrderProcessingService(
            OrderRepository orderRepository,
            InventoryService inventoryService,
            PricingService pricingService,
            PaymentService paymentService,
            EventPublisher eventPublisher,
            OrderValidator orderValidator) {
        this.orderRepository = orderRepository;
        this.inventoryService = inventoryService;
        this.pricingService = pricingService;
        this.paymentService = paymentService;
        this.eventPublisher = eventPublisher;
        this.orderValidator = orderValidator;
    }
    
    public Mono<OrderResult> processOrder(CreateOrderRequest request) {
        return validateOrderRequest(request)
            .flatMap(this::checkInventoryAvailability)
            .flatMap(this::calculatePricing)
            .flatMap(this::processPayment)
            .flatMap(this::saveOrder)
            .flatMap(this::publishOrderEvents)
            .onErrorResume(this::handleOrderProcessingError);
    }
    
    private Mono<ValidatedOrderRequest> validateOrderRequest(CreateOrderRequest request) {
        return Mono.fromCallable(() -> orderValidator.validate(request))
            .subscribeOn(Schedulers.boundedElastic())
            .map(validationResult -> {
                if (validationResult.hasErrors()) {
                    throw new OrderValidationException(validationResult.getErrors());
                }
                return new ValidatedOrderRequest(request);
            });
    }
    
    private Mono<InventoryValidatedOrder> checkInventoryAvailability(ValidatedOrderRequest request) {
        List<InventoryCheckRequest> inventoryChecks = request.getItems().stream()
            .map(item -> new InventoryCheckRequest(item.getProductId(), 
                                                  item.getQuantity(),
                                                  request.getDeliveryLocation()))
            .collect(Collectors.toList());
            
        return inventoryService.checkAvailability(inventoryChecks)
            .map(inventoryResult -> {
                if (!inventoryResult.isAvailable()) {
                    throw new InventoryUnavailableException(inventoryResult.getUnavailableItems());
                }
                return new InventoryValidatedOrder(request, inventoryResult);
            });
    }
    
    private Mono<PricedOrder> calculatePricing(InventoryValidatedOrder validatedOrder) {
        PricingRequest pricingRequest = PricingRequest.builder()
            .customerId(validatedOrder.getCustomerId())
            .items(validatedOrder.getItems())
            .shippingAddress(validatedOrder.getShippingAddress())
            .deliverySpeed(validatedOrder.getDeliveryPreferences().getSpeed())
            .build();
            
        return pricingService.calculateOrderPricing(pricingRequest)
            .map(pricingResult -> new PricedOrder(validatedOrder, pricingResult));
    }
    
    private Mono<PaymentProcessedOrder> processPayment(PricedOrder pricedOrder) {
        if (pricedOrder.getTotalAmount().compareTo(BigDecimal.ZERO) == 0) {
            // Free order, skip payment processing
            return Mono.just(new PaymentProcessedOrder(pricedOrder, 
                PaymentResult.freeOrder()));
        }
        
        PaymentRequest paymentRequest = PaymentRequest.builder()
            .customerId(pricedOrder.getCustomerId())
            .amount(pricedOrder.getTotalAmount())
            .paymentMethod(pricedOrder.getPaymentMethod())
            .orderId(pricedOrder.getOrderId())
            .build();
            
        return paymentService.processPayment(paymentRequest)
            .map(paymentResult -> {
                if (paymentResult.getStatus() == PaymentStatus.FAILED) {
                    throw new PaymentProcessingException(paymentResult.getFailureReason());
                }
                return new PaymentProcessedOrder(pricedOrder, paymentResult);
            });
    }
    
    private Mono<Order> saveOrder(PaymentProcessedOrder processedOrder) {
        Order order = buildOrderEntity(processedOrder);
        return Mono.fromCallable(() -> orderRepository.save(order))
            .subscribeOn(Schedulers.boundedElastic());
    }
    
    private Mono<OrderResult> publishOrderEvents(Order order) {
        List<DomainEvent> events = Arrays.asList(
            new OrderCreatedEvent(order.getOrderId(), order.getCustomerId(), order.getTotals().getTotal()),
            new InventoryReservedEvent(order.getOrderId(), order.getItems()),
            new PaymentProcessedEvent(order.getOrderId(), order.getTotals().getTotal())
        );
        
        return Flux.fromIterable(events)
            .flatMap(event -> eventPublisher.publishEvent(event))
            .then(Mono.just(new OrderResult(order)));
    }
    
    private Mono<OrderResult> handleOrderProcessingError(Throwable error) {
        if (error instanceof OrderValidationException) {
            return Mono.error(new BadRequestException(error.getMessage()));
        } else if (error instanceof InventoryUnavailableException) {
            return Mono.error(new ConflictException("Requested items not available"));
        } else if (error instanceof PaymentProcessingException) {
            return Mono.error(new PaymentRequiredException(error.getMessage()));
        } else {
            // Log unexpected error and return generic error
            log.error("Unexpected error during order processing", error);
            return Mono.error(new InternalServerErrorException("Order processing failed"));
        }
    }
}
```

### Order State Management

```java
@Component
public class OrderStateMachine {
    
    private final Map<OrderStatus, Set<OrderStatus>> allowedTransitions;
    
    public OrderStateMachine() {
        this.allowedTransitions = initializeTransitions();
    }
    
    private Map<OrderStatus, Set<OrderStatus>> initializeTransitions() {
        return Map.of(
            PENDING, Set.of(CONFIRMED, CANCELLED, PAYMENT_PROCESSING),
            CONFIRMED, Set.of(PAYMENT_PROCESSING, CANCELLED),
            PAYMENT_PROCESSING, Set.of(PROCESSING, PAYMENT_FAILED, CANCELLED),
            PAYMENT_FAILED, Set.of(PAYMENT_PROCESSING, CANCELLED),
            PROCESSING, Set.of(SHIPPED, CANCELLED),
            SHIPPED, Set.of(DELIVERED, RETURNED),
            DELIVERED, Set.of(RETURNED),
            CANCELLED, Set.of(), // Terminal state
            RETURNED, Set.of()   // Terminal state
        );
    }
    
    public boolean isTransitionAllowed(OrderStatus from, OrderStatus to) {
        return allowedTransitions.getOrDefault(from, Set.of()).contains(to);
    }
    
    public void validateTransition(OrderStatus from, OrderStatus to) {
        if (!isTransitionAllowed(from, to)) {
            throw new IllegalStateTransitionException(
                String.format("Cannot transition from %s to %s", from, to));
        }
    }
}
```

---

## Integration Patterns

### Event-Driven Integration

```java
@Component
public class OrderEventHandler {
    
    private final OrderRepository orderRepository;
    private final NotificationService notificationService;
    
    @EventListener
    @Async
    @Retryable(value = {Exception.class}, maxAttempts = 3, backoff = @Backoff(delay = 1000))
    public void handleInventoryReservedEvent(InventoryReservedEvent event) {
        log.info("Handling inventory reserved event for order: {}", event.getOrderId());
        
        Order order = orderRepository.findById(event.getOrderId())
            .orElseThrow(() -> new OrderNotFoundException(event.getOrderId()));
            
        if (order.getStatus() == OrderStatus.CONFIRMED) {
            order.updateStatus(OrderStatus.PROCESSING);
            orderRepository.save(order);
            
            // Notify customer
            notificationService.sendOrderStatusUpdate(order);
        }
    }
    
    @EventListener
    @Async
    @Retryable(value = {Exception.class}, maxAttempts = 3, backoff = @Backoff(delay = 1000))
    public void handlePaymentFailedEvent(PaymentFailedEvent event) {
        log.warn("Handling payment failed event for order: {}", event.getOrderId());
        
        Order order = orderRepository.findById(event.getOrderId())
            .orElseThrow(() -> new OrderNotFoundException(event.getOrderId()));
            
        order.updateStatus(OrderStatus.PAYMENT_FAILED);
        orderRepository.save(order);
        
        // Notify customer and initiate recovery workflow
        notificationService.sendPaymentFailureNotification(order);
        // Could trigger automated retry or alternative payment method workflow
    }
}
```

### Circuit Breaker Pattern

```java
@Component
public class InventoryServiceIntegration {
    
    private final WebClient inventoryServiceClient;
    private final CircuitBreaker circuitBreaker;
    private final RedisTemplate<String, Object> redisTemplate;
    
    public InventoryServiceIntegration(WebClient.Builder webClientBuilder, 
                                     CircuitBreakerFactory circuitBreakerFactory,
                                     RedisTemplate<String, Object> redisTemplate) {
        this.inventoryServiceClient = webClientBuilder
            .baseUrl("http://inventory-service")
            .build();
        this.circuitBreaker = circuitBreakerFactory.create("inventory-service");
        this.redisTemplate = redisTemplate;
    }
    
    public Mono<InventoryCheckResult> checkInventoryAvailability(List<InventoryCheckRequest> requests) {
        return circuitBreaker.executeSupplier(() -> 
            inventoryServiceClient
                .post()
                .uri("/api/v1/inventory/check")
                .bodyValue(requests)
                .retrieve()
                .bodyToMono(InventoryCheckResult.class)
                .doOnError(error -> log.error("Inventory service call failed", error))
        ).recover(throwable -> {
            log.warn("Inventory service circuit breaker activated, using fallback");
            return getFallbackInventoryData(requests);
        });
    }
    
    private Mono<InventoryCheckResult> getFallbackInventoryData(List<InventoryCheckRequest> requests) {
        // Try to get cached inventory data
        List<InventoryItem> cachedItems = requests.stream()
            .map(req -> getCachedInventoryItem(req.getProductId()))
            .filter(Objects::nonNull)
            .collect(Collectors.toList());
            
        if (cachedItems.size() == requests.size()) {
            // All items found in cache
            return Mono.just(InventoryCheckResult.fromCachedData(cachedItems));
        } else {
            // Partial or no cache data available
            return Mono.just(InventoryCheckResult.degradedMode());
        }
    }
    
    private InventoryItem getCachedInventoryItem(String productId) {
        return (InventoryItem) redisTemplate.opsForValue()
            .get("inventory:product:" + productId);
    }
}
```

---

## Performance Optimization

### Caching Strategy

```java
@Configuration
@EnableCaching
public class OrderServiceCacheConfig {
    
    @Bean
    public CacheManager cacheManager() {
        RedisCacheManager.Builder builder = RedisCacheManager
            .RedisCacheManagerBuilder
            .fromConnectionFactory(redisConnectionFactory())
            .cacheDefaults(cacheConfiguration());
            
        return builder.build();
    }
    
    private RedisCacheConfiguration cacheConfiguration() {
        return RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .serializeKeysWith(RedisSerializationContext.SerializationPair
                .fromSerializer(new StringRedisSerializer()))
            .serializeValuesWith(RedisSerializationContext.SerializationPair
                .fromSerializer(new GenericJackson2JsonRedisSerializer()));
    }
}

@Service
public class OrderCacheService {
    
    @Cacheable(value = "customer-orders", key = "#customerId")
    public List<OrderSummary> getCustomerOrders(String customerId) {
        return orderRepository.findByCustomerIdOrderByCreatedAtDesc(customerId)
            .stream()
            .map(OrderSummary::from)
            .collect(Collectors.toList());
    }
    
    @CacheEvict(value = "customer-orders", key = "#order.customerId")
    public void evictCustomerOrdersCache(Order order) {
        // Cache will be automatically evicted
    }
    
    @Cacheable(value = "order-pricing", key = "#request.hashCode()")
    public PricingResult calculateOrderPricing(PricingRequest request) {
        return pricingService.calculatePricing(request);
    }
}
```

### Database Optimization

```java
@Repository
public class OrderRepositoryImpl implements OrderRepositoryCustom {
    
    private final EntityManager entityManager;
    
    // Optimized query for order search with pagination
    public Page<Order> findOrdersWithFilters(OrderSearchCriteria criteria, Pageable pageable) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Order> query = cb.createQuery(Order.class);
        Root<Order> root = query.from(Order.class);
        
        List<Predicate> predicates = new ArrayList<>();
        
        if (criteria.getCustomerId() != null) {
            predicates.add(cb.equal(root.get("customerId"), criteria.getCustomerId()));
        }
        
        if (criteria.getStatus() != null) {
            predicates.add(cb.equal(root.get("status"), criteria.getStatus()));
        }
        
        if (criteria.getDateRange() != null) {
            predicates.add(cb.between(root.get("createdAt"), 
                criteria.getDateRange().getStart(), 
                criteria.getDateRange().getEnd()));
        }
        
        query.where(predicates.toArray(new Predicate[0]));
        query.orderBy(cb.desc(root.get("createdAt")));
        
        TypedQuery<Order> typedQuery = entityManager.createQuery(query);
        typedQuery.setFirstResult((int) pageable.getOffset());
        typedQuery.setMaxResults(pageable.getPageSize());
        
        List<Order> orders = typedQuery.getResultList();
        long total = getOrderCount(criteria);
        
        return new PageImpl<>(orders, pageable, total);
    }
    
    // Batch insert optimization for order items
    @Modifying
    @Query(value = """
        INSERT INTO order_items (order_item_id, order_id, product_id, seller_id, 
                                quantity, unit_price, total_price) 
        VALUES (:#{#items.![orderItemId]}, :#{#items.![orderId]}, :#{#items.![productId]}, 
                :#{#items.![sellerId]}, :#{#items.![quantity]}, :#{#items.![unitPrice]}, 
                :#{#items.![totalPrice]})
        """, nativeQuery = true)
    void batchInsertOrderItems(@Param("items") List<OrderItem> items);
}
```

---

## Testing Strategy

### Unit Tests

```java
@ExtendWith(MockitoExtension.class)
class OrderProcessingServiceTest {
    
    @Mock
    private OrderRepository orderRepository;
    
    @Mock
    private InventoryService inventoryService;
    
    @Mock
    private PricingService pricingService;
    
    @Mock
    private PaymentService paymentService;
    
    @Mock
    private EventPublisher eventPublisher;
    
    @InjectMocks
    private OrderProcessingService orderProcessingService;
    
    @Test
    void shouldProcessOrderSuccessfully() {
        // Given
        CreateOrderRequest request = buildValidOrderRequest();
        InventoryCheckResult inventoryResult = InventoryCheckResult.available();
        PricingResult pricingResult = buildPricingResult();
        PaymentResult paymentResult = PaymentResult.successful();
        
        when(inventoryService.checkAvailability(any())).thenReturn(Mono.just(inventoryResult));
        when(pricingService.calculateOrderPricing(any())).thenReturn(Mono.just(pricingResult));
        when(paymentService.processPayment(any())).thenReturn(Mono.just(paymentResult));
        when(orderRepository.save(any())).thenAnswer(invocation -> invocation.getArgument(0));
        when(eventPublisher.publishEvent(any())).thenReturn(Mono.empty());
        
        // When
        OrderResult result = orderProcessingService.processOrder(request).block();
        
        // Then
        assertThat(result).isNotNull();
        assertThat(result.getOrder().getStatus()).isEqualTo(OrderStatus.PROCESSING);
        verify(orderRepository).save(any(Order.class));
        verify(eventPublisher, times(3)).publishEvent(any(DomainEvent.class));
    }
    
    @Test
    void shouldHandleInventoryUnavailableException() {
        // Given
        CreateOrderRequest request = buildValidOrderRequest();
        when(inventoryService.checkAvailability(any()))
            .thenReturn(Mono.error(new InventoryUnavailableException("Out of stock")));
        
        // When & Then
        StepVerifier.create(orderProcessingService.processOrder(request))
            .expectError(ConflictException.class)
            .verify();
    }
}
```

### Integration Tests

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.redis.host=localhost",
    "spring.redis.port=6370"  // Test Redis instance
})
class OrderProcessingIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private OrderRepository orderRepository;
    
    @MockBean
    private InventoryService inventoryService;
    
    @MockBean
    private PaymentService paymentService;
    
    @Test
    void shouldCreateOrderEndToEnd() {
        // Given
        CreateOrderRequest request = buildValidOrderRequest();
        
        when(inventoryService.checkAvailability(any()))
            .thenReturn(Mono.just(InventoryCheckResult.available()));
        when(paymentService.processPayment(any()))
            .thenReturn(Mono.just(PaymentResult.successful()));
        
        // When
        ResponseEntity<OrderResponse> response = restTemplate.postForEntity(
            "/api/v1/orders", request, OrderResponse.class);
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().getOrderId()).isNotNull();
        
        // Verify order persisted
        Optional<Order> savedOrder = orderRepository.findById(response.getBody().getOrderId());
        assertThat(savedOrder).isPresent();
        assertThat(savedOrder.get().getStatus()).isEqualTo(OrderStatus.PROCESSING);
    }
}
```

This comprehensive implementation guide provides the foundation for building Amazon's Order Processing Service with enterprise-grade quality, scalability, and reliability.
